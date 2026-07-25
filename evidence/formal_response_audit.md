# Formal Response Integrity Audit

## Audit Scope

The audit was run on 25 July 2026 after review of the v3 evidence package. It checked all 90 tracking rows and response files for:

- exact duplicate file content;
- JSON parsing and required fields;
- prompt and response filename alignment with tracking metadata;
- broad answer relevance to the assigned question category.

## Errors Found

The first pass found five cross-question copy errors:

| Corrected ID | Incorrectly duplicated ID | Question category requiring correction |
|---|---|---|
| 004 | 003 | Financial situation |
| 049 | 048 | Financial situation |
| 051 | 050 | Residential context |
| 068 | 067 | Study or work |
| 075 | 074 | Activity linking |

Each affected prompt was rerun in a separate ChatGPT Temporary Chat on 25 July. The first complete rerun output replaced the incorrect response in the v4 working tree. Git tag `COMP6441-final-submission-v3` preserves the original files.

## Post-Correction Result

The final audit reported:

```text
Tracking rows checked: 90
Response files parsed: 90
Exact duplicate groups: 0
Audit issues: 0
```

The corrected records were imported into `formal_raw_results.jsonl`. All scores, metrics and figures were regenerated. The correction changed aggregate results. The final report uses the corrected values.
