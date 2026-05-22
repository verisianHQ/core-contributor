import pandas as pd
from pathlib import Path
from src.components.utils import UtilityFunctions
from src.constants import RULES_DIR, CG_CSV_PATH, FDA_CSV_PATH


def path_extender(path):
    script_dir = Path(__file__).parent.parent
    full_path = script_dir / path
    return full_path


class IngestedData:

    util = UtilityFunctions

    rules_path = path_extender(RULES_DIR)
    cg_csv_path = path_extender(CG_CSV_PATH)
    fda_csv_path = path_extender(FDA_CSV_PATH)

    cg_raw = util.load_and_filter_csv(cg_csv_path, standard="SDTMIG")
    fda_raw = util.load_and_filter_csv(fda_csv_path, standard="FDA")
    
    repo_rules = util.yml_folders(rules_path)
    core_status_data = util.get_yaml_fields(rules_path, repo_rules, keys=["Core", "Status"])
    verified_data = util.get_yaml_verified(rules_path, repo_rules)
    sdtm_rules = pd.concat([cg_raw, fda_raw], ignore_index=True)
    
    test_stats = util.get_test_execution_stats(rules_path)
    cg_data = util.get_csv_completion_data(cg_raw)
    fda_data = util.get_csv_completion_data(fda_raw)
    
    els_verified_data = pd.concat([
        cg_raw[["Rule ID"]] if not cg_raw.empty else pd.DataFrame(columns=["Rule ID"]),
        fda_raw[["Rule ID"]] if not fda_raw.empty else pd.DataFrame(columns=["Rule ID"])
    ], ignore_index=True)