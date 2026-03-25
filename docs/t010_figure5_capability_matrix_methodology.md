# T-010 — Figure 5 capability matrix

## Outputs

- `figures/figure5_capability_matrix.csv` — wide-format synthesis table: five core datasets by seven empirical-object columns, with categorical codes `direct` / `partial` / `none`, plus repeated legend-key columns.
- `intermediate/figure5_capability_matrix_run_metadata.json` — SHA-256 hashes of `docs/lineage/t010_issues.md` and `docs/lineage/t010_paper_notes_matrix.md`, frozen dataset and column lists, and synthesis-only assertion.

## Sources of truth (no new empirical estimation)

1. **Ticket structure** — [docs/lineage/t010_issues.md](lineage/t010_issues.md) (T-010): five datasets, seven empirical objects, categorical coding only, synthesis figure. Full template history: [docs/archive/issues_full.md](archive/issues_full.md).
2. **Locked cell coding** — [docs/lineage/t010_paper_notes_matrix.md](lineage/t010_paper_notes_matrix.md) (“Dataset-to-claim matrix” excerpt): legend (`✓`, `△`, `✗`) and rows for:
   - `CPS (basic monthly)`
   - `BTOS`
   - `JOLTS`
   - `OEWS`
   - `O*NET`

The retained implementation keeps seven empirical-object columns and explicitly includes `worker_firm_ai_linkage` so the core Claim 5 gap is directly represented in the matrix.

## Code mapping

| Symbol in lineage doc | CSV value |
|--------------------|-----------|
| ✓ (check) | `direct` |
| △ (triangle) | `partial` |
| ✗ (x-mark) | `none` |

Legend text in the CSV echoes the definitions in `docs/lineage/t010_paper_notes_matrix.md`.

## Registry

Provenance rows: `project_issues_md_t010` and `project_paper_notes_md_t010` in [data_registry.csv](data_registry.csv).

## QA

```bash
python scripts/qa_figure5_capability_matrix.py
```

Checks column order, exactly five dataset rows, allowed codes, legend consistency, and metadata SHA-256 match for `docs/lineage/t010_issues.md` and `docs/lineage/t010_paper_notes_matrix.md`.

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

