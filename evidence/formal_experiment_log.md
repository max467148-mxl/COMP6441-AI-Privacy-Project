# Formal Experiment Log

## Run Details

- Date: 2026-07-22
- Interface: ChatGPT Plus in Chrome
- Mode shown by interface: High
- Exact model identifier: not exposed by the interface
- Profiles: P01, P02, P03 (synthetic)
- Total prompts: 90
- Isolation: a new Temporary Chat was opened for every prompt
- Response policy: the first completed response was copied without editing
- Format result: 90 of 90 responses parsed as JSON

## Study Design

- Baseline comparison: 3 profiles x 4 context conditions x 5 questions = 60 responses
- Mitigation comparison: 3 profiles x 2 mitigations x 5 questions = 30 responses
- Mitigations were tested only under `full_aggregated_memory` to avoid mixing the mitigation effect with context size.

## Procedure Evidence

- `formal_001_temporary_chat.png` shows the beginning of the controlled run.
- `formal_090_temporary_chat.png` shows the end of the controlled run.
- `results/formal_prompts/` contains the exact submitted prompts.
- `results/formal_responses/` contains the unedited copied responses.
- `results/formal_raw_results.jsonl` contains the collected records.

## Incident and Method Change

After 36 completed prompts, Chrome briefly returned `ERR_BLOCKED_BY_CLIENT` during a full-page navigation. Reloading restored the page. The procedure was changed to use ChatGPT's own New Chat link between trials instead of repeatedly navigating the whole page. No completed response was lost or repeated.

## Final Automated Results

- Baseline leakage by condition: no memory 0.53; limited memory 0.83; full aggregated memory 0.97; compartmentalised memory 0.93.
- Full-context leakage by mitigation: none 0.97; remove exact time/place 0.93; sensitive-inference warning 0.97.
- Mean model-reported confidence increased from 0.55 under no memory to 0.83 under full aggregation.

## Scoring Correction

The first scoring pass treated `refusal_or_uncertainty=true` as a refusal before checking the answer content. Inspection showed that some answers used cautious language but still reconstructed the expected sensitive attribute. The scorer was corrected so supported sensitive content is evaluated before the model's self-reported uncertainty flag. Tests were added to prevent regression, all 90 records were rescored, and the values above are the corrected results.

Automated scores are a transparent first-pass measure based on expected-term overlap. They are reported as descriptive evidence and remain a limitation rather than a substitute for independent human coding.
