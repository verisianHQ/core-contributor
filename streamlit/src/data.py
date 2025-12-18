from pathlib import Path

from src.components.utils import (
    yml_folders,
    read_SOT,
    filter_standard,
    get_test_execution_stats,
    get_core_status_stats,
    get_xlsx_completion_data,
)
from src.constants import SOT_PATH, RULES_DIR, CG_LIB_PATH


def path_extender(path):
    script_dir = Path(__file__).parent.parent
    full_path = script_dir / path
    return full_path


rules_path = path_extender(RULES_DIR)
cg_path = path_extender(CG_LIB_PATH)

completed_rules = yml_folders(rules_path)
core_status_data = get_core_status_stats(rules_path)
sdtm_rules = filter_standard(read_SOT(SOT_PATH), "SDTMIG")
test_stats = get_test_execution_stats(rules_path)
cg_data = get_xlsx_completion_data(cg_path)
