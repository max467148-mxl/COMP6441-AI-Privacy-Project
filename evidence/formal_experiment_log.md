# Formal Experiment Log

## Run Details

- Original collection date: 2026-07-22
- Correction audit date: 2026-07-25
- Interface: ChatGPT Plus in Chrome
- Mode shown by interface: High
- Exact model identifier: not exposed by the interface
- Profiles: P01, P02, P03 (synthetic)
- Total prompt-response records: 90
- Isolation: a new Temporary Chat was opened for every original prompt and every correction rerun
- Final format result: 90 of 90 corrected responses parsed as JSON

## Study Design

- Baseline comparison: 3 profiles x 4 context conditions x 5 questions = 60 responses
- Mitigation comparison: 3 profiles x 2 mitigations x 5 questions = 30 responses
- Mitigations were tested only under `full_aggregated_memory`.

## Procedure Evidence

- `formal_001_temporary_chat.png` shows the beginning of the controlled run.
- `formal_090_temporary_chat.png` shows the end of the controlled run.
- `results/formal_prompts/` contains the submitted prompts.
- `results/formal_responses/` contains the final corrected responses.
- `results/formal_raw_results.jsonl` contains the collected records.
- `evidence/formal_response_audit.md` records the response audit and corrections.

The two screenshots are interface evidence from the beginning and end of collection. They are not complete proof of all 90 chat transitions. JSONL timestamps record import time. They do not record the generation time of each ChatGPT response.

## Browser Incident

After 36 completed prompts, Chrome returned `ERR_BLOCKED_BY_CLIENT` during a full-page navigation. Reloading restored the page. Later trials used ChatGPT's New Chat control. The prompt set remained complete.

## Response Audit and Correction

An exact-content audit on 25 July found five response files that duplicated the preceding response and answered the wrong question:

- 004 duplicated 003
- 049 duplicated 048
- 051 duplicated 050
- 068 duplicated 067
- 075 duplicated 074

The likely cause was manual copy-paste error during collection. Each affected prompt was rerun in a new Temporary Chat. The first complete correction response was saved. The v3 Git tag preserves the erroneous files. The v4 history records the correction. A second scan found 90 parseable files, no exact duplicate responses and no filename-to-tracking mismatch.

## Corrected Automated Results

- Baseline leakage: single fragment 0.53; five fragments 0.87; full 15-fragment context 1.00; keyword-ranked subset 0.97.
- Full-context leakage by mitigation: none 1.00; generalised time/place 0.97; sensitive-inference warning 0.97.
- Mean model-reported confidence rose from 0.54 with one fragment to 0.84 with all 15 fragments.

## Scoring Correction

The first scoring pass treated `refusal_or_uncertainty=true` as a refusal before checking answer content. Some answers used cautious language but still reconstructed the expected attribute. The scorer was corrected. Tests prevent regression. All 90 records were rescored.

Automated scores use expected-term overlap. They are descriptive evidence. No blinded human validation was conducted. The report treats this as a construct-validity limitation.
