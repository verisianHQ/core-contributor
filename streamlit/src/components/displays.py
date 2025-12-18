from src.components.templates.pie_chart import make_pie
from src.components.templates.bar_chart import make_horizontal_bar
from src.components.utils import perc_calc


def sdtm_rule_status_display(completed_rules, sdtm_rules):
    completed_core_ids = set(completed_rules["Core-ID"])
    sdtm_core_ids = set(sdtm_rules["Core-ID"])
    sdtm_not_completed = sdtm_core_ids - completed_core_ids

    pie_sizes = [len(completed_core_ids), len(sdtm_not_completed)]
    comp_perc, non_comp_perc = perc_calc(pie_sizes[0], pie_sizes[1])
    pie_labels = [
        f"Implemented ({comp_perc:.0%})",
        f"Missing ({non_comp_perc:.0%})",
    ]
    make_pie(pie_labels, pie_sizes, "SDTM Rule Implementation Status", color_scheme="set1")


def rule_comment_verification_display(completed_rules):
    mock_ver = 40  # mock field until rule field added
    completed_core_ids = set(completed_rules["Core-ID"])
    pie_sizes = [len(completed_core_ids) - mock_ver, mock_ver]
    not_ver_perc, ver_perc = perc_calc(pie_sizes[0], pie_sizes[1])
    pie_labels = [
        f"Verified ({ver_perc:.0%})",
        f"Not Verified ({not_ver_perc:.0%})",
    ]
    make_pie(pie_labels, pie_sizes, "Rule Comment Verification", color_scheme="set2")


def core_rule_status_display(core_status_data):
    labels = core_status_data.index.tolist()
    values = core_status_data.values.tolist()

    total = sum(values)
    formatted_labels = [f"{label} ({(val/total):.0%})" for label, val in zip(labels, values)]

    make_pie(formatted_labels, values, "Core Rule Status", color_scheme="set3")


def conformance_rules_verification_display(completed_rules, sdtm_rules):
    df_exploded = (
        sdtm_rules.assign(conformance_id=sdtm_rules["conformance_id"].str.split(";"))
        .explode("conformance_id")[["conformance_id", "Core-ID"]]
        .reset_index(drop=True)
    )
    completed_core_ids = set(completed_rules["Core-ID"])
    all_completed_conformance_ids = df_exploded.groupby("conformance_id")["Core-ID"].apply(
        lambda ids: set(ids).issubset(completed_core_ids)
    )
    complete_CGs = set(all_completed_conformance_ids[all_completed_conformance_ids].index.tolist())
    all_CGs = set(df_exploded["conformance_id"])
    uncompleted_CGs = all_CGs - complete_CGs

    pie_sizes_CG = [len(complete_CGs), len(uncompleted_CGs)]
    comp_perc_CG, non_comp_perc_CG = perc_calc(pie_sizes_CG[0], pie_sizes_CG[1])
    pie_labels_CG = [f"Completed ({comp_perc_CG:.0%})", f"Not Completed ({non_comp_perc_CG:.0%})"]
    make_pie(pie_labels_CG, pie_sizes_CG, "Conformance Rules SOT", color_scheme="tableau10")


def conformance_rule_completion_display(cg_data):
    counts = cg_data["Completion"].value_counts()
    completed_count = counts.get("Completed", 0)
    partial_count = counts.get("Partially Completed", 0)
    unimplemented_count = counts.get("Unimplemented", 0)
    missing_count = counts.get("Missing", 0)

    total = completed_count + partial_count + unimplemented_count + missing_count

    comp_perc = completed_count / total if total > 0 else 0
    partial_perc = partial_count / total if total > 0 else 0
    unimpl_perc = unimplemented_count / total if total > 0 else 0
    missing_perc = missing_count / total if total > 0 else 0

    pie_sizes_cg = [completed_count, partial_count, unimplemented_count, missing_count]
    pie_labels_cg = [
        f"Completed ({comp_perc:.0%})",
        f"Partially Completed ({partial_perc:.0%})",
        f"Unimplemented ({unimpl_perc:.0%})",
        f"Missing ({missing_perc:.0%})",
    ]

    make_pie(pie_labels_cg, pie_sizes_cg, "Conformance Rule Completion", color_scheme="tableau20")


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


def failure_error_display(combined_issues):
    make_horizontal_bar(
        combined_issues,
        "Failure & Error Details",
        tooltip_cols=["Core-ID", "Case ID", "Test Type", "Status", "Issue"],
    )
