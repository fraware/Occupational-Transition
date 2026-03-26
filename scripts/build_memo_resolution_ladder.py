"""
Build and render memo resolution-boundary ladder schematic.

Run:
  python scripts/build_memo_resolution_ladder.py
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from viz_style import apply_matplotlib_style, save_dual

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
OUT_CSV = FIG / "memo_resolution_ladder.csv"
OUT_META = INTER / "memo_resolution_ladder_run_metadata.json"
STEM = "memo_resolution_ladder"


def main() -> None:
    apply_matplotlib_style()
    rows = [
        {
            "level": 1,
            "resolution_label": "National x broad occupation groups",
            "strength_label": "strong",
            "evidence_basis": "CPS matched-month broad-group transitions and hours by frozen AI terciles",
        },
        {
            "level": 2,
            "resolution_label": "National x sector groups x monthly",
            "strength_label": "strong",
            "evidence_basis": "BTOS national/sector series + JOLTS/CES sector context",
        },
        {
            "level": 3,
            "resolution_label": "State x sector/industry aggregates",
            "strength_label": "partial",
            "evidence_basis": "Published subnational aggregates with model/coverage limits",
        },
        {
            "level": 4,
            "resolution_label": "State x occupation x month",
            "strength_label": "weak",
            "evidence_basis": "Public sample sufficiency constraints and no worker-firm linked public panel",
        },
    ]
    out = pd.DataFrame(rows)
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)

    color = {"strong": "#2ca02c", "partial": "#ff7f0e", "weak": "#d62728"}
    fig, ax = plt.subplots(figsize=(10.6, 4.8))
    for i, r in out.iterrows():
        y = len(out) - 1 - i
        ax.barh(y, 1.0, color=color[r["strength_label"]], alpha=0.75)
        ax.text(0.02, y, f"{r['resolution_label']}  [{r['strength_label']}]", va="center", ha="left", color="white", fontsize=9, weight="bold")
        ax.text(1.02, y, str(r["evidence_basis"]), va="center", ha="left", fontsize=8)
    ax.axhline(0.5, color="black", linestyle="--", linewidth=1.0)
    ax.text(0.0, 0.62, "Inference boundary: below this line, precision weakens materially.", fontsize=8)
    ax.set_xlim(0, 2.2)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title("How far public AI-and-labor measurement can credibly zoom")
    ax.grid(False)

    png, pdf = save_dual(fig, STEM)
    meta = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "output_png": str(png.relative_to(ROOT)).replace("\\", "/"),
        "output_pdf": str(pdf.relative_to(ROOT)).replace("\\", "/"),
        "source_texts": ["docs/paper/methods_data.md", "docs/archive/paper_notes_full.md"],
        "note": "Schematic only; no estimated statistics in this figure.",
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote visuals: {png.name}, {pdf.name}")


if __name__ == "__main__":
    main()

