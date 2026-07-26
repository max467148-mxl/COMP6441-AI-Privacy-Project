COMP6441 Supporting Material
Student: Xiaolong Ma
Student ID: z5557885
Project: When Harmless Fragments Become Sensitive

PURPOSE
This archive supports the submitted project report. It contains the formal
experiment inputs, outputs, analysis, source code, tests, logs and version
history. All profiles and fragments are synthetic.

FINAL SNAPSHOT
GitHub: https://github.com/max467148-mxl/COMP6441-AI-Privacy-Project
Tag: COMP6441-final-submission-v9
Report commit: d18d0c28af83763eeea8286cb22e872dc8693ba7

CONTENTS
- src/, scoring/, analysis/ and tools/: experiment, scoring and audit code.
- data/, experiments/, questions/ and mitigations/: study configuration.
- results/formal_prompts/: the 90 submitted prompts.
- results/formal_responses/: the 90 preserved final responses.
- results/formal_raw_results.jsonl: machine-readable formal records.
- results/formal_tracking.csv: trial completion records.
- results/formal_analysis/: final scores, metrics, figures and summary.
- evidence/: experiment log, response audit, screenshots, test record and
  reconstructed work diary.
- docs/: methodology, threat model, ethics, limitations and protocol.
- tests/: automated regression and workflow tests.
- presentation/: final slides, speaking script and reproducible slide source.
- git-history.bundle: portable full repository history and tags.
- MANIFEST-SHA256.txt: file hashes for archive integrity checks.

QUICK VERIFICATION
Install Python dependencies:
  py -3 -m pip install -r requirements.txt

Run tests:
  py -3 -m unittest discover -s tests -v

Audit the formal responses:
  py -3 tools/audit_formal_responses.py

Inspect the portable Git history:
  git bundle verify git-history.bundle

NOTES
The ChatGPT interface displayed Plus and High mode. It did not expose an exact
model identifier. The report therefore does not claim one. Dry-run and draft
report files are excluded from this archive. The submitted report contains the
formal AI-use declaration and remains the authoritative project narrative.
