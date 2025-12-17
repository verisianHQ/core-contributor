import streamlit as st
import pandas as pd
from utils import yml_folders, read_SOT, filter_standard, perc_calc, get_test_execution_stats
from pie_chart import make_pie
from bar_chart import make_horizontal_bar
from constants import SOT_PATH, RULES_DIR

st.set_page_config(layout="wide", page_title="Rules Contributor Dashboard")

def main():
    st.title("Rules Contributor Dashboard")
    st.markdown("---")

    completed_rules = yml_folders(RULES_DIR)
    file = read_SOT(SOT_PATH)
    sdtm_rules = filter_standard(file, "SDTMIG")
    test_stats = get_test_execution_stats(RULES_DIR)
    
    col1, col2 = st.columns(2)
    
    with col1:
        completed_core_ids = set(completed_rules["Core-ID"])
        sdtm_core_ids = set(sdtm_rules["Core-ID"])
        sdtm_not_completed = sdtm_core_ids - completed_core_ids

        pie_sizes = [len(completed_core_ids), len(sdtm_not_completed)]
        comp_perc, non_comp_perc = perc_calc(pie_sizes[0], pie_sizes[1])
        pie_labels = [
            f"Implemented ({comp_perc:.0%})",
            f"Missing ({non_comp_perc:.0%})",
        ]
        make_pie(pie_labels, pie_sizes, "Rule Implementation Status", color_scheme="set2")

    with col2:
        df_exploded = (
            sdtm_rules.assign(conformance_id=sdtm_rules["conformance_id"].str.split(";"))
            .explode("conformance_id")[["conformance_id", "Core-ID"]]
            .reset_index(drop=True)
        )
        all_completed_conformance_ids = df_exploded.groupby("conformance_id")["Core-ID"].apply(
            lambda ids: set(ids).issubset(completed_core_ids)
        )
        complete_CGs = set(all_completed_conformance_ids[all_completed_conformance_ids].index.tolist())
        all_CGs = set(df_exploded["conformance_id"])
        uncompleted_CGs = all_CGs - complete_CGs

        pie_sizes_CG = [len(complete_CGs), len(uncompleted_CGs)]
        comp_perc_CG, non_comp_perc_CG = perc_calc(pie_sizes_CG[0], pie_sizes_CG[1])
        pie_labels_CG = [f"Completed ({comp_perc_CG:.0%})", f"Not Completed ({non_comp_perc_CG:.0%})"]
        make_pie(pie_labels_CG, pie_sizes_CG, "Conformance Rules (CG) Status", color_scheme="accent")

    st.markdown("---")
    st.subheader("Test Execution Health")

    if test_stats.empty:
        st.warning("No test results found. Please run the tests to generate `results.json` files.")
    else:
        col_pie, col_bar = st.columns([1, 2])
        
        with col_pie:
            status_counts = test_stats["Status"].value_counts()
            make_pie(
                status_counts.index.tolist(), 
                status_counts.values.tolist(), 
                "Overall Test Results",
                color_scheme="category10",
                show_full_label=True
            )

        with col_bar:
            failed = test_stats[test_stats["Status"] == "Failed"].copy()
            failed["Issue"] = failed["Failure Reason"]
            
            errored = test_stats[test_stats["Status"] == "Errored"].copy()
            errored["Issue"] = errored["Exception"]
            
            combined_issues = pd.concat([failed, errored])
            
            if not combined_issues.empty:
                make_horizontal_bar(
                    combined_issues,
                    "Failure & Error Details",
                    tooltip_cols=["Core-ID", "Case ID", "Test Type", "Status", "Issue"]
                )
            else:
                st.success("No failures or errors found.")

        problematic_cases = test_stats[test_stats["Status"].isin(["Failed", "Errored"])]
        if not problematic_cases.empty:
            with st.expander("Details for Failures/Errors"):
                st.write("Filtering for Failed or Errored cases:")
                st.dataframe(problematic_cases, use_container_width=True)

if __name__ == "__main__":
    main()
