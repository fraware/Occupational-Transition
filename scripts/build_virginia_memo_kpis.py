"""
Build Virginia memo KPI table (additive, state-brief specific).

Inputs:
- figures/state_deep_dive_qcew_51_profile.csv
- figures/state_deep_dive_qcew_51_ranks.csv
- figures/state_deep_dive_qcew_51_peers.csv
- figures/memo_btos_state_ai_use_latest.csv (optional)

Outputs:
- figures/virginia_memo_kpis.csv
- intermediate/virginia_memo_kpis_run_metadata.json
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"

VA_FIPS = "51"
PROFILE = FIG / f"state_deep_dive_qcew_{VA_FIPS}_profile.csv"
RANKS = FIG / f"state_deep_dive_qcew_{VA_FIPS}_ranks.csv"
PEERS = FIG / f"state_deep_dive_qcew_{VA_FIPS}_peers.csv"
BTOS_STATE = FIG / "memo_btos_state_ai_use_latest.csv"

OUT_CSV = FIG / "virginia_memo_kpis.csv"
OUT_META = INTER / "virginia_memo_kpis_run_metadata.json"


def _kpi_row(
    kpi_id: str,
    kpi_label: str,
    value: float,
    unit: str,
    reference_period: str,
    source_path_or_endpoint: str,
    notes_limits: str,
) -> dict[str, object]:
    return {
        "kpi_id": kpi_id,
        "kpi_label": kpi_label,
        "value": float(value),
        "unit": unit,
        "reference_period": reference_period,
        "source_path_or_endpoint": source_path_or_endpoint,
        "notes_limits": notes_limits,
    }


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    for p in [PROFILE, RANKS, PEERS]:
        if not p.is_file():
            raise FileNotFoundError(
                f"missing required Virginia deep-dive input: {p}. "
                "Run scripts/build_state_qcew_deep_dive.py first."
            )

    profile = pd.read_csv(PROFILE, dtype={"state_fips": str})
    ranks = pd.read_csv(RANKS, dtype={"state_fips": str})
    peers = pd.read_csv(PEERS, dtype={"state_fips": str})

    y = int(profile["qcew_year"].iloc[0])
    q = int(profile["qcew_quarter"].iloc[0])
    period = f"{y} Q{q}"

    rows: list[dict[str, object]] = []
    hcs_share = float(
        profile.loc[
            profile["sector6_code"] == "HCS", "state_sector_employment_share"
        ].iloc[0]
    )
    mfg_share = float(
        profile.loc[
            profile["sector6_code"] == "MFG", "state_sector_employment_share"
        ].iloc[0]
    )
    ret_share = float(
        profile.loc[
            profile["sector6_code"] == "RET", "state_sector_employment_share"
        ].iloc[0]
    )
    inf_wage = float(
        profile.loc[profile["sector6_code"] == "INF", "average_weekly_wage"].iloc[0]
    )
    rows.extend(
        [
            _kpi_row(
                "va_hcs_share",
                "Virginia HCS employment share (six-sector denominator)",
                hcs_share,
                "share",
                period,
                str(PROFILE.relative_to(ROOT)).replace("\\", "/"),
                "QCEW structural benchmark; descriptive only.",
            ),
            _kpi_row(
                "va_mfg_share",
                (
                    "Virginia manufacturing employment share "
                    "(six-sector denominator)"
                ),
                mfg_share,
                "share",
                period,
                str(PROFILE.relative_to(ROOT)).replace("\\", "/"),
                "QCEW structural benchmark; descriptive only.",
            ),
            _kpi_row(
                "va_ret_share",
                "Virginia retail employment share (six-sector denominator)",
                ret_share,
                "share",
                period,
                str(PROFILE.relative_to(ROOT)).replace("\\", "/"),
                "QCEW structural benchmark; descriptive only.",
            ),
            _kpi_row(
                "va_inf_avg_weekly_wage",
                "Virginia information sector average weekly wage",
                inf_wage,
                "usd_per_week",
                period,
                str(PROFILE.relative_to(ROOT)).replace("\\", "/"),
                "Published QCEW wage aggregate in retained benchmark frame.",
            ),
        ]
    )

    ret_rank = float(
        ranks.loc[ranks["sector6_code"] == "RET", "share_rank_desc"].iloc[0]
    )
    mfg_rank = float(
        ranks.loc[ranks["sector6_code"] == "MFG", "share_rank_desc"].iloc[0]
    )
    fas_wage_rank = float(
        ranks.loc[ranks["sector6_code"] == "FAS", "wage_rank_desc"].iloc[0]
    )
    rows.extend(
        [
            _kpi_row(
                "va_ret_share_rank",
                "Virginia retail share rank (1=highest)",
                ret_rank,
                "rank",
                period,
                str(RANKS.relative_to(ROOT)).replace("\\", "/"),
                "Rank among states in retained T-017 benchmark output.",
            ),
            _kpi_row(
                "va_mfg_share_rank",
                "Virginia manufacturing share rank (1=highest)",
                mfg_rank,
                "rank",
                period,
                str(RANKS.relative_to(ROOT)).replace("\\", "/"),
                "Rank among states in retained T-017 benchmark output.",
            ),
            _kpi_row(
                "va_fas_wage_rank",
                "Virginia financial activities wage rank (1=highest)",
                fas_wage_rank,
                "rank",
                period,
                str(RANKS.relative_to(ROOT)).replace("\\", "/"),
                "Rank among states in retained T-017 benchmark output.",
            ),
        ]
    )

    hcs_peer = peers[peers["sector6_code"] == "HCS"].copy()
    va_hcs = float(
        hcs_peer.loc[
            hcs_peer["state_fips"].str.zfill(2) == VA_FIPS, "sector_share_pct"
        ].iloc[0]
    )
    peer_mean_hcs = float(
        hcs_peer.loc[
            hcs_peer["state_fips"].str.zfill(2) != VA_FIPS, "sector_share_pct"
        ].mean()
    )
    rows.append(
        _kpi_row(
            "va_hcs_share_minus_peer_mean_pp",
            "Virginia HCS share minus peer mean",
            va_hcs - peer_mean_hcs,
            "percentage_points",
            period,
            str(PEERS.relative_to(ROOT)).replace("\\", "/"),
            "Peer set is DC, KY, MD, NC, TN, WV plus Virginia.",
        )
    )

    btos_used = False
    if BTOS_STATE.is_file():
        btos = pd.read_csv(BTOS_STATE)
        va_row = btos[btos["state_abbrev"] == "VA"]
        if (
            not va_row.empty
            and int(va_row["missing_ai_current_rate"].iloc[0]) == 0
        ):
            rate = float(va_row["ai_use_current_rate"].iloc[0])
            pid = str(va_row["btos_period_id"].iloc[0])
            rows.append(
                _kpi_row(
                    "va_btos_current_ai_use_rate",
                    "Virginia BTOS current AI use share",
                    rate,
                    "share",
                    f"BTOS period {pid}",
                    str(BTOS_STATE.relative_to(ROOT)).replace("\\", "/"),
                    "Business-reported adoption share; descriptive only.",
                )
            )
            btos_used = True

    out = pd.DataFrame(rows)
    out.to_csv(OUT_CSV, index=False)

    meta = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "inputs": {
            "profile": str(PROFILE.relative_to(ROOT)).replace("\\", "/"),
            "ranks": str(RANKS.relative_to(ROOT)).replace("\\", "/"),
            "peers": str(PEERS.relative_to(ROOT)).replace("\\", "/"),
            "btos_state_optional": str(BTOS_STATE.relative_to(ROOT)).replace(
                "\\", "/"
            ),
        },
        "state_fips": VA_FIPS,
        "retained_period": period,
        "row_count": int(len(out)),
        "btos_kpi_included": btos_used,
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Wrote {OUT_CSV} ({len(out)} rows)")
    print(f"Wrote {OUT_META}")


if __name__ == "__main__":
    main()
