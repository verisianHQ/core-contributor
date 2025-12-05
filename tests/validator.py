import sys
import json

def compare_results(committed_path, generated_path, test_type, case_id):
    try:
        with open(committed_path) as f:
            committed = json.load(f)
        with open(generated_path) as f:
            generated = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {committed_path} or {generated_path}")
        sys.exit(1)

    committed_errors = sum(len(ds.get('errors', [])) for ds in committed.get('datasets', []))
    generated_errors = sum(len(ds.get('errors', [])) for ds in generated.get('datasets', []))

    if committed_errors != generated_errors:
        print(f'  {test_type}/{case_id}: Error count mismatch')
        print(f'    Committed: {committed_errors} errors')
        print(f'    Generated: {generated_errors} errors')
        sys.exit(1)

    if test_type == 'positive':
        if generated_errors == 0:
            print(f'  {test_type}/{case_id}: 0 errors (valid positive test)')
        else:
            print(f'  {test_type}/{case_id}: {generated_errors} errors (should be 0)')
            sys.exit(1)
    else:
        if generated_errors > 0:
            print(f'  {test_type}/{case_id}: {generated_errors} errors (valid negative test)')
        else:
            print(f'  {test_type}/{case_id}: 0 errors (should be >0)')
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python validator.py <committed_path> <generated_path> <test_type> <case_id>")
        sys.exit(1)

    compare_results(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])