# T-010 — Build Figure 5 capability matrix (canonical lineage excerpt)

This file is the **canonical** ticket text hashed for Figure 5 lineage metadata. The full historical template collection lives in [issues_full.md](../archive/issues_full.md).

---

## Summary

Build the condensed capability matrix for the five core datasets and seven fixed empirical objects. This is the paper's synthesis figure and should summarize the architecture without introducing new evidence.

## Figure / output

- Figure ID: `Figure 5`
- Output file(s):
  - `figures/figure5_capability_matrix.csv`

## Why this matters

Supports Claim 5 by making the public-data identification frontier explicit.

## Source data

Datasets:

- `CPS`
- `BTOS`
- `JOLTS`
- `OEWS`
- `O*NET`

## Dependencies

- Depends on: `T-001`, `T-002`, `T-003`, `T-006`, `T-008`

## Fixed design choices

- Occupation grouping: `not applicable`
- Sector grouping: `not applicable`
- Geography: `not applicable`
- Time window: `not applicable`
- Weighting / normalization: `categorical coding only: direct / partial / none`

## Task checklist

- Create rows for the five core datasets
- Create columns for the seven frozen empirical objects
- Populate cells using the locked direct / partial / none rules
- Add legend key
- Export final tidy CSV
- Add/update source note in `docs/`
- Run QA checks

## Acceptance criterion

- `figures/figure5_capability_matrix.csv` meets its acceptance criterion:
  - File contains exactly 5 dataset rows × 7 empirical-object columns plus a legend key, with no extra datasets or empirical objects.

## QA checklist

- Matrix structure matches frozen design
- No extra datasets or columns added
- Cell coding follows locked rules only
- Output is tidy and reproducible
- Interpretation sentence added to metadata / notes

## Notes

This figure is not an empirical result and should not be expanded.
