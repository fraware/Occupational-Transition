# Evidence snapshot policy (manuscript alignment)

Use this note when locking numeric prose in [paper.md](paper.md) to a specific repository state.

## This repository (worked example)

The expanded manuscript in [paper.md](paper.md) cites concrete percentages and month labels checked against commit **`72f02bf2e7897f5515ab9212f9e6fe6fbcd2c432`** (short **`72f02bf`**). When you publish a labeled freeze, add an annotated tag and replace the commit reference in the manuscript with that tag name.

To create a tag after a clean acceptance run (illustrative):

```bash
git tag -a results-YYYY-MM-DD -m "Frozen research state for manuscript"
git push origin results-YYYY-MM-DD
```

## Commit vs. build-state (why both matter)

Pointing readers to a **git commit** or **tag** proves which **versioned** `figures/*.csv` files belong with the paper. It does **not** by itself prove that locally regenerated `intermediate/` outputs (or memo KPIs that aggregate transitions) came from the **same** pipeline execution as those CSVs—unless you also archive the **acceptance log** and rely on a single full rebuild.

**Before circulating or submitting**, treat “freeze discipline” as:

1. One **full** or **strict acceptance** run whose log you keep (`intermediate/full_clean_rebuild_acceptance_<UTC>.md` or equivalent).
2. Spot-check that manuscript numbers match the **committed** figure CSVs at that commit (or at the tag).
3. For **Figure 2** especially: transition **counts** (T-004), **probabilities** (T-005), and any **memo dashboard KPI** that averages over origins must be internally consistent for the **same** origin months and weights—ideally from one uninterrupted build, not a mix of reruns. If `figure2_panelB_transition_counts.csv` is not in git, it must still exist on disk from that run and match the probs file.

## Recommended practice

1. Run a full or scoped acceptance pass and record results in [acceptance_matrix.md](../replication/acceptance_matrix.md).
2. Optionally create a git tag per [project_maintenance.md](../replication/project_maintenance.md#results-freeze-and-tagging) (for example `results-YYYY-MM-DD`) and cite that tag in the manuscript’s reproducibility section.
3. **T-004 transition counts:** `figures/figure2_panelB_transition_counts.csv` is produced by the CPS pipeline and may not be committed in every snapshot; it feeds T-005 and memo KPIs. Main-text sentences about Figure 2 Panel B should match the CSVs and run metadata generated under the same rebuild as the cited tag, or include explicit “as of [date/tag]” language. See [replication README — Committed outputs](../replication/README.md#committed-outputs-vs-build-generated).

## Authoritative tables

- Frozen figure CSVs: `figures/*.csv` as listed in `git ls-files figures`.
- Build-generated intermediates (examples): `intermediate/ai_relevance_terciles.csv`, `intermediate/*_run_metadata.json`.

Do not hand-edit numeric claims in the manuscript without reconciling to these artifacts.
