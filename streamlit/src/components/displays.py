from src.components.templates.pie_chart import make_pie
from src.components.templates.bar_chart import make_horizontal_bar
from src.components.utils import UtilityFunctions


class Displays:

    @staticmethod
    def rule_status_display(repo_rules, sot_rules, standard_name):
        repo_core_ids = set(repo_rules["Core-ID"])
        sot_core_ids = set(sot_rules["Core-ID"])

        not_completed = sot_core_ids - repo_core_ids

        pie_sizes = [len(repo_core_ids), len(not_completed)]
        comp_perc, non_comp_perc = UtilityFunctions.perc_calc(pie_sizes[0], pie_sizes[1])
        
        pie_labels = [
            f"Implemented ({comp_perc:.0%})",
            f"Missing ({non_comp_perc:.0%})",
        ]
        
        title = f"Implementation Status"
        make_pie(pie_labels, pie_sizes, title, color_scheme="set1")

    @staticmethod
    def rule_comment_verification_display(verified_data):
        labels = verified_data.index.tolist()
        values = verified_data.values.tolist()

        total = sum(values)
        formatted_labels = [f"{label} ({(val/total):.0%})" for label, val in zip(labels, values)]

        make_pie(formatted_labels, values, "Rule Comment Verification", color_scheme="set2")

    @staticmethod
    def core_rule_status_display(core_status_data):
        labels = core_status_data.index.tolist()
        values = core_status_data.values.tolist()

        total = sum(values)
        formatted_labels = [f"{label} ({(val/total):.0%})" for label, val in zip(labels, values)]

        make_pie(formatted_labels, values, "Core Rule Status", color_scheme="set3")

    @staticmethod
    def conformance_rules_verification_display(completed_rules, els_data):
        import streamlit as st
        import pandas as pd

        els_verified_cgs = set(els_data["Rule ID"]) if not els_data.empty and "Rule ID" in els_data.columns else set()
        
        if not completed_rules.empty and "conformance_id" in completed_rules.columns:
            all_cgs = set(x.strip() for ids in completed_rules["conformance_id"].dropna() for x in ids.split(";"))
        else:
            all_cgs = set()
            
        uncompleted_cgs = all_cgs - els_verified_cgs

        pie_sizes_CG = [len(els_verified_cgs), len(uncompleted_cgs)]
        comp_perc_CG, non_comp_perc_CG = UtilityFunctions.perc_calc(pie_sizes_CG[0], pie_sizes_CG[1])
        pie_labels_CG = [f"Verified ({comp_perc_CG:.0%})", f"Unverified ({non_comp_perc_CG:.0%})"]
        make_pie(pie_labels_CG, pie_sizes_CG, "CDISC Verified Rules", color_scheme="tableau10")
        with st.expander("View Unverified CG Rules"):
            if uncompleted_cgs:
                df = pd.DataFrame(sorted(uncompleted_cgs), columns=["Unverified CG Rule"])
                df.index = df.index + 1  # Start index at 1
                st.dataframe(df, width="stretch", hide_index=False)
            else:
                st.write("No unverified rules found.")

    @staticmethod
    def conformance_rule_completion_display(cg_data):
        counts = cg_data["Completion"].value_counts()
        completed_count = counts.get("Completed", 0)
        partial_count = counts.get("Partially Completed", 0)
        incomplete_count = counts.get("Incomplete", 0)
        missing_count = counts.get("Missing", 0)

        total = completed_count + partial_count + incomplete_count + missing_count

        comp_perc = completed_count / total if total > 0 else 0
        partial_perc = partial_count / total if total > 0 else 0
        unimpl_perc = incomplete_count / total if total > 0 else 0
        missing_perc = missing_count / total if total > 0 else 0

        pie_sizes_cg = [completed_count, partial_count, incomplete_count, missing_count]
        pie_labels_cg = [
            f"Completed ({comp_perc:.0%})",
            f"Partially Completed ({partial_perc:.0%})",
            f"Incomplete ({unimpl_perc:.0%})",
            f"Missing ({missing_perc:.0%})",
        ]

        make_pie(pie_labels_cg, pie_sizes_cg, "Conformance Rule Completion", color_scheme="tableau20")

    @staticmethod
    def test_results_display(test_stats):
        status_counts = test_stats["Status"].value_counts()
        pie_labels = [f"{status} ({(count / len(test_stats)):.0%})" for status, count in status_counts.items()]
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
