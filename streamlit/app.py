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
    standard_filter = st.sidebar.selectbox("Standard", ["All", "SDTMIG", "FDA", "ADaM"])

    if standard_filter == "SDTMIG":
        filtered_raw_rules = data.cg_raw
        filtered_cg_data = data.cg_data
        filtered_fda_data = pd.DataFrame()
        filtered_adam_data = pd.DataFrame()
        
        repo_rules = data.sdtm_repo_rules
        rules_path = data.sdtm_rules_path
        verified_data = data.sdtm_verified_data
        test_stats = data.sdtm_test_stats
        
        valid_core_ids = set(
            x.strip() for ids in filtered_raw_rules["CORE-ID"].dropna() 
            for x in str(ids).split(";") if x.strip() and x.strip() != "/"
        )

    elif standard_filter == "FDA":
        filtered_raw_rules = data.fda_raw
        filtered_cg_data = pd.DataFrame()
        filtered_fda_data = data.fda_data
        filtered_adam_data = pd.DataFrame()

        repo_rules = data.sdtm_repo_rules
        rules_path = data.sdtm_rules_path
        verified_data = data.sdtm_verified_data
        test_stats = data.sdtm_test_stats
        
        valid_core_ids = set(
            x.strip() for ids in filtered_raw_rules["CORE-ID"].dropna() 
            for x in str(ids).split(";") if x.strip() and x.strip() != "/"
        )

    elif standard_filter == "ADaM":
        filtered_raw_rules = data.adam_raw
        filtered_cg_data = pd.DataFrame()
        filtered_fda_data = pd.DataFrame()
        filtered_adam_data = data.adam_data

        repo_rules = data.adam_repo_rules
        rules_path = data.adam_rules_path
        verified_data = data.adam_verified_data
        test_stats = data.adam_test_stats
        
        valid_core_ids = set(
            x.strip() for ids in filtered_raw_rules["Rule ID"].dropna() 
            for x in str(ids).split(";") if x.strip() and x.strip() != "/"
        )

    else:
        filtered_raw_rules = pd.concat([data.sdtm_rules, data.adam_raw], ignore_index=True)
        filtered_cg_data = data.cg_data
        filtered_fda_data = data.fda_data
        filtered_adam_data = data.adam_data

        repo_rules = pd.concat([data.sdtm_repo_rules, data.adam_repo_rules], ignore_index=True)
        verified_data = {**data.sdtm_verified_data, **data.adam_verified_data}
        test_stats = pd.concat([data.sdtm_test_stats, data.adam_test_stats], ignore_index=True)

        sdtm_ids = set(
            x.strip() for ids in data.sdtm_rules["CORE-ID"].dropna() 
            for x in str(ids).split(";") if x.strip() and x.strip() != "/"
        )
        adam_ids = set(
            x.strip() for ids in data.adam_raw["Rule ID"].dropna() 
            for x in str(ids).split(";") if x.strip() and x.strip() != "/"
        )
        valid_core_ids = sdtm_ids.union(adam_ids)

    filtered_repo_rules = repo_rules[repo_rules["CORE-ID"].isin(valid_core_ids)]
    
    if not filtered_repo_rules.empty:
        if standard_filter == "All":
            sdtm_filtered = data.sdtm_repo_rules[data.sdtm_repo_rules["CORE-ID"].isin(valid_core_ids)]
            adam_filtered = data.adam_repo_rules[data.adam_repo_rules["CORE-ID"].isin(valid_core_ids)]
            
            sdtm_status = util.get_yaml_fields(data.sdtm_rules_path, sdtm_filtered, keys=["Core", "Status"]) if not sdtm_filtered.empty else pd.Series(dtype=int)
            adam_status = util.get_yaml_fields(data.adam_rules_path, adam_filtered, keys=["Core", "Status"]) if not adam_filtered.empty else pd.Series(dtype=int)
            
            filtered_core_status_data = sdtm_status.add(adam_status, fill_value=0).astype(int)
        else:
            filtered_core_status_data = util.get_yaml_fields(rules_path, filtered_repo_rules, keys=["Core", "Status"])
    else:
        filtered_core_status_data = pd.Series(dtype=int)

    filtered_verified_data = {
        k: v for k, v in verified_data.items() if k in valid_core_ids
    }

    if not test_stats.empty:
        filtered_test_stats = test_stats[test_stats["CORE-ID"].isin(valid_core_ids)]
    else:
        filtered_test_stats = pd.DataFrame()

    st.title("Rules Contributor Dashboard")
    st.markdown(f"**Viewing:** {standard_filter}")
    st.markdown("---")
    
    st.subheader("Rule Status")
    col1, col2 = st.columns(2)
    with col1:
        title = (
            "ADaM Rule Implementation Status" if standard_filter == "ADaM" 
            else "SDTM/ADaM Rule Implementation Status" if standard_filter == "All" 
            else "SDTM Rule Implementation Status"
        )
        dsp.rule_status_display(filtered_repo_rules, filtered_raw_rules, title=title)

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
        if standard_filter == "ADaM":
            if not filtered_adam_data.empty:
                print(filtered_adam_data)
                dsp.conformance_rule_completion_display(filtered_adam_data, pd.DataFrame())
            else:
                st.info("No Excel data available for Rule ID tracking for this filter.")
        elif standard_filter == "All":
            combined_cg_adam = pd.concat(
                [filtered_cg_data, filtered_adam_data], ignore_index=True
            ) if not filtered_adam_data.empty else filtered_cg_data
            dsp.conformance_rule_completion_display(combined_cg_adam, filtered_fda_data)
        else:
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
