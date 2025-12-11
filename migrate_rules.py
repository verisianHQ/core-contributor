import os
import shutil
import re
from pathlib import Path

# These paths are specific to Maximo Lopez's (@YetiGonk) environment
RULES_SOURCE_DIR = Path("../../Downloads/Rules")
TEST_DATA_SOURCE_DIR = Path("../cdisc-rules-engine/tests/resources/unitTesting/SDTMIG")
REPO_RULES_DIR = Path("./rules")

def get_core_id_from_yaml(file_path):
    """
    Reads a YAML file and extracts the value of 'Id' nested under 'Core'.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        match = re.search(r'Core:\s*\n\s*Id:\s*[\'"]?(CORE-[A-Za-z0-9]+)[\'"]?', content)
        if match:
            return match.group(1)
            
        match_simple = re.search(r'\bId:\s*[\'"]?(CORE-[A-Za-z0-9]+)[\'"]?', content)
        if match_simple:
            return match_simple.group(1)
            
    except Exception as e:
        print(f"Error reading {file_path.name}: {e}")
    
    return None

def migrate():
    print("Starting migration...")
    
    if not REPO_RULES_DIR.exists():
        print(f"ERROR: Destination directory does not exist: {REPO_RULES_DIR}")
        return

    rule_files = list(RULES_SOURCE_DIR.glob("CG*.yaml")) + list(RULES_SOURCE_DIR.glob("CG*.yml"))
    
    if not rule_files:
        print(f"No YAML files starting with 'CG' found in {RULES_SOURCE_DIR}")
        return

    for rule_file in rule_files:
        print(f"\nProcessing {rule_file.name}...")
        
        core_id = get_core_id_from_yaml(rule_file)
        if not core_id:
            print(f"SKIPPED: Could not find 'Core: Id: CORE-XXXXXX' in {rule_file.name}")
            continue

        cg_match = re.match(r'(CG\d+)', rule_file.name)
        if not cg_match:
            print(f"SKIPPED: Could not extract CG identifier from filename {rule_file.name}")
            continue
        cg_id = cg_match.group(1)

        dest_rule_path = REPO_RULES_DIR / core_id
        os.makedirs(dest_rule_path, exist_ok=True)
        
        shutil.copy2(rule_file, dest_rule_path / rule_file.name)
        print(f"Rule copied to {dest_rule_path}")

        source_test_path = TEST_DATA_SOURCE_DIR / cg_id
        
        if not source_test_path.exists():
            print(f"WARNING: No test data folder found at: {source_test_path}")
            continue

        for test_type in ["positive", "negative"]:
            src_type_dir = source_test_path / test_type
            
            if not src_type_dir.exists():
                continue

            for case_dir in src_type_dir.iterdir():
                if not case_dir.is_dir():
                    continue

                src_data_dir = case_dir / "data"
                
                dest_case_dir = dest_rule_path / test_type / case_dir.name
                dest_data_dir = dest_case_dir / "data"
                dest_results_dir = dest_case_dir / "results"

                if src_data_dir.exists():
                    if dest_data_dir.exists():
                        shutil.rmtree(dest_data_dir)
                    
                    shutil.copytree(src_data_dir, dest_data_dir)
                    print(f"Copied {test_type}/{case_dir.name} data")
                else:
                    print(f"WARNING: No data folder in {test_type}/{case_dir.name}")

                if dest_results_dir.exists():
                    shutil.rmtree(dest_results_dir)
                os.makedirs(dest_results_dir)

    print("\nMigration completed")

if __name__ == "__main__":
    migrate()