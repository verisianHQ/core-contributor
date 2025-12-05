#!/usr/bin/env python3
"""
Contributor test script for SQL CDISC Rules Engine Contributor Repo.
Runs validation using the engine submodule with PostgreSQL.
"""

import sys
from pathlib import Path
from typing import List, Optional, Tuple
import logging

logging.basicConfig(level=logging.CRITICAL)


def get_available_rules() -> List[str]:
    rules_dir = Path("rules")
    if not rules_dir.exists():
        print("Error: 'rules' directory not found!")
        sys.exit(1)

    rule_dirs = [d.name for d in rules_dir.iterdir() if d.is_dir() and d.name.startswith("CG")]
    return sorted(rule_dirs)


def prompt_for_rule(available_rules: List[str]) -> str:
    print("\nAvailable Rules:")
    print("-" * 60)

    for i, rule in enumerate(available_rules, 1):
        print(f"  {i}. {rule}")

    print("\nWhich rule would you like to test?")

    while True:
        choice = input("Enter rule ID (e.g., CG0001) or number: ").strip()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(available_rules):
                return available_rules[idx]
        elif choice in available_rules:
            return choice

        print(f"Invalid choice. Please enter a number 1-{len(available_rules)} or a valid rule ID.")


def get_test_cases(rule_id: str) -> dict:
    rule_path = Path("rules") / rule_id

    test_cases = {"positive": [], "negative": []}

    for test_type in ["positive", "negative"]:
        test_type_path = rule_path / test_type
        if test_type_path.exists():
            for case_dir in sorted(test_type_path.iterdir()):
                if case_dir.is_dir():
                    data_dir = case_dir / "data"
                    test_files = list(data_dir.glob("*.xlsx"))
                    if test_files:
                        test_cases[test_type].append({"case_id": case_dir.name, "data_path": str(data_dir)})

    return test_cases


def run_validation(
    rule_id: str, test_type: str, case_id: str, data_path: str
) -> Optional[Tuple[Optional[dict], Optional[dict]]]:
    print(f"\nRunning {test_type} test case: {case_id}")

    rule_path = Path("rules") / rule_id

    rule_yaml_files = list(rule_path.glob("*.yml"))
    if not rule_yaml_files:
        print(f"  Error: No rule YAML file found")
        return None

    data_path_obj = Path(data_path)
    excel_files = list(data_path_obj.glob("*.xlsx")) + list(data_path_obj.glob("*.xls"))
    if not excel_files:
        print(f"  Error: No Excel files found")
        return None

    try:
        engine_path = Path("engine")
        if str(engine_path) not in sys.path:
            sys.path.insert(0, str(engine_path))

        from engine.cdisc_rules_engine.utilities.ig_specification import IGSpecification
        from engine.tests.rule_regression.regression import sharepoint_xlsx_to_test_datasets, process_test_case_dataset
        import yaml

        with open(rule_yaml_files[0], "r") as f:
            rule = yaml.safe_load(f)

        print(f"  Loading test data...")
        test_datasets = sharepoint_xlsx_to_test_datasets(str(excel_files[0]))

        regression_errors = {}
        ig_specs = IGSpecification(
            standard="sdtmig", standard_version="3.4", standard_substandard=None, define_xml_version=None
        )

        print(f"  Running validation...")
        sql_results, _ = process_test_case_dataset(
            regression_errors=regression_errors,
            define_xml_file_path=None,
            data_test_datasets=test_datasets,
            ig_specs=ig_specs,
            rule=rule,
            test_case_folder_path=data_path,
            cur_core_id=rule_id,
            use_pgserver=True,
        )

        regression_error_results = None
        if "results_sql" in regression_errors:
            regression_error_results = regression_errors["results_sql"]
            total_errors = sum(len(ds.get("errors", [])) for ds in regression_error_results)
            print(f"  Validation completed: {total_errors} errors found")
            return sql_results, {"datasets": regression_error_results}

        return sql_results, None

    except Exception as e:
        print(f"  Error: {e}")
        import traceback

        traceback.print_exc()
        return None


def json_to_readable(results_data: dict, output_path: Path):
    """Make a readable text file from JSON results."""
    with output_path.open("w") as f:
        datasets = results_data.get("datasets", [])
        
        if not datasets:
            f.write("No validation results found.\n")
            return
        
        total_errors = sum(len(ds.get("errors", [])) for ds in datasets)
        f.write(f"Total Errors Found: {total_errors}\n")
        f.write("\n")
        
        for dataset in datasets:
            dataset_name = dataset.get("dataset", "Unknown")
            domain = dataset.get("domain", "N/A")
            execution_message = dataset.get("execution_message", "")
            errors = dataset.get("errors", [])
            
            f.write(f"Dataset: {dataset_name}\n")
            f.write(f"Domain: {domain}\n")
            if execution_message:
                f.write(f"Rule Message: {execution_message}\n")
            f.write(f"Errors in this dataset: {len(errors)}\n")
            
            if not errors:
                f.write("  No errors found in this dataset.\n")
            else:
                f.write("\n")
                for i, error in enumerate(errors, 1):
                    f.write(f"  Error {i}:\n")
                    
                    row_num = error.get("row")
                    if row_num is not None:
                        f.write(f"    Row: {row_num}\n")
                    
                    for key, val in error.items():
                        if key not in ["row", "value"]:
                            f.write(f"    {key}: {val}\n")
                    
                    value_dict = error.get("value", {})
                    if value_dict:
                        f.write(f"    Problematic values:\n")
                        for key, val in value_dict.items():
                            f.write(f"      {key}: {val}\n")
                    
                    f.write("\n")
            
            f.write("\n")


def analyse_results(rule_id: str, test_cases: dict) -> dict:
    """Analyse test results and determine pass/fail."""
    summary = {"rule_id": rule_id, "positive_tests": [], "negative_tests": [], "status": "passed"}

    for test_type in ["positive", "negative"]:
        expected = "0 errors" if test_type == "positive" else ">0 errors"

        for case in test_cases[test_type]:
            case_id = case["case_id"]
            _, regression_error_results = run_validation(rule_id, test_type, case_id, case["data_path"])

            results_path = Path("rules") / rule_id / test_type / case_id / "results"
            if not results_path.exists():
                results_path.mkdir(parents=True, exist_ok=True)
            
            results_json_file = results_path / "results.json"
            results_txt_file = results_path / "results.txt"
            
            with results_json_file.open("w") as f:
                from json import dump

                if regression_error_results:
                    dump(regression_error_results, f, indent=2)
                else:
                    dump({"datasets": []}, f, indent=2)
            
            if regression_error_results:
                json_to_readable(regression_error_results, results_txt_file)
            else:
                json_to_readable({"datasets": []}, results_txt_file)

            if regression_error_results is None:
                summary[f"{test_type}_tests"].append(
                    {
                        "case_id": case_id,
                        "passed": False,
                        "total_errors": None,
                        "expected": expected,
                        "error": "Failed to run validation",
                        "results_path": str(results_path)
                    }
                )
                summary["status"] = "failed"
                continue

            total_errors = 0
            for dataset_result in regression_error_results.get("datasets", []):
                total_errors += len(dataset_result.get("errors", []))

            if test_type == "positive":
                passed = total_errors == 0
            else:
                passed = total_errors > 0

            summary[f"{test_type}_tests"].append(
                {
                    "case_id": case_id,
                    "passed": passed,
                    "total_errors": total_errors,
                    "expected": expected,
                    "results_path": str(results_path)
                }
            )

            if not passed:
                summary["status"] = "failed"

    return summary


def display_summary(summary: dict):
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    rule_id = summary["rule_id"]
    status = summary["status"]

    print(f"\nRule: {rule_id}")
    print(f"Overall Status: {status.upper()}")

    print(f"\nPositive Test Cases: {len(summary['positive_tests'])}")
    for test in summary["positive_tests"]:
        case_id = test["case_id"]
        passed = test["passed"]
        status_symbol = "[PASS]" if passed else "[FAIL]"
        results_path = test.get("results_path", "")
        print(f"  {status_symbol} Case {case_id} - Results at: {results_path}")
        if not passed:
            print(f"      Expected: {test['expected']}")
            if test.get("total_errors") is not None:
                print(f"      Got: {test['total_errors']} errors")
            if test.get("error"):
                print(f"      Error: {test['error']}")

    print(f"\nNegative Test Cases: {len(summary['negative_tests'])}")
    for test in summary["negative_tests"]:
        case_id = test["case_id"]
        passed = test["passed"]
        status_symbol = "[PASS]" if passed else "[FAIL]"
        results_path = test.get("results_path", "")
        print(f"  {status_symbol} Case {case_id} - Results at: {results_path}")
        if not passed:
            print(f"      Expected: {test['expected']}")
            if test.get("total_errors") is not None:
                print(f"      Got: {test['total_errors']} errors")
            if test.get("error"):
                print(f"      Error: {test['error']}")

    print("\n" + "=" * 60)


def generate_rule_results(rule_id: str, save_results: bool = True) -> dict:
    """
    Generate validation results for a rule. Called by github actions.
    """
    summary = {"rule_id": rule_id, "positive_tests": [], "negative_tests": [], "status": "passed"}

    rule_path = Path("rules") / rule_id

    rule_yaml_files = list(rule_path.glob("*.yml"))
    if not rule_yaml_files:
        return summary

    engine_path = Path("engine")
    if str(engine_path) not in sys.path:
        sys.path.insert(0, str(engine_path))

    try:
        from engine.cdisc_rules_engine.utilities.ig_specification import IGSpecification
        from engine.tests.rule_regression.regression import sharepoint_xlsx_to_test_datasets, process_test_case_dataset
        import yaml

        with open(rule_yaml_files[0], "r") as f:
            rule = yaml.safe_load(f)

        ig_specs = IGSpecification(
            standard="sdtmig", standard_version="3.4", standard_substandard=None, define_xml_version=None
        )

        for test_type in ["positive", "negative"]:
            test_type_path = rule_path / test_type
            if not test_type_path.exists():
                continue

            expected = "0 errors" if test_type == "positive" else ">0 errors"

            for case_dir in sorted(test_type_path.iterdir()):
                if not case_dir.is_dir():
                    continue

                case_id = case_dir.name
                data_dir = case_dir / "data"

                excel_files = list(data_dir.glob("*.xlsx")) + list(data_dir.glob("*.xls"))
                if not excel_files:
                    continue

                try:
                    test_datasets = sharepoint_xlsx_to_test_datasets(str(excel_files[0]))

                    regression_errors = {}
                    sql_results, _ = process_test_case_dataset(
                        regression_errors=regression_errors,
                        define_xml_file_path=None,
                        data_test_datasets=test_datasets,
                        ig_specs=ig_specs,
                        rule=rule,
                        test_case_folder_path=str(data_dir),
                        cur_core_id=rule_id,
                        use_pgserver=True,
                    )

                    if "results_sql" not in regression_errors:
                        summary[f"{test_type}_tests"].append(
                            {
                                "case_id": case_id,
                                "passed": False,
                                "total_errors": None,
                                "expected": expected,
                                "error": "No SQL results",
                            }
                        )
                        summary["status"] = "failed"
                        continue

                    regression_error_results = regression_errors["results_sql"]
                    total_errors = sum(len(ds.get("errors", [])) for ds in regression_error_results)

                    if save_results:
                        results_path = Path("rules") / rule_id / test_type / case_id / "results"
                        results_path.mkdir(parents=True, exist_ok=True)
                        results_json_file = results_path / "results.json"
                        results_txt_file = results_path / "results.txt"

                        with results_json_file.open("w") as f:
                            from json import dump
                            dump({"datasets": regression_error_results}, f, indent=2)
                        
                        json_to_readable({"datasets": regression_error_results}, results_txt_file)

                    if test_type == "positive":
                        passed = total_errors == 0
                    else:
                        passed = total_errors > 0

                    summary[f"{test_type}_tests"].append(
                        {"case_id": case_id, "passed": passed, "total_errors": total_errors, "expected": expected}
                    )

                    if not passed:
                        summary["status"] = "failed"

                except Exception as e:
                    import traceback

                    traceback.print_exc()

                    summary[f"{test_type}_tests"].append(
                        {
                            "case_id": case_id,
                            "passed": False,
                            "total_errors": None,
                            "expected": expected,
                            "error": str(e),
                        }
                    )
                    summary["status"] = "failed"

    except Exception as e:
        import traceback

        traceback.print_exc()

    return summary


def main():
    print("Core SQL Rules Engine - Contributor Test Suite")
    print("=" * 60)

    available_rules = get_available_rules()

    if not available_rules:
        print("Error: No rules found in the 'rules' directory!")
        sys.exit(1)

    rule_id = prompt_for_rule(available_rules)

    print(f"\nCollecting test cases for {rule_id}...")
    test_cases = get_test_cases(rule_id)

    if not test_cases["positive"] and not test_cases["negative"]:
        print(f"Error: No test cases found for {rule_id}")
        sys.exit(1)

    print(f"Found {len(test_cases['positive'])} positive and {len(test_cases['negative'])} negative test cases")

    summary = analyse_results(rule_id, test_cases)
    display_summary(summary)

    if summary["status"] == "failed":
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest suite interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
