# T-005 — Figure 2 Panel B: transition probabilities (methodology)

Last source verification refresh: 2026-03-22.

## Scope

Derive row-normalized transition probabilities from T-004 matched-person weighted transition counts. No additional Census CPS microdata are read in this step.

## Inputs (project artifacts)

- `figures/figure2_panelB_transition_counts.csv` (T-004)
- `intermediate/figure2_panelB_counts_run_metadata.json` (T-004 lineage)

Registry: `docs/data_registry.csv` (`project_t005_figure2_panelB_transition_probs_derived`).

## Official conceptual references

Underlying CPS definitions and weights are documented in the CPS Public Use documentation and in T-003/T-004 methodology. T-005 only transforms T-004 outputs.

| Role | Source |
|------|--------|
| CPS methodology | `https://www2.census.gov/programs-surveys/cps/methodology/PublicUseDocumentation_final.pdf` |

## Normalization

For each `month` (origin month of the transition) and `origin_state`:

`origin_mass = sum(weighted_transition_count)` over all `destination_state` rows in that cell.

`transition_probability = weighted_transition_count / origin_mass`.

So for each `month x origin_state`, probabilities over destinations sum to 1 (within floating-point tolerance).

## Output file

`figures/figure2_panelB_transition_probs.csv` — single tidy file with two `record_type` values:

| record_type | Meaning |
|-------------|---------|
| `matrix` | Full origin–destination cells: `destination_state`, `weighted_transition_count`, `origin_mass`, `transition_probability`
| `summary` | Derived metrics: `metric_name`, `metric_value`; other matrix columns left blank |

## Summary metrics (per `month x origin_state`)

From the matrix row for that origin:

- `retention_rate`: `transition_probability` where `destination_state == origin_state`
- `occ_switch_rate`: if `origin_state` is `occ22_*`, sum of `transition_probability` to other `occ22_*` destinations (not equal to `origin_state`); if `origin_state` is `unemployed` or `nilf`, not applicable (`NA`)
- `unemployment_entry_rate`: sum of `transition_probability` where `destination_state == unemployed`
- `nilf_entry_rate`: sum of `transition_probability` where `destination_state == nilf`

## Run metadata

`intermediate/figure2_panelB_probs_run_metadata.json` records SHA-256 hashes of the T-004 inputs, normalization rule, tolerance, and summary metric definitions.

## Reproducibility commands

```bash
pip install -r requirements.txt
python scripts/build_figure2_panelB_probs.py
python scripts/qa_figure2_panelB_probs.py
```

Prerequisite: T-004 outputs must exist (`build_figure2_panelB_counts.py`).

## QA checks

Implemented in `scripts/qa_figure2_panelB_probs.py`:

- schema and non-null rules by `record_type`
- matrix probabilities in `[0, 1]` and row sums equal to 1 within tolerance
- `occ_switch_rate` is `NA` for non-occupational origins
- summary metrics in `[0, 1]` when not `NA`
- origin months align with T-004 pair list in `figure2_panelB_counts_run_metadata.json`

## Figure rendering

Publication-ready static visuals are generated from the existing figure CSV
outputs (no data-value changes) using:

```bash
python scripts/run_visuals_all.py
python scripts/qa_visuals.py
```

Artifacts:

- `visuals/png/*.png`
- `visuals/vector/*.pdf`
- `intermediate/visuals_run_manifest.json`

Style and chart standards are documented in `docs/quality/README.md#visual-style-guide`.

