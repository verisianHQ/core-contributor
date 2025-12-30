#!/usr/bin/env python3
"""
Contributor test script for SQL CDISC Rules Engine Contributor Repo.
"""

import sys
import argparse
import json
import logging
import warnings
import textwrap
import openpyxl as op
from pathlib import Path
from typing import List, Optional, Tuple, Any, Dict

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
logging.basicConfig(level=logging.CRITICAL)

RULES_DIR = Path("rules")
ENGINE_DIR = Path("engine")


class ResultReporter:
    """Handles formatting, printing, and saving of test results."""

    @classmethod
    def json_to_readable(cls, results_data: dict, output_path: Path):
        """Write a human-readable summary of the JSON results to a text file."""
        with output_path.open("w") as f:
            if "error" in results_data:
                f.write("EXECUTION ERROR\n===============\n")
                f.write(f"{results_data['error']}\n")
                if "exception" in results_data:
                    f.write(f"Details: {results_data['exception']}\n")
                return

            datasets = results_data.get("datasets", [])
            if not datasets:
                f.write("No validation results found.\n")
                return

            total_errors = sum(len(ds.get("errors", [])) for ds in datasets)
            f.write(f"Total Errors Found: {total_errors}\n\n")

            for dataset in datasets:
                f.write(f"Dataset: {dataset.get('dataset', 'Unknown')}\n")
                f.write(f"Domain: {dataset.get('domain', 'N/A')}\n")
                if msg := dataset.get("execution_message"):
                    f.write(f"Rule Message: {msg}\n")

                errors = dataset.get("errors", [])
                f.write(f"Errors in this dataset: {len(errors)}\n")

                if not errors:
                    f.write("  No errors found in this dataset.\n")
                else:
                    f.write("\n")
                    for i, error in enumerate(errors, 1):
                        f.write(f"  Error {i}:\n")
                        if row := error.get("row"):
                            f.write(f"    Row: {row}\n")

                        for key, val in error.items():
                            if key not in ["row", "value", "highlighted_in_test_case"]:
                                f.write(f"    {key}: {val}\n")

                        if value_dict := error.get("value", {}):
                            f.write("    Problematic values:\n")
                            for k, v in value_dict.items():
                                f.write(f"      {k}: {v}\n")

                        if error.get("highlighted_in_test_case") is not None:
                            highlight_status = "Yes" if error["highlighted_in_test_case"] else "No"
                            f.write(f"    Highlighted in Test Case: {highlight_status}\n")
                        f.write("\n")
                f.write("\n")

            if unmatched := results_data.get("unmatched_highlights_in_test_case"):
                f.write(f"Unmatched highlighted cells in test case: {len(unmatched)}\n")
                f.write("Check results.json for more information, or examine the test case file directly.\n")

    @classmethod
    def save_case_results(cls, rule_id: str, test_type: str, case_id: str, results: dict):
        """Saves JSON and TXT results to the file system."""
        results_path = RULES_DIR / rule_id / test_type / case_id / "results"
        results_path.mkdir(parents=True, exist_ok=True)

        with (results_path / "results.json").open("w") as f:
            json.dump(results, f, indent=2, default=str),

        cls.json_to_readable(results, results_path / "results.txt")
        return str(results_path)

    @staticmethod
    def display_rule_summary(summary: dict, verbose: bool = False):
        """Prints the execution summary for a single rule to the console."""
        print(f"\n{'='*60}\n{summary['rule_id']} Test Results Summary")
        print(f"\nRule: {summary['rule_id']}")
        print(f"Overall Status: {summary['status'].upper()}")

        for test_type in ["positive", "negative"]:
            tests = summary[f"{test_type}_tests"]
            print(f"{'-'*54}")
            print(f"{test_type.capitalize()} Test Cases: {len(tests)}")
            for test in tests:
                symbol = "[PASS]" if test["passed"] else "[FAIL]"
                print(f"\n  {symbol} Case {test['case_id']} - Results at: {test['results_path']}")

                if verbose:
                    txt_path = Path(test["results_path"]) / "results.txt"
                    if txt_path.exists():
                        print(f"\n{textwrap.indent(txt_path.read_text().strip(), "     ")}")

                if not test["passed"] and not verbose:
                    print(f"      Expected: {test['expected']}")
                    if test.get("total_errors") is not None:
                        print(f"      Got: {test['total_errors']} errors")
                    if test.get("error"):
                        print(f"      Error: {test['error']}")
                        print(f"      Exception: {test.get('exception', 'N/A')}")

        print("\n" + "=" * 60)


class TestRunner:
    """Test execution logic."""

    def __init__(self):
        self._setup_engine_path()
        self.ig_specs = self._init_engine_specs()

    @staticmethod
    def _setup_engine_path():
        """Ensures the engine submodule is in sys.path."""
        if str(ENGINE_DIR) not in sys.path:
            sys.path.insert(0, str(ENGINE_DIR))

    @staticmethod
    def get_available_rules() -> List[str]:
        if not RULES_DIR.exists():
            return []
        return sorted([d.name for d in RULES_DIR.iterdir() if d.is_dir() and d.name.startswith("CORE-")])

    @staticmethod
    def get_test_cases(rule_id: str) -> dict:
        """Scans directories to find available test cases for a rule."""
        cases = {"positive": [], "negative": []}
        rule_path = RULES_DIR / rule_id

        for test_type in ["positive", "negative"]:
            test_type_path = rule_path / test_type
            if test_type_path.exists():
                for case_dir in sorted(test_type_path.iterdir()):
                    if case_dir.is_dir():
                        data_dir = case_dir / "data"
                        if list(data_dir.glob("[!~]*.xls*")):
                            cases[test_type].append({"case_id": case_dir.name, "data_path": str(data_dir)})
        return cases

    def _init_engine_specs(self):
        """Initialises and returns IG Specifications."""
        try:
            from engine.cdisc_rules_engine.utilities.ig_specification import IGSpecification

            return IGSpecification(
                standard="sdtmig", standard_version="3.4", standard_substandard=None, define_xml_version=None
            )
        except ImportError:
            print("Error: Could not import engine modules. Is the submodule initialised?")
            sys.exit(1)

    def run_validation(self, rule_id: str, data_path: str) -> Tuple[Any, Optional[dict]]:
        """Invokes the engine to validate data against the rule."""
        rule_path = RULES_DIR / rule_id
        rule_ymls = list(rule_path.glob("[!~]*.yml"))

        if not rule_ymls:
            return None, {"error": "Rule YAML missing", "exception": f"No YAML found in {rule_path}"}

        if len(rule_ymls) > 1:
            return None, {"error": "Multiple Rule YAMLs", "exception": f"Multiple Rule YAMLs found in {rule_path}"}

        data_path_obj = Path(data_path)
        excel_files = list(data_path_obj.glob("[!~]*.xlsx")) + list(data_path_obj.glob("[!~]*.xls"))

        if not excel_files:
            return None, {"error": "Excel data missing", "exception": f"No Excel files in {data_path}"}

        try:
            import yaml
            from engine.tests.rule_regression.regression import (
                sharepoint_xlsx_to_test_datasets,
                process_test_case_dataset,
            )

            with open(rule_ymls[0], "r") as f:
                rule = yaml.safe_load(f)

            test_datasets = sharepoint_xlsx_to_test_datasets(str(excel_files[0]))
            regression_errors = {}

            sql_results, _ = process_test_case_dataset(
                regression_errors=regression_errors,
                define_xml_file_path=None,
                data_test_datasets=test_datasets,
                ig_specs=self.ig_specs,
                rule=rule,
                test_case_folder_path=data_path,
                cur_core_id=rule_id,
                use_pgserver=True,
            )

            if "results_sql" in regression_errors:
                return sql_results, {"datasets": regression_errors["results_sql"]}

            return sql_results, {"datasets": []}

        except Exception as e:
            return None, {
                "error": f"No result - either the rule or test case data {excel_files[0].name} is broken",
                "exception": str(e),
            }

    def evaluate_case(self, rule_id: str, test_type: str, case_info: dict) -> dict:
        """Runs validation, saves results, and determines pass/fail status."""
        case_id = case_info["case_id"]
        expected = "0 errors" if test_type == "positive" else ">0 errors"

        _, results_data = self.run_validation(rule_id, case_info["data_path"])

        if results_data is None:
            results_data = {"error": "Unknown Error", "exception": "Engine returned None"}

        if test_type == "negative":
            test_case_cell_errors = self.get_excel_errors(case_info["data_path"])
            for ds in results_data.get("datasets", []):
                for err in ds.get("errors", []):
                    if "row" in err:
                        if not test_case_cell_errors:
                            err.update({"highlighted_in_test_case": False})
                            continue
                        for ref in test_case_cell_errors.get(ds.get("dataset", []), []):
                            if err.get("row") == ref.get("row") and err.get("value") == ref.get("value"):
                                err.update({"highlighted_in_test_case": True})
                                ref.update({"matched": True})
                                break
                            else:
                                err.update({"highlighted_in_test_case": False})

            # get list of unmatched highlights from test case
            unmatched = {
                ds: [ref for ref in test_case_cell_errors.get(ds, []) if not ref.get("matched")]
                for ds in test_case_cell_errors
            }

            # remove datasets with no unmatched highlights
            unmatched = {ds: v for ds, v in unmatched.items() if v}

            if unmatched:
                results_data["unmatched_highlights_in_test_case"] = unmatched

        results_path = ResultReporter.save_case_results(rule_id, test_type, case_id, results_data)

        if "error" in results_data:
            return {
                "case_id": case_id,
                "passed": False,
                "total_errors": None,
                "expected": expected,
                "error": results_data["error"],
                "exception": results_data.get("exception"),
                "results_path": results_path,
            }

        total_errors = sum(len(ds.get("errors", [])) for ds in results_data.get("datasets", []))
        passed = (total_errors == 0) if test_type == "positive" else (total_errors > 0)

        return {
            "case_id": case_id,
            "passed": passed,
            "total_errors": total_errors,
            "expected": expected,
            "results_path": results_path,
        }

    def get_excel_errors(self, data_path: str):
        xl_path = list(Path(data_path).glob("[!~]*.xls*"))[0]
        highlighted_cells = {}

        wb = op.load_workbook(xl_path, data_only=True)
        for sheet in wb.worksheets:
            for row in sheet.iter_rows():
                for cell in row:
                    if cell.fill.start_color.index == "FFFFFF00":
                        highlighted_cells.setdefault(sheet.title, []).append(
                            {
                                "row": int(cell.row) - 4,
                                "value": {sheet.cell(row=1, column=cell.column).value: cell.value},
                            }
                        )
        return highlighted_cells

    def _get_cases_to_run(self, rule_id: str, specific_case: str = None) -> Dict[str, List[dict]]:
        all_cases = self.get_test_cases(rule_id)

        if not specific_case:
            return all_cases

        target_type, target_id = specific_case.split("/")
        filtered = {"positive": [], "negative": []}

        if target_type in filtered:
            found = next((c for c in all_cases[target_type] if c["case_id"] == target_id), None)
            if found:
                filtered[target_type].append(found)

        return filtered

    def run_rule_suite(self, rule_id: str, specific_case: str = None) -> dict:
        """Runs test cases based on the filtered list."""
        summary = {"rule_id": rule_id, "positive_tests": [], "negative_tests": [], "status": "passed"}

        cases_to_run = self._get_cases_to_run(rule_id, specific_case)

        if not cases_to_run["positive"] and not cases_to_run["negative"]:
            return summary

        for test_type in ["positive", "negative"]:
            for case in cases_to_run[test_type]:
                result = self.evaluate_case(rule_id, test_type, case)
                summary[f"{test_type}_tests"].append(result)
                if not result["passed"]:
                    summary["status"] = "failed"

        return summary


class InteractiveHandler:
    """Handles user prompts for interactive mode."""

    @staticmethod
    def prompt_rule(available: List[str]) -> str:
        print("\nWhich rule would you like to test?")
        while True:
            choice = input("Enter rule ID (e.g. CORE-000215): ").strip()
            if choice in available:
                return choice
            print(f"Invalid. Available: {', '.join(available[:5])}...")

    @staticmethod
    def prompt_case(available: dict) -> Optional[str]:
        print("\nTest specific case? (Leave blank for all)")
        flat_list = []
        for t_type in ["positive", "negative"]:
            for c in available[t_type]:
                flat_list.append(f"{t_type}/{c['case_id']}")

        if not flat_list:
            return None

        for i, tc in enumerate(flat_list, 1):
            print(f"  {i}. {tc}")

        while True:
            choice = input("\nEnter case (e.g., positive/01, number, or Enter): ").strip()
            if not choice:
                return None
            if choice in flat_list:
                return choice
            if choice.isdigit() and 0 <= int(choice) - 1 < len(flat_list):
                return flat_list[int(choice) - 1]
            print("Invalid choice.")


def parse_args():
    parser = argparse.ArgumentParser(description="CDISC SQL Rules Engine Tester")
    parser.add_argument("-r", "--rule", help="Rule ID (e.g., CORE-000176)")
    parser.add_argument("-all", "--all-rules", action="store_true", help="Run all rules")
    parser.add_argument("-tc", "--test-case", help="Specific case (e.g., positive/01)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print detailed results")
    return parser.parse_args()


def main():
    args = parse_args()
    runner = TestRunner()
    available_rules = runner.get_available_rules()

    if not available_rules:
        print("Error: No rules found in 'rules' directory.")
        sys.exit(1)

    if not args.all_rules:
        if args.rule:
            rule_id = args.rule
        else:
            rule_id = InteractiveHandler.prompt_rule(available_rules)

        if args.rule and args.test_case:
            specific_case = args.test_case
        elif not args.rule:
            cases = runner.get_test_cases(rule_id)
            specific_case = InteractiveHandler.prompt_case(cases)
        else:
            specific_case = None

        print(f"\nRunning {rule_id}...")
        summary = runner.run_rule_suite(rule_id, specific_case)

        ResultReporter.display_rule_summary(summary, verbose=args.verbose)
        sys.exit(0 if summary["status"] == "passed" else 1)

    if args.test_case:
        print("Error: --test-case cannot be used with --all-rules.")
        sys.exit(1)

    rules_to_run = available_rules
    results = {"passed": [], "failed": [], "error": []}
    total = len(rules_to_run)

    print("Core SQL Rules Engine - Test Suite")
    print("=" * 60)

    for i, rule_id in enumerate(rules_to_run, 1):
        sys.stdout.write(f"\r[{i}/{total}] Testing {rule_id}...")
        sys.stdout.flush()

        summary = runner.run_rule_suite(rule_id)

        has_error = any(t.get("error") for t in summary["positive_tests"] + summary["negative_tests"])

        if has_error:
            results["error"].append(summary)
        elif summary["status"] == "passed":
            results["passed"].append(summary)
        else:
            results["failed"].append(summary)

    sys.stdout.write("\n\n")
    print("=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(
        f"Total: {total} | Passed: {len(results['passed'])} | Failed: {len(results['failed'])} | Errors: {len(results['error'])}"  # noqa
    )

    if results["failed"]:
        print("\nFailed Validation:")
        for s in results["failed"]:
            print(f"  - {s['rule_id']}")
            if args.verbose:
                for t in s["positive_tests"]:
                    if not t["passed"]:
                        print(
                            f"      Case positive/{t['case_id']}: Expected {t['expected']}, Got {t['total_errors']} errors"  # noqa
                        )
                for t in s["negative_tests"]:
                    if not t["passed"]:
                        print(
                            f"      Case negative/{t['case_id']}: Expected {t['expected']}, Got {t['total_errors']} errors"  # noqa
                        )

    if results["error"]:
        print("\nExecution Errors:")
        for s in results["error"]:
            print(f"  - {s['rule_id']}")
            if args.verbose:
                for t in s["positive_tests"]:
                    if t.get("error"):
                        print(f"      Case positive/{t['case_id']}")
                        print(f"      - Error: {t['error']}")
                        if t.get("exception"):
                            print(f"      - Exception: {t['exception']}")
                for t in s["negative_tests"]:
                    if t.get("error"):
                        print(f"      Case negative/{t['case_id']}")
                        print(f"      - Error: {t['error']}")
                        if t.get("exception"):
                            print(f"      - Exception: {t['exception']}")

    sys.exit(1 if results["failed"] or results["error"] else 0)


def generate_rule_results(rule_id: str) -> dict:
    """Function run by the pr comment bot github action run_validation."""
    runner = TestRunner()
    return runner.run_rule_suite(rule_id)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)
