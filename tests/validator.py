import sys
import json
from typing import Any, Dict


def normalize_json(data: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(data, dict):
        return data

    if "datasets" in data:
        data["datasets"] = sorted(
            data["datasets"], 
            key=lambda ds: ds.get("domain", "")
        )
        
        for ds in data["datasets"]:
            if "errors" in ds:
                ds["errors"] = sorted(
                    ds["errors"], 
                    key=lambda e: (e.get("row", 0), str(sorted(e.items())))
                )

    return data


def compare_results(committed_path: str, generated_path: str, test_type: str, case_id: str):
    """
    Compare committed and generated validation results.
    """
    try:
        with open(committed_path) as f:
            committed = json.load(f)
        with open(generated_path) as f:
            generated = json.load(f)
    except FileNotFoundError as e:
        print(f"  {test_type}/{case_id}: File not found - {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"  {test_type}/{case_id}: Invalid JSON - {e}")
        sys.exit(1)

    norm_committed = normalize_json(committed)
    norm_generated = normalize_json(generated)

    if norm_committed == norm_generated:
        sys.exit(0)
    else:
        print(f"  {test_type}/{case_id}: Results mismatch detected!")
        print(f"    The generated JSON payload does not perfectly match the committed JSON payload.")
        
        c_datasets = len(norm_committed.get("datasets", []))
        g_datasets = len(norm_generated.get("datasets", []))
        
        if c_datasets != g_datasets:
            print(f"    Dataset count mismatch: Committed={c_datasets}, Generated={g_datasets}")
        else:
            c_errors = sum(len(ds.get("errors", [])) for ds in norm_committed.get("datasets", []))
            g_errors = sum(len(ds.get("errors", [])) for ds in norm_generated.get("datasets", []))
            if c_errors != g_errors:
                print(f"    Total error count mismatch: Committed={c_errors}, Generated={g_errors}")
            else:
                print("    Error counts and dataset counts match. The difference is in the specific values (e.g., messages, rows, fields).")
        
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python validator.py <committed_path> <generated_path> <test_type> <case_id>")
        sys.exit(1)

    compare_results(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
