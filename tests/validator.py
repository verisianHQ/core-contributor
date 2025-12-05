import sys
import json
from typing import Any, Dict, List, Tuple


def normalize_dataset(dataset: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a dataset for comparison by sorting errors and removing non-deterministic fields.
    """
    normalized = dataset.copy()
    
    if 'errors' in normalized:
        normalized['errors'] = sorted(
            normalized['errors'],
            key=lambda e: (
                e.get('row', 0),
                str(sorted(e.items()))
            )
        )
    
    return normalized


def compare_errors(committed_errors: List[Dict], generated_errors: List[Dict], test_type: str, case_id: str) -> Tuple[bool, List[str]]:
    """
    Compare two lists of errors and return whether they match and any differences found.
    """
    differences = []
    
    if len(committed_errors) != len(generated_errors):
        differences.append(f"Error count mismatch: committed={len(committed_errors)}, generated={len(generated_errors)}")
        return False, differences
    
    for idx, (committed_err, generated_err) in enumerate(zip(committed_errors, generated_errors)):
        if committed_err.get('row') != generated_err.get('row'):
            differences.append(
                f"Error {idx+1}: Row mismatch - "
                f"committed row {committed_err.get('row')} vs generated row {generated_err.get('row')}"
            )
        
        committed_value = committed_err.get('value', {})
        generated_value = generated_err.get('value', {})
        
        all_keys = set(committed_value.keys()) | set(generated_value.keys())
        
        for key in all_keys:
            committed_val = committed_value.get(key)
            generated_val = generated_value.get(key)
            
            if committed_val != generated_val:
                differences.append(
                    f"Error {idx+1}, row {committed_err.get('row')}: "
                    f"Field '{key}' mismatch - committed='{committed_val}' vs generated='{generated_val}'"
                )
        
        for field in ['SEQ', 'USUBJID']:
            if field in committed_err or field in generated_err:
                if committed_err.get(field) != generated_err.get(field):
                    differences.append(
                        f"Error {idx+1}: {field} mismatch - "
                        f"committed='{committed_err.get(field)}' vs generated='{generated_err.get(field)}'"
                    )
    
    return len(differences) == 0, differences


def compare_datasets(committed_ds: Dict, generated_ds: Dict, test_type: str, case_id: str) -> Tuple[bool, List[str]]:
    """
    Compare two dataset results and return whether they match and any differences.
    """
    differences = []
    
    for field in ['dataset', 'domain', 'execution_status']:
        if committed_ds.get(field) != generated_ds.get(field):
            differences.append(
                f"Dataset '{committed_ds.get('domain', 'unknown')}': "
                f"{field} mismatch - committed='{committed_ds.get(field)}' vs generated='{generated_ds.get(field)}'"
            )
    
    committed_error_count = committed_ds.get('number_errors', 0)
    generated_error_count = generated_ds.get('number_errors', 0)
    
    if committed_error_count != generated_error_count:
        differences.append(
            f"Dataset '{committed_ds.get('domain', 'unknown')}': "
            f"number_errors mismatch - committed={committed_error_count} vs generated={generated_error_count}"
        )
    
    committed_errors = committed_ds.get('errors', [])
    generated_errors = generated_ds.get('errors', [])
    
    _, error_diffs = compare_errors(committed_errors, generated_errors, test_type, case_id)
    differences.extend(error_diffs)
    
    return len(differences) == 0, differences


def compare_results(committed_path: str, generated_path: str, test_type: str, case_id: str):
    """
    Compare committed and generated validation results.
    Performs deep comparison of error content, not just counts.
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
    
    committed_datasets = committed.get('datasets', [])
    generated_datasets = generated.get('datasets', [])
    
    committed_total_errors = sum(len(ds.get('errors', [])) for ds in committed_datasets)
    generated_total_errors = sum(len(ds.get('errors', [])) for ds in generated_datasets)
    
    if len(committed_datasets) != len(generated_datasets):
        print(f"  {test_type}/{case_id}: Dataset count mismatch")
        print(f"    Committed: {len(committed_datasets)} datasets")
        print(f"    Generated: {len(generated_datasets)} datasets")
        sys.exit(1)
    
    all_differences = []
    
    committed_by_domain = {ds.get('domain', f'unknown_{i}'): ds for i, ds in enumerate(committed_datasets)}
    generated_by_domain = {ds.get('domain', f'unknown_{i}'): ds for i, ds in enumerate(generated_datasets)}
    
    for domain in committed_by_domain.keys():
        if domain not in generated_by_domain:
            all_differences.append(f"Domain '{domain}' missing in generated results")
            continue
        
        committed_ds = normalize_dataset(committed_by_domain[domain])
        generated_ds = normalize_dataset(generated_by_domain[domain])
        
        matches, differences = compare_datasets(committed_ds, generated_ds, test_type, case_id)
        if not matches:
            all_differences.extend(differences)
    
    for domain in generated_by_domain.keys():
        if domain not in committed_by_domain:
            all_differences.append(f"Extra domain '{domain}' in generated results")
    
    if all_differences:
        print(f"  {test_type}/{case_id}: Results mismatch detected!")
        print(f"    Total errors - Committed: {committed_total_errors}, Generated: {generated_total_errors}")
        print(f"\n    Differences found:")
        for diff in all_differences:
            print(f"      • {diff}")
        if len(all_differences) > 10:
            print(f"      ... and {len(all_differences) - 10} more differences")
        sys.exit(1)
    
    if test_type == 'positive':
        if generated_total_errors == 0:
            print(f'  {test_type}/{case_id}: 0 errors (valid positive test)')
        else:
            print(f'  {test_type}/{case_id}: {generated_total_errors} errors (should be 0)')
            sys.exit(1)
    else:
        if generated_total_errors > 0:
            print(f'  {test_type}/{case_id}: {generated_total_errors} errors (valid negative test)')
        else:
            print(f'  {test_type}/{case_id}: 0 errors (should be >0)')
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python validator.py <committed_path> <generated_path> <test_type> <case_id>")
        sys.exit(1)
    
    compare_results(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])