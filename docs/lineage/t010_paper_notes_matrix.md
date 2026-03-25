# Dataset-to-claim matrix — T-010 / Figure 5 canonical excerpt

This file is the **canonical** narrative and legend hashed for Figure 5 lineage metadata. The full research notes and extended matrix (many datasets) live in [paper_notes_full.md](../archive/paper_notes_full.md).

**Implementation:** Cell codes are frozen in `scripts/build_figure5_capability_matrix.py` (`_CAPABILITY`). The seven empirical-object columns are:

1. `worker_outcomes`
2. `worker_occupational_transitions`
3. `firm_ai_adoption`
4. `labor_demand_turnover`
5. `occupational_structure_wages`
6. `task_exposure_mechanism`
7. `worker_firm_ai_linkage` (worker–firm linked AI claims; public data do not support this directly)

## Legend

- ✓ = can directly support this claim with public data → coded **`direct`** in CSV
- △ = can support it only indirectly, partially, or with important caveats → **`partial`**
- ✗ = cannot support this claim with public data → **`none`**

## Frozen rows (five core datasets × seven empirical objects)

| Dataset | worker_outcomes | worker_occupational_transitions | firm_ai_adoption | labor_demand_turnover | occupational_structure_wages | task_exposure_mechanism | worker_firm_ai_linkage |
|---------|----------------|--------------------------------|-----------------|------------------------|------------------------------|-------------------------|-------------------------|
| CPS (basic monthly) | ✓ | ✓ | ✗ | △ | △ | ✗ | ✗ |
| BTOS | △ | ✗ | ✓ | △ | ✗ | △ | ✗ |
| JOLTS | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| OEWS | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| O*NET | ✗ | ✗ | ✗ | ✗ | △ | ✓ | ✗ |

Legend strings in `figures/figure5_capability_matrix.csv` repeat the prose definitions (check / triangle / x-mark) mapped to `direct` / `partial` / `none` in `scripts/build_figure5_capability_matrix.py`.
