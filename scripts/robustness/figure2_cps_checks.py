"""
Figure 2 robustness: summary-metric stability over time; row-normalization spot check.

Reads `figures/figure2_panelB_transition_probs.csv` and optionally counts metadata.
Writes `intermediate/robustness/figure2_cps_checks.md`.

Run from repo root:
    python scripts/robustness/figure2_cps_checks.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))

from _report import write_report  # noqa: E402

PROBS = ROOT / "figures" / "figure2_panelB_transition_probs.csv"
COUNTS_META = ROOT / "intermediate" / "figure2_panelB_counts_run_metadata.json"


def main() -> int:
    if not PROBS.is_file():
        write_report(
            "figure2_cps_checks.md",
            f"SKIP: missing {PROBS}",
        )
        print("SKIP: missing transition probs")
        return 0

    df = pd.read_csv(PROBS)
    mat = df[df["record_type"] == "matrix"].copy()
    if mat.empty:
        write_report("figure2_cps_checks.md", "FAIL: no matrix rows")
        return 1

    chk = (
        mat.groupby(["month", "origin_state"], sort=False)["transition_probability"]
        .sum()
        .sub(1.0)
        .abs()
    )
    max_dev = float(chk.max())

    summ = df[df["record_type"] == "summary"].copy()
    lines = [
        "## Row-normalization check (matrix rows)",
        f"- Max |sum(p)-1| over month x origin: {max_dev:.2e}",
        "",
        "## Summary metric range (national origins, illustrative)",
    ]
    if not summ.empty:
        # One occupation group: first occ22_* origin in sorted order
        occ_origins = sorted(
            {x for x in summ["origin_state"].astype(str) if x.startswith("occ22_")}
        )
        if occ_origins:
            o0 = occ_origins[0]
            sub = summ[summ["origin_state"] == o0]
            for mname in ["retention_rate", "occ_switch_rate"]:
                ssub = sub[sub["metric_name"] == mname]
                if ssub.empty:
                    continue
                months = pd.to_datetime(ssub["month"], errors="coerce")
                vals = ssub["metric_value"].astype(float)
                first = vals.iloc[0]
                last = vals.iloc[-1]
                spread = float(vals.max() - vals.min())
                lines.append(
                    f"- `{o0}` {mname}: first={first:.4f}, last={last:.4f}, "
                    f"range across months={spread:.4f}"
                )
        lines.append(
            "- Interpretation: large ranges flag time-varying transition hazards; "
            "they are not themselves errors."
        )
    else:
        lines.append("- No summary rows found.")

    lines.extend(["", "## Counts metadata (if present)"])
    if COUNTS_META.is_file():
        meta = json.loads(COUNTS_META.read_text(encoding="utf-8"))
        lines.append(f"- Keys present: {sorted(meta.keys())[:12]}...")
        if "row_count" in meta:
            lines.append(f"- `row_count`: {meta['row_count']}")
    else:
        lines.append(f"- Missing `{COUNTS_META.name}`")

    write_report("figure2_cps_checks.md", "\n".join(lines))
    print("Wrote intermediate/robustness/figure2_cps_checks.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
