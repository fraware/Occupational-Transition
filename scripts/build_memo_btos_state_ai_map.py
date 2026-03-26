"""
Build BTOS state AI-use latest CSV and render a tile choropleth (memo t105).

Precision summary (full detail: docs/quality/README.md#memo-visuals-t-101-to-t-108-precision-and-non-invention-rules):
- Period ID = last btos_period_id in figures/figure3_panelA_btos_ai_trends.csv
  (aligned with Figure 3 Panel A national series).
- State list = STRATA_TYPE 'state' from BTOS /strata, intersected with 50 states + DC.
- Extract only OPTION_TEXT 'AI current' + ANSWER 'Yes' (ESTIMATE_PERCENTAGE/100).
- Per state: missing_reason distinguishes fetch_failed vs no_ai_current_yes_row;
  fail closed if fewer than 45 states are published.

Run:
  python scripts/build_memo_btos_state_ai_map.py
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import matplotlib.pyplot as plt
import pandas as pd

from viz_style import apply_matplotlib_style, save_dual

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"

OUT_CSV = FIG / "memo_btos_state_ai_use_latest.csv"
OUT_META = INTER / "memo_btos_state_ai_use_latest_run_metadata.json"
STEM = "memo_btos_state_choropleth"

BTOS_API_BASE = "https://www.census.gov/hfp/btos/api"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# BTOS publishes state strata as two-letter USPS-style codes via /strata (STRATA_TYPE=state).
STATE50_DC: set[str] = {
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "DC",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
}

# Compact tile positions for state abbreviations.
STATE_TILE_POS = {
    "WA": (0, 0), "MT": (2, 0), "ND": (4, 0), "MN": (6, 0), "WI": (7, 0), "MI": (8, 0), "VT": (10, 0), "ME": (11, 0),
    "OR": (0, 1), "ID": (1, 1), "WY": (3, 1), "SD": (4, 1), "IA": (6, 1), "IL": (7, 1), "IN": (8, 1), "OH": (9, 1), "NY": (10, 1), "NH": (11, 1),
    "CA": (0, 2), "NV": (1, 2), "UT": (2, 2), "CO": (3, 2), "NE": (4, 2), "MO": (6, 2), "KY": (8, 2), "WV": (9, 2), "PA": (10, 2), "MA": (11, 2),
    "AZ": (1, 3), "NM": (2, 3), "KS": (4, 3), "AR": (6, 3), "TN": (7, 3), "VA": (9, 3), "MD": (10, 3), "NJ": (11, 3), "CT": (12, 3), "RI": (13, 3),
    "AK": (0, 4), "HI": (1, 4), "TX": (4, 4), "OK": (5, 4), "LA": (6, 4), "MS": (7, 4), "AL": (8, 4), "NC": (9, 4), "SC": (10, 4), "DE": (11, 4), "DC": (12, 4),
    "FL": (9, 5), "GA": (8, 5),
}


def _fetch_json(url: str):
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def _extract_yes_current(payload: object) -> float | None:
    if isinstance(payload, list):
        # Some endpoints return an empty list when no rows exist.
        return None
    if not isinstance(payload, dict):
        return None
    for row in payload.values():
        if (
            isinstance(row, dict)
            and row.get("OPTION_TEXT") == "AI current"
            and row.get("ANSWER") == "Yes"
            and row.get("ESTIMATE_PERCENTAGE") not in (None, "")
        ):
            return float(row["ESTIMATE_PERCENTAGE"]) / 100.0
    return None


def _ai_period_ids() -> list[int]:
    questions = _fetch_json(f"{BTOS_API_BASE}/questions")
    out: set[int] = set()
    for row in questions:
        q = str(row.get("QUESTION") or "").lower()
        if "intelligence" in q and row.get("PERIOD_ID") is not None:
            out.add(int(row["PERIOD_ID"]))
    return sorted(out)


def _state_codes_from_strata_catalog() -> list[str]:
    rows = _fetch_json(f"{BTOS_API_BASE}/strata")
    codes = sorted(
        {
            str(r.get("STRATA_VALUE"))
            for r in rows
            if str(r.get("STRATA_TYPE")) == "state" and str(r.get("STRATA_VALUE")) in STATE50_DC
        }
    )
    if len(codes) != len(STATE50_DC):
        raise RuntimeError(
            "Unexpected state strata catalog from BTOS /strata endpoint "
            f"(expected {len(STATE50_DC)} states+DC, got {len(codes)})."
        )
    return codes


def _detect_state_ai_probe_period(ai_period_ids: list[int]) -> tuple[int, str]:
    """
    Find the earliest AI period where a state stratum returns a parseable AI-current Yes rate.

    Returns (period_id, probe_state_code).
    """
    probe_state = "AL"
    for pid in ai_period_ids:
        url = f"{BTOS_API_BASE}/periods/{pid}/data/state/{probe_state}"
        try:
            payload = _fetch_json(url)
        except Exception:
            continue
        rate = _extract_yes_current(payload)
        if rate is None:
            continue
        return int(pid), probe_state
    raise RuntimeError(
        "Could not verify BTOS state-strata AI-current estimates for any AI period. "
        "No state choropleth produced."
    )


def main() -> None:
    apply_matplotlib_style()
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    pids = _ai_period_ids()
    if not pids:
        raise RuntimeError("No AI periods detected from BTOS questions endpoint.")

    trends_path = FIG / "figure3_panelA_btos_ai_trends.csv"
    if not trends_path.is_file():
        raise FileNotFoundError(
            "Missing figures/figure3_panelA_btos_ai_trends.csv. "
            "Build Figure 3 Panel A first so the memo map uses the same latest AI period."
        )
    trends = pd.read_csv(trends_path).sort_values("period_start_date")
    latest_pid = int(str(trends["btos_period_id"].iloc[-1]))

    periods = _fetch_json(f"{BTOS_API_BASE}/periods")
    period_meta = {int(p["PERIOD_ID"]): p for p in periods}
    if latest_pid not in period_meta:
        raise RuntimeError("Latest AI period missing in periods endpoint.")

    probe_pid, probe_state = _detect_state_ai_probe_period(pids)
    strata_type = "state"
    detected_probe_code = probe_state
    codes = _state_codes_from_strata_catalog()

    rows = []
    errors = []
    for code in codes:
        url = f"{BTOS_API_BASE}/periods/{latest_pid}/data/{strata_type}/{code}"
        try:
            payload = _fetch_json(url)
            rate = _extract_yes_current(payload)
        except (HTTPError, URLError, TimeoutError, OSError) as e:
            err_s = str(e)[:200]
            errors.append({"code": code, "reason": err_s})
            rows.append(
                {
                    "state_code_input": code,
                    "state_abbrev": code,
                    "ai_use_current_rate": float("nan"),
                    "missing_ai_current_rate": 1,
                    "missing_reason": "fetch_failed",
                    "btos_period_id": int(latest_pid),
                    "period_start_date": str(period_meta[latest_pid].get("COLLECTION_START", "")),
                    "strata_type": strata_type,
                }
            )
            time.sleep(0.1)
            continue
        if rate is None:
            errors.append({"code": code, "reason": "no_ai_current_yes_row"})
            rows.append(
                {
                    "state_code_input": code,
                    "state_abbrev": code,
                    "ai_use_current_rate": float("nan"),
                    "missing_ai_current_rate": 1,
                    "missing_reason": "no_ai_current_yes_row",
                    "btos_period_id": int(latest_pid),
                    "period_start_date": str(period_meta[latest_pid].get("COLLECTION_START", "")),
                    "strata_type": strata_type,
                }
            )
            time.sleep(0.1)
            continue
        rows.append(
            {
                "state_code_input": code,
                "state_abbrev": code,
                "ai_use_current_rate": float(rate),
                "missing_ai_current_rate": 0,
                "missing_reason": "published",
                "btos_period_id": int(latest_pid),
                "period_start_date": str(period_meta[latest_pid].get("COLLECTION_START", "")),
                "strata_type": strata_type,
            }
        )
        time.sleep(0.1)

    out = pd.DataFrame(rows).sort_values("state_abbrev").reset_index(drop=True)
    out_cols = [
        "state_code_input",
        "state_abbrev",
        "ai_use_current_rate",
        "missing_ai_current_rate",
        "missing_reason",
        "btos_period_id",
        "period_start_date",
        "strata_type",
    ]
    out = out[out_cols]
    if out["missing_reason"].isna().any():
        raise RuntimeError("Internal error: missing_reason must be set for every state row.")
    present = int(out["missing_ai_current_rate"].eq(0).sum())
    if present < 45:
        raise RuntimeError(
            "Too few states returned a published AI-current Yes share for this period "
            f"({present} < 45). Failing closed."
        )
    out.to_csv(OUT_CSV, index=False)

    # Tile choropleth render.
    fig, ax = plt.subplots(figsize=(12.8, 6.2))
    vals = out.set_index("state_abbrev")["ai_use_current_rate"].to_dict()
    finite = [float(v) for v in vals.values() if pd.notna(v)]
    vmin = min(finite)
    vmax = max(finite)
    cmap = plt.cm.Blues

    for abbr, (x, y) in STATE_TILE_POS.items():
        if abbr not in vals:
            continue
        v = vals[abbr]
        if pd.isna(v):
            rect = plt.Rectangle((x, y), 0.95, 0.95, facecolor="#f0f0f0", edgecolor="#bdbdbd", linewidth=1.0, linestyle="--")
            ax.add_patch(rect)
            ax.text(x + 0.475, y + 0.5, abbr, ha="center", va="center", fontsize=8, color="#333333", weight="bold")
            continue
        frac = 0.5 if vmax == vmin else (float(v) - vmin) / (vmax - vmin)
        color = cmap(frac)
        rect = plt.Rectangle((x, y), 0.95, 0.95, facecolor=color, edgecolor="white", linewidth=1.0)
        ax.add_patch(rect)
        txt_color = "white" if frac > 0.55 else "black"
        ax.text(x + 0.475, y + 0.5, abbr, ha="center", va="center", fontsize=8, color=txt_color, weight="bold")

    ax.set_xlim(-0.2, 14.3)
    ax.set_ylim(6.3, -0.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"BTOS current AI use by state (latest available period {latest_pid})")
    ax.text(
        0.0,
        6.15,
        "Grey dashed: see CSV missing_reason (fetch_failed vs no_ai_current_yes_row).",
        fontsize=8,
    )

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, fraction=0.02, pad=0.02)
    cbar.set_label("AI current use share")

    png, pdf = save_dual(fig, STEM)

    meta = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "output_png": str(png.relative_to(ROOT)).replace("\\", "/"),
        "output_pdf": str(pdf.relative_to(ROOT)).replace("\\", "/"),
        "btos_api_base": BTOS_API_BASE,
        "latest_period_id": int(latest_pid),
        "detected_state_strata_type": strata_type,
        "detected_probe_code": detected_probe_code,
        "probe_period_id_used_for_verification": int(probe_pid),
        "rows_returned": int(len(out)),
        "states_with_published_ai_current_rate": int(present),
        "dropped_or_failed_codes": errors,
        "precision_reference": "docs/quality/README.md#memo-visuals-t-101-to-t-108-precision-and-non-invention-rules",
        "missing_reason_values": ["published", "fetch_failed", "no_ai_current_yes_row"],
        "notes": (
            "State map ties period to figure3_panelA_btos_ai_trends last row; "
            "missing_reason documents why a state has no published share."
        ),
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV} ({len(out)} rows)")
    print(f"Wrote visuals: {png.name}, {pdf.name}")
    print(f"Wrote {OUT_META}")


if __name__ == "__main__":
    main()

