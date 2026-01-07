from pathlib import Path

from src.components.utils import UtilityFunctions
from src.constants import SOT_PATH, RULES_DIR, CG_LIB_PATH, CG_CSV_PATH


def path_extender(path):
    script_dir = Path(__file__).parent.parent
    full_path = script_dir / path
    return full_path


class IngestedData:
    util = UtilityFunctions

    rules_path = path_extender(RULES_DIR)
    cg_path = path_extender(CG_LIB_PATH)
    cg_csv_path = path_extender(CG_CSV_PATH)

    repo_rules = util.get_all_yml_data(rules_path)
    sot_rules = util.get_csv_cols(SOT_PATH)
    
    test_stats = util.get_test_execution_stats(rules_path)
    cg_data = util.get_xlsx_completion_data(cg_path)
    els_verified_data = util.get_csv_cols(cg_csv_path, cols=["Rule ID"])
