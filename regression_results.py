#!/usr/bin/env python3
"""Create isolated regression snapshots and compare rule outputs.

Key behavior:
- Snapshot and isolated compare runs DO NOT write into rules/*/results.
- Snapshot outputs are written only under the baseline directory.
- Isolated compare outputs are written to a temporary folder and removed.
- Comparison directory stores summary outputs only.
- Comparison can also run against existing real results under rules/.

The script compares case-level results.json files and ignores only
`dictionary_versions` during diff normalization. The `validated` field is
included in comparisons.
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_BASELINE_DIR = Path(".regression/baseline")
DEFAULT_COMPARISON_DIR = Path(".regression/comparison")

SUPPORTED_DICT_KEYS = {
    "whodrug",
    "meddra",
    "unii",
    "medrt",
    "loinc",
    "snomed",
    "ct",
}


def load_dictionary_paths(config_path: Optional[Path]) -> Dict[str, str]:
    """Load dictionary paths from JSON or key=value text file."""
    if not config_path:
        return {}

    if not config_path.exists():
        raise FileNotFoundError(f"Dictionary paths file not found: {config_path}")

    raw = config_path.read_text(encoding="utf-8")

    # JSON object format: {"unii": "dummy_ex_dicts/unii", ...}
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            output: Dict[str, str] = {}
            for key, value in parsed.items():
                key_l = str(key).strip().lower()
                if key_l in SUPPORTED_DICT_KEYS and value is not None:
                    output[key_l] = str(Path(str(value).strip()).expanduser())
            return output
    except json.JSONDecodeError:
        pass

    # Fallback text format:
    # key=value
    # key: value
    output: Dict[str, str] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if "=" in line:
            key, value = line.split("=", 1)
        elif ":" in line:
            key, value = line.split(":", 1)
        else:
            continue

        key_l = key.strip().lower()
        value_s = value.strip().strip('"').strip("'")
        if key_l in SUPPORTED_DICT_KEYS and value_s:
            output[key_l] = str(Path(value_s).expanduser())

    return output


def build_runner(use_postgres: bool, dictionary_paths: Dict[str, str]) -> Any:
    """Construct TestRunner with optional dictionary path overrides."""
    from test import TestRunner

    return TestRunner(
        use_pgserver=not use_postgres,
        whodrug_path=dictionary_paths.get("whodrug"),
        meddra_path=dictionary_paths.get("meddra"),
        unii_path=dictionary_paths.get("unii"),
        medrt_path=dictionary_paths.get("medrt"),
        loinc_path=dictionary_paths.get("loinc"),
        snomed_path=dictionary_paths.get("snomed"),
        ct=dictionary_paths.get("ct"),
    )


def _total_errors(payload: Dict[str, Any]) -> int:
    return sum(len(ds.get("errors", [])) for ds in payload.get("datasets", []))


def _execute_case(runner: Any, rule_id: str, test_type: str, case_info: Dict[str, str]) -> Dict[str, Any]:
    """Run one test case and return a results.json payload (without writing to rules/)."""
    _, results_data = runner.run_validation(rule_id, case_info["data_path"])

    if results_data is None:
        results_data = {"error": "Unknown Error", "exception": "Engine returned None"}

    if not results_data.get("error") and test_type == "negative":
        validations = runner.get_validation_info(case_info["data_path"])
        results_data, unmatched = runner.validate_errors(results_data, validations)
        highlights = runner.get_excel_highlights(case_info["data_path"])
        unhighlighted_validations, unvalidated_highlights = runner.check_highlights(validations, highlights)

        if unmatched:
            results_data["unmatched_validation"] = unmatched
        if unhighlighted_validations:
            results_data["unhighlighted_validations"] = unhighlighted_validations
        if unvalidated_highlights:
            results_data["unvalidated_highlights"] = unvalidated_highlights

    if runner.version_info:
        return {**results_data, "dictionary_versions": runner.version_info}

    return results_data


def run_isolated_suite(
    output_dir: Path,
    use_postgres: bool,
    dictionary_paths_file: Optional[Path],
    clean: bool,
) -> Dict[str, Any]:
    """Run all cases and write results.json outputs under output_dir/rules/ only."""

    dictionary_paths = load_dictionary_paths(dictionary_paths_file)

    if clean and output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    runner = build_runner(use_postgres=use_postgres, dictionary_paths=dictionary_paths)

    summary = {
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "output_dir": str(output_dir),
        "use_postgres": use_postgres,
        "dictionary_paths_file": str(dictionary_paths_file) if dictionary_paths_file else None,
        "dictionary_paths": dictionary_paths,
        "total_rules": 0,
        "total_cases": 0,
        "cases_with_execution_error": 0,
    }

    try:
        rules = runner.get_available_rules()
        summary["total_rules"] = len(rules)

        for index, rule_id in enumerate(rules, start=1):
            print(f"[{index}/{len(rules)}] Running {rule_id}")
            rule_cases = runner.get_test_cases(rule_id)

            for test_type in ("positive", "negative"):
                for case_info in rule_cases[test_type]:
                    case_id = case_info["case_id"]
                    payload = _execute_case(runner, rule_id, test_type, case_info)

                    out_results_dir = output_dir / "rules" / rule_id / test_type / case_id / "results"
                    out_results_dir.mkdir(parents=True, exist_ok=True)

                    with (out_results_dir / "results.json").open("w", encoding="utf-8") as f:
                        json.dump(payload, f, indent=2, sort_keys=True)

                    summary["total_cases"] += 1
                    if "error" in payload:
                        summary["cases_with_execution_error"] += 1
    finally:
        # Best effort cleanup of DB connection used by the shared data service singleton.
        try:
            runner.data_service.pgi.close()
        except Exception:
            pass

    with (output_dir / "baseline_run_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)

    print(
        "Run complete | "
        f"Rules: {summary['total_rules']} | "
        f"Cases: {summary['total_cases']} | "
        f"Execution errors: {summary['cases_with_execution_error']}"
    )

    return summary


def _extract_case_key(path: Path, root: Path) -> Optional[str]:
    """Extract case key as RULE/TYPE/CASE from a results.json path."""
    try:
        rel_parts = list(path.relative_to(root).parts)
    except ValueError:
        return None

    if len(rel_parts) < 5:
        return None

    if rel_parts[-2:] != ["results", "results.json"]:
        return None

    # Accept roots that are either:
    # - <root>/rules/<rule>/<type>/<case>/results/results.json
    # - <root>/<rule>/<type>/<case>/results/results.json
    rule, test_type, case_id = rel_parts[-5], rel_parts[-4], rel_parts[-3]
    if test_type not in {"positive", "negative"}:
        return None

    return f"{rule}/{test_type}/{case_id}"


RULES_DIR = Path("rules")


def is_rule_verified(rule_id: str) -> bool:
    """Return True if the rule YAML starts with a '# verified' comment (case-insensitive)."""
    rule_path = RULES_DIR / rule_id
    ymls = list(rule_path.glob("[!~]*.yml"))
    if not ymls:
        return False
    try:
        for line in ymls[0].read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if not stripped.startswith("#"):
                # Reached non-comment content without finding verified
                return False
            if stripped.lstrip("#").strip().lower() == "verified":
                return True
    except OSError:
        pass
    return False


def collect_results(root: Path) -> Dict[str, Dict[str, Any]]:
    """Load case-level results.json files from a root directory."""
    output: Dict[str, Dict[str, Any]] = {}
    if not root.exists():
        return output

    for path in sorted(root.rglob("results.json")):
        case_key = _extract_case_key(path, root)
        if not case_key:
            continue

        with path.open("r", encoding="utf-8") as f:
            output[case_key] = json.load(f)

    return output


def _normalize_for_compare(value: Any) -> Any:
    """Normalize JSON while keeping validated fields and ignoring dictionary_versions."""
    if isinstance(value, dict):
        normalized: Dict[str, Any] = {}
        for key in sorted(value.keys()):
            if key == "dictionary_versions":
                continue
            normalized[key] = _normalize_for_compare(value[key])
        return normalized

    if isinstance(value, list):
        normalized_list = [_normalize_for_compare(item) for item in value]
        return sorted(normalized_list, key=lambda item: json.dumps(item, sort_keys=True))

    return value


def _normalize_for_trivial_compare(value: Any) -> Any:
    """Normalize JSON and ignore trivial fields for trivial diff detection.

    This is used to identify cases where payloads differ only by row locations
    or execution message text.
    """
    if isinstance(value, dict):
        normalized: Dict[str, Any] = {}
        for key in sorted(value.keys()):
            if key in {
                "dictionary_versions",
                "row",
                "row_num",
                "row_number",
                "execution_message",
            }:
                continue
            normalized[key] = _normalize_for_trivial_compare(value[key])
        return normalized

    if isinstance(value, list):
        normalized_list = [_normalize_for_trivial_compare(item) for item in value]
        return sorted(normalized_list, key=lambda item: json.dumps(item, sort_keys=True))

    return value


def compare_case(old_payload: Dict[str, Any], new_payload: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """Compare two case payloads and return changed flag plus details."""
    old_n = _normalize_for_compare(old_payload)
    new_n = _normalize_for_compare(new_payload)

    if old_n == new_n:
        return False, {}

    old_text = json.dumps(old_n, indent=2, sort_keys=True).splitlines()
    new_text = json.dumps(new_n, indent=2, sort_keys=True).splitlines()
    unified = list(difflib.unified_diff(old_text, new_text, fromfile="baseline", tofile="current", lineterm=""))

    # Trivial if the only material difference is row-position metadata or execution message text.
    old_row_agnostic = _normalize_for_trivial_compare(old_payload)
    new_row_agnostic = _normalize_for_trivial_compare(new_payload)
    is_trivial = old_row_agnostic == new_row_agnostic

    return True, {
        "is_trivial": is_trivial,
        "old_total_errors": _total_errors(old_payload),
        "new_total_errors": _total_errors(new_payload),
        "old_execution_error": "error" in old_payload,
        "new_execution_error": "error" in new_payload,
        "unified_diff": unified,
    }


def write_diff_summary(
    summary_path: Path,
    baseline_root: Path,
    current_root: Path,
    baseline_results: Dict[str, Dict[str, Any]],
    current_results: Dict[str, Dict[str, Any]],
    max_diff_lines: int,
    verified_only: bool = False,
) -> Dict[str, Any]:
    """Write a readable markdown diff summary and return top-level stats.

    When verified_only=True, only cases whose rule_id has a '# verified' comment
    at the top of its YAML are included.
    """
    if verified_only:
        all_keys = baseline_results.keys() | current_results.keys()
        verified_rules = {k for k in all_keys if is_rule_verified(k.split("/")[0])}
        baseline_results = {k: v for k, v in baseline_results.items() if k in verified_rules}
        current_results = {k: v for k, v in current_results.items() if k in verified_rules}

    baseline_keys = set(baseline_results.keys())
    current_keys = set(current_results.keys())

    added_cases = sorted(current_keys - baseline_keys)
    removed_cases = sorted(baseline_keys - current_keys)
    common_cases = sorted(baseline_keys & current_keys)

    changed_cases: List[Tuple[str, Dict[str, Any]]] = []
    trivial_diff_cases: List[Tuple[str, Dict[str, Any]]] = []
    unchanged_cases = 0

    for case_key in common_cases:
        changed, details = compare_case(baseline_results[case_key], current_results[case_key])
        if changed:
            if details.get("is_trivial"):
                trivial_diff_cases.append((case_key, details))
            else:
                changed_cases.append((case_key, details))
        else:
            unchanged_cases += 1

    stats = {
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "baseline_root": str(baseline_root),
        "current_root": str(current_root),
        "baseline_cases": len(baseline_results),
        "current_cases": len(current_results),
        "added_cases": len(added_cases),
        "removed_cases": len(removed_cases),
        "changed_cases": len(changed_cases),
        "trivial_diff_cases": len(trivial_diff_cases),
        "unchanged_cases": unchanged_cases,
    }

    lines: List[str] = []
    lines.append("# Regression Diff Summary" + (" (Verified Rules Only)" if verified_only else ""))
    lines.append("")
    lines.append(f"Generated (UTC): {stats['generated_utc']}")
    lines.append(f"Baseline root: {baseline_root}")
    lines.append(f"Current root: {current_root}")
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    lines.append(f"- Baseline cases: {stats['baseline_cases']}")
    lines.append(f"- Current cases: {stats['current_cases']}")
    lines.append(f"- Added cases: {stats['added_cases']}")
    lines.append(f"- Removed cases: {stats['removed_cases']}")
    lines.append(f"- Changed cases: {stats['changed_cases']}")
    lines.append(f"- Trivial diffs (row/execution-message only): {stats['trivial_diff_cases']}")
    lines.append(f"- Unchanged cases: {stats['unchanged_cases']}")
    lines.append("")
    lines.append("Comparison normalization:")
    lines.append("- `dictionary_versions` ignored")
    lines.append("- `validated` included")
    lines.append("- Main changed cases exclude row-only and execution-message-only differences")
    lines.append("")

    lines.append("## Added Cases")
    lines.append("")
    if added_cases:
        for case_key in added_cases:
            lines.append(f"- {case_key}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Removed Cases")
    lines.append("")
    if removed_cases:
        for case_key in removed_cases:
            lines.append(f"- {case_key}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Changed Cases")
    lines.append("")
    if not changed_cases:
        lines.append("- None")
    else:
        for case_key, details in changed_cases:
            lines.append(f"### {case_key}")
            lines.append("")
            lines.append(f"- Total errors: {details['old_total_errors']} -> {details['new_total_errors']}")
            lines.append(f"- Execution error: {details['old_execution_error']} -> {details['new_execution_error']}")
            lines.append("")
            lines.append("```diff")
            diff_lines = details["unified_diff"][:max_diff_lines]
            for diff_line in diff_lines:
                lines.append(diff_line)
            if len(details["unified_diff"]) > max_diff_lines:
                lines.append("... diff truncated ...")
            lines.append("```")
            lines.append("")

    lines.append("## Trivial Diffs")
    lines.append("")
    if not trivial_diff_cases:
        lines.append("- None")
    else:
        lines.append("Cases where differences are row-only or execution-message-only after normalization.")
        lines.append("")
        for case_key, details in trivial_diff_cases:
            lines.append(f"### {case_key}")
            lines.append("")
            lines.append(f"- Total errors: {details['old_total_errors']} -> {details['new_total_errors']}")
            lines.append(f"- Execution error: {details['old_execution_error']} -> {details['new_execution_error']}")
            lines.append("")
            lines.append("```diff")
            diff_lines = details["unified_diff"][:max_diff_lines]
            for diff_line in diff_lines:
                lines.append(diff_line)
            if len(details["unified_diff"]) > max_diff_lines:
                lines.append("... diff truncated ...")
            lines.append("```")
            lines.append("")

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    sidecar_path = summary_path.parent / "run_summary.json"
    sidecar_path.write_text(
        json.dumps(stats, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Isolated regression snapshot and compare utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot = subparsers.add_parser(
        "snapshot",
        help="Run all rules in isolated mode and write baseline outputs outside rules/",
    )
    snapshot.add_argument("--baseline-dir", type=Path, default=DEFAULT_BASELINE_DIR)
    snapshot.add_argument("--dictionary-paths-file", type=Path)
    snapshot.add_argument("--use-postgres", action="store_true", help="Use PostgreSQL instead of pgserver")
    snapshot.add_argument(
        "--clean",
        action="store_true",
        help="Delete baseline-dir before writing new outputs",
    )

    compare = subparsers.add_parser(
        "compare",
        help="Compare baseline outputs against isolated current run, rules/, or a custom folder",
    )
    compare.add_argument("--baseline-dir", type=Path, default=DEFAULT_BASELINE_DIR)
    compare.add_argument(
        "--current-source",
        choices=["isolated", "rules", "folder"],
        default="isolated",
        help="Source of current results to compare against baseline",
    )
    compare.add_argument(
        "--comparison-dir",
        type=Path,
        default=DEFAULT_COMPARISON_DIR,
        help="Directory for regression diff summary output",
    )
    compare.add_argument("--current-dir", type=Path, help="Used when --current-source folder")
    compare.add_argument("--dictionary-paths-file", type=Path)
    compare.add_argument("--use-postgres", action="store_true", help="Use PostgreSQL instead of pgserver")
    compare.add_argument("--summary-file", type=Path, help="Output markdown summary file path")
    compare.add_argument(
        "--max-diff-lines",
        type=int,
        default=120,
        help="Maximum unified diff lines shown per changed case",
    )
    compare.add_argument(
        "--clean",
        action="store_true",
        help="Delete existing summary outputs before writing (if they exist)",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.command == "snapshot":
        run_isolated_suite(
            output_dir=args.baseline_dir,
            use_postgres=args.use_postgres,
            dictionary_paths_file=args.dictionary_paths_file,
            clean=args.clean,
        )
        print(f"Baseline created at: {args.baseline_dir}")
        print("No files were written to rules/*/results by this command.")
        return 0

    baseline_root = args.baseline_dir
    baseline_results = collect_results(baseline_root)
    if not baseline_results:
        print(f"No baseline results found in: {baseline_root}")
        print("Create one with: python regression_results.py snapshot --clean")
        return 1

    if args.current_source == "isolated":
        with tempfile.TemporaryDirectory(prefix="regression_current_") as tmp_dir:
            isolated_root = Path(tmp_dir)
            run_isolated_suite(
                output_dir=isolated_root,
                use_postgres=args.use_postgres,
                dictionary_paths_file=args.dictionary_paths_file,
                clean=False,
            )
            current_root = isolated_root

            summary_file = args.summary_file or (args.comparison_dir / "regression_diff_summary.md")
            if args.summary_file:
                verified_summary_file = summary_file.with_stem(summary_file.stem + "_verified")
            else:
                verified_summary_file = args.comparison_dir / "regression_diff_summary_verified.md"
            for f in (summary_file, verified_summary_file, summary_file.parent / "run_summary.json"):
                if args.clean and f.exists():
                    f.unlink()

            current_results_snapshot = collect_results(current_root)

            stats = write_diff_summary(
                summary_path=summary_file,
                baseline_root=baseline_root,
                current_root=current_root,
                baseline_results=baseline_results,
                current_results=current_results_snapshot,
                max_diff_lines=args.max_diff_lines,
            )
            write_diff_summary(
                summary_path=verified_summary_file,
                baseline_root=baseline_root,
                current_root=current_root,
                baseline_results=baseline_results,
                current_results=current_results_snapshot,
                max_diff_lines=args.max_diff_lines,
                verified_only=True,
            )

            print(f"Summary written: {summary_file}")
            print(f"Verified summary written: {verified_summary_file}")
            print(
                " | ".join(
                    [
                        f"Added {stats['added_cases']}",
                        f"Removed {stats['removed_cases']}",
                        f"Changed {stats['changed_cases']}",
                        f"Trivial {stats['trivial_diff_cases']}",
                        f"Unchanged {stats['unchanged_cases']}",
                    ]
                )
            )
            print("Isolated compare run used a temporary folder; only summary files were written to comparison-dir.")

            return 0 if (stats["added_cases"] + stats["removed_cases"] + stats["changed_cases"]) == 0 else 2
    elif args.current_source == "rules":
        current_root = Path("rules")
    else:
        if not args.current_dir:
            print("--current-dir is required when --current-source folder")
            return 1
        current_root = args.current_dir

    current_results = collect_results(current_root)
    if not current_results:
        print(f"No current results found in: {current_root}")
        return 1

    summary_file = args.summary_file or (args.comparison_dir / "regression_diff_summary.md")
    if args.summary_file:
        verified_summary_file = summary_file.with_stem(summary_file.stem + "_verified")
    else:
        verified_summary_file = args.comparison_dir / "regression_diff_summary_verified.md"
    for f in (summary_file, verified_summary_file, summary_file.parent / "run_summary.json"):
        if args.clean and f.exists():
            f.unlink()

    stats = write_diff_summary(
        summary_path=summary_file,
        baseline_root=baseline_root,
        current_root=current_root,
        baseline_results=baseline_results,
        current_results=current_results,
        max_diff_lines=args.max_diff_lines,
    )
    write_diff_summary(
        summary_path=verified_summary_file,
        baseline_root=baseline_root,
        current_root=current_root,
        baseline_results=baseline_results,
        current_results=current_results,
        max_diff_lines=args.max_diff_lines,
        verified_only=True,
    )

    print(f"Summary written: {summary_file}")
    print(f"Verified summary written: {verified_summary_file}")
    print(
        " | ".join(
            [
                f"Added {stats['added_cases']}",
                f"Removed {stats['removed_cases']}",
                f"Changed {stats['changed_cases']}",
                f"Trivial {stats['trivial_diff_cases']}",
                f"Unchanged {stats['unchanged_cases']}",
            ]
        )
    )

    return 0 if (stats["added_cases"] + stats["removed_cases"] + stats["changed_cases"]) == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
