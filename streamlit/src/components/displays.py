import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from src.components.templates.pie_chart import make_pie
from src.components.templates.bar_chart import make_horizontal_bar
from src.components.templates.area_chart import make_stacked_area
from src.components.utils import UtilityFunctions


class Displays:

    @staticmethod
    def sdtm_rule_status_display(repo_rules, sdtm_rules):
        repo_core_ids = set(repo_rules["Core-ID"])
        
        sdtm_core_ids = set(
            x.strip() for ids in sdtm_rules["CORE-ID"].dropna() 
            for x in str(ids).split(";") if x.strip() and x.strip() != "/"
        )
        
        sdtm_not_completed = sdtm_core_ids - repo_core_ids

        pie_sizes = [len(repo_core_ids), len(sdtm_not_completed)]
        comp_perc, non_comp_perc = UtilityFunctions.perc_calc(pie_sizes[0], pie_sizes[1])
        pie_labels = [
            f"Implemented ({comp_perc:.1%})",
            f"Missing ({non_comp_perc:.1%})",
        ]
        make_pie(pie_labels, pie_sizes, "SDTM Rule Implementation Status", color_scheme="set1")

    @staticmethod
    def rule_comment_verification_display(verified_data):
        counts = pd.Series(list(verified_data.values())).value_counts()
        labels = counts.index.tolist()
        values = counts.values.tolist()

        total = sum(values)
        formatted_labels = [f"{label} ({(val/total):.1%})" for label, val in zip(labels, values)]

        make_pie(formatted_labels, values, "Rule Comment Verification", color_scheme="set2")
        with st.expander("View Conformance Rules Verification Status"):
            df = pd.DataFrame(list(verified_data.items()), columns=["Core-ID", "Verification Status"])
            st.dataframe(df, width="stretch", hide_index=False)


    @staticmethod
    def core_rule_status_display(core_status_data):
        labels = core_status_data.index.tolist()
        values = core_status_data.values.tolist()

        total = sum(values)
        formatted_labels = [f"{label} ({(val/total):.1%})" for label, val in zip(labels, values)]

        make_pie(formatted_labels, values, "Core Rule Status", color_scheme="set3")

    @staticmethod
    def conformance_rule_completion_display(cg_data: pd.DataFrame, fda_data: pd.DataFrame):
        combined_data = pd.concat([cg_data, fda_data], ignore_index=True)
        counts = combined_data["Completion"].value_counts().to_dict()
        completed_count = counts.get("Completed", 0)
        partial_count = counts.get("Partially Completed", 0)
        unimplemented_count = counts.get("Unimplemented", 0)
        missing_count = counts.get("Missing", 0)

        total = completed_count + partial_count + unimplemented_count + missing_count

        comp_perc = completed_count / total if total > 0 else 0
        partial_perc = partial_count / total if total > 0 else 0
        unimpl_perc = unimplemented_count / total if total > 0 else 0
        missing_perc = missing_count / total if total > 0 else 0

        pie_sizes = [completed_count, partial_count, unimplemented_count, missing_count]
        pie_labels = [
            f"Completed ({comp_perc:.1%})",
            f"Partially Completed ({partial_perc:.1%})",
            f"Unimplemented ({unimpl_perc:.1%})",
            f"Missing ({missing_perc:.1%})",
        ]

        make_pie(pie_labels, pie_sizes, "Conformance Rule Completion", color_scheme="tableau20")
        with st.expander("View Conformance Rule Id to CORE Id Mapping"):
            combined_data = combined_data.rename(columns={
                combined_data.columns[1]: "Version 1",
                combined_data.columns[2]: "Version 2",
                combined_data.columns[3]: "Version 3",
            })
            combined_data.index = combined_data.index + 1
            st.dataframe(combined_data, width="stretch", hide_index=False)

    @staticmethod
    def test_results_display(test_stats):
        status_counts = test_stats["Status"].value_counts()
        pie_labels = [f"{status} ({(count / len(test_stats)):.1%})" for status, count in status_counts.items()]
        make_pie(
            pie_labels,
            status_counts.values.tolist(),
            "Overall Test Results",
            color_scheme="category10",
            show_full_label=True,
        )

    @staticmethod
    def failure_error_display(combined_issues):
        make_horizontal_bar(
            combined_issues,
            "Failure & Error Details",
            tooltip_cols=["Core-ID", "Case ID", "Test Type", "Status", "Issue"],
        )

    def rule_validation_area_display(sot_rules, rules_dir):
        validation_dates, unvalidated_current = UtilityFunctions.get_validation_data(rules_dir)
        sot_total = len(sot_rules)
        
        total_in_repo = len(validation_dates) + unvalidated_current
        missing_current = max(0, sot_total - total_in_repo)

        if total_in_repo == 0:
            st.info("No rule data found in the repository.")
            return

        date_counts = pd.Series(validation_dates).value_counts().sort_index()
        
        today = pd.to_datetime(datetime.now().strftime("%Y-%m-%d"))
        if not date_counts.empty:
            start_date = pd.to_datetime(date_counts.index[0])
            if start_date == today:
                start_date = today - timedelta(days=3)
        else:
            start_date = today - timedelta(days=7)

        date_range = pd.date_range(start=start_date, end=today, freq='D')
        
        date_counts_dict = {pd.to_datetime(d): count for d, count in date_counts.items()}

        data = []
        cumulative_validated = 0

        for current_date in date_range:
            if current_date in date_counts_dict:
                cumulative_validated += date_counts_dict[current_date]
            
            unvalidated_for_day = total_in_repo - cumulative_validated
            
            date_str = current_date.strftime("%Y-%m-%d")
            data.append({"Date": date_str, "Category": "Validated Rules", "Count": cumulative_validated, "Order": 1})
            data.append({"Date": date_str, "Category": "Unvalidated Rules", "Count": unvalidated_for_day, "Order": 2})
            data.append({"Date": date_str, "Category": "Missing from Repo", "Count": missing_current, "Order": 3})

        df = pd.DataFrame(data)
        make_stacked_area(df, "Date", "Count", "Category", "Rule Validation Progress")