# Evidence snapshot policy (manuscript alignment)

Use this note when locking numeric prose in [paper_final.md](paper_final.md) to a specific repository state.

## This repository (worked example)

The expanded manuscript in [paper_final.md](paper_final.md) cites concrete percentages and month labels checked against commit **`72f02bf2e7897f5515ab9212f9e6fe6fbcd2c432`** (short **`72f02bf`**). When you publish a labeled freeze, add an annotated tag and replace the commit reference in the manuscript with that tag name.

To create a tag after a clean acceptance run (illustrative):

```bash
git tag -a results-YYYY-MM-DD -m "Frozen research state for manuscript"
git push origin results-YYYY-MM-DD
```

## Recommended practice

1. Run a full or scoped acceptance pass and record results in [acceptance_matrix.md](acceptance_matrix.md).
2. Optionally create a git tag per [release_process.md](release_process.md) (for example `results-YYYY-MM-DD`) and cite that tag in the manuscript’s reproducibility section.
3. **T-004 transition counts:** `figures/figure2_panelB_transition_counts.csv` is produced by the CPS pipeline and may not be committed in every snapshot; it feeds T-005 and memo KPIs. Main-text sentences about Figure 2 Panel B should match the CSVs and run metadata generated under the same rebuild as the cited tag, or include explicit “as of [date/tag]” language. See [committed_outputs.md](committed_outputs.md).

## Authoritative tables

- Frozen figure CSVs: `figures/*.csv` as listed in `git ls-files figures`.
- Build-generated intermediates (examples): `intermediate/ai_relevance_terciles.csv`, `intermediate/*_run_metadata.json`.

Do not hand-edit numeric claims in the manuscript without reconciling to these artifacts.
