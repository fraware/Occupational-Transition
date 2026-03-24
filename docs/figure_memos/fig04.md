# Figure 4 memo — JOLTS and CES sector context

## Question

How do JOLTS flow rates (openings, hires, quits, layoffs/discharges) and CES payroll employment trajectories compare across the paper’s selected six-sector comparison set over the same broad period as other figures?

## Datasets

- BLS JOLTS LABSTAT time series (openings rate and related series as implemented).
- BLS CES LABSTAT employment series by detailed industry, mapped through `crosswalks/sector6_crosswalk.csv`.

## Construction

T-008 assembles JOLTS rates by `sector6` label; T-009 builds CES payroll levels and indexes to August 2023 = 100. See `docs/t008_*` and `docs/t009_*`; run metadata JSONs in `intermediate/`.

## Main takeaway

Labor-demand and payroll dynamics vary materially by sector group, providing official context for interpreting worker- and firm-side figures that are not occupation-specific in JOLTS.

## What the figure does not identify

- Occupation-level vacancies, hires, or separations (not in public JOLTS core as used here).
- AI-specific labor demand (series are total flows and payroll, not AI-attributed).

## Possible reviewer objections

- **Model-based state/sector detail:** JOLTS subnational estimates rely on BLS models; the figure uses published series as selected in the build.
- **Sector mapping:** Robustness checks validate labels against `sector6_crosswalk.csv`.
