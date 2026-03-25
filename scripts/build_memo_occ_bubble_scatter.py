"""
Build figures/memo_occ_bubble_scatter.csv and render memo bubble-scatter visual.

This is a memo-friendly re-skin of Figure 1 inputs:
- Employment & wages: figures/figure1_panelA_occ_baseline.csv (T-001)
- Task z-scores: figures/figure1_panelB_task_heatmap.csv (T-002)
- Frozen terciles and AI Task Index: intermediate/ai_relevance_terciles.csv (T-002)

The x-axis uses the AI Task Index (ATI): mean of four digital-information-related
task z-scores, exactly as defined in docs/methods_data.md and implemented in T-002.

Run from repo root:
  python scripts/build_memo_occ_bubble_scatter.py
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

IN_BASELINE = FIG / "figure1_panelA_occ_baseline.csv"
IN_TASKS = FIG / "figure1_panelB_task_heatmap.csv"
IN_TERCILES = INTER / "ai_relevance_terciles.csv"

OUT_CSV = FIG / "memo_occ_bubble_scatter.csv"
OUT_META = INTER / "memo_occ_bubble_scatter_run_metadata.json"
STEM = "t104_memo_occ_bubble_scatter"

ATI_ZCOLS = [
    "z_analyzing_data_or_information",
    "z_processing_information",
    "z_documenting_recording_information",
    "z_working_with_computers",
]


def _require_cols(df: pd.DataFrame, cols: list[str], name: str) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"{name} missing required columns: {missing}")


def compute_ati_from_heatmap(tasks: pd.DataFrame) -> pd.Series:
    _require_cols(tasks, ["occupation_group"] + ATI_ZCOLS, "figure1_panelB_task_heatmap.csv")
    ati = tasks[ATI_ZCOLS].astype(float).mean(axis=1)
    return ati


def main() -> None:
    apply_matplotlib_style()
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    baseline = pd.read_csv(IN_BASELINE)
    tasks = pd.read_csv(IN_TASKS)
    terc = pd.read_csv(IN_TERCILES)

    _require_cols(
        baseline,
        ["occupation_group", "employment", "employment_share", "median_annual_wage"],
        "figure1_panelA_occ_baseline.csv",
    )
    _require_cols(terc, ["occupation_group", "ai_task_index", "ai_relevance_tercile"], "ai_relevance_terciles.csv")

    tasks = tasks.copy()
    tasks["ai_task_index_from_z"] = compute_ati_from_heatmap(tasks)

    # Join on the stable label key used by the Figure 1 CSV outputs.
    m = (
        baseline.merge(terc[["occupation_group", "ai_task_index", "ai_relevance_tercile"]], on="occupation_group", how="inner")
        .merge(tasks[["occupation_group", "ai_task_index_from_z"]], on="occupation_group", how="inner")
    )
    if len(m) != len(baseline):
        raise RuntimeError(
            "Unexpected row-count after joins. "
            f"baseline={len(baseline)} merged={len(m)}; check occupation_group keys."
        )

    # Consistency check: ATI in terciles should match mean-of-z ATI derived from heatmap columns.
    diff = (m["ai_task_index"].astype(float) - m["ai_task_index_from_z"].astype(float)).abs()
    max_diff = float(diff.max())
    if max_diff > 1e-8:
        raise RuntimeError(
            "AI Task Index mismatch between intermediate/ai_relevance_terciles.csv and "
            "mean-of-z computed from figures/figure1_panelB_task_heatmap.csv. "
            f"max_abs_diff={max_diff}"
        )

    out = m[
        [
            "occupation_group",
            "employment",
            "employment_share",
            "median_annual_wage",
            "ai_task_index",
            "ai_relevance_tercile",
        ]
    ].copy()
    out = out.sort_values(["ai_relevance_tercile", "ai_task_index", "occupation_group"]).reset_index(drop=True)
    out["ai_task_index"] = out["ai_task_index"].astype(float).round(12)

    out.to_csv(OUT_CSV, index=False)

    # Render memo bubble scatter.
    color_map = {"low": STYLE.low_color, "middle": STYLE.middle_color, "high": STYLE.high_color}
    fig, ax = plt.subplots(figsize=(9.5, 5.2))

    # Bubble size scaling: area in points^2. Use sqrt scaling to prevent domination.
    emp = out["employment"].astype(float)
    if (emp <= 0).any():
        raise ValueError("Employment must be positive for bubble sizing.")
    size = (emp / emp.max()) ** 0.5
    s = 1400.0 * size

    for tercile in ("low", "middle", "high"):
        sub = out[out["ai_relevance_tercile"] == tercile]
        ax.scatter(
            sub["ai_task_index"].astype(float),
            sub["median_annual_wage"].astype(float),
            s=s[sub.index],
            alpha=0.72,
            color=color_map[tercile],
            edgecolor="white",
            linewidth=0.6,
            label=f"{tercile.title()} AI relevance tercile",
        )

    ax.set_title("Memo: Employment size, wages, and task-based AI intensity (22 occupation groups)")
    ax.set_xlabel("AI Task Index (mean of four digital-information task z-scores)")
    ax.set_ylabel("Median annual wage (OEWS)")
    ax.legend(loc="best", frameon=True)

    # Add light annotation for interpretive boundary.
    ax.text(
        0.01,
        0.01,
        "Descriptive task-based index; not an impact estimate.",
        transform=ax.transAxes,
        fontsize=8,
        color=STYLE.neutral_color,
        va="bottom",
    )

    png, pdf = save_dual(fig, STEM)

    meta = {
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "output_png": str(png.relative_to(ROOT)).replace("\\", "/"),
        "output_pdf": str(pdf.relative_to(ROOT)).replace("\\", "/"),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "baseline": str(IN_BASELINE.relative_to(ROOT)).replace("\\", "/"),
            "tasks": str(IN_TASKS.relative_to(ROOT)).replace("\\", "/"),
            "terciles": str(IN_TERCILES.relative_to(ROOT)).replace("\\", "/"),
        },
        "ai_task_index_definition": {
            "rule": "mean of four z-scored digital-information task dimensions (T-002)",
            "z_columns": ATI_ZCOLS,
            "consistency_check_max_abs_diff_threshold": 1e-8,
        },
        "notes_limits": "Task-based index and terciles are grouping devices; not causal impacts of AI.",
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Wrote {OUT_CSV}")
    print(f"Wrote visuals: {png.name}, {pdf.name}")
    print(f"Wrote metadata: {OUT_META}")


if __name__ == "__main__":
    main()

