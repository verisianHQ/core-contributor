"""
Script to create a new rule directory with the required structure and template files for testing.
"""

import sys
import shutil
from pathlib import Path
import openpyxl

RULES_DIR = Path("rules")
PLACEHOLDER_RULE_ID = "NEW-RULE"

def create_excel_file(filepath: Path, is_negative: bool):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    ws_lib = wb.create_sheet("Library")
    ws_lib.append(["Product", "Version"])
    ws_lib["A2"] = "sdtmig"
    ws_lib["B2"] = "3-4"

    ws_data = wb.create_sheet("Datasets")
    ws_data.append(["Filename", "Label"])
    ws_data.append(["", ""])

    if is_negative:
        ws_val = wb.create_sheet("Validation")
        ws_val.append(["Error group", "Sheet", "Error level", "Row num", "Variable", "Error value"])
        ws_val.append(["", "", "", "", "", ""])

    wb.save(filepath)

def create_test_cases(rule_dir: Path, test_type: str, count: int):
    for i in range(1, count + 1):
        case_id = f"{i:02d}"
        case_dir = rule_dir / test_type / case_id
        
        data_dir = case_dir / "data"
        results_dir = case_dir / "results"
        data_dir.mkdir(parents=True, exist_ok=True)
        results_dir.mkdir(parents=True, exist_ok=True)
        
        excel_filename = f"{PLACEHOLDER_RULE_ID.lower()}-{test_type}-{case_id}.xlsx"
        excel_path = data_dir / excel_filename
        create_excel_file(excel_path, is_negative=(test_type == "negative"))

def main():
    rule_dir = RULES_DIR / PLACEHOLDER_RULE_ID

    if rule_dir.exists():
        do_wipe: bool = True if input("Another new rule folder already exists. Would you like to erase it and make a new one? (Y/N) ").lower() == "y" else False
        if not do_wipe:
            print("Aborting.")
            sys.exit(0)
        shutil.rmtree(rule_dir, ignore_errors=False)

    rule_dir.mkdir(parents=True, exist_ok=True)

    yml_file = rule_dir / f"{PLACEHOLDER_RULE_ID.lower()}.yml"
    shutil.copy("tests/template-rule.yml", yml_file)

    n_pos_cases = int(input("Enter the number of positive test cases to create: "))
    n_neg_cases = int(input("Enter the number of negative test cases to create: "))

    if n_pos_cases > 0:
        create_test_cases(rule_dir, "positive", n_pos_cases)

    if n_neg_cases > 0:
        create_test_cases(rule_dir, "negative", n_neg_cases)

    print(f"\nSuccess!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)