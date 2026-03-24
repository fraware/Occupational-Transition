# Figure 3 memo — BTOS AI adoption and workforce effects

## Question

What do published BTOS national rates show about business AI use over time, and what shares do businesses report for selected workforce impacts in the AI supplement window?

## Datasets

- Census Business Trends and Outlook Survey (BTOS) public API for national firm-weighted AI use series.
- Census-published BTOS AI Supplement Table (XLSX) for workforce-effect category shares.

## Construction

T-006 pulls published national stratum series for current and expected AI use by collection period. T-007 reads published supplement shares for retained categories; see methodology for window and any documented proxy mapping for task-related rows. Metadata: `intermediate/figure3_panelA_*` and `intermediate/figure3_panelB_*`.

## Main takeaway

Public business-side data support time series of stated AI adoption and supplement summaries for retained workforce categories; employment-effect categories are the strongest interpretable rows, while task-effect interpretation should be treated as proxy-based when item-25 option rows are not in the public workbook.

## What the figure does not identify

- Worker-level outcomes linked to adopting establishments.
- Causal impacts of AI on employment (self-reported categories, not modeled treatment effects).

## Possible reviewer objections

- **Questionnaire changes:** BTOS is experimental; robustness scripts check period and definition consistency where encoded in outputs.
- **Supplement mapping:** `README.md` Known Deviations documents any deviation from the literal six-category template when public tables require proxies.
