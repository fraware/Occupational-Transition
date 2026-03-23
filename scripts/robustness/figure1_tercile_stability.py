"""
Figure 1 robustness: compare AI terciles under alternative z-score aggregations.

Uses only existing pipeline outputs (heatmap CSV and terciles CSV). Writes
`intermediate/robustness/figure1_tercile_stability.md`.

Run from repo root:
    python scripts/robustness/figure1_tercile_stability.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))

from _report import write_report  # noqa: E402

HEAT = ROOT / "figures" / "figure1_panelB_task_heatmap.csv"
TERC = ROOT / "intermediate" / "ai_relevance_terciles.csv"

DIGITAL_SLUGS = [
    "z_analyzing_data_or_information",
    "z_processing_information",
    "z_documenting_recording_information",
    "z_working_with_computers",
]
PHYSICAL_SLUGS = [
    "z_assisting_and_caring_for_others",
    "z_handling_and_moving_objects",
]


def tercile_series(occ22_id: pd.Series, idx: pd.Series) -> pd.Series:
    """Same 7/7/8 split as T-002 on sorted (index, occ22_id)."""
    df = pd.DataFrame({"occ22_id": occ22_id, "idx": idx})
    d = df.sort_values(["idx", "occ22_id"]).reset_index(drop=True)
    labels = np.empty(len(d), dtype=object)
    labels[0:7] = "low"
    labels[7:14] = "middle"
    labels[14:22] = "high"
    return pd.Series(labels, index=d["occ22_id"])


def main() -> int:
    if not HEAT.is_file() or not TERC.is_file():
        write_report(
            "figure1_tercile_stability.md",
            "SKIP: required inputs missing:\n"
            f"- {HEAT}\n"
            f"- {TERC}\n",
        )
        print("SKIP: missing figure1 inputs")
        return 0

    hm = pd.read_csv(HEAT).sort_values("occ22_id")
    tr = pd.read_csv(TERC)

    missing = [c for c in DIGITAL_SLUGS + PHYSICAL_SLUGS if c not in hm.columns]
    if missing:
        write_report(
            "figure1_tercile_stability.md",
            f"FAIL: missing columns in heatmap: {missing}",
        )
        return 1

    prod = tr.set_index("occ22_id")["ai_relevance_tercile"]

    dig = hm[DIGITAL_SLUGS].mean(axis=1)
    allsix = hm[DIGITAL_SLUGS + PHYSICAL_SLUGS].mean(axis=1)
    phys = hm[PHYSICAL_SLUGS].mean(axis=1)
    occ = hm["occ22_id"]

    t_d4 = tercile_series(occ, dig)
    t_a6 = tercile_series(occ, allsix)
    t_p2 = tercile_series(occ, phys)

    def agree(mask: pd.Series) -> float:
        a = prod.reindex(mask.index)
        return float((a.values == mask.values).mean())

    r1 = dig.corr(allsix, method="spearman")
    r2 = dig.corr(phys, method="spearman")

    lines = [
        "## Inputs",
        f"- `{HEAT.relative_to(ROOT)}`",
        f"- `{TERC.relative_to(ROOT)}`",
        "",
        "## Spearman rank correlations (22 occupation groups)",
        f"- digital-mean-4 vs all-6 z-means: {r1:.4f}",
        f"- digital-mean-4 vs physical-mean-2: {r2:.4f}",
        "",
        "## Tercile agreement with production `ai_relevance_terciles`",
        f"- digital-mean-4 rule vs production: {agree(t_d4):.2%}",
        f"- all-6 z-means rule vs production: {agree(t_a6):.2%}",
        f"- physical-mean-2 rule vs production: {agree(t_p2):.2%}",
        "",
        "## Interpretation",
        "Digital-mean-4 should match production if the pipeline index equals "
        "the mean of the four digital z-scores. All-6 and physical-only rules "
        "probe sensitivity to expanding or changing the task set.",
    ]
    write_report("figure1_tercile_stability.md", "\n".join(lines))
    print("Wrote intermediate/robustness/figure1_tercile_stability.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
