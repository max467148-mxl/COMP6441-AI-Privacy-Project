# Manual ChatGPT Experiment Instructions

This folder contains 90 prompts for manual testing with ChatGPT Plus.

## Workflow

1. Open `results/manual_tracking.csv`.
2. Start with prompt `001`.
3. Open the prompt file listed in `prompt_file`.
4. Copy the full prompt into a new ChatGPT message.
5. Copy ChatGPT's full response.
6. Paste it into the matching file in `results/manual_responses/`.
7. Mark the row as complete in the tracking CSV if you want a progress record.
8. Save screenshots for several representative prompts and responses.

## Important

- Do not edit the prompt text before sending it.
- Do not use real personal data.
- Keep responses in JSON shape where possible.
- If ChatGPT refuses or answers in prose, save the full answer anyway.
- Do not use dry-run outputs as final evidence.

## After Responses Are Filled

Run:

```powershell
py -3 -m src.manual_experiment collect
py -3 -m analysis.analyze_results --input results/manual_raw_results.jsonl
```

The analysis script will produce:

- `results/scored_results.csv`
- `results/leakage_by_condition.png`
- `results/leakage_by_category.png`
- `results/mitigation_comparison.png`
- `results/summary.md`
