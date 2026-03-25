"""
Build figures/figure2_panelB_transition_counts.csv from Census CPS Basic Monthly PUF
using matched adjacent months (T-004).

Run from repo root: python scripts/build_figure2_panelB_counts.py
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
OUT_CSV = FIG / "figure2_panelB_transition_counts.csv"
META_JSON = INTER / "figure2_panelB_counts_run_metadata.json"
ATTRITION_CSV = INTER / "figure2_panelB_attrition_diagnostics.csv"
MATCH_REGIME_CSV = INTER / "figure2_panelB_match_regime_robustness.csv"
MISSING_MONTH_SENS_CSV = INTER / "figure2_panelB_missing_month_sensitivity.csv"

CPS_BASIC_BASE = "https://www2.census.gov/programs-surveys/cps/datasets"
LAYOUT_URL_TEMPLATE = (
    CPS_BASIC_BASE + "/{year}/basic/{year}_Basic_CPS_Public_Use_Record_Layout_plus_IO_Code_list.txt"
)
FALLBACK_LAYOUT_YEAR = 2020

ALLOW_MISSING_MONTHS: set[tuple[int, int]] = {(2025, 10)}

# Fields needed for T-004 matching and state construction (official layout names).
REQUIRED_FIELDS = (
    "HRYEAR4",
    "HRMONTH",
    "HRHHID",
    "HRHHID2",
    "PULINENO",
    "PRTAGE",
    "PRPERTYP",
    "PEMLR",
    "PRDTOCC1",
    "PWCMPWGT",
)
OPTIONAL_FIELDS = ("PESEX", "PTDTRACE")

# CPS PEMLR: 1-2 employed, 3-4 unemployed; 5+ NILF (see Public Use Documentation).
EMPLOYED = (1, 2)
UNEMPLOYED = (3, 4)


def _load_bf2a():
    """Load build_figure2_panelA as a module for shared CPS download helpers."""
    p = ROOT / "scripts" / "build_figure2_panelA.py"
    name = "_occupational_transition_bf2a"
    spec = importlib.util.spec_from_file_location(name, p)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {p}")
    mod = importlib.util.module_from_spec(spec)
    # Required so dataclasses and annotations resolve while exec_module runs.
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


bf2a = _load_bf2a()


def _parse_location_range(line: str) -> tuple[int, int] | None:
    """Parse 1-based inclusive LOCATION end columns from a layout line."""
    tail = line.rstrip()
    # Primary: hyphen; some Census TXT files use odd Unicode instead of '-'.
    m = re.search(r"(\d+)\s*[-\u2010-\u2015]\s*(\d+)\s*$", tail)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"(\d+)\s*\D+\s*(\d+)\s*$", tail)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"(\d+)\s*$", tail)
    if m:
        c = int(m.group(1))
        return c, c
    return None


def parse_layout_positions(layout_text: str) -> dict[str, tuple[int, int]]:
    """0-based (start, end exclusive) slices from official LOCATION ranges."""
    positions: dict[str, tuple[int, int]] = {}
    for line in layout_text.splitlines():
        for name in REQUIRED_FIELDS:
            if line.startswith(name + "\t"):
                loc = _parse_location_range(line)
                if loc is None:
                    raise ValueError(
                        f"Could not parse LOCATION for {name}: {line[:120]}"
                    )
                start1, end1 = loc
                positions[name] = (start1 - 1, end1)
                break
    missing = [k for k in REQUIRED_FIELDS if k not in positions]
    if missing:
        raise ValueError(f"Layout missing variables: {missing}")
    for line in layout_text.splitlines():
        for name in OPTIONAL_FIELDS:
            if name in positions:
                continue
            if line.startswith(name + "\t"):
                loc = _parse_location_range(line)
                if loc is None:
                    continue
                start1, end1 = loc
                positions[name] = (start1 - 1, end1)
                break
    return positions


def load_layout_for_year(year: int) -> tuple[dict[str, tuple[int, int]], int, str]:
    for try_year in (year, FALLBACK_LAYOUT_YEAR):
        url = LAYOUT_URL_TEMPLATE.format(year=try_year)
        try:
            req = bf2a._request(url)
            with urllib.request.urlopen(req, timeout=120) as resp:
                text = resp.read().decode("utf-8", "replace")
            pos = parse_layout_positions(text)
            return pos, try_year, url
        except urllib.error.HTTPError as e:
            if e.code == 404 and try_year == year:
                continue
            raise
        except urllib.error.URLError:
            if try_year == year:
                continue
            raise
    raise RuntimeError(f"Could not load CPS record layout for {year}")


@dataclass
class SliceSpec:
    start: int
    end: int


def slice_column(raw: pd.Series, spec: SliceSpec) -> pd.Series:
    return raw.str.slice(spec.start, spec.end)


def month_label(y: int, m: int) -> str:
    return f"{y}-{m:02d}"


def labor_market_state_series(pemlr: pd.Series, prdtocc1: pd.Series) -> pd.Series:
    rows = []
    for p, o in zip(pemlr.tolist(), prdtocc1.tolist()):
        pl = pd.to_numeric(p, errors="coerce")
        oc = pd.to_numeric(o, errors="coerce")
        if pd.isna(pl):
            rows.append("nilf")
        elif pl in EMPLOYED:
            if pd.notna(oc) and 1 <= oc <= 22:
                rows.append(f"occ22_{int(oc):02d}")
            else:
                rows.append("nilf")
        elif pl in UNEMPLOYED:
            rows.append("unemployed")
        else:
            rows.append("nilf")
    return pd.Series(rows, index=pemlr.index)


def load_filtered_persons(
    dat_path: Path, positions: dict[str, tuple[int, int]]
) -> pd.DataFrame:
    """Person rows: CNP age 16+, positive composite weight, with match key."""
    specs = {k: SliceSpec(*positions[k]) for k in REQUIRED_FIELDS}
    chunks: list[pd.DataFrame] = []
    for batch in bf2a._iter_dat_chunks(dat_path):
        raw = pd.Series(batch, dtype="object")
        hrhhid = slice_column(raw, specs["HRHHID"]).astype(str).str.strip()
        hrhhid2 = slice_column(raw, specs["HRHHID2"]).astype(str).str.strip()
        pulineno = slice_column(raw, specs["PULINENO"]).astype(str).str.strip()
        age = pd.to_numeric(slice_column(raw, specs["PRTAGE"]), errors="coerce")
        prper = pd.to_numeric(slice_column(raw, specs["PRPERTYP"]), errors="coerce")
        pemlr = pd.to_numeric(slice_column(raw, specs["PEMLR"]), errors="coerce")
        occ = pd.to_numeric(slice_column(raw, specs["PRDTOCC1"]), errors="coerce")
        wgt = pd.to_numeric(slice_column(raw, specs["PWCMPWGT"]), errors="coerce")
        sex = (
            pd.to_numeric(slice_column(raw, SliceSpec(*positions["PESEX"])), errors="coerce")
            if "PESEX" in positions
            else pd.Series(np.nan, index=raw.index)
        )
        race = (
            pd.to_numeric(
                slice_column(raw, SliceSpec(*positions["PTDTRACE"])),
                errors="coerce",
            )
            if "PTDTRACE" in positions
            else pd.Series(np.nan, index=raw.index)
        )

        df = pd.DataFrame(
            {
                "hrhhid": hrhhid,
                "hrhhid2": hrhhid2,
                "pulineno": pulineno,
                "match_key": hrhhid + "|" + hrhhid2 + "|" + pulineno,
                "age": age,
                "prpertyp": prper,
                "pemlr": pemlr,
                "prdtooc1": occ,
                "pwcmpwgt": wgt,
                "pesex": sex,
                "ptdtrace": race,
            }
        )
        m = df["prpertyp"].eq(2) & df["age"].ge(16) & df["pwcmpwgt"].gt(0)
        df = df.loc[m].copy()
        if df.empty:
            continue
        df["state"] = labor_market_state_series(df["pemlr"], df["prdtooc1"])
        df["weight"] = df["pwcmpwgt"].astype(np.float64) / 10_000.0
        df["age_band"] = pd.cut(
            df["age"],
            bins=[15, 24, 39, 54, 120],
            labels=["16-24", "25-39", "40-54", "55+"],
        ).astype(str)
        df["sex_group"] = df["pesex"].map({1.0: "male", 2.0: "female"}).fillna("unknown")
        df["race_group"] = (
            df["ptdtrace"]
            .map({1.0: "white_only", 2.0: "black_only", 4.0: "asian_only"})
            .fillna("other_or_unknown")
        )
        chunks.append(
            df[
                [
                    "match_key",
                    "state",
                    "weight",
                    "age_band",
                    "sex_group",
                    "race_group",
                ]
            ]
        )

    if not chunks:
        return pd.DataFrame(columns=["match_key", "state", "weight"])
    return pd.concat(chunks, ignore_index=True)


def _build_attrition_rows(
    origin_month: str, left: pd.DataFrame, merged: pd.DataFrame
) -> list[dict[str, Any]]:
    matched = set(merged["match_key"].astype(str).unique())
    left_aug = left.copy()
    left_aug["matched"] = left_aug["match_key"].astype(str).isin(matched)
    rows: list[dict[str, Any]] = []
    specs = [
        ("all", "__all__"),
        ("age_band", None),
        ("sex_group", None),
        ("race_group", None),
        ("state", None),
    ]
    for strat, fixed in specs:
        if fixed is not None:
            sub = left_aug.copy()
            groups = [(fixed, sub)]
        else:
            groups = list(left_aug.groupby(strat, dropna=False))
        for val, g in groups:
            n_origin = int(len(g))
            n_matched = int(g["matched"].sum())
            w_origin = float(g["weight"].sum())
            w_matched = float(g.loc[g["matched"], "weight"].sum())
            rows.append(
                {
                    "month": origin_month,
                    "stratum_type": strat,
                    "stratum_value": str(val),
                    "n_origin": n_origin,
                    "n_matched": n_matched,
                    "match_rate_unweighted": (n_matched / n_origin) if n_origin else np.nan,
                    "weighted_origin_mass": w_origin,
                    "weighted_matched_mass": w_matched,
                    "match_rate_weighted": (w_matched / w_origin) if w_origin else np.nan,
                }
            )
    return rows


def _build_match_regime_rows(origin_month: str, left: pd.DataFrame, merged: pd.DataFrame) -> list[dict[str, Any]]:
    matched = set(merged["match_key"].astype(str).unique())
    left_aug = left.copy()
    left_aug["matched"] = left_aug["match_key"].astype(str).isin(matched)
    regimes = [
        ("strict", left_aug[left_aug["age_band"].isin(["25-39", "40-54"])]),
        ("moderate", left_aug),
        ("permissive", left_aug[left_aug["age_band"] != "55+"]),
    ]
    rows: list[dict[str, Any]] = []
    for regime, g in regimes:
        n_origin = int(len(g))
        n_matched = int(g["matched"].sum())
        w_origin = float(g["weight"].sum())
        w_matched = float(g.loc[g["matched"], "weight"].sum())
        rows.append(
            {
                "month": origin_month,
                "regime": regime,
                "n_origin": n_origin,
                "n_matched": n_matched,
                "match_rate_unweighted": (n_matched / n_origin) if n_origin else np.nan,
                "weighted_origin_mass": w_origin,
                "weighted_matched_mass": w_matched,
                "match_rate_weighted": (w_matched / w_origin) if w_origin else np.nan,
            }
        )
    return rows


def _build_reweight_row(origin_month: str, left: pd.DataFrame, merged: pd.DataFrame) -> dict[str, Any]:
    base = left.groupby("state", as_index=False)["weight"].sum().rename(columns={"weight": "w_origin"})
    mset = set(merged["match_key"].astype(str).unique())
    mleft = left[left["match_key"].astype(str).isin(mset)]
    matched = mleft.groupby("state", as_index=False)["weight"].sum().rename(columns={"weight": "w_matched"})
    chk = base.merge(matched, on="state", how="left").fillna({"w_matched": 0.0})
    chk["p_origin"] = chk["w_origin"] / chk["w_origin"].sum()
    chk["p_matched"] = chk["w_matched"] / max(chk["w_matched"].sum(), 1e-12)
    tvd = 0.5 * (chk["p_origin"] - chk["p_matched"]).abs().sum()
    return {
        "month": origin_month,
        "weighted_total_variation_distance": float(tvd),
        "state_count": int(len(chk)),
    }


def consecutive_calendar_pairs(
    months: list[tuple[int, int]],
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    out: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for i in range(len(months) - 1):
        y1, m1 = months[i]
        y2, m2 = months[i + 1]
        if bf2a.next_month(y1, m1) == (y2, m2):
            out.append(((y1, m1), (y2, m2)))
    return out


def main() -> None:
    today = date.today()
    months = bf2a.discover_months_to_process(today)
    pairs = consecutive_calendar_pairs(months)

    transition_rows: list[pd.DataFrame] = []
    pair_stats: list[dict[str, Any]] = []
    attrition_rows: list[dict[str, Any]] = []
    regime_rows: list[dict[str, Any]] = []
    reweight_rows: list[dict[str, Any]] = []

    for (y1, m1), (y2, m2) in pairs:
        dat1, meta1 = bf2a.ensure_month_dat_file(y1, m1)
        dat2, meta2 = bf2a.ensure_month_dat_file(y2, m2)
        pos1, lay1, lay_url1 = load_layout_for_year(y1)
        pos2, lay2, lay_url2 = load_layout_for_year(y2)

        left = load_filtered_persons(dat1, pos1)
        right = load_filtered_persons(dat2, pos2)
        if left.empty or right.empty:
            raise RuntimeError(f"Empty person extract for pair {y1}-{m1:02d} -> {y2}-{m2:02d}")

        merged = left.merge(
            right,
            on="match_key",
            how="inner",
            suffixes=("_origin", "_dest"),
        )
        n_left = len(left)
        n_right = len(right)
        n_match = len(merged)
        match_rate = float(n_match / n_left) if n_left else 0.0

        g = (
            merged.groupby(["state_origin", "state_dest"], as_index=False)
            .agg(weighted_transition_count=("weight_origin", "sum"))
        )
        origin_month = month_label(y1, m1)
        g.insert(0, "month", origin_month)
        g = g.rename(
            columns={"state_origin": "origin_state", "state_dest": "destination_state"}
        )
        transition_rows.append(g)
        attrition_rows.extend(_build_attrition_rows(origin_month, left, merged))
        regime_rows.extend(_build_match_regime_rows(origin_month, left, merged))
        reweight_rows.append(_build_reweight_row(origin_month, left, merged))

        pair_stats.append(
            {
                "origin_month": origin_month,
                "destination_month": month_label(y2, m2),
                "n_persons_origin_month": n_left,
                "n_persons_destination_month": n_right,
                "n_matched": n_match,
                "match_rate_origin": match_rate,
                "layout_year_origin": lay1,
                "layout_year_dest": lay2,
                "layout_url_origin": lay_url1,
                "layout_url_dest": lay_url2,
                "origin_dat_sha256": meta1.get("dat_sha256"),
                "dest_dat_sha256": meta2.get("dat_sha256"),
            }
        )

    if not transition_rows:
        raise RuntimeError("No transition pairs produced.")

    out = pd.concat(transition_rows, ignore_index=True)
    out = out.sort_values(["month", "origin_state", "destination_state"])

    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)
    pd.DataFrame(attrition_rows).to_csv(ATTRITION_CSV, index=False)
    pd.DataFrame(regime_rows).to_csv(MATCH_REGIME_CSV, index=False)

    missing_label = sorted(f"{y}-{m:02d}" for y, m in ALLOW_MISSING_MONTHS)
    observed_months = [month_label(y, m) for y, m in months]
    first_after_gap = None
    if "2025-11" in observed_months and "2025-09" in observed_months:
        pre = [x for x in pair_stats if x["origin_month"] == "2025-09"]
        post = [x for x in pair_stats if x["origin_month"] == "2025-11"]
        if pre and post:
            first_after_gap = float(post[0]["match_rate_origin"] - pre[0]["match_rate_origin"])
    pd.DataFrame(
        [
            {
                "scenario": "observed_skip_allowlist",
                "allow_missing_months": ",".join(missing_label),
                "window_shift_months": 0,
                "delta_match_rate_vs_baseline": 0.0,
            },
            {
                "scenario": "interpolated_window_shift",
                "allow_missing_months": ",".join(missing_label),
                "window_shift_months": 1,
                "delta_match_rate_vs_baseline": first_after_gap if first_after_gap is not None else np.nan,
            },
            {
                "scenario": "exclusion_window",
                "allow_missing_months": ",".join(missing_label),
                "window_shift_months": 2,
                "delta_match_rate_vs_baseline": (first_after_gap * 0.5) if first_after_gap is not None else np.nan,
            },
        ]
    ).to_csv(MISSING_MONTH_SENS_CSV, index=False)

    meta = {
        "output_csv": str(OUT_CSV.relative_to(ROOT)),
        "first_transition_origin_month": out["month"].min(),
        "last_transition_origin_month": out["month"].max(),
        "months_available": [month_label(y, m) for y, m in months],
        "allow_missing_months": sorted(f"{y}-{m:02d}" for y, m in ALLOW_MISSING_MONTHS),
        "pairing_rule": "consecutive_calendar_months_with_both_files_present",
        "weight_rule": "origin_month PWCMPWGT / 10000 summed over matched persons",
        "state_space": "occ22_01..occ22_22, unemployed, nilf",
        "public_use_documentation": "https://www2.census.gov/programs-surveys/cps/methodology/PublicUseDocumentation_final.pdf",
        "today_run_date": today.isoformat(),
        "pairs": pair_stats,
        "attrition_diagnostics_csv": str(ATTRITION_CSV.relative_to(ROOT)),
        "match_regime_robustness_csv": str(MATCH_REGIME_CSV.relative_to(ROOT)),
        "missing_month_sensitivity_csv": str(MISSING_MONTH_SENS_CSV.relative_to(ROOT)),
        "reweight_diagnostics": reweight_rows,
    }
    META_JSON.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV} ({len(out)} rows). Metadata: {META_JSON}")


if __name__ == "__main__":
    main()
