#!/usr/bin/env python3
"""
Contributor test script for SQL CDISC Rules Engine Contributor Repo.
"""

import sys
import argparse
import json
import logging
import warnings
from pathlib import Path
from typing import List, Optional, Tuple, Any

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
logging.basicConfig(level=logging.CRITICAL)

RULES_DIR = Path("rules")
ENGINE_DIR = Path("engine")


class ResultReporter:
    """Handles formatting, printing, and saving of test results."""

    @staticmethod
    def json_to_readable(results_data: dict, output_path: Path):
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
                            if key not in ["row", "value"]:
                                f.write(f"    {key}: {val}\n")
                        
                        if value_dict := error.get("value", {}):
                            f.write("    Problematic values:\n")
                            for k, v in value_dict.items():
                                f.write(f"      {k}: {v}\n")
                        f.write("\n")
                f.write("\n")

    @staticmethod
    def save_case_results(rule_id: str, test_type: str, case_id: str, results: dict):
        """Saves JSON and TXT results to the file system."""
        results_path = RULES_DIR / rule_id / test_type / case_id / "results"
        results_path.mkdir(parents=True, exist_ok=True)

        with (results_path / "results.json").open("w") as f:
            json.dump(results, f, indent=2)

        ResultReporter.json_to_readable(results, results_path / "results.txt")
        return str(results_path)

    @staticmethod
    def display_rule_summary(summary: dict):
        """Prints the execution summary for a single rule to the console."""
        print(f"\n{'='*60}\n{summary['rule_id']} Test Results Summary")
        print(f"\nRule: {summary['rule_id']}")
        print(f"Overall Status: {summary['status'].upper()}")

        for test_type in ["positive", "negative"]:
            tests = summary[f"{test_type}_tests"]
            print(f"\n{test_type.capitalize()} Test Cases: {len(tests)}")
            for test in tests:
                symbol = "[PASS]" if test["passed"] else "[FAIL]"
                print(f"  {symbol} Case {test['case_id']} - Results at: {test['results_path']}")
                if not test["passed"]:
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
        self.ig_specs = None
        self._init_engine_specs()

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
                        if list(data_dir.glob("*.xls*")):
                            cases[test_type].append({"case_id": case_dir.name, "data_path": str(data_dir)})
        return cases

    def _init_engine_specs(self):
        """Initialises IG Specifications once to avoid overhead."""
        try:
            from engine.cdisc_rules_engine.utilities.ig_specification import IGSpecification
            self.ig_specs = IGSpecification(
                standard="sdtmig", standard_version="3.4", 
                standard_substandard=None, define_xml_version=None
            )
        except ImportError:
            print("Error: Could not import engine modules. Is the submodule initialised?")
            sys.exit(1)

    def run_validation(self, rule_id: str, data_path: str) -> Tuple[Any, Optional[dict]]:
        """Invokes the engine to validate data against the rule."""
        rule_path = RULES_DIR / rule_id
        rule_ymls = list(rule_path.glob("*.yml"))
        
        if not rule_ymls:
            return None, {"error": "Rule YAML missing", "exception": f"No YAML found in {rule_path}"}

        data_path_obj = Path(data_path)
        excel_files = list(data_path_obj.glob("*.xlsx")) + list(data_path_obj.glob("*.xls"))
        
        if not excel_files:
            return None, {"error": "Excel data missing", "exception": f"No Excel files in {data_path}"}

        try:
            import yaml
            from engine.tests.rule_regression.regression import sharepoint_xlsx_to_test_datasets, process_test_case_dataset

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
            return None, {"error": f"No result - either the rule or test case data {excel_files[0].name} is broken", "exception": str(e)}

    def evaluate_case(self, rule_id: str, test_type: str, case_info: dict) -> dict:
        """Runs validation, saves results, and determines pass/fail status."""
        case_id = case_info["case_id"]
        expected = "0 errors" if test_type == "positive" else ">0 errors"
        
        _, results_data = self.run_validation(rule_id, case_info["data_path"])
        
        if results_data is None:
             results_data = {
                "error": "Unknown Error",
                "exception": "Engine returned None"
            }

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
            "results_path": results_path
        }

    def run_rule_suite(self, rule_id: str, specific_case: str = None) -> dict:
        """Runs all (or one) test cases for a specific rule."""
        summary = {
            "rule_id": rule_id,
            "positive_tests": [], 
            "negative_tests": [],
            "status": "passed"
        }
        
        all_cases = self.get_test_cases(rule_id)
        
        if specific_case:
            target_type, target_id = specific_case.split('/')
            all_cases = {
                target_type: [c for c in all_cases[target_type] if c['case_id'] == target_id]
            }
            if target_type == "positive": all_cases["negative"] = []
            else: all_cases["positive"] = []

        if not all_cases["positive"] and not all_cases["negative"]:
            return summary

        for test_type in ["positive", "negative"]:
            for case in all_cases[test_type]:
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
            if choice in available: return choice
            print(f"Invalid. Available: {', '.join(available[:5])}...")

    @staticmethod
    def prompt_case(available: dict) -> Optional[str]:
        print("\nTest specific case? (Leave blank for all)")
        flat_list = []
        for t_type in ["positive", "negative"]:
            for c in available[t_type]:
                flat_list.append(f"{t_type}/{c['case_id']}")
        
        if not flat_list: return None

        for i, tc in enumerate(flat_list, 1):
            print(f"  {i}. {tc}")

        while True:
            choice = input("\nEnter case (e.g., positive/01, number, or Enter): ").strip()
            if not choice: return None
            if choice in flat_list: return choice
            if choice.isdigit() and 0 <= int(choice)-1 < len(flat_list):
                return flat_list[int(choice)-1]
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

    if not args.rule and not args.all_rules:
        rule_id = InteractiveHandler.prompt_rule(available_rules)
        cases = runner.get_test_cases(rule_id)
        specific_case = InteractiveHandler.prompt_case(cases)
        
        print(f"\nRunning {rule_id}...")
        summary = runner.run_rule_suite(rule_id, specific_case)
        ResultReporter.display_rule_summary(summary)
        sys.exit(0 if summary["status"] == "passed" else 1)

    if args.test_case and not args.rule:
        print("Error: --test-case requires --rule.")
        sys.exit(1)

    rules_to_run = available_rules if args.all_rules else [args.rule]
    if not args.all_rules and args.rule not in available_rules:
        print(f"Error: Rule {args.rule} not found.")
        sys.exit(1)

    results = {"passed": [], "failed": [], "error": []}
    total = len(rules_to_run)
    use_bar = args.all_rules

    for i, rule_id in enumerate(rules_to_run, 1):
        if use_bar:
            sys.stdout.write(f"\r[{i}/{total}] Testing {rule_id}...")
            sys.stdout.flush()
        
        summary = runner.run_rule_suite(rule_id, args.test_case)
        
        has_error = any(t.get("error") for t in summary["positive_tests"] + summary["negative_tests"])
        
        if has_error:
            results["error"].append(summary)
        elif summary["status"] == "passed":
            results["passed"].append(summary)
        else:
            results["failed"].append(summary)

        if not use_bar:
            ResultReporter.display_rule_summary(summary)

    if use_bar:
        sys.stdout.write("\n\n")
        print("=" * 60)
        print("FINAL SUMMARY")
        print("=" * 60)
        print(f"Total: {total} | Passed: {len(results['passed'])} | Failed: {len(results['failed'])} | Errors: {len(results['error'])}")
        
        if results["failed"]:
            print("\nFailed Validation:")
            for s in results["failed"]: print(f"  - {s['rule_id']}")
        
        if results["error"]:
            print("\nExecution Errors:")
            for s in results["error"]: print(f"  - {s['rule_id']}")

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
