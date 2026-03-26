from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from viz_style import STYLE, apply_matplotlib_style, save_dual
from viz_utils import TERCILE_ORDER, read_figure_csv


def _plot_tercile_lines(
    df: pd.DataFrame, x: str, y: str, title: str, stem: str
) -> str:
    fig, ax = plt.subplots(figsize=(9.8, 4.8))
    colors = {
        "low": STYLE.low_color,
        "middle": STYLE.middle_color,
        "high": STYLE.high_color,
    }
    for t in TERCILE_ORDER:
        g = df[df["ai_relevance_tercile"] == t].sort_values(x)
        ax.plot(g[x], g[y], label=t, color=colors[t], linewidth=2)
    ax.set_title(title)
    ax.set_xlabel(x.replace("_", " "))
    ax.set_ylabel(y.replace("_", " "))
    ax.legend(title="AI tercile")
    p, _ = save_dual(fig, stem)
    return p.stem


def render_t011() -> str:
    df = read_figure_csv("figureA1_asec_welfare_by_ai_tercile.csv")
    return _plot_tercile_lines(
        df,
        "year",
        "mean_annual_income",
        "Figure A1: Mean Annual Income by AI Tercile",
        "asec_mean_income",
    )


def render_t012() -> str:
    df = read_figure_csv("figureA2_sipp_event_study.csv")
    return _plot_tercile_lines(
        df,
        "event_time",
        "mean_employment_rate",
        "Figure A2: Event-Time Employment Rate",
        "sipp_event_employment",
    )


def render_t013() -> str:
    df = read_figure_csv("figureA3_cps_supp_validation.csv").copy()
    df = df.sort_values("occupational_mobility_share", ascending=True)
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.barh(
        df["ai_relevance_tercile"],
        df["occupational_mobility_share"],
        color="#6b8e23",
    )
    ax.set_title("Figure A3: Occupational Mobility Share")
    ax.set_xlabel("Share")
    ax.set_ylabel("AI tercile")
    p, _ = save_dual(fig, "cps_supp_mobility_share")
    return p.stem


def render_t014() -> str:
    df = read_figure_csv("figureA4_abs_structural_adoption.csv").copy()
    sub = (
        df.groupby("measure_label", as_index=False)["weighted_share"]
        .mean()
        .sort_values("weighted_share", ascending=True)
    )
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.barh(sub["measure_label"], sub["weighted_share"], color="#4682b4")
    ax.set_title("Figure A4: Mean Weighted Share by ABS Measure")
    ax.set_xlabel("Weighted share")
    p, _ = save_dual(fig, "abs_measure_shares")
    return p.stem


def render_t015() -> str:
    df = read_figure_csv("figureA5_ces_payroll_hours.csv").copy()
    df["month_dt"] = pd.to_datetime(
        df["month"], format="%Y-%m", errors="coerce"
    )
    sub = (
        df.groupby("month_dt", as_index=False)["payroll_index_aug2023_100"]
        .mean()
        .sort_values("month_dt")
    )
    fig, ax = plt.subplots(figsize=(9.8, 4.8))
    ax.plot(
        sub["month_dt"],
        sub["payroll_index_aug2023_100"],
        color=STYLE.high_color,
        linewidth=2,
    )
    ax.axhline(100.0, color=STYLE.neutral_color, linestyle="--", linewidth=1)
    ax.set_title("Figure A5: Mean Payroll Index Across Sectors")
    ax.set_xlabel("Month")
    ax.set_ylabel("Index")
    p, _ = save_dual(fig, "ces_payroll_index_mean")
    return p.stem


def render_t016() -> str:
    df = read_figure_csv("figureA6_bed_churn.csv").copy()
    sub = df.groupby("quarter", as_index=False)["gross_job_gains_rate"].mean()
    fig, ax = plt.subplots(figsize=(9.8, 4.8))
    ax.plot(
        sub["quarter"],
        sub["gross_job_gains_rate"],
        color=STYLE.middle_color,
        linewidth=2,
    )
    ax.set_title("Figure A6: Mean Gross Job Gains Rate")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Rate")
    ax.tick_params(axis="x", rotation=45)
    p, _ = save_dual(fig, "bed_gross_job_gains")
    return p.stem


def render_t017() -> str:
    df = read_figure_csv("figureA7_qcew_state_benchmark.csv").copy()
    sub = (
        df.groupby("state_name", as_index=False)["state_total_employment"]
        .first()
        .sort_values("state_total_employment", ascending=False)
        .head(20)
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(sub["state_name"], sub["state_total_employment"], color="#7b68ee")
    ax.set_title("Figure A7: Top 20 States by Total Employment")
    ax.set_xlabel("State")
    ax.set_ylabel("State total employment")
    ax.tick_params(axis="x", rotation=65)
    p, _ = save_dual(fig, "qcew_top20_state_employment")
    return p.stem


def render_t018() -> str:
    df = read_figure_csv("figureA8_lehd_benchmark.csv").copy()
    fig, ax = plt.subplots(figsize=(9.8, 4.8))
    ax.plot(df["quarter"], df["benchmark_rate"], color="#20b2aa", linewidth=2)
    ax.set_title("Figure A8: LEHD Benchmark Rate")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Benchmark rate")
    ax.tick_params(axis="x", rotation=45)
    p, _ = save_dual(fig, "lehd_benchmark_rate")
    return p.stem


def render_t019() -> str:
    df = read_figure_csv("figureA9_acs_local_composition.csv").copy()
    sub = (
        df.sort_values("high_ai_tercile_share", ascending=False)
        .head(30)
        .copy()
    )
    sub["puma_label"] = (
        pd.to_numeric(sub["puma"], errors="coerce")
        .fillna(0)
        .astype(int)
        .astype(str)
        .str.zfill(5)
    )
    sub = sub.sort_values("high_ai_tercile_share", ascending=True)
    fig, ax = plt.subplots(figsize=(10.8, 7.4))
    y = list(range(len(sub)))
    ax.barh(y, sub["high_ai_tercile_share"], color=STYLE.high_color)
    ax.set_title("Figure A9: Top 30 PUMAs by High-AI Share")
    ax.set_xlabel("High AI tercile share")
    ax.set_ylabel("High AI tercile share")
    ax.set_yticks(y)
    ax.set_yticklabels(sub["puma_label"], fontsize=7)
    ax.set_ylabel("PUMA")
    p, _ = save_dual(fig, "top30_puma_high_ai_share")
    return p.stem


def render_t020() -> str:
    df = read_figure_csv("figureA10_nls_longrun.csv").copy()
    fig, ax = plt.subplots(figsize=(9.8, 4.8))
    colors = {
        "low": STYLE.low_color,
        "middle": STYLE.middle_color,
        "high": STYLE.high_color,
    }
    for t in TERCILE_ORDER:
        g = df[df["baseline_ai_tercile"] == t].sort_values("survey_round")
        ax.plot(
            g["survey_round"],
            g["occupation_switch_rate"],
            label=t,
            color=colors[t],
            linewidth=2,
        )
    ax.set_title(
        "Figure A10: Occupation Switch Rate by Baseline Tercile"
    )
    ax.set_xlabel("Survey round")
    ax.set_ylabel("Occupation switch rate")
    ax.legend(title="Baseline AI tercile")
    p, _ = save_dual(fig, "nls_occupation_switch_rate")
    return p.stem


def main() -> None:
    apply_matplotlib_style()
    stems = [
        render_t011(),
        render_t012(),
        render_t013(),
        render_t014(),
        render_t015(),
        render_t016(),
        render_t017(),
        render_t018(),
        render_t019(),
        render_t020(),
    ]
    print("Wrote appendix visuals:", ", ".join(stems))


if __name__ == "__main__":
    main()
