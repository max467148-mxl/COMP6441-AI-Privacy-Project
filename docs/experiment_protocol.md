# Experiment Protocol

1. Confirm the Git working tree state and record the commit hash.
2. Confirm `.env` exists locally and is not committed.
3. Run a dry-run pipeline check.
4. Inspect `results/raw_results.jsonl` and `results/summary.md`.
5. Delete dry-run outputs or clearly archive them as dry-run.
6. Run a small real model experiment with `--limit-profiles 2`.
7. Manually inspect responses for format and safety problems.
8. Run the full experiment only after the small run is acceptable.
9. Run the analysis script.
10. Save screenshots of terminal commands, output files, and generated charts.
11. Add a work diary entry with time spent and issues encountered.
12. Use raw outputs and screenshots as appendix evidence.

