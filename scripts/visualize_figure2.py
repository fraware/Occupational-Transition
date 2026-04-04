"""Figure 2: hours, coarse transition heatmap, summary grid, PIL composite."""

from __future__ import annotations

import tempfile
import textwrap
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont

from viz_style import (
    PNG_DIR,
    VECTOR_DIR,
    apply_matplotlib_style,
    ensure_visual_dirs,
    save_dual,
)
from viz_utils import ROOT, parse_month_col, read_figure_csv

COMPOSITE_STEM = "figure2_redesigned_composite"

# Frozen occ22 -> tercile (Technical Note 1 ordering) if
# intermediate/ai_relevance_terciles.csv is missing.
OCC_TO_TERCILE_FALLBACK: dict[str, str] = {
    "occ22_13": "low",
    "occ22_14": "low",
    "occ22_15": "low",
    "occ22_22": "low",
    "occ22_18": "low",
    "occ22_16": "low",
    "occ22_19": "low",
    "occ22_21": "middle",
    "occ22_09": "middle",
    "occ22_20": "middle",
    "occ22_08": "middle",
    "occ22_11": "middle",
    "occ22_17": "middle",
    "occ22_06": "middle",
    "occ22_12": "high",
    "occ22_07": "high",
    "occ22_01": "high",
    "occ22_10": "high",
    "occ22_04": "high",
    "occ22_02": "high",
    "occ22_05": "high",
    "occ22_03": "high",
}

ORDER = ["low", "middle", "high"]
LABEL_MAP = {
    "low": "Low AI relevance",
    "middle": "Middle AI relevance",
    "high": "High AI relevance",
}
PRETTY = {
    "low": "Low",
    "middle": "Middle",
    "high": "High",
    "unemployed": "Unemployed",
    "nilf": "NILF",
}


def load_occ_to_tercile(root: Path) -> dict[str, str]:
    tpath = root / "intermediate" / "ai_relevance_terciles.csv"
    if not tpath.is_file():
        return dict(OCC_TO_TERCILE_FALLBACK)
    df = pd.read_csv(tpath)
    if "occ22_id" not in df.columns or "ai_relevance_tercile" not in df.columns:
        return dict(OCC_TO_TERCILE_FALLBACK)
    out: dict[str, str] = {}
    for _, row in df.iterrows():
        oid = int(row["occ22_id"])
        out[f"occ22_{oid:02d}"] = str(row["ai_relevance_tercile"]).strip().lower()
    return out


def _pil_dejavu_fonts() -> tuple[ImageFont.ImageFont, ImageFont.ImageFont]:
    try:
        path = Path(font_manager.findfont("DejaVu Sans"))
        return ImageFont.truetype(str(path), 30), ImageFont.truetype(str(path), 18)
    except OSError:
        return ImageFont.load_default(), ImageFont.load_default()


def build_hours_panel(hours: pd.DataFrame) -> plt.Figure:
    hours = hours.copy()
    hours["month"] = parse_month_col(hours, "month")

    latest_month = hours["month"].max()
    latest_hours = (
        hours.loc[
            hours["month"] == latest_month,
            ["ai_relevance_tercile", "mean_usual_weekly_hours"],
        ]
        .set_index("ai_relevance_tercile")["mean_usual_weekly_hours"]
        .to_dict()
    )
    gap_latest = latest_hours["high"] - latest_hours["low"]

    fig, ax = plt.subplots(figsize=(11.6, 5.2))
    for tercile in ORDER:
        d = hours[hours["ai_relevance_tercile"] == tercile].sort_values("month")
        ax.plot(d["month"], d["mean_usual_weekly_hours"], linewidth=2.2)

    for tercile in ORDER:
        d = hours[hours["ai_relevance_tercile"] == tercile].sort_values("month")
        x = d["month"].iloc[-1]
        y = d["mean_usual_weekly_hours"].iloc[-1]
        ax.annotate(
            f"{LABEL_MAP[tercile]}\n{y:.2f} h",
            xy=(x, y),
            xytext=(8, 0),
            textcoords="offset points",
            fontsize=10.0,
            ha="left",
            va="center",
        )

    ax.annotate(
        f"Latest high-minus-low gap: {gap_latest:.2f} hours",
        xy=(latest_month, latest_hours["high"]),
        xytext=(pd.Timestamp("2025-03-01"), latest_hours["high"] + 0.65),
        arrowprops={"arrowstyle": "->", "lw": 1.0},
        fontsize=10.2,
        ha="left",
        va="center",
    )

    ax.set_title(
        "Figure 2 Panel A: Worker-side hours by frozen AI-relevance group",
        fontsize=13.4,
        pad=10,
    )
    ax.set_ylabel("Mean usual weekly hours", fontsize=11)
    ax.set_xlabel("")
    ax.grid(True, axis="y", linewidth=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
    fig.tight_layout()
    return fig


def build_support_heatmap(
    probs: pd.DataFrame, occ_to_tercile: dict[str, str]
) -> plt.Figure:
    probs = probs.copy()
    probs["month"] = parse_month_col(probs, "month")
    latest_matrix = probs[
        (probs["record_type"] == "matrix") & (probs["month"] == probs["month"].max())
    ].copy()

    def coarse_state(x: str) -> str | None:
        if x in occ_to_tercile:
            return occ_to_tercile[x]
        if x == "unemployed":
            return "unemployed"
        if x == "nilf":
            return "nilf"
        return None

    latest_matrix["origin_coarse"] = latest_matrix["origin_state"].map(coarse_state)
    latest_matrix["destination_coarse"] = latest_matrix["destination_state"].map(
        coarse_state
    )
    latest_matrix = latest_matrix.dropna(
        subset=["origin_coarse", "destination_coarse"]
    ).copy()

    coarse = latest_matrix.groupby(
        ["origin_coarse", "destination_coarse"], as_index=False
    )["weighted_transition_count"].sum()
    coarse["row_total"] = coarse.groupby("origin_coarse")[
        "weighted_transition_count"
    ].transform("sum")
    coarse["prob"] = coarse["weighted_transition_count"] / coarse["row_total"]

    state_order = ["low", "middle", "high", "unemployed", "nilf"]
    heat = (
        coarse.pivot(
            index="origin_coarse",
            columns="destination_coarse",
            values="prob",
        )
        .reindex(index=state_order, columns=state_order)
        .fillna(0.0)
    )

    fig, ax = plt.subplots(figsize=(6.6, 5.8))
    vmax = max(float(heat.values.max()), 0.01)
    im = ax.imshow(heat.values, aspect="auto", vmin=0, vmax=max(vmax, 0.95))
    ax.set_xticks(range(len(state_order)))
    ax.set_yticks(range(len(state_order)))
    ax.set_xticklabels([PRETTY[s] for s in state_order], fontsize=10)
    ax.set_yticklabels([PRETTY[s] for s in state_order], fontsize=10)
    ax.set_title("Latest coarse-state transition matrix", fontsize=12.4, pad=10)
    ax.set_xlabel("Destination state", fontsize=10.2)
    ax.set_ylabel("Origin state", fontsize=10.2)

    for i in range(len(state_order)):
        for j in range(len(state_order)):
            ax.text(
                j,
                i,
                f"{heat.values[i, j] * 100:.1f}",
                ha="center",
                va="center",
                fontsize=9.0,
            )

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Row-normalized probability", fontsize=9.8)
    fig.tight_layout()
    return fig


def _weighted_metric_agg(summ: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (month, tercile, metric_name), g in summ.groupby(
        ["month", "tercile", "metric_name"]
    ):
        w = g["weighted_n"].astype(float)
        v = g["metric_value"].astype(float)
        if w.sum() <= 0 or v.notna().sum() == 0:
            continue
        mask = v.notna() & w.gt(0)
        if not mask.any():
            continue
        val = float(np.average(v[mask], weights=w[mask]))
        rows.append(
            {
                "month": month,
                "tercile": tercile,
                "metric_name": metric_name,
                "metric_value": val,
            }
        )
    return pd.DataFrame(rows)


def build_summary_metric_panels(
    probs: pd.DataFrame,
    occ_to_tercile: dict[str, str],
) -> tuple[Path, Path]:
    probs = probs.copy()
    probs["month"] = parse_month_col(probs, "month")
    summ = probs[probs["record_type"] == "summary"].copy()
    occ_keys = frozenset(occ_to_tercile.keys())
    summ = summ[summ["origin_state"].isin(occ_keys)].copy()
    summ["tercile"] = summ["origin_state"].map(occ_to_tercile)
    summ = summ.dropna(subset=["tercile"])
    summ["metric_value"] = pd.to_numeric(summ["metric_value"], errors="coerce")
    summ["weighted_n"] = pd.to_numeric(summ["weighted_n"], errors="coerce")
    summ = summ[summ["metric_value"].notna() & summ["weighted_n"].gt(0)]

    metric_titles = {
        "retention_rate": "Retention",
        "occ_switch_rate": "Occupation switching",
        "unemployment_entry_rate": "Entry to unemployment",
        "nilf_entry_rate": "Entry to NILF",
    }
    metric_order = [
        "retention_rate",
        "occ_switch_rate",
        "unemployment_entry_rate",
        "nilf_entry_rate",
    ]
    summ = summ[summ["metric_name"].isin(metric_order)].copy()
    agg = _weighted_metric_agg(summ)
    if agg.empty:
        raise RuntimeError("no summary metrics after aggregation")

    ensure_visual_dirs()
    out_png = PNG_DIR / "transition_summary_metrics.png"
    out_pdf = VECTOR_DIR / "transition_summary_metrics.pdf"
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        panel_paths: list[Path] = []
        for metric in metric_order:
            d = agg[agg["metric_name"] == metric].sort_values("month")
            fig, ax = plt.subplots(figsize=(5.8, 3.4))
            for tercile in ORDER:
                dd = d[d["tercile"] == tercile]
                if dd.empty:
                    continue
                ax.plot(dd["month"], dd["metric_value"] * 100, linewidth=2.0)
            for tercile in ORDER:
                dd = d[d["tercile"] == tercile]
                if dd.empty:
                    continue
                x = dd["month"].iloc[-1]
                y = dd["metric_value"].iloc[-1] * 100
                ax.annotate(
                    f"{PRETTY[tercile]}\n{y:.1f}%",
                    xy=(x, y),
                    xytext=(6, 0),
                    textcoords="offset points",
                    fontsize=8.7,
                    ha="left",
                    va="center",
                )

            ax.set_title(metric_titles[metric], fontsize=11.8, pad=8)
            ax.grid(True, axis="y", linewidth=0.45)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.set_xlabel("")
            ax.xaxis.set_major_locator(mdates.YearLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
            if metric == "retention_rate":
                ax.set_ylabel("Probability (%)", fontsize=9.8)
            else:
                ax.set_ylabel("")
            fig.tight_layout()
            path_png = td_path / f"{metric}.png"
            fig.savefig(path_png, bbox_inches="tight")
            plt.close(fig)
            panel_paths.append(path_png)

        images: list[Image.Image] = []
        for pth in panel_paths:
            with Image.open(pth) as im:
                images.append(im.convert("RGB").copy())

        w = max(im.width for im in images)
        h = max(im.height for im in images)
        gap = 26
        canvas = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
        positions = [(0, 0), (w + gap, 0), (0, h + gap), (w + gap, h + gap)]
        for im, pos in zip(images, positions, strict=True):
            canvas.paste(im, pos)

        canvas.save(out_png)
        canvas.save(out_pdf, format="PDF")

    return out_png, out_pdf


def build_composite(hours_png: Path, summary_png: Path) -> tuple[Path, Path]:
    im_a = Image.open(hours_png).convert("RGB")
    im_b = Image.open(summary_png).convert("RGB")

    margin = 56
    font_title, font_body = _pil_dejavu_fonts()
    title = (
        "Figure 2. Frozen AI-relevance groups carry real worker-side behavioral "
        "content in public CPS data"
    )
    subtitle = (
        "Panel A shows a persistent hours gradient across the low-, middle-, and "
        "high-AI-relevance terciles. Panel B summarizes broad worker-side movement "
        "using retention, occupation switching, unemployment entry, and NILF entry "
        "aggregated from the frozen coarse-state transition layer."
    )
    sub_lines = textwrap.wrap(subtitle, width=72)

    y_cursor = 28
    header_height = y_cursor + 44 + len(sub_lines) * 22 + 24

    canvas_w = max(im_a.width, im_b.width) + 2 * margin
    canvas_h = header_height + im_a.height + margin + im_b.height + margin + 40
    canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
    draw = ImageDraw.Draw(canvas)

    draw.text((margin, y_cursor), title, font=font_title, fill="black")
    y_cursor += 44
    for line in sub_lines:
        draw.text((margin, y_cursor), line, font=font_body, fill="black")
        y_cursor += 22

    canvas.paste(im_a, (margin, header_height))
    canvas.paste(im_b, (margin, header_height + im_a.height + margin))

    ensure_visual_dirs()
    out_png = PNG_DIR / f"{COMPOSITE_STEM}.png"
    out_pdf = VECTOR_DIR / f"{COMPOSITE_STEM}.pdf"
    canvas.save(out_png)
    canvas.save(out_pdf, format="PDF")
    return out_png, out_pdf


def main() -> None:
    apply_matplotlib_style()
    occ_to_tercile = load_occ_to_tercile(ROOT)

    hours = read_figure_csv("figure2_panelA_hours_by_ai_tercile.csv").copy()
    probs = read_figure_csv("figure2_panelB_transition_probs.csv").copy()

    fig_hours = build_hours_panel(hours)
    hours_png, _ = save_dual(fig_hours, "hours_timeseries")

    fig_heat = build_support_heatmap(probs, occ_to_tercile)
    save_dual(fig_heat, "transition_coarse_matrix_latest")

    summary_png, _ = build_summary_metric_panels(probs, occ_to_tercile)
    c_png, c_pdf = build_composite(Path(hours_png), summary_png)

    print(
        "Wrote figure2 visuals:",
        "hours_timeseries",
        "transition_coarse_matrix_latest",
        "transition_summary_metrics",
        c_png.name,
        c_pdf.name,
    )


if __name__ == "__main__":
    main()
