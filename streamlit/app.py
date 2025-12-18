import streamlit as st
from src.components.utils import extract_issues
from src.data import (
    completed_rules,
    core_status_data,
    sdtm_rules,
    test_stats,
    cg_data,
)
from src.components.displays import (
    sdtm_rule_status_display,
    rule_comment_verification_display,
    core_rule_status_display,
    conformance_rules_verification_display,
    conformance_rule_completion_display,
    test_results_display,
    failure_error_display,
)

st.set_page_config(layout="wide", page_title="Rules Contributor Dashboard")


def main():
    st.title("Rules Contributor Dashboard")
    st.markdown("---")
    st.subheader("Rule Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        sdtm_rule_status_display(completed_rules, sdtm_rules)

    with col2:
        rule_comment_verification_display(completed_rules)

    with col3:
        if not core_status_data.empty:
            core_rule_status_display(core_status_data)
        else:
            st.info("No YAML status data found.")

    col4, col5 = st.columns(2)

    with col4:
        conformance_rules_verification_display(completed_rules, sdtm_rules)

    with col5:
        if not cg_data.empty:
            conformance_rule_completion_display(cg_data)
        else:
            st.info("No Excel data available for Rule ID tracking.")

    st.markdown("---")
    st.subheader("Test Execution Health")

    if test_stats.empty:
        st.warning("No test results found. Please run the tests to generate `results.json` files.")
    else:
        col_pie, col_bar = st.columns([1, 2])

        with col_pie:
            test_results_display(test_stats)

        with col_bar:
            combined_issues = extract_issues(test_stats)
            if not combined_issues.empty:
                failure_error_display(combined_issues)
            else:
                st.success("No failures or errors found.")

        problematic_cases = test_stats[test_stats["Status"].isin(["Failed", "Errored"])]
        if not problematic_cases.empty:
            with st.expander("Details for Failures/Errors"):
                st.write("Filtering for Failed or Errored cases:")
                st.dataframe(problematic_cases, width="stretch")


if __name__ == "__main__":
    main()
