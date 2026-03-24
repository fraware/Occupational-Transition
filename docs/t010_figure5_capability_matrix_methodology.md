# T-010 — Figure 5 capability matrix

## Outputs

- `figures/figure5_capability_matrix.csv` — wide-format synthesis table: five core datasets by seven empirical-object columns, with categorical codes `direct` / `partial` / `none`, plus repeated legend-key columns.
- `intermediate/figure5_capability_matrix_run_metadata.json` — SHA-256 hashes of `issues.md` and `paper-notes.md`, frozen dataset and column lists, and synthesis-only assertion.

## Sources of truth (no new empirical estimation)

1. **Ticket structure** — [issues.md](../issues.md) section T-010: five datasets, seven empirical objects, categorical coding only, synthesis figure.
2. **Locked cell coding** — [paper-notes.md](../paper-notes.md) “Dataset-to-claim matrix” block: legend (`✓`, `△`, `✗`) and rows for:
   - `CPS (basic monthly)`
   - `BTOS`
   - `JOLTS`
   - `OEWS`
   - `O*NET`

The retained implementation keeps seven empirical-object columns and explicitly includes `worker_firm_ai_linkage` so the core Claim 5 gap is directly represented in the matrix.

## Code mapping

| paper-notes symbol | CSV value |
|--------------------|-----------|
| ✓ (check) | `direct` |
| △ (triangle) | `partial` |
| ✗ (x-mark) | `none` |

Legend text in the CSV echoes the definitions in `paper-notes.md` (Legend subsection immediately above the matrix).

## Registry

Provenance rows: `project_issues_md_t010` and `project_paper_notes_md_t010` in [data_registry.csv](data_registry.csv).

## QA

```bash
python scripts/qa_figure5_capability_matrix.py
```

Checks column order, exactly five dataset rows, allowed codes, legend consistency, and metadata SHA-256 match for `issues.md` and `paper-notes.md`.

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

Style and chart standards are documented in `docs/visual_style_guide.md`.

