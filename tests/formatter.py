import sys
from pathlib import Path
from typing import List, Optional, Dict
import openpyxl
from openpyxl.styles import Font, PatternFill

RULES_DIR = Path("rules")

BOLD_FONT = Font(bold=True)
ITALIC_FONT = Font(italic=True)
METADATA_FILL = PatternFill(start_color="FFFFCC", end_color="FFFFCC", fill_type="solid")

class FileManager:
    """Collect test case files from repo."""

    @staticmethod
    def get_available_rules() -> List[str]:
        if not RULES_DIR.exists():
            return []
        return sorted([d.name for d in RULES_DIR.iterdir() if d.is_dir() and d.name.startswith("CORE-")])

    @staticmethod
    def get_all_test_cases() -> List[dict]:
        """Returns a flat list of all test cases across all rules."""
        all_cases = []
        rules = FileManager.get_available_rules()
        for rule in rules:
            all_cases.extend(FileManager.get_test_cases(rule))
        return all_cases

    @staticmethod
    def get_test_cases(rule_id: str) -> list:
        rule_path = RULES_DIR / rule_id
        cases = []

        for test_type in ["positive", "negative"]:
            test_type_path = rule_path / test_type
            if test_type_path.exists():
                for case_dir in sorted(test_type_path.iterdir()):
                    if case_dir.is_dir():
                        data_dir = case_dir / "data"
                        # Grab all excel files that aren't temp files (~$)
                        data_files = list(data_dir.glob("[!~]*.xls*"))
                        if data_files:
                            cases.append(
                                {
                                    "rule_id": rule_id,
                                    "case_id": case_dir.name,
                                    "type": test_type,
                                    "path": data_files[0]
                                }
                            )
        return cases


class LabelManager:
    """Scrapes existing 'Datasets' sheets to learn label mappings."""
    
    def __init__(self):
        self.label_map: Dict[str, str] = {}

    def scan_all_files(self, cases: List[dict]):
        print("Scanning all files to build dataset label map...")
        for case in cases:
            try:
                wb = openpyxl.load_workbook(case["path"], read_only=True, data_only=True)
                if "Datasets" in wb.sheetnames:
                    ws = wb["Datasets"]
                    for row in ws.iter_rows(min_row=2, values_only=True):
                        if row and len(row) >= 2:
                            fname = row[0]
                            flabel = row[1]
                            if fname and flabel and isinstance(fname, str):
                                self.label_map[fname] = flabel
                wb.close()
            except Exception as e:
                print(f"Warning: Could not scan {case['path']}: {e}")
        
        print(f"Found {len(self.label_map)} unique dataset labels.")

    def get_label(self, filename: str) -> str:
        return self.label_map.get(filename, "Unknown Dataset")


class Formatter:
    """Handle formatting and styling of xlsx files using openpyxl."""
    
    def __init__(self, file_path: Path, label_manager: LabelManager):
        self.file_path = file_path
        self.label_manager = label_manager
        self.wb = None

    def format(self) -> bool:
        try:
            self.wb = openpyxl.load_workbook(self.file_path)
            
            self._ensure_library_sheet()
            self._ensure_datasets_sheet()
            self._format_xpt_sheets()
            
            self.wb.save(self.file_path)
            return True
        except Exception as e:
            print(f"Failed to format {self.file_path}: {e}")
            return False

    def _ensure_library_sheet(self):
        """Creates or updates the Library sheet."""
        if "Library" in self.wb.sheetnames:
            ws = self.wb["Library"]
        else:
            ws = self.wb.create_sheet("Library", 0)

        ws["A1"] = "Product"
        ws["B1"] = "Version"
        ws["A1"].font = BOLD_FONT
        ws["B1"].font = BOLD_FONT
        ws["A2"] = "sdtmig" if ws["A2"] else ws["A2"]
        ws["B2"] = "3-4" if ws["B2"] else ws["B2"]

    def _ensure_datasets_sheet(self):
        """Creates or updates the Datasets sheet based on .xpt sheets present."""
        if "Datasets" in self.wb.sheetnames:
            ws = self.wb["Datasets"]
            ws.delete_rows(1, ws.max_row)
        else:
            ws = self.wb.create_sheet("Datasets", 1)

        ws["A1"] = "Filename"
        ws["B1"] = "Label"
        ws["A1"].font = BOLD_FONT
        ws["B1"].font = BOLD_FONT

        xpt_sheets = [name for name in self.wb.sheetnames if name.lower().endswith(".xpt")]
        
        for index, sheet_name in enumerate(xpt_sheets, start=2):
            label = self.label_manager.get_label(sheet_name)
            ws.cell(row=index, column=1, value=sheet_name)
            ws.cell(row=index, column=2, value=label)

    def _format_xpt_sheets(self):
        """Applies styling to all .xpt sheets."""
        for sheet_name in self.wb.sheetnames:
            if not sheet_name.lower().endswith(".xpt"):
                continue
            
            ws = self.wb[sheet_name]
            
            # Rule 1: Top row bold
            for cell in ws[1]:
                cell.font = BOLD_FONT
            
            # Rule 2: Rows 2-4 highlighted #FFFFCC and italic
            for row in ws.iter_rows(min_row=2, max_row=4):
                for cell in row:
                    cell.fill = METADATA_FILL
                    cell.font = ITALIC_FONT
            
            # Rule 3: Rows 5+ unstyled

class InteractiveHandler:
    """Handles user prompts for interactive mode."""

    @staticmethod
    def prompt_case(available: list[dict]) -> Optional[list[dict]]:
        print(f"\nFound {len(available)} total test cases.")
        print("Format specific case? (Leave blank for all)")
        
        lookup = []
        for idx, tc in enumerate(available):
            id_str = f"{tc['rule_id']}/{tc['type']}/{tc['case_id']}"
            lookup.append(id_str)

        while True:
            choice = input("\nEnter case (e.g., CORE-000424/positive/01) or Enter for all): ").strip()
            
            if not choice:
                return available
            
            matches = [tc for tc in available if f"{tc['rule_id']}/{tc['type']}/{tc['case_id']}" == choice]
            if matches:
                return matches
                
            print("Invalid choice. Try again.")


def main():
    all_cases = FileManager.get_all_test_cases()

    if not all_cases:
        print("Error: No test cases found in 'rules' directory.")
        sys.exit(1)

    label_manager = LabelManager()
    label_manager.scan_all_files(all_cases)

    selected_cases = InteractiveHandler.prompt_case(all_cases)
    
    if not selected_cases:
        print("No cases selected.")
        sys.exit(0)

    print(f"\nProcessing {len(selected_cases)} files...")
    success_count = 0
    
    for case in selected_cases:
        print(f" -> Formatting {case['rule_id']}/{case['type']}/{case['case_id']} ... ", end="")
        formatter = Formatter(case['path'], label_manager)
        if formatter.format():
            print("OK")
            success_count += 1
        else:
            print("FAILED")

    print(f"\nDone. {success_count}/{len(selected_cases)} files formatted.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)