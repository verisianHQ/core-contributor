from pathlib import Path

from src.components.utils import UtilityFunctions
from src.constants import SOT_PATH, RULES_DIR, CG_CSV_PATH


def path_extender(path):
    script_dir = Path(__file__).parent.parent
    full_path = script_dir / path
    return full_path


class IngestedData:

    util = UtilityFunctions

    rules_path = path_extender(RULES_DIR)
    cg_csv_path = path_extender(CG_CSV_PATH)

    completed_rules = util.yml_folders(rules_path)
    core_status_data = util.get_yaml_fields(rules_path, keys=["Core", "Status"])
    verified_data = util.get_yaml_fields(rules_path, keys=["Verification"], null_value="Unverified")
    sot_rules = util.get_csv_cols(SOT_PATH)
    sdtm_rules = util.filter_standard(sot_rules, "SDTMIG")
    test_stats = util.get_test_execution_stats(rules_path)
    cg_data = util.get_csv_completion_data(cg_csv_path)
    els_verified_data = util.get_csv_cols(cg_csv_path, cols=["Rule ID"])
