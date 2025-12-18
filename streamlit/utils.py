import pandas as pd
import os
import json
from pathlib import Path


def yml_folders(rules_dir):
    folders_with_yml = []
    for root, dirs, files in os.walk(rules_dir):
        yml_files = [f for f in files if f.endswith(".yml")]
        if yml_files:
            folder_name = os.path.relpath(root, rules_dir)
            folders_with_yml.append({"Core-ID": folder_name})
    return pd.DataFrame(folders_with_yml)


def read_SOT(filepath):
    df = pd.read_csv(filepath)
    return df


def filter_standard(df, standard):
    filtered_df = df[df["Standard Name"].str.contains(standard, na=False)]
    return filtered_df


def perc_calc(part1, part2):
    if part1 + part2 == 0:
        return 0, 0
    else:
        return part1 / (part1 + part2), part2 / (part1 + part2)


def get_test_execution_stats(rules_dir):
    results_data = []

    rules_path = Path(rules_dir)
    if not rules_path.exists():
        return pd.DataFrame()

    for rule_folder in rules_path.iterdir():
        if not rule_folder.is_dir():
            continue

        core_id = rule_folder.name

        for test_type in ["positive", "negative"]:
            type_dir = rule_folder / test_type
            if not type_dir.exists():
                continue

            for case_dir in type_dir.iterdir():
                if not case_dir.is_dir():
                    continue

                result_file = case_dir / "results" / "results.json"
                if not result_file.exists():
                    continue

                try:
                    with open(result_file, "r") as f:
                        data = json.load(f)

                    status = "Unknown"
                    reason = None
                    exception = None

                    if "error" in data:
                        status = "Errored"
                        exception = data.get("exception", data.get("error", "Unknown Error"))
                    else:
                        datasets = data.get("datasets", [])
                        total_errors = sum(len(ds.get("errors", [])) for ds in datasets)

                        if test_type == "positive":
                            if total_errors == 0:
                                status = "Passed"
                            else:
                                status = "Failed"
                                for ds in datasets:
                                    if ds.get("errors"):
                                        reason = ds["errors"][0].get("message", "Unexpected error found")
                                        break
                        elif test_type == "negative":
                            if total_errors > 0:
                                status = "Passed"
                            else:
                                status = "Failed"
                                reason = "Expected errors but found none"

                    results_data.append(
                        {
                            "Core-ID": core_id,
                            "Test Type": test_type,
                            "Case ID": case_dir.name,
                            "Status": status,
                            "Failure Reason": reason,
                            "Exception": exception,
                        }
                    )

                except Exception as e:
                    print(f"Error reading {result_file}: {e}")

    return pd.DataFrame(results_data)
