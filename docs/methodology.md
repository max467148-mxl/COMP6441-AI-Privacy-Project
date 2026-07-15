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
- memory expiry.
- sensitive inference warning instruction.

Dependent variables:

- leakage score.
- response confidence.
- refusal or uncertainty rate.
- leakage category.

## Procedure

1. Load ten synthetic profiles.
2. For each profile, construct prompts under each context condition and mitigation.
3. Ask the same five standardised questions.
4. Save prompt, response, timestamp, model, condition, mitigation, and category.
5. Score each response using a transparent rubric.
6. Compare leakage score across conditions and mitigations.

## Methodological Weaknesses

- The synthetic profiles are simplified and may not represent real user behaviour.
- Scoring partly relies on keyword overlap and should be manually checked before final reporting.
- A model may produce cautious answers because the prompt explicitly mentions privacy.
- One model/provider is not enough to generalise to all AI systems.
- Dry-run mode is only for pipeline testing and is not experimental evidence.

