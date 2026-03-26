import streamlit as st
from src.components.utils import UtilityFunctions
from src.data import IngestedData
from src.components.displays import Displays

st.set_page_config(layout="wide", page_title="Rules Contributor Dashboard")


def main():

    dsp = Displays
    data = IngestedData
    util = UtilityFunctions

    st.title("Rules Contributor Dashboard")
    st.markdown("---")
    st.subheader("Rule Status")

    col1, col2 = st.columns(2)
    with col1:
        dsp.sdtm_rule_status_display(data.repo_rules, data.sdtm_rules)

    with col2:
        if not data.core_status_data.empty:
            dsp.core_rule_status_display(data.core_status_data)
        else:
            st.info("No YAML status data found.")

    col3, col4 = st.columns(2)
    with col3:
        dsp.rule_comment_verification_display(data.verified_data)

    with col4:
        if not data.cg_data.empty or not data.fda_data.empty:
            dsp.conformance_rule_completion_display(data.cg_data, data.fda_data)
        else:
            st.info("No Excel data available for Rule ID tracking.")

    st.markdown("---")
    st.subheader("Test Execution Health")

    if data.test_stats.empty:
        st.warning("No test results found. Please run the tests to generate `results.json` files.")
    else:
        col_pie, col_bar = st.columns([1, 2])

        with col_pie:
            dsp.test_results_display(data.test_stats)

        with col_bar:
            combined_issues = util.extract_issues(data.test_stats)
            if not combined_issues.empty:
                dsp.failure_error_display(combined_issues)
            else:
                st.success("No failures or errors found.")

        problematic_cases = data.test_stats[data.test_stats["Status"].isin(["Failed", "Errored"])]
        if not problematic_cases.empty:
            with st.expander("Details for Failures/Errors"):
                st.write("Filtering for Failed or Errored cases:")
                st.dataframe(problematic_cases, width="stretch")


if __name__ == "__main__":
    main()
