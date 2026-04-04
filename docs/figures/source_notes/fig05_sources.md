# Figure 5 — Data sources and provenance

## Primary sources

- **Coding rules:** Frozen categorical matrix from `docs/lineage/t010_paper_notes_matrix.md` (dataset-to-claim matrix) and `docs/lineage/t010_issues.md` (T-010); implemented in `scripts/build_figure5_capability_matrix.py`. No empirical estimation beyond verifying structure in QA.

## Run metadata

- `intermediate/figure5_capability_matrix_run_metadata.json` (includes hashes for `docs/lineage/t010_issues.md` and `docs/lineage/t010_paper_notes_matrix.md` as rule sources).

## Provenance pointers

- **Figure CSV output:** `figures/figure5_capability_matrix.csv`
- **Methodology doc:** `docs/methodology/tickets/t010_figure5_capability_matrix_methodology.md`
- **Rule inputs:** `docs/lineage/t010_paper_notes_matrix.md`, `docs/lineage/t010_issues.md`

## Reproducibility hashes (SHA256)

- `figures/figure5_capability_matrix.csv` — `04d1c49a3cef96cfd4ce459eb6afe31bcd9b88835febfa8fa9079cd04e655674`
- `intermediate/figure5_capability_matrix_run_metadata.json` — `9635482a52f9036feaa357a1491457d215ce389b09d27b1696204d9a57fc0248`
- `docs/lineage/t010_paper_notes_matrix.md` — `4f9cf066d59d557022b31583318f47dfbcdf36d6c4c345a44ffd023d07d9c385`
- `docs/lineage/t010_issues.md` — `aa0fdb74636ab44cfb77a538b136e73adb06cc826ea4ece991b8eafd8c6158d4`

## Limitations

- Cells are interpretive documentation of what each public source can support, not statistical estimates of adoption or harm.
- The matrix is not a substitute for causal identification of AI effects.

## Presentation layer (Figure 5 visual redesign)

Source note: Figure 5 is a rule-based synthesis artifact constructed from the released public measurement objects used in the paper’s main empirical architecture. It is derived from the frozen capability-matrix CSV `figures/figure5_capability_matrix.csv`.

Interpretation note: “Direct” means the released public source observes the empirical object itself. “Partial” means the object is informed only indirectly, through aggregation, proxying, or important conceptual caveats. “Not observed” means the released public source does not observe the relationship at all.

Presentation note: The grouped headers (worker-side, firm-side, context, structure and mechanism, integrated linkage) are editorial presentation only. They do not alter the underlying coded matrix.
