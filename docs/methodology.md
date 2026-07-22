# Methodology

This project uses a controlled experiment to test inference-based privacy leakage from synthetic low-sensitivity fragments.

## Variables

Independent variable: context condition.

- `no_memory`: one fragment.
- `limited_memory`: five fragments.
- `full_aggregated_memory`: all fifteen fragments.
- `compartmentalised_memory`: five fragments selected from a relevant compartment.

Mitigation variable:

- no mitigation.
- generalise exact time and place hints.
- sensitive inference warning instruction.

Dependent variables:

- leakage score.
- response confidence.
- refusal or uncertainty rate.
- leakage category.

## Procedure

1. Load three synthetic profiles (P01-P03).
2. Generate 60 baseline prompts: three profiles by four context conditions by five standardised questions.
3. Generate 30 mitigation prompts under full aggregation: three profiles by two mitigations by five questions.
4. Submit each of the 90 prompts in a separate ChatGPT Temporary Chat and preserve the first completed response without editing.
5. Save prompt, response, model-interface label, condition, mitigation, category, and collection status.
6. Parse the required JSON and score each response using a transparent expected-term rubric.
7. Compare context conditions only within the no-mitigation baseline, and compare mitigations only within full aggregated context to avoid confounding.

## Methodological Weaknesses

- The synthetic profiles are simplified and may not represent real user behaviour.
- Scoring partly relies on keyword overlap and should be manually checked before final reporting.
- The prompt's privacy framing may itself change model behaviour.
- One model/provider is not enough to generalise to all AI systems.
- The interface exposed `ChatGPT Plus` and `High` mode but not an exact model identifier.
- The 90 responses are descriptive observations; no inferential significance test is claimed.
