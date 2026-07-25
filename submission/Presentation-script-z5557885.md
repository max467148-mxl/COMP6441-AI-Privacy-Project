# Five-Minute Presentation Script

## Slide 1 — When harmless fragments become sensitive (0:00–0:40)

My project asks a simple privacy question: what happens when an AI system combines ordinary information that was never presented as a secret? A bus time, a campus library visit, shared rent and a retail shift are low-sensitivity fragments by themselves. Together, they can reveal where someone probably lives, when they are away from home, what they study and how they manage money. I tested this composition effect using synthetic profiles, so no real person was identified or targeted.

## Slide 2 — Aggregation creates a disclosure surface (0:40–1:20)

The threat is application-layer inference, not hacking model weights or extracting another user's training data. Fragments cross a context-selection boundary, the model correlates them, and the response becomes a disclosure surface. I used LINDDUN as the privacy lens, especially linkability, disclosure and user unawareness. The main security control point is before the prompt: which memories are allowed to cross into the current task?

## Slide 3 — Ninety isolated trials (1:20–2:05)

I created three synthetic profiles with fifteen fragments each and asked five standard questions about residential context, absence times, occupation, finances and links between activities. The 60 baseline trials compared one fragment, five fragments, all fifteen fragments and a five-fragment subset. Another 30 trials tested two mitigations under full context. The original procedure used a separate Temporary Chat for each prompt. A later audit found five copy-transfer errors. I reran those prompts and regenerated the results. All 90 final outputs parsed as JSON. The interface showed ChatGPT Plus in High mode, but it did not expose an exact model identifier, so I do not claim one.

## Slide 4 — Context increased leakage (2:05–2:55)

The strongest result is the context gradient. Mean leakage was 0.53 with one fragment, 0.87 with five, 0.97 in the keyword-ranked subset and 1.00 with all fifteen. Model-reported confidence rose from 0.54 to 0.84. These are descriptive scores across fifteen responses per condition, not population estimates. Full aggregation changed both the frequency and confidence of privacy-sensitive inference.

## Slide 5 — Weak mitigations failed (2:55–3:50)

The mitigations were less effective than expected. Generalising exact time and place details reduced leakage only from 1.00 to 0.97 because the broader routine remained linkable. A warning instruction produced the same small reduction. The keyword-ranked subset retained 0.97 leakage because its five fragments were correlated. A label is not enough. Boundaries must be designed around purpose and tested for the inferences they still enable.

During analysis I also found a scoring defect: the first version treated an uncertainty flag as a refusal before checking the answer. Some answers were cautious but still revealed the target attribute. I corrected the scoring order, added a regression test and rescored all records. This reinforced that privacy should be measured by information disclosed, not by cautious wording.

## Slide 6 — Engineering implications (3:50–5:00)

I draw four recommendations. First, minimise context at prompt construction and retrieve only what the current task needs. Second, isolate data by purpose, not by an arbitrary fragment count. Third, red-team combinations and attribute inference rather than checking only for direct secrets. Fourth, treat prompt warnings as defence in depth, not an access-control boundary.

The experiment is limited to three synthetic profiles, five questions and one interface mode, and the automated rubric is coarse. Future work should add blinded human coding, more models and stronger retrieval and retention controls while measuring utility as well as privacy. The main conclusion is that privacy is a property of the combination, not just the individual fragment.
