import pandas as pd
import os
import json
from pathlib import Path
import yaml


class UtilityFunctions:

    @staticmethod
    def get_all_yml_data(rules_dir):
        ymls = []
        for root, _, files in os.walk(rules_dir):
            yml_files = [f for f in files if f.endswith((".yml", ".yaml"))]
            if yml_files:
                folder_name = os.path.relpath(root, rules_dir)
                try:
                    with open(os.path.join(root, yml_files[0]), "r") as f:
                        rule_data = yaml.safe_load(f)

                    standards = set()
                    authorities = UtilityFunctions.chain_get(rule_data, ["Authorities"], nv=[])
                    for auth in authorities:
                        auth_standards = UtilityFunctions.chain_get(auth, ["Standards"], nv=[])
                        for std in auth_standards:
                            name = std.get("Name")
                            if name:
                                standards.add(name)
                    
                    status = UtilityFunctions.chain_get(rule_data, ["Core", "Status"], nv="No Status")
                    verification = UtilityFunctions.chain_get(rule_data, ["Verification"], nv="Unverified")

                    ymls.append({
                        "Core-ID": folder_name,
                        "Standard": sorted(list(standards)),
                        "Core-Status": status,
                        "Verification": verification
                    })
                except Exception as e:
                    print(f"Error processing {folder_name}: {e}")

        if not ymls:
            return pd.DataFrame(columns=["Core-ID", "Standard", "Core-Status", "Verification"])

        return pd.DataFrame(ymls)

    @staticmethod
    def get_csv_cols(filepath, cols=None):
        try:
            df = pd.read_csv(filepath)
            if not cols:
                return df
            else:
                return df[cols]
        except Exception as e:
            print(f"Error reading CSV {filepath}: {e}")
            return pd.DataFrame()

    @staticmethod
    def sort_standards(df):
        if df.empty or "Standard Name" not in df.columns:
            return []
        standards_list = []
        for s in df["Standard Name"].dropna().unique().tolist():
            for t in s.split(","):
                standards_list.append(t.strip())
        return sorted(set(standards_list))

    @staticmethod
    def filter_standard(df, standard):
        if df.empty or "Standard Name" not in df.columns:
            return pd.DataFrame(columns=df.columns)
        filtered_df = df[df["Standard Name"].str.contains(standard, na=False)]
        return filtered_df

    @staticmethod
    def perc_calc(part1, part2):
        if part1 + part2 == 0:
            return 0, 0
        else:
            return part1 / (part1 + part2), part2 / (part1 + part2)

    @staticmethod
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

    @staticmethod
    def get_xlsx_completion_data(filepath):
        try:
            df = pd.read_excel(filepath)
            df["Completion"] = df.apply(UtilityFunctions.determine_cg_completion, axis=1)
            return df
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return pd.DataFrame()

    @staticmethod
    def determine_cg_completion(row):
        core_id = row["CORE-ID"]
        status = row["Status"]

        if pd.isna(core_id) or core_id == "":
            return "Missing"

        if pd.isna(status):
            status = ""
        else:
            status = str(status)

        if "DRAFT" in status and "PUBLISHED" in status:
            return "Partially Completed"

        if status in ["DRAFT", "DRAFT - NOT EXECUTABLE"]:
            return "Incomplete"

        if status == "PUBLISHED":
            return "Completed"

        return "Unknown"

    @staticmethod
    def get_yaml_fields(rules_dir, keys, null_value="No Value"):
        vals = []
        rules_path = Path(rules_dir)

        if not rules_path.exists():
            return pd.DataFrame()

        for rule_folder in rules_path.iterdir():
            if not rule_folder.is_dir():
                continue

            yml_files = list(rule_folder.glob("*.yml")) + list(rule_folder.glob("*.yaml"))
            if not yml_files:
                continue

            try:
                with open(yml_files[0], "r") as f:
                    data = yaml.safe_load(f)
                    output = UtilityFunctions.chain_get(data, keys, nv=null_value)
                    vals.append(output)
            except Exception as e:
                print(f"Error reading YAML in {rule_folder.name}: {e}")

        return pd.Series(vals).value_counts()

    @staticmethod
    def chain_get(dct, keys, nv=None):
        for key in keys:
            if isinstance(dct, dict) and key in dct:
                dct = dct[key]
            else:
                return nv
        return dct

    @staticmethod
    def extract_issues(test_stats):
        if test_stats.empty:
            return pd.DataFrame()
        
        failed = test_stats[test_stats["Status"] == "Failed"].copy()
        failed["Issue"] = failed["Failure Reason"]

        errored = test_stats[test_stats["Status"] == "Errored"].copy()
        errored["Issue"] = errored["Exception"]

        combined_issues = pd.concat([failed, errored])
        return combined_issues
