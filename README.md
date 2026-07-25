# When Harmless Fragments Become Sensitive

This COMP6441 independent cybersecurity project measures inference-based privacy leakage when an AI system aggregates individually low-sensitivity context fragments. All profiles are synthetic; the project does not identify or test real people.

## Formal Study

The completed study contains 90 isolated ChatGPT trials:

- 3 synthetic profiles.
- 5 standardised privacy-inference questions.
- 60 baseline trials across four context conditions.
- 30 mitigation trials under full aggregated context.
- A new Temporary Chat for every prompt.
- The first completed response preserved without editing.

The interface displayed ChatGPT Plus in High mode but did not expose an exact model identifier.

## Main Results

| Treatment | Mean leakage score |
|---|---:|
| No memory | 0.53 |
| Limited memory | 0.83 |
| Full aggregated memory | 0.97 |
| Implemented keyword-ranked compartment | 0.93 |
| Full context with exact time/place generalised | 0.93 |
| Full context with sensitive-inference warning | 0.97 |

These are descriptive results from a transparent expected-term scorer. The metric measures attribute reconstruction, not disclosure specificity; the final report discusses this construct-validity limitation.

## Evidence Map

- `results/formal_prompts/`: exact submitted prompts.
- `results/formal_responses/`: unedited copied responses.
- `results/formal_raw_results.jsonl`: machine-readable formal records.
- `results/formal_tracking.csv`: completion status for all 90 trials.
- `results/formal_analysis/`: corrected scores, metrics and figures.
- `evidence/formal_experiment_log.md`: procedure, browser incident and scoring correction.
- `evidence/screenshots/`: beginning and end Temporary Chat evidence.
- `evidence/work_diary.md`: reconstructed 30-hour activity log with artefact references.
- `submission/`: final report, presentation, script and checklist.

## Reproduction

Install dependencies:

```powershell
py -3 -m pip install -r requirements.txt
```

Regenerate the formal prompt design and run tests:

```powershell
py -3 -m src.manual_experiment export --design formal90
py -3 -m unittest discover -s tests -v
```

After response files have been populated, collect and analyse them:

```powershell
py -3 -m src.manual_experiment collect --tracking results/formal_tracking.csv
py -3 -m analysis.analyze_results results/formal_raw_results.jsonl --output-dir results/formal_analysis
```

## Submission Integrity

- Dry-run outputs are not used as formal evidence.
- The project reports inference-based privacy leakage, not a confirmed production data breach.
- Generative AI assistance is disclosed in the report.
- Public repository: https://github.com/max467148-mxl/COMP6441-AI-Privacy-Project
- The current submitted snapshot is marked by the immutable tag `COMP6441-final-submission-v2`; the earlier `COMP6441-final-submission` tag is retained as a historical snapshot.
