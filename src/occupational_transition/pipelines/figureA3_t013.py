"""
Build figures/figureA3_cps_supp_validation.csv from CPS January supplement public-use microdata
(Displaced Worker, Employee Tenure, and Occupational Mobility supplement).

Run from repo root:
  python scripts/build_figureA3_cps_supp_validation.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class FigureA3Layout:
    root: Path
    raw: Path
    fig: Path
    inter: Path
    cross: Path
    terciles: Path
    out_csv: Path
    meta_json: Path


def _figure_a3_layout(root: Path) -> FigureA3Layout:
    fig = root / "figures"
    inter = root / "intermediate"
    return FigureA3Layout(
        root=root,
        raw=root / "raw" / "cps" / "supp",
        fig=fig,
        inter=inter,
        cross=root / "crosswalks" / "occ22_crosswalk.csv",
        terciles=inter / "ai_relevance_terciles.csv",
        out_csv=fig / "figureA3_cps_supp_validation.csv",
        meta_json=inter / "figureA3_cps_supp_validation_run_metadata.json",
    )


def run(root: Path) -> None:
    build_figure_a3_cps_supp_validation(_figure_a3_layout(root))


# Official Jan-2024 CPS displaced worker / tenure / occupational mobility supplement URLs
JAN24_PUB_URL = "https://www2.census.gov/programs-surveys/cps/datasets/2024/supp/jan24pub.csv"
JAN24_TECHDOC_URL = "https://www2.census.gov/programs-surveys/cps/techdocs/cpsjan24.pdf"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

REQUIRED_COLS = (
    "PRDISPWK",
    "PTST1TN",
    "PEST20",
    "PRDTOCC1",
    "PWSUPWGT",
    "PWTENWGT",
)

# Scaling: CPS supplement weights (Length=10 with 4 implied decimals) -> divide by 10,000.
SUPP_WEIGHT_DIVISOR = 10_000.0

# PTST1TN tenure recode (two implied decimals) -> divide by 100 to express years.
TENURE_YEARS_DIVISOR = 100.0

# Keep only occupation recodes that map cleanly into the 22-group system.
PRDTOCC1_MIN = 1
PRDTOCC1_MAX = 22

# PTST1TN topcode described in cpsjan24 technical documentation as 3100 (before implied-decimal scaling).
PTST1TN_MAX_RAW = 3100

TERCILE_ORDER = ["low", "middle", "high"]


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _request(url: str) -> urllib.request.Request:
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
            "Referer": "https://www.census.gov/",
        },
    )


def download_to_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return
    with urllib.request.urlopen(_request(url), timeout=600) as resp:
        # Stream to disk to avoid keeping 160MB+ in memory.
        with dest.open("wb") as f:
            shutil.copyfileobj(resp, f)


def load_occ22_mapping(cross: Path) -> dict[int, int]:
    """
    Map PRDTOCC1 (Basic CPS occupation recode) -> occ22_id via crosswalks/occ22_crosswalk.csv
    where source_system == CPS_PRDTOCC1.
    """
    df = pd.read_csv(cross)
    sub = df[df["source_system"] == "CPS_PRDTOCC1"].copy()
    if sub.empty:
        raise ValueError("crosswalks/occ22_crosswalk.csv missing CPS_PRDTOCC1 rows")

    out: dict[int, int] = {}
    for _, row in sub.iterrows():
        code_raw = row["source_occ_code"]
        if pd.isna(code_raw):
            continue
        code = int(code_raw)
        occ22_id = row["occ22_id"]
        if pd.isna(occ22_id) or occ22_id == "":
            continue
        out[code] = int(occ22_id)
    return out


def load_tercile_mapping(terciles: Path) -> dict[int, str]:
    df = pd.read_csv(terciles)
    out: dict[int, str] = {}
    for _, row in df.iterrows():
        out[int(row["occ22_id"])] = str(row["ai_relevance_tercile"]).strip().lower()
    return out


def parse_int01(v: str) -> int | None:
    try:
        x = int(float(v))
    except (TypeError, ValueError):
        return None
    if x in (0, 1):
        return x
    return None


def parse_int_pe(v: str) -> int | None:
    try:
        x = int(float(v))
    except (TypeError, ValueError):
        return None
    if x in (1, 2):
        return x
    return None


def parse_int_range(v: str, lo: int, hi: int) -> int | None:
    try:
        x = int(float(v))
    except (TypeError, ValueError):
        return None
    if lo <= x <= hi:
        return x
    return None


def parse_float_nonneg_scaled_tenure(v: str) -> float | None:
    """
    PTST1TN is stored with two implied decimals; technical doc recode is topcoded.
    We accept only raw values in [0, 3100] before scaling.
    """
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(x):
        return None
    if x < 0 or x > PTST1TN_MAX_RAW:
        return None
    return x / TENURE_YEARS_DIVISOR


def stream_and_aggregate_jan24(
    csv_path: Path,
    occ22_map: dict[int, int],
    tercile_by_occ22: dict[int, str],
) -> dict[str, dict[str, float]]:
    """
    Stream jan24pub.csv and compute weighted outcomes by AI tercile.

    Returns per tercile accumulators:
      - disp_w_sum, disp_w_num
      - ten_w_sum, ten_w_year_sum, mob_w_num
    """
    acc: dict[str, dict[str, float]] = {t: {} for t in TERCILE_ORDER}
    for t in TERCILE_ORDER:
        acc[t] = {
            "disp_w_sum": 0.0,
            "disp_w_num": 0.0,
            "ten_w_sum": 0.0,
            "ten_w_year_sum": 0.0,
            "mob_w_num": 0.0,
        }

    required_idx: dict[str, int] | None = None
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        header_map = {name: i for i, name in enumerate(header)}
        missing = [c for c in REQUIRED_COLS if c not in header_map]
        if missing:
            raise ValueError(f"jan24pub.csv missing required columns: {missing}")

        required_idx = {c: header_map[c] for c in REQUIRED_COLS}

        for row in reader:
            # Extract as strings; avoid numeric conversion when mapping fails.
            prd_occ1_raw = row[required_idx["PRDTOCC1"]]
            prd_occ1 = parse_int_range(prd_occ1_raw, PRDTOCC1_MIN, PRDTOCC1_MAX)
            if prd_occ1 is None:
                continue
            occ22_id = occ22_map.get(prd_occ1)
            if occ22_id is None:
                continue
            terr = tercile_by_occ22.get(occ22_id)
            if terr is None:
                continue

            # Displaced worker indicator and displaced weight.
            disp_ind = parse_int01(row[required_idx["PRDISPWK"]])
            if disp_ind is None:
                continue
            w_disp = row[required_idx["PWSUPWGT"]]
            try:
                w_disp_f = float(w_disp)
            except (TypeError, ValueError):
                continue
            if not np.isfinite(w_disp_f) or w_disp_f <= 0:
                continue
            w_disp_scaled = w_disp_f / SUPP_WEIGHT_DIVISOR

            # Tenure + mobility are tallied with PWTENWGT.
            w_ten = row[required_idx["PWTENWGT"]]
            try:
                w_ten_f = float(w_ten)
            except (TypeError, ValueError):
                continue
            if not np.isfinite(w_ten_f) or w_ten_f <= 0:
                continue
            w_ten_scaled = w_ten_f / SUPP_WEIGHT_DIVISOR

            tenure_years = parse_float_nonneg_scaled_tenure(row[required_idx["PTST1TN"]])
            if tenure_years is None:
                continue
            pest20 = parse_int_pe(row[required_idx["PEST20"]])
            if pest20 is None:
                continue

            # Accumulate.
            a = acc[terr]
            a["disp_w_sum"] += w_disp_scaled
            a["disp_w_num"] += w_disp_scaled * float(disp_ind)

            a["ten_w_sum"] += w_ten_scaled
            a["ten_w_year_sum"] += w_ten_scaled * tenure_years
            a["mob_w_num"] += w_ten_scaled * float(1 if pest20 == 2 else 0)

    return acc


def build_figure_a3_cps_supp_validation(layout: FigureA3Layout) -> None:
    layout.fig.mkdir(parents=True, exist_ok=True)
    layout.inter.mkdir(parents=True, exist_ok=True)
    layout.raw.mkdir(parents=True, exist_ok=True)

    # Download/cache data.
    jan24_csv_path = layout.raw / "jan24pub.csv"
    jan24_pdf_path = layout.raw / "cpsjan24.pdf"

    download_to_file(JAN24_PUB_URL, jan24_csv_path)
    download_to_file(JAN24_TECHDOC_URL, jan24_pdf_path)

    # Crosswalk / tercile mapping lineage.
    occ22_map = load_occ22_mapping(layout.cross)
    tercile_by_occ22 = load_tercile_mapping(layout.terciles)

    acc = stream_and_aggregate_jan24(
        csv_path=jan24_csv_path,
        occ22_map=occ22_map,
        tercile_by_occ22=tercile_by_occ22,
    )

    rows: list[dict[str, Any]] = []
    for t in TERCILE_ORDER:
        a = acc[t]
        if a["disp_w_sum"] <= 0 or a["ten_w_sum"] <= 0:
            # Keep strictness: output must have all denominators positive.
            continue
        displaced_inc = a["disp_w_num"] / a["disp_w_sum"]
        mean_tenure = a["ten_w_year_sum"] / a["ten_w_sum"]
        mobility_share = a["mob_w_num"] / a["ten_w_sum"]

        rows.append(
            {
                "ai_relevance_tercile": t,
                "displaced_worker_incidence": round(displaced_inc, 6),
                "mean_current_job_tenure_years": round(mean_tenure, 6),
                "occupational_mobility_share": round(mobility_share, 6),
                "sum_displaced_worker_person_weight": round(a["disp_w_sum"], 6),
                "sum_job_tenure_person_weight": round(a["ten_w_sum"], 6),
            }
        )

    out = pd.DataFrame(rows, columns=[
        "ai_relevance_tercile",
        "displaced_worker_incidence",
        "mean_current_job_tenure_years",
        "occupational_mobility_share",
        "sum_displaced_worker_person_weight",
        "sum_job_tenure_person_weight",
    ])

    # Strict expectations: must contain exactly 3 terciles.
    if out.empty or len(out) != 3:
        raise RuntimeError(
            f"Unexpected output size for T-013: expected 3 terciles, got {len(out)}. "
            "Check that supplement filters and required fields produce nonzero denominators."
        )

    # Enforce presentation order for deterministic QA.
    out["ai_relevance_tercile"] = pd.Categorical(out["ai_relevance_tercile"], categories=TERCILE_ORDER, ordered=True)
    out = out.sort_values(["ai_relevance_tercile"]).reset_index(drop=True)

    out.to_csv(layout.out_csv, index=False)

    lineage = {
        "crosswalks/occ22_crosswalk.csv": _sha256_file(layout.cross),
        "intermediate/ai_relevance_terciles.csv": _sha256_file(layout.terciles),
    }

    meta = {
        "schema_version": "1.0",
        "task_id": "T-013",
        "output_csv": str(layout.out_csv.relative_to(layout.root)).replace("\\", "/"),
        "build_date_utc": date.today().isoformat(),
        "geography": "national only",
        "supplement_cycle": {"jan_year": 2024, "month": "January"},
        "occupation_source": "PRDTOCC1 occupation recode mapped to occ22_id via crosswalks/occ22_crosswalk.csv",
        "ai_terciles": "intermediate/ai_relevance_terciles.csv on occ22_id",
        "weight_variable_displacement": "PWSUPWGT",
        "weight_variable_tenure_mobility": "PWTENWGT",
        "weight_scaling_rule": {
            "PWSUPWGT": f"divide by {SUPP_WEIGHT_DIVISOR:g}",
            "PWTENWGT": f"divide by {SUPP_WEIGHT_DIVISOR:g}",
        },
        "tenure_years_scaling_rule": f"PTST1TN divide by {TENURE_YEARS_DIVISOR:g} to express years",
        "outcome_variables": {
            "displacement_indicator": {"source": "PRDISPWK", "valid_codes": [0, 1]},
            "tenure_years": {"source": "PTST1TN", "filter_raw_range_inclusive": [0, PTST1TN_MAX_RAW]},
            "occupational_mobility": {"source": "PEST20", "valid_codes": [1, 2], "mobility_is_code": 2},
        },
        "sources": [
            {
                "download_url": JAN24_PUB_URL,
                "file_name": "jan24pub.csv",
                "file_sha256": _sha256_file(jan24_csv_path),
            },
            {
                "download_url": JAN24_TECHDOC_URL,
                "file_name": "cpsjan24.pdf",
                "file_sha256": _sha256_file(jan24_pdf_path),
            },
        ],
        "lineage_file_sha256": lineage,
        "provenance_statement": (
            "Only official CPS Displaced Worker / Employee Tenure / Occupational Mobility supplement public-use files "
            "from www2.census.gov were used."
        ),
        "filters": {
            "PRDTOCC1_universe": [PRDTOCC1_MIN, PRDTOCC1_MAX],
            "PRDISPWK_universe": [0, 1],
            "PEST20_universe": [1, 2],
            "PTST1TN_raw_universe_inclusive": [0, PTST1TN_MAX_RAW],
        },
    }

    layout.meta_json.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {layout.out_csv}")
    print(f"Wrote {layout.meta_json}")

