# Analysis Catalog

Intent-first guide to choose analyses, data, and outputs.

| Analysis intent | Bundle / tickets | Primary sources | Main outputs |
|---|---|---|---|
| Occupational baseline and task structure | `quick-start` (`T-001`,`T-002`) | OEWS, O*NET | `figures/figure1_panelA_occ_baseline.csv`, `figures/figure1_panelB_task_heatmap.csv` |
| Worker hours and transitions | `quick-start` (`T-003` to `T-005`) | CPS | `figures/figure2_panelA_hours_by_ai_tercile.csv`, `figures/figure2_panelB_transition_probs.csv` |
| Business-side AI adoption and effects | `quick-start` (`T-006`,`T-007`) | BTOS | `figures/figure3_panelA_btos_ai_trends.csv`, `figures/figure3_panelB_btos_workforce_effects.csv` |
| Sector demand context | `quick-start` (`T-008`,`T-009`) | JOLTS, CES | `figures/figure4_panelA_jolts_sector_rates.csv`, `figures/figure4_panelB_ces_sector_index.csv` |
| Identification frontier matrix | `core-paper` (`T-010`) | Documentation synthesis | `figures/figure5_capability_matrix.csv` |
| Full appendix + robustness inputs | `full-replication` (`T-011` to `T-026`) | ASEC, SIPP, ABS, LEHD, NLS, CPS, BTOS, QCEW | `figures/figureA*.csv`, `metrics/*.csv`, `intermediate/*.json` |

## Bundle presets

- `quick-start`: `T-001` to `T-008`
- `core-paper`: `T-001` to `T-010`
- `full-replication`: `PR-000`, `T-001` to `T-026`
- `release-signoff`: same as full replication, plus signoff gate

## Commands

```bash
ot list-analyses
ot run --bundle quick-start
ot run --tickets T-001,T-002,T-006
```
