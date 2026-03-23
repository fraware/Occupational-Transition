"""
Build figures/figureA2_sipp_event_study.csv from Census SIPP public-use person-month
microdata (official www2.census.gov releases) and frozen occ22 / AI tercile mappings.

Run from repo root: python scripts/build_figureA2_sipp_event_study.py
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import sqlite3
import urllib.request
import uuid
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "sipp"
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
CROSS = ROOT / "crosswalks" / "occ22_crosswalk.csv"
TERCILES = INTER / "ai_relevance_terciles.csv"
OUT_CSV = FIG / "figureA2_sipp_event_study.csv"
META_JSON = INTER / "figureA2_sipp_event_study_run_metadata.json"

SIPP_DATASETS_BASE = "https://www2.census.gov/programs-surveys/sipp/data/datasets"

# Post-2019 SIPP annual releases used (each has pu{YYYY}_csv.zip primary person-month file).
PANEL_RELEASE_YEARS = (2022, 2023, 2024)

# Event window relative to transition month (event_time = 0).
EVENT_K_MIN = -12
EVENT_K_MAX = 24

MIN_AGE = 16

# RMESR: monthly employment status recode (SIPP public-use). Employed-with-job codes
# used for "employed" state; all other codes treated as not employed for transition detection.
# See 2024_SIPP_Data_Dictionary.pdf (Census) variable RMESR.
EMPLOYED_RMESR = (1, 2)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

USECOLS = [
    "SSUID",
    "PNUM",
    "SPANEL",
    "SWAVE",
    "MONTHCODE",
    "RMESR",
    "TJB1_OCC",
    "WPFINWGT",
    "TPTOTINC",
    "RSNAP_MNYN",
    "RIN_UNIV",
    "TAGE",
]


def _request(url: str) -> urllib.request.Request:
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
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


def pu_csv_zip_url(release_year: int) -> str:
    return f"{SIPP_DATASETS_BASE}/{release_year}/pu{release_year}_csv.zip"


def pu_schema_json_url(release_year: int) -> str:
    return f"{SIPP_DATASETS_BASE}/{release_year}/pu{release_year}_schema.json"


def download_zip(release_year: int) -> tuple[Path, bytes, str]:
    url = pu_csv_zip_url(release_year)
    dest = RAW / f"pu{release_year}_csv.zip"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file():
        data = dest.read_bytes()
        return dest, data, url
    with urllib.request.urlopen(_request(url), timeout=600) as resp:
        data = resp.read()
    dest.write_bytes(data)
    return dest, data, url


def load_peio_to_occ22() -> dict[str, int]:
    df = pd.read_csv(CROSS)
    sub = df[df["source_system"] == "CPS_PEIO1OCD_2018"].copy()
    if sub.empty:
        raise ValueError("crosswalks/occ22_crosswalk.csv missing CPS_PEIO1OCD_2018 rows")
    m: dict[str, int] = {}
    for _, row in sub.iterrows():
        code = str(row["source_occ_code"]).strip()
        if not code or code.lower() == "nan":
            continue
        z = code.zfill(4) if code.isdigit() else code
        oid = row["occ22_id"]
        if pd.isna(oid) or oid == "":
            continue
        m[z] = int(oid)
    return m


def load_tercile_by_occ22() -> dict[int, str]:
    df = pd.read_csv(TERCILES)
    out: dict[int, str] = {}
    for _, row in df.iterrows():
        out[int(row["occ22_id"])] = str(row["ai_relevance_tercile"]).strip().lower()
    return out


def normalize_occ_code(raw: Any) -> str | None:
    if raw is None or (isinstance(raw, float) and np.isnan(raw)):
        return None
    try:
        v = int(float(raw))
    except (TypeError, ValueError):
        return None
    if v <= 0:
        return None
    return str(v).zfill(4)


def occ22_from_tjb(
    occ_raw: Any,
    peio_map: dict[str, int],
) -> int | None:
    z = normalize_occ_code(occ_raw)
    if z is None:
        return None
    oid = peio_map.get(z)
    return int(oid) if oid is not None else None


def is_employed(rmesr: Any) -> bool:
    try:
        r = int(rmesr)
    except (TypeError, ValueError):
        return False
    return r in EMPLOYED_RMESR


def snap_participation(v: Any) -> float:
    try:
        if pd.isna(v):
            return 0.0
        return 1.0 if int(v) == 1 else 0.0
    except (TypeError, ValueError):
        return 0.0


def income_numeric(v: Any) -> float:
    try:
        if pd.isna(v):
            return 0.0
        x = float(v)
        return x if np.isfinite(x) and x >= 0 else 0.0
    except (TypeError, ValueError):
        return 0.0


@dataclass
class MonthRow:
    swave: int
    monthcode: int
    rmesr: int
    tjb_occ: Any
    weight: float
    income: float
    snap: float
    age: int
    rin_univ: int


def sort_key(m: MonthRow) -> tuple[int, int]:
    return (m.swave, m.monthcode)


def detect_event_index(months: list[MonthRow], peio_map: dict[str, int]) -> int | None:
    """Index of first transition month (event_time=0) or None."""
    if len(months) < 2:
        return None
    for i in range(1, len(months)):
        prev = months[i - 1]
        cur = months[i]
        if prev.rin_univ != 1 or cur.rin_univ != 1:
            continue
        if prev.age < MIN_AGE or cur.age < MIN_AGE:
            continue
        if not is_employed(prev.rmesr):
            continue
        prev_occ = occ22_from_tjb(prev.tjb_occ, peio_map)
        if prev_occ is None or not (1 <= prev_occ <= 22):
            continue
        cur_emp = is_employed(cur.rmesr)
        cur_occ = occ22_from_tjb(cur.tjb_occ, peio_map) if cur_emp else None
        if not cur_emp:
            return i
        if cur_occ is not None and 1 <= cur_occ <= 22 and cur_occ != prev_occ:
            return i
    return None


def process_person_months(
    months: list[MonthRow],
    event_idx: int,
    baseline_occ22: int,
    tercile_by_occ22: dict[int, str],
    agg: dict[tuple[int, str], list[float]],
) -> None:
    terr = tercile_by_occ22.get(baseline_occ22)
    if terr is None:
        return
    for k in range(EVENT_K_MIN, EVENT_K_MAX + 1):
        j = event_idx + k
        if j < 0 or j >= len(months):
            continue
        m = months[j]
        if m.rin_univ != 1 or m.age < MIN_AGE:
            continue
        w = m.weight
        if w <= 0 or not np.isfinite(w):
            continue
        emp = 1.0 if is_employed(m.rmesr) else 0.0
        key = (k, terr)
        a = agg[key]
        a[0] += w
        a[1] += w * emp
        a[2] += w * m.income
        a[3] += w * m.snap


def _opt_int_field(raw: str | None) -> int | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if not s or s == ".":
        return None
    try:
        return int(float(s))
    except (TypeError, ValueError):
        return None


def _opt_float_field(raw: str | None) -> float | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if not s or s == ".":
        return None
    try:
        x = float(s)
    except (TypeError, ValueError):
        return None
    return x if np.isfinite(x) else None


def _row_tuple_from_csv(row: dict[str, str]) -> tuple[Any, ...]:
    """Insert tuple matching pm column order."""
    tjb = row.get("TJB1_OCC")
    tjb_s = None if tjb is None or str(tjb).strip() == "" or str(tjb).strip() == "." else str(tjb).strip()
    return (
        str(row["SSUID"]).strip(),
        str(row["PNUM"]).strip(),
        str(row["SPANEL"]).strip(),
        _opt_int_field(row.get("SWAVE")),
        _opt_int_field(row.get("MONTHCODE")),
        _opt_int_field(row.get("RMESR")),
        tjb_s,
        _opt_float_field(row.get("WPFINWGT")),
        _opt_float_field(row.get("TPTOTINC")),
        _opt_int_field(row.get("RSNAP_MNYN")),
        _opt_int_field(row.get("RIN_UNIV")),
        _opt_int_field(row.get("TAGE")),
    )


def _monthrow_from_sql_row(row: tuple[Any, ...]) -> MonthRow:
    """Map ordered SELECT columns to MonthRow (see ingest_panel_sqlite query)."""
    _ssuid, _pnum, _spanel, sw, mc, rmesr, tjb, wgt, inc, snap, rin, age = row
    return MonthRow(
        swave=int(sw) if sw is not None else -1,
        monthcode=int(mc) if mc is not None else -1,
        rmesr=int(rmesr) if rmesr is not None else -1,
        tjb_occ=tjb,
        weight=float(wgt) if wgt is not None else 0.0,
        income=income_numeric(inc),
        snap=snap_participation(snap),
        rin_univ=int(rin) if rin is not None else 0,
        age=int(age) if age is not None else 0,
    )


def ingest_panel_sqlite(
    release_year: int,
    peio_map: dict[str, int],
    tercile_by_occ22: dict[int, str],
    agg: dict[tuple[int, str], list[float]],
) -> dict[str, Any]:
    """
    Chunk-read each panel ZIP into an on-disk SQLite table, ORDER BY person and time,
    then stream person-month groups. Avoids loading full CSV into RAM (OOM on large panels)
    and is correct when person-month rows are not contiguous in the raw file.
    """
    zip_path, zip_bytes, zip_url = download_zip(release_year)
    zip_hash = _sha256_bytes(zip_bytes)

    csv_name = "pu.csv"
    # Unique path avoids PermissionError on Windows if a prior build is still running or the file is locked.
    db_path = INTER / f"_sipp_panel_{release_year}_{uuid.uuid4().hex}.sqlite"

    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        csv_name = next(n for n in names if n.lower().endswith(".csv"))
        with zf.open(csv_name) as zstream, sqlite3.connect(db_path) as conn:
            conn.execute("PRAGMA journal_mode=OFF")
            conn.execute("PRAGMA synchronous=OFF")
            conn.execute(
                """
                CREATE TABLE pm (
                    ssuid TEXT NOT NULL,
                    pnum TEXT NOT NULL,
                    spanel TEXT NOT NULL,
                    swave INTEGER,
                    monthcode INTEGER,
                    rmesr INTEGER,
                    tjb_occ TEXT,
                    wpfinwgt REAL,
                    tptotinc REAL,
                    rsnap_mnyn INTEGER,
                    rin_univ INTEGER,
                    tage INTEGER
                )
                """
            )
            insert_sql = (
                "INSERT INTO pm (ssuid, pnum, spanel, swave, monthcode, rmesr, tjb_occ, "
                "wpfinwgt, tptotinc, rsnap_mnyn, rin_univ, tage) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
            )
            batch_size = 50_000
            batch: list[tuple[Any, ...]] = []
            text_io = io.TextIOWrapper(zstream, encoding="utf-8", newline="")
            reader = csv.DictReader(text_io, delimiter="|")
            fields = reader.fieldnames or []
            missing = [c for c in USECOLS if c not in fields]
            if missing:
                raise ValueError(
                    f"SIPP CSV missing columns {missing}; fieldnames={fields[:30]}"
                )
            for row in reader:
                clean = {k: ("" if row.get(k) is None else str(row.get(k))) for k in USECOLS}
                batch.append(_row_tuple_from_csv(clean))
                if len(batch) >= batch_size:
                    conn.executemany(insert_sql, batch)
                    batch.clear()
                    conn.commit()
            if batch:
                conn.executemany(insert_sql, batch)
                conn.commit()

            conn.execute(
                "CREATE INDEX idx_pm_person_time ON pm (ssuid, pnum, spanel, swave, monthcode)"
            )
            conn.commit()

            cur = conn.execute(
                """
                SELECT ssuid, pnum, spanel, swave, monthcode, rmesr, tjb_occ,
                       wpfinwgt, tptotinc, rsnap_mnyn, rin_univ, tage
                FROM pm
                ORDER BY ssuid, pnum, spanel, swave, monthcode
                """
            )

            buf: list[MonthRow] = []
            prev_key: tuple[str, str, str] | None = None

            def flush_group() -> None:
                nonlocal buf
                if not buf:
                    return
                months = buf
                buf = []
                months.sort(key=sort_key)
                ev = detect_event_index(months, peio_map)
                if ev is not None:
                    prev_m = months[ev - 1]
                    bo = occ22_from_tjb(prev_m.tjb_occ, peio_map)
                    if bo is not None and 1 <= bo <= 22:
                        process_person_months(months, ev, bo, tercile_by_occ22, agg)

            for row in cur:
                key = (str(row[0]), str(row[1]), str(row[2]))
                if prev_key is None:
                    prev_key = key
                elif key != prev_key:
                    flush_group()
                    prev_key = key
                buf.append(_monthrow_from_sql_row(row))
            flush_group()

    try:
        db_path.unlink()
    except OSError:
        pass

    return {
        "sipp_release_year": release_year,
        "download_url": zip_url,
        "zip_sha256": zip_hash,
        "zip_cached_path": str(zip_path.relative_to(ROOT)).replace("\\", "/"),
        "csv_member": csv_name,
        "schema_url": pu_schema_json_url(release_year),
        "sqlite_ingest_batch_rows": 50_000,
        "ingest_note": "stdlib csv.DictReader streaming into SQLite (avoids pandas OOM on large pu.csv).",
    }


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    peio_map = load_peio_to_occ22()
    tercile_by_occ22 = load_tercile_by_occ22()

    agg: dict[tuple[int, str], list[float]] = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    sources: list[dict[str, Any]] = []

    for yr in PANEL_RELEASE_YEARS:
        meta = ingest_panel_sqlite(yr, peio_map, tercile_by_occ22, agg)
        sources.append(meta)

    tercile_order = ["low", "middle", "high"]
    # event_time k is kept only if all three terciles have positive person-weight totals (complete grid).
    ks_any = {k for (k, _t) in agg.keys()}
    valid_ks: list[int] = []
    for k in sorted(ks_any):
        if all(agg.get((k, t), [0.0])[0] > 0 for t in tercile_order):
            valid_ks.append(k)

    rows: list[dict[str, Any]] = []
    for k in valid_ks:
        for t in tercile_order:
            sw, se, si, sn = agg[(k, t)]
            rows.append(
                {
                    "event_time": k,
                    "ai_relevance_tercile": t,
                    "mean_employment_rate": round(se / sw, 6),
                    "mean_monthly_income": round(si / sw, 6),
                    "mean_snap_participation": round(sn / sw, 6),
                    "sum_person_weight": round(sw, 6),
                }
            )

    out = pd.DataFrame(rows)
    if out.empty:
        raise RuntimeError("No event-study rows produced; check SIPP inputs and filters.")
    # QA enforces deterministic presentation order per event_time: low, middle, high.
    tercile_order = ["low", "middle", "high"]
    tercile_rank = {t: i for i, t in enumerate(tercile_order)}
    out["tercile_rank"] = out["ai_relevance_tercile"].map(tercile_rank)
    if out["tercile_rank"].isnull().any():
        bad = out.loc[out["tercile_rank"].isnull(), "ai_relevance_tercile"].unique().tolist()
        raise RuntimeError(f"Unexpected ai_relevance_tercile values in output: {bad}")
    out = (
        out.sort_values(["event_time", "tercile_rank"], kind="mergesort")
        .drop(columns=["tercile_rank"])
        .reset_index(drop=True)
    )
    out.to_csv(OUT_CSV, index=False)

    lineage = {
        "crosswalks/occ22_crosswalk.csv": _sha256_file(CROSS),
        "intermediate/ai_relevance_terciles.csv": _sha256_file(TERCILES),
    }

    meta_out: dict[str, Any] = {
        "schema_version": "1.0",
        "task_id": "T-012",
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "build_date_utc": date.today().isoformat(),
        "geography": "national (SIPP person weights; no subnational filter applied)",
        "sipp_panel_release_years": list(PANEL_RELEASE_YEARS),
        "event_window": {"min_k": EVENT_K_MIN, "max_k": EVENT_K_MAX},
        "occupation_source": "TJB1_OCC mapped via CPS_PEIO1OCD_2018 rows in crosswalks/occ22_crosswalk.csv",
        "ai_terciles": "intermediate/ai_relevance_terciles.csv on occ22_id",
        "employed_rmesr_codes": list(EMPLOYED_RMESR),
        "weight_variable": "WPFINWGT",
        "weight_note": (
            "Monthly final person weight on the SIPP person-month record (see Census SIPP primary file "
            "variable WPFINWGT and Guide to Selecting Weights for 2018+ SIPP)."
        ),
        "filters": {
            "rin_univ": "RIN_UNIV == 1",
            "min_age": MIN_AGE,
        },
        "transition_definition": (
            "First month where prior month is employed (RMESR in employed codes) with baseline "
            "TJB1_OCC mapping to occ22 1..22, and current month is either not employed or employed "
            "in a different occ22 1..22."
        ),
        "sources": sources,
        "lineage_file_sha256": lineage,
        "provenance_statement": (
            "Only official Census SIPP public-use person-month files published on www2.census.gov were used."
        ),
    }
    META_JSON.write_text(json.dumps(meta_out, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {META_JSON}")


if __name__ == "__main__":
    main()
