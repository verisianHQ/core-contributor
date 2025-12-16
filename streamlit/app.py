import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt


def yml_folders(rules_dir):
    folders_with_yml = []
    for root, dirs, files in os.walk(rules_dir):
        yml_files = [f for f in files if f.endswith(".yml")]
        if yml_files:
            folder_name = os.path.relpath(root, rules_dir)
            folders_with_yml.append({"Core-ID": folder_name, "yml_count": len(yml_files)})
    return pd.DataFrame(folders_with_yml)


def read_SOT(filepath):
    df = pd.read_csv(filepath)
    return df


def filter_standard(df, standard):
    filtered_df = df[df["Standard Name"].str.contains(standard, na=False)]
    return filtered_df


def main():
    st.title("Rules Dashboard")

    rules_dir = "./rules"
    completed_rules = yml_folders(rules_dir)

    file = read_SOT(
        "https://github.com/verisianHQ/cdisc-rules-engine/blob/phjlk/rule_overview_by_type/tests/rule_analysis/Rule_centric_SOT.csv?raw=true"
    )

    sdtm_rules = filter_standard(file, "SDTMIG")

    st.header("Dataframes")
    st.dataframe(completed_rules)
    st.dataframe(sdtm_rules)

    completed_core_ids = set(completed_rules["Core-ID"])
    sdtm_core_ids = set(sdtm_rules["Core-ID"])
    sdtm_not_completed = sdtm_core_ids - completed_core_ids

    pie_labels = ["Completed Rules", "SDTM Rules (Not Completed)"]
    pie_sizes = [len(completed_core_ids), len(sdtm_not_completed)]

    fig, ax = plt.subplots()
    ax.pie(pie_sizes, labels=pie_labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.header("Completion Pie Chart")
    st.pyplot(fig)


if __name__ == "__main__":
    main()
