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

    st.sidebar.title("Dashboard Filters")
    
    if not data.sot_rules.empty:
        available_standards = ["All"] + util.sort_standards(data.sot_rules)
        selected_standard = st.sidebar.selectbox("Select Standard", available_standards, index=0)
    else:
        selected_standard = "No Data"

    if selected_standard == "No Data":
        filtered_repo = pd.DataFrame(columns=["Core-ID", "Standard", "Core-Status", "Verification"])
        filtered_sot = pd.DataFrame(columns=["Core-ID"])
    elif selected_standard == "All":
        filtered_repo = data.repo_rules
        filtered_sot = data.sot_rules
    else:
        if not data.repo_rules.empty and "Standard" in data.repo_rules.columns:
            filtered_repo = data.repo_rules[data.repo_rules["Standard"].apply(lambda x: selected_standard in x)]
        else:
            filtered_repo = pd.DataFrame(columns=["Core-ID", "Standard", "Core-Status", "Verification"])
            
        filtered_sot = util.filter_standard(data.sot_rules, selected_standard)

    active_ids = set()
    if not filtered_repo.empty and "Core-ID" in filtered_repo.columns:
        active_ids.update(filtered_repo["Core-ID"])
    if not filtered_sot.empty and "Core-ID" in filtered_sot.columns:
        active_ids.update(filtered_sot["Core-ID"])

    filtered_test_stats = pd.DataFrame()
    if not data.test_stats.empty and "Core-ID" in data.test_stats.columns:
        filtered_test_stats = data.test_stats[data.test_stats["Core-ID"].isin(active_ids)]

    filtered_cg_data = pd.DataFrame()
    if not data.cg_data.empty and "CORE-ID" in data.cg_data.columns:
        filtered_cg_data = data.cg_data[data.cg_data["CORE-ID"].isin(active_ids)]
    
    v_counts = filtered_repo["Verification"].value_counts() if not filtered_repo.empty and "Verification" in filtered_repo.columns else pd.Series()
    s_counts = filtered_repo["Core-Status"].value_counts() if not filtered_repo.empty and "Core-Status" in filtered_repo.columns else pd.Series()

    st.title("Rules Contributor Dashboard")
    st.markdown("---")
    st.subheader(f"{selected_standard} Rules")

    col1, col2, col3 = st.columns(3)

    with col1:
        dsp.rule_status_display(filtered_repo, filtered_sot, selected_standard)

    with col2:
        dsp.rule_comment_verification_display(v_counts)

    with col3:
        if not s_counts.empty:
            dsp.core_rule_status_display(s_counts)
        else:
            st.info("No status data for selection.")

    col4, col5 = st.columns(2)

    with col4:
        dsp.conformance_rules_verification_display(filtered_sot, data.els_verified_data)

    with col5:
        if not filtered_cg_data.empty:
            dsp.conformance_rule_completion_display(filtered_cg_data)
        else:
            st.info(f"No Excel tracking found for {selected_standard}.")

    st.markdown("---")
    st.subheader(f"{selected_standard} Test Cases")

    if filtered_test_stats.empty:
        st.warning("No test results for the selected criteria.")
    else:
        col_pie, col_bar = st.columns([1, 2])
        with col_pie:
            dsp.test_results_display(filtered_test_stats)
        with col_bar:
            issues = util.extract_issues(filtered_test_stats)
            if not issues.empty:
                dsp.failure_error_display(issues)
            else:
                st.success("All tests passed for this standard.")


if __name__ == "__main__":
    main()
