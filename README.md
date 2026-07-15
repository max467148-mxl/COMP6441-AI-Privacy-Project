# When Harmless Fragments Become Sensitive

Measuring privacy leakage through AI context aggregation.

This is a reproducible cybersecurity experiment about inference-based privacy leakage. It uses synthetic user profiles only. The project measures how much sensitive information an AI system can infer when individually low-sensitivity fragments are retained and combined.

## Research Questions

1. To what extent can an AI system infer private information by combining individually non-sensitive data fragments?
2. How does retained context affect privacy-sensitive inference rate and confidence?
3. Which simple controls reduce inference-based leakage most effectively?

## Setup

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -3 -m pip install -r requirements.txt
```

## Dry Run

Dry-run mode creates reproducible placeholder responses. It is useful for checking the pipeline before spending API credits.

```powershell
py -3 -m unittest discover -s tests
py -3 -m src.run_experiment --dry-run
py -3 -m analysis.analyze_results --input results/raw_results.jsonl
```

## Real Model Run

Create `.env` from `.env.example`, add an API key, and run:

```powershell
py -3 -m src.run_experiment --provider openai --limit-profiles 2
py -3 -m analysis.analyze_results --input results/raw_results.jsonl
```

Start with `--limit-profiles 2` so you can inspect the outputs before running the full experiment.

## Manual ChatGPT Run Without API Billing

If you only have ChatGPT Plus and do not want separate API billing, export prompts and answer them manually in ChatGPT:

```powershell
py -3 -m src.manual_experiment export --limit-profiles 3
```

This creates:

- `results/manual_prompts/`: prompts to copy into ChatGPT.
- `results/manual_responses/`: response files where you paste ChatGPT answers.
- `results/manual_tracking.csv`: progress sheet.
- `results/manual_instructions.md`: step-by-step instructions.

After filling the response files:

```powershell
py -3 -m src.manual_experiment collect
py -3 -m analysis.analyze_results --input results/manual_raw_results.jsonl
```

For a manageable high-quality report, start with `--limit-profiles 3`. That creates 240 prompts if all mitigations are included, which is substantial. For a smaller pilot, use one mitigation:

```powershell
py -3 -m src.manual_experiment export --limit-profiles 3 --mitigations none
```

## Outputs

- `results/raw_results.jsonl`: prompts, responses, condition, model, timestamp.
- `results/scored_results.csv`: scored results.
- `results/leakage_by_condition.png`: leakage rate by context condition.
- `results/leakage_by_category.png`: leakage rate by attribute category.
- `results/mitigation_comparison.png`: mitigation comparison.

## Academic Integrity Notes

Do not submit dry-run outputs as final experiment evidence. Real results should come from a documented model run, with raw logs, screenshots, and a work diary. The report must acknowledge AI assistance and explain what you personally checked and understood.
