import pandas as pd
from pathlib import Path
from src.components.utils import UtilityFunctions
from src.constants import SDTM_RULES_DIR, CG_CSV_PATH, FDA_CSV_PATH, ADAM_CSV_PATH, ADAM_RULES_DIR


def path_extender(path):
    script_dir = Path(__file__).parent.parent
    full_path = script_dir / path
    return full_path


class IngestedData:

    util = UtilityFunctions

    sdtm_rules_path = path_extender(SDTM_RULES_DIR)
    adam_rules_path = path_extender(ADAM_RULES_DIR)
    cg_csv_path = path_extender(CG_CSV_PATH)
    fda_csv_path = path_extender(FDA_CSV_PATH)
    adam_csv_path = path_extender(ADAM_CSV_PATH)

    cg_raw = util.load_and_filter_csv(cg_csv_path, standard="SDTMIG")
    fda_raw = util.load_and_filter_csv(fda_csv_path, standard="FDA")
    adam_raw = util.load_and_filter_csv(adam_csv_path, standard="ADaM")
    
    sdtm_repo_rules = util.yml_folders(sdtm_rules_path)
    sdtm_core_status_data = util.get_yaml_fields(sdtm_rules_path, sdtm_repo_rules, keys=["Core", "Status"])
    sdtm_verified_data = util.get_yaml_verified(sdtm_rules_path, sdtm_repo_rules)
    sdtm_rules = pd.concat([cg_raw, fda_raw], ignore_index=True)

    adam_repo_rules = util.yml_folders(adam_rules_path)
    adam_core_status_data = util.get_yaml_fields(adam_rules_path, adam_repo_rules, keys=["Core", "Status"])
    adam_verified_data = util.get_yaml_verified(adam_rules_path, adam_repo_rules)
    adam_rules = adam_repo_rules
    
    sdtm_test_stats = util.get_test_execution_stats(sdtm_rules_path)
    adam_test_stats = util.get_test_execution_stats(adam_rules_path)
    cg_data = util.get_csv_completion_data(cg_raw)
    fda_data = util.get_csv_completion_data(fda_raw)
    adam_data = util.get_csv_completion_data(adam_raw)
    
    els_verified_data = pd.concat([
        cg_raw[["Rule ID"]] if not cg_raw.empty else pd.DataFrame(columns=["Rule ID"]),
        fda_raw[["Rule ID"]] if not fda_raw.empty else pd.DataFrame(columns=["Rule ID"]),
        adam_raw[["Rule ID"]] if not adam_raw.empty else pd.DataFrame(columns=["Rule ID"])
    ], ignore_index=True)