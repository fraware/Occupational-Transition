"""
Build figures/figureA1_asec_welfare_by_ai_tercile.csv from official Census CPS ASEC
March public-use CSV microdata (www2.census.gov) and frozen occ22 / AI tercile mappings.

Run from repo root: python scripts/build_figureA1_asec_welfare_by_ai_tercile.py
"""

from __future__ import annotations

import hashlib
import io
import json
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "cps" / "asec"
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
CROSS = ROOT / "crosswalks" / "occ22_crosswalk.csv"
TERCILES = INTER / "ai_relevance_terciles.csv"
OUT_CSV = FIG / "figureA1_asec_welfare_by_ai_tercile.csv"
META_JSON = INTER / "figureA1_asec_welfare_by_ai_tercile_run_metadata.json"

CPS_ASEC_BASE = "https://www2.census.gov/programs-surveys/cps/datasets"

# Official person-record fields (CPS ASEC public-use CSV person file; see persfmt.txt per year).
REQUIRED_PERSON_COLUMNS = (
    "A_DTOCC",
    "A_FNLWGT",
    "PEMLR",
    "WKSWORK",
    "PTOTVAL",
    "SPM_POOR",
)

# Census www2 may reject non-browser user agents.
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# Labor-force codes for unemployment rate (employed + unemployed); see Census CPS PEMLR.
LF_CODES = (1, 2, 3, 4)
UNEMP_CODES = (3, 4)

# A_FNLWGT: Census person layout documents width/range; public CSV stores two implied decimals.
A_FNLWGT_SCALE = 100.0

# Keep small: wide ASEC person CSVs have hundreds of columns; reading only
# REQUIRED_PERSON_COLUMNS avoids OOM in pandas' C tokenizer/parser.
CHUNKSIZE = 50_000


def _request(url: str, method: str = "GET") -> urllib.request.Request:
    return urllib.request.Request(
        url,
        method=method,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.census.gov/",
        },
    )


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def asec_csv_zip_url(year: int) -> str:
    yy = year % 100
    return f"{CPS_ASEC_BASE}/{year}/march/asecpub{yy:02d}csv.zip"


def probe_year_available(year: int) -> bool:
    url = asec_csv_zip_url(year)
    req = _request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return 200 <= resp.status < 300
    except (urllib.error.HTTPError, urllib.error.URLError, OSError):
        return False


def discover_retained_years(start_year: int = 2019) -> list[int]:
    """Years from start_year through the latest year with an official asecpubYYcsv.zip."""
    years: list[int] = []
    y = start_year
    while probe_year_available(y):
        years.append(y)
        y += 1
    if not years:
        raise RuntimeError(
            f"No CPS ASEC CSV zip found at {asec_csv_zip_url(start_year)}; "
            "check network or Census release schedule."
        )
    return years


def find_person_csv_member(names: list[str]) -> str:
    cands = [n for n in names if n.lower().endswith(".csv") and "pppub" in n.lower()]
    if not cands:
        raise ValueError(f"No pppub*.csv in bundle: {names[:20]}...")
    return sorted(cands, key=len)[0]


def load_dtocc_to_occ22() -> dict[int, int]:
    cross = pd.read_csv(CROSS)
    sub = cross[cross["source_system"] == "CPS_PRDTOCC1"].copy()
    if sub.empty:
        raise ValueError("crosswalks/occ22_crosswalk.csv missing CPS_PRDTOCC1 rows")
    m: dict[int, int] = {}
    for _, row in sub.iterrows():
        code = int(row["source_occ_code"])
        oid = row["occ22_id"]
        if pd.isna(oid) or oid == "":
            continue
        m[code] = int(oid)
    return m


def load_tercile_by_occ22() -> dict[int, str]:
    df = pd.read_csv(TERCILES)
    out: dict[int, str] = {}
    for _, row in df.iterrows():
        out[int(row["occ22_id"])] = str(row["ai_relevance_tercile"]).strip().lower()
    return out


@dataclass
class YearAgg:
    sum_w: np.ndarray
    sum_w_income: np.ndarray
    sum_w_poor: np.ndarray
    sum_w_weeks: np.ndarray
    sum_w_unemp: np.ndarray
    sum_w_lf: np.ndarray


def _empty_agg(n_terc: int) -> YearAgg:
    z = np.zeros(n_terc, dtype=np.float64)
    return YearAgg(z.copy(), z.copy(), z.copy(), z.copy(), z.copy(), z.copy())


def process_year_chunk(
    df: pd.DataFrame,
    dtocc_to_occ22: dict[int, int],
    tercile_by_occ22: dict[int, str],
    tercile_index: dict[str, int],
    agg: YearAgg,
) -> None:
    """Accumulate weighted sums into agg (same order as tercile_index keys)."""
    dto = pd.to_numeric(df["A_DTOCC"], errors="coerce")
    ok = dto.notna() & (dto >= 1) & (dto <= 22)
    if not ok.any():
        return
    df = df.loc[ok].copy()
    dto_i = dto.loc[ok].astype(int)
    occ22 = dto_i.map(dtocc_to_occ22)
    terr = occ22.map(lambda x: tercile_by_occ22.get(int(x)) if pd.notna(x) else np.nan)
    valid = terr.notna()
    if not valid.any():
        return
    df = df.loc[valid]
    terr = terr.loc[valid]
    ti = terr.map(tercile_index).astype(int).to_numpy()

    w = pd.to_numeric(df["A_FNLWGT"], errors="coerce").fillna(0).to_numpy(dtype=np.float64) / A_FNLWGT_SCALE
    pemlr = pd.to_numeric(df["PEMLR"], errors="coerce").fillna(-1).astype(int).to_numpy()
    ptot = pd.to_numeric(df["PTOTVAL"], errors="coerce").to_numpy(dtype=np.float64)
    ptot_safe = np.where(np.isfinite(ptot) & (ptot >= 0), ptot, 0.0)
    poor = pd.to_numeric(df["SPM_POOR"], errors="coerce").fillna(0).to_numpy(dtype=np.float64)
    wks = pd.to_numeric(df["WKSWORK"], errors="coerce").fillna(0).to_numpy(dtype=np.float64)

    in_lf = np.isin(pemlr, LF_CODES)
    unemp = np.isin(pemlr, UNEMP_CODES)

    for j in range(len(ti)):
        k = int(ti[j])
        ww = float(w[j])
        if ww <= 0 or not np.isfinite(ww):
            continue
        agg.sum_w[k] += ww
        agg.sum_w_income[k] += ww * ptot_safe[j]
        agg.sum_w_poor[k] += ww * poor[j]
        agg.sum_w_weeks[k] += ww * wks[j]
        if in_lf[j]:
            agg.sum_w_lf[k] += ww
            if unemp[j]:
                agg.sum_w_unemp[k] += ww


def download_zip_bytes(year: int, raw_path: Path) -> tuple[bytes, Path]:
    url = asec_csv_zip_url(year)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    if raw_path.is_file():
        return raw_path.read_bytes(), raw_path
    req = _request(url)
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = resp.read()
    raw_path.write_bytes(data)
    return data, raw_path


def aggregate_year(
    year: int,
    dtocc_to_occ22: dict[int, int],
    tercile_by_occ22: dict[int, str],
    tercile_order: list[str],
) -> tuple[pd.DataFrame, dict[str, Any]]:
    raw_zip = RAW / f"asecpub{year % 100:02d}csv.zip"
    data, used_path = download_zip_bytes(year, raw_zip)
    h = _sha256_bytes(data)
    zf = zipfile.ZipFile(io.BytesIO(data))
    member = find_person_csv_member(zf.namelist())
    tercile_index = {t: i for i, t in enumerate(tercile_order)}
    n_t = len(tercile_order)
    agg = _empty_agg(n_t)

    with zf.open(member) as zstream:
        reader = pd.read_csv(
            zstream,
            encoding="latin-1",
            chunksize=CHUNKSIZE,
            usecols=list(REQUIRED_PERSON_COLUMNS),
            low_memory=True,
        )
        for chunk in reader:
            missing = [c for c in REQUIRED_PERSON_COLUMNS if c not in chunk.columns]
            if missing:
                raise ValueError(
                    f"{year} person CSV {member} missing columns {missing}; "
                    "refuse guessed mappings."
                )
            process_year_chunk(
                chunk,
                dtocc_to_occ22,
                tercile_by_occ22,
                tercile_index,
                agg,
            )

    rows: list[dict[str, Any]] = []
    for t in tercile_order:
        i = tercile_index[t]
        sw = agg.sum_w[i]
        if sw <= 0:
            raise RuntimeError(f"{year} tercile {t}: zero or negative total weight after filters")
        mean_inc = agg.sum_w_income[i] / sw
        pov_r = agg.sum_w_poor[i] / sw
        mean_wks = agg.sum_w_weeks[i] / sw
        lf = agg.sum_w_lf[i]
        unemp_r = (agg.sum_w_unemp[i] / lf) if lf > 0 else 0.0
        rows.append(
            {
                "year": year,
                "ai_relevance_tercile": t,
                "mean_annual_income": round(mean_inc, 6),
                "poverty_rate": round(float(pov_r), 6),
                "mean_weeks_worked": round(mean_wks, 6),
                "unemployment_incidence": round(float(unemp_r), 6),
                "sum_asec_person_weight": round(float(sw), 6),
            }
        )

    meta = {
        "year": year,
        "download_url": asec_csv_zip_url(year),
        "zip_sha256": h,
        "zip_cached_path": str(used_path.relative_to(ROOT)).replace("\\", "/"),
        "person_csv_member": member,
    }
    out_df = pd.DataFrame(rows)
    return out_df, meta


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    dtocc_to_occ22 = load_dtocc_to_occ22()
    tercile_by_occ22 = load_tercile_by_occ22()
    tercile_order = ["low", "middle", "high"]

    years = discover_retained_years(2019)
    frames: list[pd.DataFrame] = []
    year_sources: list[dict[str, Any]] = []

    for y in years:
        ydf, ymeta = aggregate_year(y, dtocc_to_occ22, tercile_by_occ22, tercile_order)
        frames.append(ydf)
        year_sources.append(ymeta)

    out = pd.concat(frames, ignore_index=True)
    tercile_rank = {t: i for i, t in enumerate(tercile_order)}
    out["_tercile_rank"] = out["ai_relevance_tercile"].map(tercile_rank)
    out = out.sort_values(["year", "_tercile_rank"]).drop(columns=["_tercile_rank"]).reset_index(drop=True)
    out.to_csv(OUT_CSV, index=False)

    lineage = {
        "crosswalks/occ22_crosswalk.csv": _sha256_file(CROSS),
        "intermediate/ai_relevance_terciles.csv": _sha256_file(TERCILES),
    }

    meta: dict[str, Any] = {
        "schema_version": "1.0",
        "task_id": "T-011",
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "build_date_utc": date.today().isoformat(),
        "source_selection_mode": "rolling_latest_allowed_by_ticket",
        "source_selection_rule": (
            "Probe consecutive asecpubYYcsv.zip bundles from the fixed start "
            "year (2019) and retain contiguous available years only."
        ),
        "retained_year_range": {"start": int(years[0]), "end": int(years[-1])},
        "retained_years": years,
        "geography": "national (CPS ASEC; no subnational restriction applied)",
        "universe_note": (
            "Persons in CPS ASEC person file with A_DTOCC in 1..22 (major occupation groups), "
            "excluding A_DTOCC 0 (NIU/unknown) and 23 (armed forces), per CPS_PRDTOCC1 crosswalk."
        ),
        "weight_variable": "A_FNLWGT",
        "weight_scaling_rule": (
            "Divide A_FNLWGT by 100.0 to obtain person weight (two implied decimal places; "
            "see official CPS ASEC person record layout persfmt.txt for the retained years)."
        ),
        "poverty_indicator": "SPM_POOR",
        "poverty_note": (
            "poverty_rate is the SPM_POOR-weighted share (Supplemental Poverty Measure poor flag "
            "on the person record; see CPS ASEC documentation)."
        ),
        "annual_income_variable": "PTOTVAL",
        "annual_income_note": "Negative PTOTVAL values are truncated to 0 for mean_annual_income.",
        "weeks_worked_variable": "WKSWORK",
        "unemployment_definition": (
            "unemployment_incidence = sum(weight * I[PEMLR in (3,4)]) / "
            "sum(weight * I[PEMLR in (1,2,3,4)]) within the same A_DTOCC 1..22 universe."
        ),
        "occupation_variable": "A_DTOCC",
        "occupation_mapping": "CPS_PRDTOCC1 rows in crosswalks/occ22_crosswalk.csv to occ22_id",
        "ai_terciles_mapping": "intermediate/ai_relevance_terciles.csv on occ22_id",
        "sources": year_sources,
        "lineage_file_sha256": lineage,
        "provenance_statement": (
            "Only official Census CPS ASEC March public-use files published on www2.census.gov "
            "were used for microdata (asecpubYYcsv.zip bundles)."
        ),
    }
    META_JSON.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {META_JSON}")


if __name__ == "__main__":
    main()
