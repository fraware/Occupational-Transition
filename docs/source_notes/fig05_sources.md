# Figure 5 — Data sources and provenance

## Primary sources

- **Coding rules:** Frozen categorical matrix from `paper-notes.md` (dataset-to-claim matrix) and `issues.md` T-010; implemented in `scripts/build_figure5_capability_matrix.py`. No empirical estimation beyond verifying structure in QA.

## Run metadata

- `intermediate/figure5_capability_matrix_run_metadata.json` (includes hashes for `issues.md` and `paper-notes.md` as rule sources).

## Provenance pointers

- **Figure CSV output:** `figures/figure5_capability_matrix.csv`
- **Methodology doc:** `docs/t010_figure5_capability_matrix_methodology.md`
- **Rule inputs:** `paper-notes.md`, `issues.md`

## Limitations

- Cells are interpretive documentation of what each public source can support, not statistical estimates of adoption or harm.
- The matrix is not a substitute for causal identification of AI effects.
