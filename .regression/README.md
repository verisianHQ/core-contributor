Regression testing checks that a change (for example to the engine, or to many rules at once) doesn't change any rule results by mistake. You first save the current results of all rules (the "baseline"), make your change, and then compare a new run against the baseline.

The commands below run the rules in isolation, without writing to the rules' own `results` folders. Run them from the core-contributor directory with the virtual environment activated (see Advanced Usage in the [main README](../README.md#advanced-usage)).

- Choose the rules to run with `--standard`: `sdtm` (the default, rules in `sdtm_rules/`) or `adam` (rules in `adam_rules/`). Use the same `--standard` for the baseline and the comparison: the tool refuses to compare results of different standards.
- Create baseline outputs in a separate folder (default `.regression/<standard>/baseline`, e.g. `.regression/sdtm/baseline`):
   - `python regression_results.py snapshot --clean`
   - `--clean` deletes the previous baseline first. Without it, a snapshot is refused if the folder holds a baseline of a different standard.
- Snapshot writes only `results.json` files (no `results.txt`) plus `baseline_run_summary.json` in the baseline directory.
- Compare the baseline to a new isolated current run:
   - `python regression_results.py compare --clean`
   - Current run output is generated in a temporary folder and automatically removed.
   - Regression summary files written to `--comparison-dir` (default `.regression/<standard>/comparison`) are:
      - `regression_diff_summary.md` — all rules
      - `regression_diff_summary_verified.md` — verified rules only (rules with `# verified` or `# Verified` at the top of their YAML)
      - `run_summary.json` — summary counts
   - `--clean` deletes the previous summary files first.
- Compare the baseline against the existing outputs already in the rules' own `results` folders (e.g. `sdtm_rules/*/.../results`):
   - `python regression_results.py compare --current-source rules`
   - With `--summary-file <file>`, the summary is written to that file instead, and the verified summary next to it with a `_verified` suffix.
- Compare the baseline against another folder of results:
   - `python regression_results.py compare --current-source folder --current-dir <folder>`
- To use another baseline folder, add `--baseline-dir <folder>` to both commands.
- Pass external dictionary paths using a config file:
   - `python regression_results.py snapshot --dictionary-paths-file dictionary_paths`
   - `python regression_results.py compare --dictionary-paths-file dictionary_paths`
- `dictionary_paths` file can be either JSON (eg `{"unii": "dummy_ex_dicts/unii"}`) or key/value text (`key=value` or `key: value`, one per line). Supported keys:
   - `whodrug`, `meddra`, `unii`, `medrt`, `loinc`, `snomed`, `ct`
- Other options: `--use-postgres` (use PostgreSQL instead of pgserver) and, for `compare`, `--max-diff-lines` (default 120 diff lines shown per changed case). Run `python regression_results.py <snapshot|compare> -h` for details.
- `compare` exits with code 0 if there are no added, removed or changed cases, 2 if there are, and 1 if it could not run (e.g. no baseline found).
- Diff behavior:
   - `dictionary_versions` is ignored
   - `validated` is included
   - Row-only (or execution-message-only) differences are excluded from the main changed list and shown under `Trivial Diffs`
