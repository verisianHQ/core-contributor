#!/usr/bin/env python3
"""
Contributor test script for CDISC Rules Engine.
Runs validation using the engine submodule with PostgreSQL.
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple
import logging

logging.basicConfig(level=logging.CRITICAL)

def check_setup() -> bool:
    """Verify that setup has been completed, run setup if needed."""
    venv_path = Path("engine/venv")
    engine_path = Path("engine")
    
    if not engine_path.exists() or not any(engine_path.iterdir()):
        print("Engine submodule not initialized.")
        return run_setup()
    
    if not venv_path.exists():
        print("Virtual environment not found.")
        return run_setup()
    
    return True


def run_setup() -> bool:
    """Run the appropriate setup script for the current platform."""
    print("\nRunning setup...")
    
    setup_path = Path("setup")
    if sys.platform == "win32":
        setup_script = "setup.bat"
    else:
        setup_script = "setup.sh"
        subprocess.run(["chmod", "+x", setup_path / setup_script], check=False)
    
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                [setup_path / setup_script],
                shell=True,
                cwd=Path.cwd()
            )
        else:
            result = subprocess.run(
                ["bash", setup_path / setup_script],
                cwd=Path.cwd()
            )
        
        if result.returncode == 0:
            print("\nSetup completed successfully!")
            return True
        else:
            print(f"\nSetup failed with return code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"\nError running setup: {e}")
        return False


def get_available_rules() -> List[str]:
    """Get list of available rule directories."""
    rules_dir = Path("rules")
    if not rules_dir.exists():
        print("Error: 'rules' directory not found!")
        sys.exit(1)
    
    rule_dirs = [d.name for d in rules_dir.iterdir() if d.is_dir() and d.name.startswith("CG")]
    return sorted(rule_dirs)


def prompt_for_rule(available_rules: List[str]) -> str:
    """Prompt user to select which rule to test."""
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
    """Get positive and negative test cases for a rule."""
    rule_path = Path("rules") / rule_id
    
    test_cases = {
        "positive": [],
        "negative": []
    }
    
    for test_type in ["positive", "negative"]:
        test_type_path = rule_path / test_type
        if test_type_path.exists():
            for case_dir in sorted(test_type_path.iterdir()):
                if case_dir.is_dir():
                    data_dir = case_dir / "data"
                    test_files = list(data_dir.glob("*.xlsx"))
                    if test_files:
                        test_cases[test_type].append({
                            "case_id": case_dir.name,
                            "data_path": str(data_dir)
                        })
    
    return test_cases


def run_validation(rule_id: str, test_type: str, case_id: str, data_path: str) -> Tuple[Optional[dict], Optional[dict]]:
    """Run validation using engine's regression test infrastructure."""
    print(f"\nRunning {test_type} test case: {case_id}")
    
    rule_path = Path("rules") / rule_id
    
    # Find rule YAML
    rule_yaml_files = list(rule_path.glob("*.yml"))
    if not rule_yaml_files:
        print(f"  Error: No rule YAML file found")
        return None
    
    # Find Excel file
    data_path_obj = Path(data_path)
    excel_files = list(data_path_obj.glob("*.xlsx")) + list(data_path_obj.glob("*.xls"))
    if not excel_files:
        print(f"  Error: No Excel files found")
        return None
    
    try:
        # Add engine to path
        engine_path = Path("engine")
        if str(engine_path) not in sys.path:
            sys.path.insert(0, str(engine_path))
        
        from engine.tests.rule_regression.regression import sharepoint_xlsx_to_test_datasets, process_test_case_dataset
        import yaml
        
        # Load rule
        with open(rule_yaml_files[0], 'r') as f:
            rule = yaml.safe_load(f)
        
        # Convert Excel to TestDatasets
        print(f"  Loading test data...")
        test_datasets = sharepoint_xlsx_to_test_datasets(str(excel_files[0]))
        
        # Setup args for process_test_case_dataset
        regression_errors = {}
        from engine.cdisc_rules_engine.utilities.ig_specification import IGSpecification
        ig_specs = IGSpecification(
            standard="sdmtig",
            standard_version="3.4",
            standard_substandard=None,
            define_xml_version=None
        )
        
        # Run validation
        print(f"  Running validation...")
        sql_results, _ = process_test_case_dataset(
            regression_errors=regression_errors,
            define_xml_file_path=None,
            data_test_datasets=test_datasets,
            ig_specs=ig_specs,
            rule=rule,
            test_case_folder_path=data_path,
            cur_core_id=rule_id,
            use_pgserver=True
        )

        # Extract results from regression_errors dict
        regression_error_results = None
        if "results_sql" in regression_errors:
            regression_error_results = regression_errors["results_sql"]
            total_errors = sum(len(ds.get('errors', [])) for ds in regression_error_results)
            print(f"  Validation completed: {total_errors} errors found")
            return sql_results, {"datasets": regression_error_results}
        
        return sql_results, None
        
    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def analyze_results(rule_id: str, test_cases: dict) -> dict:
    """Analyze test results and determine pass/fail."""
    summary = {
        "rule_id": rule_id,
        "positive_tests": [],
        "negative_tests": [],
        "status": "passed"
    }
    
    for test_type in ["positive", "negative"]:
        expected = "0 errors" if test_type == "positive" else ">0 errors"
        
        for case in test_cases[test_type]:
            case_id = case["case_id"]
            sql_results, regression_error_results = run_validation(rule_id, test_type, case_id, case["data_path"])
            
            results_path = Path("rules") / rule_id / test_type / case_id / "results"
            if not results_path.exists():
                results_path.mkdir(parents=True, exist_ok=True)
            results_path /= "results.json"
            with results_path.open("w") as f:
                from json import dump
                dump(sql_results, f, indent=2)

            if regression_error_results is None:
                summary[f"{test_type}_tests"].append({
                    "case_id": case_id,
                    "passed": False,
                    "total_errors": None,
                    "expected": expected,
                    "error": "Failed to run validation"
                })
                summary["status"] = "failed"
                continue
            
            total_errors = 0
            for dataset_result in regression_error_results.get("datasets", []):
                total_errors += len(dataset_result.get("errors", []))
            
            if test_type == "positive":
                passed = (total_errors == 0)
            else:
                passed = (total_errors > 0)
            
            summary[f"{test_type}_tests"].append({
                "case_id": case_id,
                "passed": passed,
                "total_errors": total_errors,
                "expected": expected
            })
            
            if not passed:
                summary["status"] = "failed"
    
    return summary


def display_summary(summary: dict):
    """Display test results summary."""
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    rule_id = summary["rule_id"]
    status = summary["status"]
    
    print(f"\nRule: {rule_id}")
    print(f"Overall Status: {status.upper()}")
    
    print(f"\nPositive Test Cases: {len(summary['positive_tests'])}")
    for test in summary["positive_tests"]:
        case_id = test["case_id"]
        passed = test["passed"]
        status_symbol = "[PASS]" if passed else "[FAIL]"
        print(f"  {status_symbol} Case {case_id}")
        if not passed:
            print(f"      Expected: {test['expected']}")
            if test.get('total_errors') is not None:
                print(f"      Got: {test['total_errors']} errors")
            if test.get('error'):
                print(f"      Error: {test['error']}")
    
    print(f"\nNegative Test Cases: {len(summary['negative_tests'])}")
    for test in summary["negative_tests"]:
        case_id = test["case_id"]
        passed = test["passed"]
        status_symbol = "[PASS]" if passed else "[FAIL]"
        print(f"  {status_symbol} Case {case_id}")
        if not passed:
            print(f"      Expected: {test['expected']}")
            if test.get('total_errors') is not None:
                print(f"      Got: {test['total_errors']} errors")
            if test.get('error'):
                print(f"      Error: {test['error']}")
    
    print("\n" + "="*60)
    
    results_path = Path("rules") / rule_id / "results"
    print(f"\nDetailed results saved to: {results_path}")


def main():
    """Main execution function."""
    print("CDISC Rules Engine - Contributor Test Suite")
    print("="*60)
    
    if not check_setup():
        sys.exit(1)
    
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
    
    summary = analyze_results(rule_id, test_cases)
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