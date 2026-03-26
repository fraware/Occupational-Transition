"""
Render memo dashboard PNG/PDF from figures/memo_dashboard_kpis.csv.

Run:
  python scripts/build_memo_dashboard_png.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from viz_style import STYLE, apply_matplotlib_style, save_dual

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
STEM = "memo_dashboard"


def _fmt_value(v: float, unit: str) -> str:
    if unit == "share":
        return f"{v * 100:.1f}%"
    if unit == "hours":
        return f"{v:.2f} hrs"
    if unit == "percentage_points":
        return f"{v:.2f} p.p."
    if unit == "index_points":
        return f"{v:.2f} idx pts"
    return f"{v:.3f}"


def main() -> None:
    apply_matplotlib_style()
    df = pd.read_csv(FIG / "memo_dashboard_kpis.csv")

    n = len(df)
    ncols = 3
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(12.0, 2.9 * nrows))
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for i, ax in enumerate(axes):
        ax.axis("off")
        if i >= n:
            continue
        r = df.iloc[i]
        value = _fmt_value(float(r["value"]), str(r["unit"]))
        title = str(r["kpi_label"])
        ref = str(r["reference_period"])
        chv = r.get("change_value")
        cht = ""
        if pd.notna(chv):
            sign = "+" if float(chv) >= 0 else ""
            cu = str(r.get("change_unit") or "")
            if cu == "share":
                cht = f"\nChange ({r.get('change_window')}): {sign}{float(chv) * 100:.1f} p.p."
            else:
                cht = f"\nChange ({r.get('change_window')}): {sign}{float(chv):.3f} {cu}"
        ax.text(0.02, 0.92, title, va="top", ha="left", fontsize=10, weight="bold")
        ax.text(0.02, 0.58, value, va="top", ha="left", fontsize=16, color=STYLE.high_color, weight="bold")
        ax.text(0.02, 0.30, f"Reference: {ref}{cht}", va="top", ha="left", fontsize=8, color=STYLE.neutral_color)
        ax.text(
            0.02,
            0.06,
            "Descriptive monitoring metric; not causal attribution.",
            va="bottom",
            ha="left",
            fontsize=7,
            color=STYLE.neutral_color,
        )

    fig.suptitle("What we can measure now (public federal data dashboard)", y=0.995, fontsize=12)
    p1, _ = save_dual(fig, STEM)
    print(f"Wrote visuals: {p1.name}")


if __name__ == "__main__":
    main()

