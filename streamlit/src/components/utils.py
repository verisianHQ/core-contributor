import pandas as pd
import os
import json
from pathlib import Path
import yaml


class UtilityFunctions:

    @staticmethod
    def yml_folders(rules_dir):
        folders_with_yml = []
        for root, dirs, files in os.walk(rules_dir):
            yml_files = [f for f in files if f.endswith(".yml")]
            if yml_files:
                folder_name = os.path.relpath(root, rules_dir)
                folders_with_yml.append({"Core-ID": folder_name})
        return pd.DataFrame(folders_with_yml)

    @staticmethod
    def get_csv_cols(filepath, cols=None):
        df = pd.read_csv(filepath)
        if not cols:
            return df
        else:
            return df[cols]

    @staticmethod
    def filter_standard(df, standard):
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
                        with open(result_file, "r", encoding="utf-8") as f:
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
    def load_and_filter_csv(filepath, is_fda=False):
        try:
            try:
                df = pd.read_csv(filepath, encoding="utf-8-sig")
            except UnicodeDecodeError:
                df = pd.read_csv(filepath, encoding="cp1252")

            if len(df.columns) > 0 and df.columns[0].endswith("Rule ID"):
                df = df.rename(columns={df.columns[0]: "Rule ID"})
                
            if is_fda:                
                sdtm_cols = df.columns[2:5]
                
                mask = df[sdtm_cols].apply(lambda col: col.astype(str).str.contains('x', case=False, na=False)).any(axis=1)
                df = df[mask].copy()
                
                df = df.rename(columns={
                    df.columns[2]: "SDTMIG Version 3.2",
                    df.columns[3]: "SDTMIG Version 3.3",
                    df.columns[4]: "SDTMIG Version 3.4"
                })
            else:
                sdtm_cols = df.columns[1:4]
                mask = df[sdtm_cols].any(axis=1)
                df = df[mask].copy()
                
                df = df.rename(columns={
                    df.columns[1]: "SDTMIG Version 3.2",
                    df.columns[2]: "SDTMIG Version 3.3",
                    df.columns[3]: "SDTMIG Version 3.4"
                })
            return df
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return pd.DataFrame(columns=["Rule ID", "CORE-ID", "Status", "Status Rule", "SDTMIG Version 3.2", "SDTMIG Version 3.3", "SDTMIG Version 3.4"])

    @staticmethod
    def get_csv_completion_data(df):
        if df.empty:
            return df
        df = df.copy()
        df["Completion"] = df.apply(UtilityFunctions.determine_completion, axis=1)
        return df

    @staticmethod
    def determine_completion(row):
        core_id = row.get("CORE-ID")
        status = row.get("Status")
        status_rule = row.get("Status Rule")

        if pd.isna(core_id) or str(core_id).strip() in ["", "/", "nan"]:
            return "Missing"

        status = str(status).strip().upper()
        status_rule = str(status_rule).strip().upper()

        if status == "PUBLISHED":
            if status_rule == "MERGED":
                return "Completed"
            else:
                return "Partially Completed"

        if status in ["DRAFT", "DRAFT - NOT EXECUTABLE", "OPEN"]:
            return "Unimplemented"
            
        if status == "NOT EXECUTABLE":
            return "Not Executable"
            
        return "Unknown"

    @staticmethod
    def get_yaml_fields(rules_dir, repo_rules, keys, null_value="No Value"):
        vals = []

        for rule_folder in repo_rules["Core-ID"].to_list():
            path = Path(rules_dir) / rule_folder
            yml_file = list(path.glob("*.yml")) + list(path.glob("*.yaml"))
            if not yml_file or len(yml_file) == 0:
                continue
            try:
                with open(yml_file[0], "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    output = UtilityFunctions.chain_get(data, keys, nv=null_value)
                    vals.append(output)
            except Exception as e:
                print(f"Error reading YAML in {rule_folder.name}: {e}")

        return pd.Series(vals).value_counts()

    @staticmethod
    def get_yaml_verified(rules_dir, repo_rules):
        vals = {}

        for rule_folder in repo_rules["Core-ID"].to_list():
            path = Path(rules_dir) / rule_folder
            yml_file = list(path.glob("*.yml")) + list(path.glob("*.yaml"))
            if not yml_file or len(yml_file) == 0:
                continue
            try:
                with open(yml_file[0], "r", encoding="utf-8") as f:
                    if any(line.strip() == "# verified" for line in f):
                        vals[rule_folder] = "Verified"
                    else:
                        vals[rule_folder] = "Unverified"
            except Exception as e:
                print(f"Error reading YAML in {rule_folder.name}: {e}")

        return vals

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
        failed = test_stats[test_stats["Status"] == "Failed"].copy()
        failed["Issue"] = failed["Failure Reason"]

        errored = test_stats[test_stats["Status"] == "Errored"].copy()
        errored["Issue"] = errored["Exception"]

        combined_issues = pd.concat([failed, errored])
        return combined_issues
