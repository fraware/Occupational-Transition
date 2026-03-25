"""Render additive Virginia memo visual pack (va01-va08)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from viz_style import STYLE, apply_matplotlib_style, save_dual

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"

VA_PROFILE = FIG / "state_deep_dive_qcew_51_profile.csv"
VA_RANKS = FIG / "state_deep_dive_qcew_51_ranks.csv"
VA_PEERS = FIG / "state_deep_dive_qcew_51_peers.csv"
VA_KPIS = FIG / "virginia_memo_kpis.csv"

BTOS_STATE = FIG / "memo_btos_state_ai_use_latest.csv"
OCC_BUBBLE = FIG / "memo_occ_bubble_scatter.csv"

SECTOR_ORDER = ["HCS", "MFG", "RET", "PBS", "FAS", "INF"]


def _read_required(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"missing required input: {path}")
    return pd.read_csv(path)


def render_va01(profile: pd.DataFrame) -> str:
    d = profile.copy()
    d["sector6_code"] = pd.Categorical(
        d["sector6_code"], SECTOR_ORDER, ordered=True
    )
    d = d.sort_values("sector6_code")
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    ax.bar(d["sector6_label"], d["sector_share_pct"], color=STYLE.palette_sector)
    ax.set_title("Virginia six-sector employment composition (QCEW benchmark)")
    ax.set_xlabel("")
    ax.set_ylabel("Share (%)")
    ax.tick_params(axis="x", rotation=25)
    p, _ = save_dual(fig, "va01_virginia_sector_composition")
    return p.stem


def render_va02(profile: pd.DataFrame) -> str:
    d = profile.copy()
    d["sector6_code"] = pd.Categorical(
        d["sector6_code"], SECTOR_ORDER, ordered=True
    )
    d = d.sort_values("sector6_code")
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    ax.barh(d["sector6_label"], d["average_weekly_wage_usd"], color=STYLE.high_color)
    ax.set_title("Virginia six-sector average weekly wage")
    ax.set_xlabel("USD per week")
    ax.set_ylabel("")
    p, _ = save_dual(fig, "va02_virginia_sector_wages")
    return p.stem


def render_va03(peers: pd.DataFrame) -> str:
    d = peers.copy()
    d = d[d["sector6_code"].isin(["HCS", "MFG", "RET", "PBS"])]
    states = sorted(d["state_name"].unique())
    x = range(len(states))

    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.2), sharey=True)
    axes = axes.flatten()
    sectors = [
        ("HCS", "Health care"),
        ("MFG", "Manufacturing"),
        ("RET", "Retail"),
        ("PBS", "Professional/business"),
    ]
    for i, (code, ttl) in enumerate(sectors):
        ax = axes[i]
        s = d[d["sector6_code"] == code].set_index("state_name")
        vals = [float(s.loc[n, "sector_share_pct"]) for n in states]
        colors = [
            STYLE.high_color if n == "Virginia" else "#b0b0b0" for n in states
        ]
        ax.bar(x, vals, color=colors)
        ax.set_title(ttl)
        ax.set_xticks(x)
        ax.set_xticklabels(states, rotation=35, ha="right")
        ax.set_ylabel("Share (%)")
    fig.suptitle("Virginia vs peers: sector employment shares")
    p, _ = save_dual(fig, "va03_virginia_peers_sector_shares")
    return p.stem


def render_va04(peers: pd.DataFrame) -> str:
    d = peers.copy()
    d = d[d["sector6_code"].isin(["HCS", "MFG", "RET", "PBS"])]
    states = sorted(d["state_name"].unique())
    x = range(len(states))

    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.2), sharey=True)
    axes = axes.flatten()
    sectors = [
        ("HCS", "Health care"),
        ("MFG", "Manufacturing"),
        ("RET", "Retail"),
        ("PBS", "Professional/business"),
    ]
    for i, (code, ttl) in enumerate(sectors):
        ax = axes[i]
        s = d[d["sector6_code"] == code].set_index("state_name")
        vals = [float(s.loc[n, "average_weekly_wage"]) for n in states]
        colors = [
            STYLE.high_color if n == "Virginia" else "#b0b0b0" for n in states
        ]
        ax.bar(x, vals, color=colors)
        ax.set_title(ttl)
        ax.set_xticks(x)
        ax.set_xticklabels(states, rotation=35, ha="right")
        ax.set_ylabel("USD per week")
    fig.suptitle("Virginia vs peers: sector average weekly wages")
    p, _ = save_dual(fig, "va04_virginia_peers_sector_wages")
    return p.stem


def render_va05(ranks: pd.DataFrame) -> str:
    d = ranks.copy()
    d["sector6_code"] = pd.Categorical(
        d["sector6_code"], SECTOR_ORDER, ordered=True
    )
    d = d.sort_values("sector6_code")
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.8))
    axes[0].barh(
        d["sector6_label"], d["share_rank_desc"], color=STYLE.middle_color
    )
    axes[0].invert_xaxis()
    axes[0].set_title("Share rank (1=highest)")
    axes[0].set_xlabel("Rank")
    axes[1].barh(d["sector6_label"], d["wage_rank_desc"], color=STYLE.high_color)
    axes[1].invert_xaxis()
    axes[1].set_title("Wage rank (1=highest)")
    axes[1].set_xlabel("Rank")
    fig.suptitle("Virginia state-rank profile by sector")
    p, _ = save_dual(fig, "va05_virginia_sector_ranks")
    return p.stem


def render_va06(kpis: pd.DataFrame) -> str:
    d = kpis.copy()
    d["label_wrapped"] = d["kpi_label"].astype(str).str.slice(0, 48)
    fig, ax = plt.subplots(figsize=(11.5, 6.2))
    ax.axis("off")
    y = 0.95
    step = 0.09
    ax.text(
        0.01,
        y,
        "Virginia KPI dashboard (briefing extract)",
        fontsize=13,
        weight="bold",
        transform=ax.transAxes,
    )
    y -= 0.12
    for row in d.itertuples(index=False):
        if row.unit == "share":
            val = f"{float(row.value) * 100:.2f}%"
        elif row.unit == "percentage_points":
            val = f"{float(row.value):.2f} pp"
        elif row.unit == "usd_per_week":
            val = f"${float(row.value):,.0f}"
        else:
            val = f"{float(row.value):.2f}"
        ax.text(
            0.02,
            y,
            f"- {row.label_wrapped}: {val}",
            fontsize=10,
            transform=ax.transAxes,
        )
        y -= step
        if y < 0.06:
            break
    p, _ = save_dual(fig, "va06_virginia_kpi_dashboard")
    return p.stem


def render_va07_optional() -> str | None:
    if not BTOS_STATE.is_file():
        return None
    d = pd.read_csv(BTOS_STATE)
    d = d[pd.to_numeric(d["missing_ai_current_rate"], errors="coerce") == 0].copy()
    if d.empty or "VA" not in set(d["state_abbrev"]):
        return None
    d["ai_use_current_rate"] = pd.to_numeric(
        d["ai_use_current_rate"], errors="coerce"
    )
    d = d.sort_values("ai_use_current_rate", ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(9.2, 5.0))
    colors = [
        STYLE.high_color if s == "VA" else "#b0b0b0"
        for s in d["state_abbrev"]
    ]
    ax.bar(d["state_abbrev"], d["ai_use_current_rate"] * 100.0, color=colors)
    ax.set_title("BTOS current AI use share (top states shown; VA highlighted)")
    ax.set_xlabel("State")
    ax.set_ylabel("Share (%)")
    p, _ = save_dual(fig, "va07_virginia_btos_state_highlight")
    return p.stem


def render_va08_optional() -> str | None:
    if not OCC_BUBBLE.is_file():
        return None
    d = pd.read_csv(OCC_BUBBLE)
    d = d.sort_values("employment_share", ascending=False).head(12)
    fig, ax = plt.subplots(figsize=(10.2, 5.2))
    c = {
        "low": STYLE.low_color,
        "middle": STYLE.middle_color,
        "high": STYLE.high_color,
    }
    colors = [c.get(str(x), STYLE.neutral_color) for x in d["ai_relevance_tercile"]]
    ax.bar(d["occupation_group"], d["employment_share"] * 100.0, color=colors)
    ax.set_title("Occupation structure context (top groups by employment share)")
    ax.set_xlabel("")
    ax.set_ylabel("Employment share (%)")
    ax.tick_params(axis="x", rotation=65)
    p, _ = save_dual(fig, "va08_virginia_occ_context")
    return p.stem


def main() -> None:
    apply_matplotlib_style()
    profile = _read_required(VA_PROFILE)
    ranks = _read_required(VA_RANKS)
    peers = _read_required(VA_PEERS)
    kpis = _read_required(VA_KPIS)

    stems = [
        render_va01(profile),
        render_va02(profile),
        render_va03(peers),
        render_va04(peers),
        render_va05(ranks),
        render_va06(kpis),
    ]
    s7 = render_va07_optional()
    s8 = render_va08_optional()
    if s7:
        stems.append(s7)
    if s8:
        stems.append(s8)
    print("Wrote Virginia memo visuals:", ", ".join(stems))


if __name__ == "__main__":
    main()
