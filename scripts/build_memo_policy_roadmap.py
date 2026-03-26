"""
Build and render memo policy roadmap schematic.

Run:
  python scripts/build_memo_policy_roadmap.py
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
OUT_CSV = FIG / "memo_policy_roadmap.csv"
OUT_META = INTER / "memo_policy_roadmap_run_metadata.json"
STEM = "memo_policy_roadmap"


def main() -> None:
    apply_matplotlib_style()
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    rows = [
        {
            "effort_tier": "low",
            "instrument": "BTOS",
            "proposed_addition": "Add 1-2 questions on share of workers affected and broad role location",
            "unlocks": "Better bridge from business adoption to worker-side outcomes",
            "key_boundary": "Still no worker-firm linked microdata in public release",
        },
        {
            "effort_tier": "low",
            "instrument": "CPS",
            "proposed_addition": "Short AI-use module in supplement format",
            "unlocks": "Worker-reported AI use, task change, hours/pay/training by occupation",
            "key_boundary": "Survey self-report and matched-month design limits",
        },
        {
            "effort_tier": "medium",
            "instrument": "JOLTS",
            "proposed_addition": "Rotating supplement with coarse occupation groups + wage bands",
            "unlocks": "Demand-side openings/hires/quits/layoffs by coarse occupation bins",
            "key_boundary": "Do not overload monthly core; sample constraints remain binding",
        },
        {
            "effort_tier": "medium",
            "instrument": "NLS",
            "proposed_addition": "Longitudinal AI items in planned cohorts",
            "unlocks": "Career-path adaptation and long-run mobility measurement",
            "key_boundary": "Not a near-real-time monitoring instrument",
        },
        {
            "effort_tier": "large",
            "instrument": "Linked admin ideal",
            "proposed_addition": "Worker-job-quarter occupation transitions linked to employer AI adoption",
            "unlocks": "Closest public infrastructure to causal worker-firm attribution",
            "key_boundary": "High legal, operational, and governance burden",
        },
    ]
    out = pd.DataFrame(rows)
    out.to_csv(OUT_CSV, index=False)

    tier_order = ["low", "medium", "large"]
    tier_x = {"low": 0, "medium": 1, "large": 2}
    colors = {"low": "#2ca02c", "medium": "#ff7f0e", "large": "#d62728"}

    fig, ax = plt.subplots(figsize=(12.2, 5.8))
    y = {"low": 4.3, "medium": 2.8, "large": 1.2}
    for tier in tier_order:
        ax.text(tier_x[tier], 5.2, tier.upper(), ha="center", va="center", fontsize=11, weight="bold", color=colors[tier])
    for i, r in out.iterrows():
        x = tier_x[r["effort_tier"]]
        yy = y[r["effort_tier"]] - 0.65 * (i % 2 if r["effort_tier"] != "large" else 0)
        ax.scatter([x], [yy], s=130, color=colors[r["effort_tier"]], alpha=0.85)
        ax.text(x + 0.06, yy + 0.08, f"{r['instrument']}: {r['proposed_addition']}", fontsize=8, va="bottom")
        ax.text(x + 0.06, yy - 0.08, f"Unlock: {r['unlocks']}", fontsize=8, va="top")

    ax.set_xlim(-0.25, 2.65)
    ax.set_ylim(0.4, 5.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    ax.set_title("Policy roadmap: effort tier and measurement unlocks")
    ax.text(0.0, 0.5, "All unlocks are measurement capabilities, not causal effect claims.", fontsize=8)

    png, pdf = save_dual(fig, STEM)

    meta = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "output_png": str(png.relative_to(ROOT)).replace("\\", "/"),
        "output_pdf": str(pdf.relative_to(ROOT)).replace("\\", "/"),
        "source_texts": ["docs/archive/paper_notes_full.md", "docs/paper/methods_data.md"],
        "note": "Structured schematic consistent with policy-design section; non-estimated.",
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote visuals: {png.name}, {pdf.name}")


if __name__ == "__main__":
    main()

