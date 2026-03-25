"""
Build memo CPS transition flows (latest month) and render Sankey-like chart.

Run:
  python scripts/build_memo_cps_transition_flows.py
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from viz_style import STYLE, apply_matplotlib_style, save_dual

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"

IN_TRANS = FIG / "figure2_panelB_transition_probs.csv"
IN_TERC = INTER / "ai_relevance_terciles.csv"
OUT_CSV = FIG / "memo_cps_transition_flows.csv"
OUT_META = INTER / "memo_cps_transition_flows_run_metadata.json"
STEM = "t103_memo_cps_sankey"


def _map_state_to_group(state: str, terc_map: dict[str, str]) -> str:
    s = str(state)
    if s.startswith("occ22_"):
        return terc_map.get(s, "unknown_occ")
    if s == "unemployed":
        return "unemployed"
    if s == "nilf":
        return "nilf"
    return "other"


def _map_series_to_group(s: pd.Series, terc_map: dict[str, str]) -> pd.Series:
    return s.astype(str).map(lambda x: _map_state_to_group(x, terc_map))


def main() -> None:
    apply_matplotlib_style()
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    trans = pd.read_csv(IN_TRANS)
    terc = pd.read_csv(IN_TERC)
    terc_map = {
        f"occ22_{int(r.occ22_id):02d}": str(r.ai_relevance_tercile)
        for r in terc.itertuples(index=False)
    }

    matrix = trans[trans["record_type"] == "matrix"].copy()
    latest = str(matrix["month"].max())
    m = matrix[matrix["month"] == latest].copy()
    m["origin_group"] = _map_series_to_group(m["origin_state"], terc_map)
    m["destination_group"] = _map_series_to_group(m["destination_state"], terc_map)

    keep = {"low", "middle", "high", "unemployed", "nilf"}
    m = m[m["origin_group"].isin(keep) & m["destination_group"].isin(keep)].copy()

    agg = (
        m.groupby(["month", "origin_group", "destination_group"], as_index=False)["weighted_transition_count"]
        .sum()
        .rename(columns={"weighted_transition_count": "weighted_count"})
    )
    agg["origin_mass"] = agg.groupby(["month", "origin_group"])["weighted_count"].transform("sum")
    agg["share_of_origin"] = agg["weighted_count"] / agg["origin_mass"]
    agg = agg[["month", "origin_group", "destination_group", "weighted_count", "share_of_origin"]]
    agg.to_csv(OUT_CSV, index=False)

    # Render a Sankey-like weighted flow diagram with line widths.
    order = ["low", "middle", "high", "unemployed", "nilf"]
    y_pos = {k: i for i, k in enumerate(order)}
    x0, x1 = 0.1, 0.9
    cmap = {
        "low": STYLE.low_color,
        "middle": STYLE.middle_color,
        "high": STYLE.high_color,
        "unemployed": "#8c564b",
        "nilf": "#7f7f7f",
    }
    fig, ax = plt.subplots(figsize=(10.8, 5.4))
    max_w = float(agg["weighted_count"].max())
    for r in agg.itertuples(index=False):
        lw = 0.4 + 8.0 * (float(r.weighted_count) / max_w) ** 0.5
        ax.plot(
            [x0, x1],
            [y_pos[str(r.origin_group)], y_pos[str(r.destination_group)]],
            color=cmap[str(r.origin_group)],
            alpha=0.35,
            linewidth=lw,
        )

    for k in order:
        ax.scatter([x0], [y_pos[k]], color=cmap[k], s=45)
        ax.scatter([x1], [y_pos[k]], color=cmap[k], s=45)
        ax.text(x0 - 0.02, y_pos[k], k, ha="right", va="center", fontsize=9)
        ax.text(x1 + 0.02, y_pos[k], k, ha="left", va="center", fontsize=9)

    ax.set_title(f"Memo CPS flow map (latest matched month: {latest})")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.7, len(order) - 0.3)
    ax.set_xticks([x0, x1], ["Origin group", "Destination group"])
    ax.set_yticks([])
    ax.grid(False)

    png, pdf = save_dual(fig, STEM)

    meta = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_transition_csv": str(IN_TRANS.relative_to(ROOT)).replace(
            "\\", "/"
        ),
        "input_terciles_csv": str(IN_TERC.relative_to(ROOT)).replace("\\", "/"),
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "output_png": str(png.relative_to(ROOT)).replace("\\", "/"),
        "output_pdf": str(pdf.relative_to(ROOT)).replace("\\", "/"),
        "latest_month_used": latest,
        "state_group_order": order,
        "notes_limits": "Matched-month CPS flow groups are descriptive constructs, not causal AI treatment effects.",
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote visuals: {png.name}, {pdf.name}")
    print(f"Wrote metadata: {OUT_META}")


if __name__ == "__main__":
    main()
