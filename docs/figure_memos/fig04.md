# Figure 4 memo — JOLTS and CES sector context

## Question

How do JOLTS flow rates (openings, hires, quits, layoffs/discharges) and CES payroll trajectories compare across the paper's six-sector comparison set over the same broad period as other figures?

## Datasets

- BLS JOLTS LABSTAT time series (openings rate and related series as implemented).
- BLS CES LABSTAT employment series by detailed industry, mapped through `crosswalks/sector6_crosswalk.csv`.

## Construction

T-008 assembles JOLTS rates by `sector6` label. T-009 builds CES payroll levels and indexes to August 2023 = 100. See `docs/t008_*` and `docs/t009_*`. Run metadata JSONs are in `intermediate/`.

## Main takeaway

Labor-demand and payroll dynamics vary materially by sector group. This provides official context for interpreting worker-side and firm-side figures when JOLTS is not occupation-specific.

## How to read quickly

- In Panel A, compare level and trend differences across sectors for each JOLTS flow rate.
- In Panel B, read deviations from 100 as payroll movement relative to August 2023.
- Use the figure as macro/sector context for other main-text descriptive panels.
- Avoid interpreting these series as occupation-level or AI-attributed demand measures.

## What the figure does not identify

- Occupation-level vacancies, hires, quits, or layoffs (public series here are sector aggregates).
- AI-specific demand signals (rates and payroll levels are total, not AI-attributed).
- Causal effects of AI adoption on sector labor-demand flows.

## Possible reviewer objections

- **Model-based state/sector detail:** JOLTS subnational estimates rely on BLS models; the figure uses published series as selected in the build.
- **Sector mapping:** Robustness checks validate labels against `sector6_crosswalk.csv`.
