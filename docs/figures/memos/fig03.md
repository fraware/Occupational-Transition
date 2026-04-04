# Figure 3 memo — BTOS AI adoption and workforce effects

## Question

What do published BTOS national rates show about business AI use over time, and what shares do businesses report for selected workforce effects in the AI supplement window?

## Datasets

- Census Business Trends and Outlook Survey (BTOS) public API for national firm-weighted AI use series.
- Census-published BTOS AI Supplement Table (XLSX) for workforce-effect category shares.

## Construction

T-006 pulls published national-stratum series for current and expected AI use by collection period. T-007 reads published supplement shares for retained categories. See methodology for the retained window and any documented proxy mapping for task-related rows. Metadata is in `intermediate/figure3_panelA_*` and `intermediate/figure3_panelB_*`.

## Main takeaway

Public business-side data support time series of stated AI adoption and supplement summaries for retained workforce categories. Employment-effect categories are the strongest interpretable rows. Task-effect interpretation remains proxy-based when item-25 option rows are not in the public workbook.

## How to read quickly

- Use Panel A to read trend direction and level differences between current and expected AI use.
- Use Panel B to compare the size of retained workforce-effect categories in the supplement window.
- Treat employment-effect categories as directly published rows and task-effect categories as proxy-interpreted when item-25 option rows are absent.
- Keep interpretation at the business-reported descriptive level.

## What the figure does not identify

- Worker-level outcomes linked to specific adopting establishments.
- Causal impacts of AI on employment, hours, or turnover (self-reported categories are not treatment-effect estimates).
- Complete task-effect tabulations when detailed item-25 rows are not publicly released.

## Possible reviewer objections

- **Questionnaire changes:** BTOS is experimental; robustness scripts check period and definition consistency where encoded in outputs.
- **Supplement mapping:** `README.md` Known Deviations documents any deviation from the literal six-category template when public tables require proxies.

## Redesign objective

Figure 3 should be the paper’s evidentiary-discipline figure.

The visual priority is not simply to show BTOS levels. It is to make two things legible immediately:

1. business-reported AI adoption is now clearly visible in direct published public data;
2. workforce-effect evidence does not all carry the same evidentiary weight.

Implementation rule:

- Preserve the frozen Figure 3 CSVs.
- Treat the November 2025 wording change as a comparability event in Panel A.
- In Panel B, visually separate direct published rows from proxy-interpreted indicators.
- Make the “Employment did not change” direct row the visual anchor of the panel.
- Run `python scripts/visualize_figure3.py` before visual QA; `scripts/qa_visuals.py` expects PNG+PDF for `btos_ai_trends`, `btos_workforce_effects_barh`, and the stacked manuscript stem `figure3_redesigned_composite` (listed in `docs/figures/figure_catalog.md` and `docs/figures/visual_packaging_manifest.md`).
