import streamlit as st
import pandas as pd
from src.components.utils import UtilityFunctions
from src.data import IngestedData
from src.components.displays import Displays

st.set_page_config(layout="wide", page_title="Rules Contributor Dashboard")


def main():

    dsp = Displays
    data = IngestedData
    util = UtilityFunctions

    st.sidebar.title("Filters")
    standard_filter = st.sidebar.selectbox("Standard", ["All", "SDTMIG", "FDA"])

    if standard_filter == "SDTMIG":
        filtered_sdtm_rules = data.cg_raw
        filtered_cg_data = data.cg_data
        filtered_fda_data = pd.DataFrame(columns=data.fda_data.columns) 
    elif standard_filter == "FDA":
        filtered_sdtm_rules = data.fda_raw
        filtered_cg_data = pd.DataFrame(columns=data.cg_data.columns)
        filtered_fda_data = data.fda_data
    else:
        filtered_sdtm_rules = data.sdtm_rules
        filtered_cg_data = data.cg_data
        filtered_fda_data = data.fda_data

    valid_core_ids = set(
        x.strip() for ids in filtered_sdtm_rules["CORE-ID"].dropna() 
        for x in str(ids).split(";") if x.strip() and x.strip() != "/"
    )

    filtered_repo_rules = data.repo_rules[data.repo_rules["Core-ID"].isin(valid_core_ids)]
    
    if not filtered_repo_rules.empty:
        filtered_core_status_data = util.get_yaml_fields(
            data.rules_path, 
            filtered_repo_rules, 
            keys=["Core", "Status"]
        )
    else:
        filtered_core_status_data = pd.Series(dtype=int)

    filtered_verified_data = {
        k: v for k, v in data.verified_data.items() if k in valid_core_ids
    }

    if not data.test_stats.empty:
        filtered_test_stats = data.test_stats[data.test_stats["Core-ID"].isin(valid_core_ids)]
    else:
        filtered_test_stats = pd.DataFrame()

    st.title("Rules Contributor Dashboard")
    st.markdown(f"**Viewing:** {standard_filter}")
    st.markdown("---")
    
    st.subheader("Rule Status")

    col1, col2 = st.columns(2)
    with col1:
        dsp.sdtm_rule_status_display(filtered_repo_rules, filtered_sdtm_rules)

    with col2:
        if not filtered_core_status_data.empty:
            dsp.core_rule_status_display(filtered_core_status_data)
        else:
            st.info("No YAML status data found for this filter.")

    col3, col4 = st.columns(2)
    with col3:
        if filtered_verified_data:
            dsp.rule_comment_verification_display(filtered_verified_data)
        else:
            st.info("No verification data found for this filter.")

    with col4:
        if not filtered_cg_data.empty or not filtered_fda_data.empty:
            dsp.conformance_rule_completion_display(filtered_cg_data, filtered_fda_data)
        else:
            st.info("No Excel data available for Rule ID tracking for this filter.")

    st.markdown("---")
    st.subheader("Test Execution Health")

    if filtered_test_stats.empty:
        st.warning("No test results found for the selected filter.")
    else:
        col_pie, col_bar = st.columns([1, 2])

        with col_pie:
            dsp.test_results_display(filtered_test_stats)

        with col_bar:
            combined_issues = util.extract_issues(filtered_test_stats)
            if not combined_issues.empty:
                dsp.failure_error_display(combined_issues)
            else:
                st.success("No failures or errors found.")

        problematic_cases = filtered_test_stats[filtered_test_stats["Status"].isin(["Failed", "Errored"])]
        if not problematic_cases.empty:
            with st.expander("Details for Failures/Errors"):
                st.write("Filtering for Failed or Errored cases:")
                st.dataframe(problematic_cases, width="stretch")


if __name__ == "__main__":
    main()
