"""
Build figures/figure2_panelA_hours_by_ai_tercile.csv from Census CPS Basic Monthly PUF
and frozen AI relevance terciles (T-002).

Run from repo root: python scripts/build_figure2_panelA.py
"""

from __future__ import annotations

import gzip
import hashlib
import json
import re
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterator

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "cps" / "basic"
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
CROSS = ROOT / "crosswalks" / "occ22_crosswalk.csv"
TERCILES = INTER / "ai_relevance_terciles.csv"
OUT_CSV = FIG / "figure2_panelA_hours_by_ai_tercile.csv"
META_JSON = INTER / "figure2_panelA_run_metadata.json"

CPS_BASIC_BASE = "https://www2.census.gov/programs-surveys/cps/datasets"
LAYOUT_URL_TEMPLATE = (
    CPS_BASIC_BASE + "/{year}/basic/{year}_Basic_CPS_Public_Use_Record_Layout_plus_IO_Code_list.txt"
)
FALLBACK_LAYOUT_YEAR = 2020

MONTH_ABBR = (
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
)

# Officially missing CPS Basic microdata month (see Census CPS Basic footnotes).
ALLOW_MISSING_MONTHS: set[tuple[int, int]] = {(2025, 10)}

REQUIRED_FIELDS = (
    "HRYEAR4",
    "HRMONTH",
    "PRTAGE",
    "PRPERTYP",
    "PEMLR",
    "PEHRUSL1",
    "PRDTOCC1",
    "PWCMPWGT",
)

# Census www2 may reject non-browser user agents; match a common browser string.
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


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


def _probe_month_asset(url: str) -> bytes | None:
    """Read first bytes of a month file (Range request) without downloading the full object."""
    try:
        req = _request(url)
        req.add_header("Range", "bytes=0-7")
        with urllib.request.urlopen(req, timeout=90) as resp:
            return resp.read(8)
    except (urllib.error.HTTPError, urllib.error.URLError, OSError):
        return None


def month_asset_available(year: int, month: int) -> bool:
    """True if either the monthly ZIP or the .dat.gz exists on Census servers."""
    for url in (month_zip_url(year, month), month_dat_gz_url(year, month)):
        head = _probe_month_asset(url)
        if head is None:
            continue
        if head.startswith(b"PK\x03\x04") or head.startswith(b"\x1f\x8b"):
            return True
    return False


def month_stem(year: int, month: int) -> str:
    if not 1 <= month <= 12:
        raise ValueError(f"Invalid month: {month}")
    yy = year % 100
    return f"{MONTH_ABBR[month - 1]}{yy:02d}pub"


def month_zip_url(year: int, month: int) -> str:
    return f"{CPS_BASIC_BASE}/{year}/basic/{month_stem(year, month)}.zip"


def month_dat_gz_url(year: int, month: int) -> str:
    """Alternate CPS Basic delivery (.dat.gz) when .zip is blocked or unavailable."""
    return f"{CPS_BASIC_BASE}/{year}/basic/{month_stem(year, month)}.dat.gz"


def next_month(y: int, m: int) -> tuple[int, int]:
    m += 1
    if m > 12:
        return y + 1, 1
    return y, m


def month_index(y: int, m: int) -> int:
    return y * 12 + m


def parse_layout_positions(layout_text: str) -> dict[str, tuple[int, int]]:
    """
    Parse Census Basic CPS record layout text into 0-based (start, end) slices
    (end exclusive) for each variable's LOCATION range (1-based inclusive in file).
    Only the variables listed in REQUIRED_FIELDS are extracted (avoids false matches).
    """
    positions: dict[str, tuple[int, int]] = {}
    for line in layout_text.splitlines():
        for name in REQUIRED_FIELDS:
            if line.startswith(name + "\t"):
                m = re.search(r"(\d+)\s*-\s*(\d+)\s*$", line.rstrip())
                if not m:
                    raise ValueError(f"Could not parse LOCATION for {name}: {line[:120]}")
                start1, end1 = int(m.group(1)), int(m.group(2))
                positions[name] = (start1 - 1, end1)
                break
    missing = [k for k in REQUIRED_FIELDS if k not in positions]
    if missing:
        raise ValueError(f"Layout missing variables: {missing}")
    return positions


def load_layout_for_year(year: int) -> tuple[dict[str, tuple[int, int]], int, str]:
    """
    Download year-specific layout; fall back to FALLBACK_LAYOUT_YEAR if missing.
    Returns (positions, layout_year_used, layout_url).
    """
    for try_year in (year, FALLBACK_LAYOUT_YEAR):
        url = LAYOUT_URL_TEMPLATE.format(year=try_year)
        try:
            req = _request(url)
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


def _is_zip_file(path: Path) -> bool:
    """Return True if path looks like a local ZIP (PK header)."""
    try:
        with open(path, "rb") as f:
            return f.read(4) == b"PK\x03\x04"
    except OSError:
        return False


def _is_gzip_file(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            return f.read(2) == b"\x1f\x8b"
    except OSError:
        return False


def _download_url_to_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    req = _request(url)
    with urllib.request.urlopen(req, timeout=300) as resp, open(dest, "wb") as out:
        out.write(resp.read())


def decompress_gz_to_dat(gz_path: Path, dat_path: Path) -> None:
    with gzip.open(gz_path, "rb") as gzf, open(dat_path, "wb") as out:
        while True:
            chunk = gzf.read(1 << 20)
            if not chunk:
                break
            out.write(chunk)


def ensure_month_dat_file(year: int, month: int) -> tuple[Path, dict[str, Any]]:
    """
    Return path to the monthly person-record .dat and provenance metadata.

    Tries the official ``monYYpub.zip`` first; if the ZIP is rejected or not a
    valid archive (some months have been observed to return an HTML block page
    from the CDN), falls back to ``monYYpub.dat.gz``.
    """
    base_dir = RAW / str(year)
    stem = month_stem(year, month)
    dat_path = base_dir / f"{stem}.dat"
    zip_path = base_dir / f"{stem}.zip"
    gz_path = base_dir / f"{stem}.dat.gz"
    zip_url = month_zip_url(year, month)
    gz_url = month_dat_gz_url(year, month)

    base_dir.mkdir(parents=True, exist_ok=True)

    meta: dict[str, Any] = {
        "cps_zip_url": zip_url,
        "cps_dat_gz_url": gz_url,
        "local_dat_path": str(dat_path.relative_to(ROOT)).replace("\\", "/"),
    }

    if dat_path.exists() and dat_path.stat().st_size > 1_000_000:
        meta["asset_kind"] = "cached_dat"
        meta["dat_sha256"] = sha256_file(dat_path)
        return dat_path, meta

    zip_ok = zip_path.exists() and _is_zip_file(zip_path)
    if not zip_ok:
        try:
            _download_url_to_file(zip_url, zip_path)
            zip_ok = _is_zip_file(zip_path)
        except (urllib.error.HTTPError, urllib.error.URLError, OSError):
            zip_ok = False
        if not zip_ok and zip_path.exists():
            zip_path.unlink()

    if zip_ok:
        dat_extracted = extract_dat_path(zip_path)
        meta["asset_kind"] = "zip"
        meta["zip_sha256"] = sha256_file(zip_path)
        meta["dat_sha256"] = sha256_file(dat_extracted)
        meta["local_zip_path"] = str(zip_path.relative_to(ROOT)).replace("\\", "/")
        if dat_extracted.resolve() != dat_path.resolve():
            raise RuntimeError(f"Unexpected .dat name in ZIP: {dat_extracted}")
        return dat_path, meta

    if not gz_path.exists() or not _is_gzip_file(gz_path):
        _download_url_to_file(gz_url, gz_path)
    if not _is_gzip_file(gz_path):
        raise RuntimeError(
            f"CPS monthly gzip is invalid after download: {gz_url} -> {gz_path}"
        )

    decompress_gz_to_dat(gz_path, dat_path)
    meta["asset_kind"] = "dat_gz"
    meta["gzip_sha256"] = sha256_file(gz_path)
    meta["dat_sha256"] = sha256_file(dat_path)
    meta["local_gzip_path"] = str(gz_path.relative_to(ROOT)).replace("\\", "/")
    return dat_path, meta


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_dat_path(zip_path: Path) -> Path:
    with zipfile.ZipFile(zip_path, "r") as zf:
        dats = [n for n in zf.namelist() if n.lower().endswith(".dat")]
        if len(dats) != 1:
            raise ValueError(f"Expected one .dat in {zip_path}, got {dats}")
        zf.extract(dats[0], path=zip_path.parent)
        return zip_path.parent / dats[0]


@dataclass
class SliceSpec:
    start: int
    end: int


def load_pr_occ22_tercile() -> tuple[pd.DataFrame, pd.DataFrame]:
    """PRDTOCC1 (1-22) -> occ22_id; occ22_id -> ai_relevance_tercile."""
    cx = pd.read_csv(CROSS)
    pr = cx[cx["source_system"] == "CPS_PRDTOCC1"].copy()
    pr = pr[~pr["is_military_excluded"].astype(str).str.lower().eq("true")]
    pr["prdtocc1"] = pd.to_numeric(pr["source_occ_code"], errors="coerce").astype("Int64")
    pr = pr.dropna(subset=["prdtocc1", "occ22_id"])
    pr_map = pr[["prdtocc1", "occ22_id"]].drop_duplicates("prdtocc1")

    ter = pd.read_csv(TERCILES)
    ter["occ22_id"] = pd.to_numeric(ter["occ22_id"], errors="coerce").astype("Int64")
    ter = ter.dropna(subset=["occ22_id"])
    ter = ter[["occ22_id", "ai_relevance_tercile"]].drop_duplicates("occ22_id")
    return pr_map, ter


def slice_column(raw: pd.Series, spec: SliceSpec) -> pd.Series:
    return raw.str.slice(spec.start, spec.end)


def _iter_dat_chunks(dat_path: Path, chunk_size: int = 50_000) -> Iterator[list[str]]:
    batch: list[str] = []
    with open(dat_path, encoding="latin-1", errors="replace", newline="") as f:
        for line in f:
            s = line.rstrip("\r\n")
            if len(s) >= 1000:
                batch.append(s)
            if len(batch) >= chunk_size:
                yield batch
                batch = []
    if batch:
        yield batch


def weighted_mean_hours(dat_path: Path, positions: dict[str, tuple[int, int]]) -> pd.DataFrame:
    pr_map, ter = load_pr_occ22_tercile()

    specs = {k: SliceSpec(*positions[k]) for k in REQUIRED_FIELDS}

    chunks: list[pd.DataFrame] = []
    for batch in _iter_dat_chunks(dat_path):
        raw = pd.Series(batch, dtype="object")

        year = pd.to_numeric(slice_column(raw, specs["HRYEAR4"]), errors="coerce")
        month = pd.to_numeric(slice_column(raw, specs["HRMONTH"]), errors="coerce")
        age = pd.to_numeric(slice_column(raw, specs["PRTAGE"]), errors="coerce")
        prper = pd.to_numeric(slice_column(raw, specs["PRPERTYP"]), errors="coerce")
        pemlr = pd.to_numeric(slice_column(raw, specs["PEMLR"]), errors="coerce")
        hrs = pd.to_numeric(slice_column(raw, specs["PEHRUSL1"]), errors="coerce")
        occ = pd.to_numeric(slice_column(raw, specs["PRDTOCC1"]), errors="coerce")
        wgt = pd.to_numeric(slice_column(raw, specs["PWCMPWGT"]), errors="coerce")

        df = pd.DataFrame(
            {
                "year": year,
                "month": month,
                "age": age,
                "prpertyp": prper,
                "pemlr": pemlr,
                "pehrusl1": hrs,
                "prdtooc1": occ,
                "pwcmpwgt": wgt,
            }
        )

        m = (
            df["prpertyp"].eq(2)
            & df["age"].ge(16)
            & df["pemlr"].isin([1, 2])
            & df["pehrusl1"].between(1, 99)
            & df["prdtooc1"].between(1, 22)
            & df["pwcmpwgt"].gt(0)
        )
        df = df.loc[m].copy()
        if df.empty:
            continue

        df["weight"] = df["pwcmpwgt"].astype(np.float64) / 10_000.0
        df = df.merge(pr_map, left_on="prdtooc1", right_on="prdtocc1", how="inner")
        df = df.merge(ter, on="occ22_id", how="inner")
        chunks.append(df[["year", "month", "weight", "pehrusl1", "ai_relevance_tercile"]])

    if not chunks:
        return pd.DataFrame(
            columns=["month_str", "ai_relevance_tercile", "mean_usual_weekly_hours", "weight_sum"]
        )

    all_df = pd.concat(chunks, ignore_index=True)
    all_df["w_h"] = all_df["weight"] * all_df["pehrusl1"]
    g = all_df.groupby(["year", "month", "ai_relevance_tercile"], as_index=False).agg(
        sum_w_h=("w_h", "sum"),
        weight_sum=("weight", "sum"),
    )
    g["mean_usual_weekly_hours"] = g["sum_w_h"] / g["weight_sum"]
    g["month_str"] = (
        g["year"].astype(int).astype(str)
        + "-"
        + g["month"].astype(int).astype(str).str.zfill(2)
    )
    return g[
        ["month_str", "ai_relevance_tercile", "mean_usual_weekly_hours", "weight_sum"]
    ]


def discover_months_to_process(today: date) -> list[tuple[int, int]]:
    """
    Months from 2019-01 through the last CPS Basic month with a retrievable file.

    Behavior (see docs/memo_visual_precision.md, section 3):
    - Append (y, m) while Census hosts that month's CPS Basic asset.
    - Skip months listed in ALLOW_MISSING_MONTHS without failing.
    - If the first missing month is at or after today's calendar month index, stop
      (publication lag: files not released yet). This is not treated as an error.
    - If a month before today is missing and not allowlisted, raise (unexpected gap).
    """
    months: list[tuple[int, int]] = []
    y, m = 2019, 1
    today_idx = month_index(today.year, today.month)

    while True:
        if month_asset_available(y, m):
            months.append((y, m))
            y, m = next_month(y, m)
            continue

        if (y, m) in ALLOW_MISSING_MONTHS:
            y, m = next_month(y, m)
            continue

        # Census publication lags: do not treat "no file yet" for months at or
        # beyond the calendar month as a pipeline failure. Stop at the last
        # available month instead (still strict for missing interior months).
        if month_index(y, m) >= today_idx:
            break

        zip_u = month_zip_url(y, m)
        gz_u = month_dat_gz_url(y, m)
        raise RuntimeError(
            "Unexpected missing CPS Basic file (not allowlisted): "
            f"{y}-{m:02d} (tried {zip_u} and {gz_u})"
        )

    return months


def main() -> None:
    today = date.today()
    months = discover_months_to_process(today)

    processed: list[dict[str, Any]] = []
    skipped_missing: list[str] = []
    rows: list[pd.DataFrame] = []

    for y, m in months:
        dat_path, asset_meta = ensure_month_dat_file(y, m)
        layout_pos, layout_year, layout_url = load_layout_for_year(y)

        sub = weighted_mean_hours(dat_path, layout_pos)
        if sub.empty:
            raise RuntimeError(f"No rows after filters for {y}-{m:02d}")

        sub = sub.rename(columns={"month_str": "month", "weight_sum": "sum_composite_weight"})
        rows.append(
            sub[
                [
                    "month",
                    "ai_relevance_tercile",
                    "mean_usual_weekly_hours",
                    "sum_composite_weight",
                ]
            ]
        )

        processed.append(
            {
                "year": y,
                "month": m,
                "asset_kind": asset_meta.get("asset_kind"),
                "cps_zip_url": asset_meta.get("cps_zip_url"),
                "cps_dat_gz_url": asset_meta.get("cps_dat_gz_url"),
                "zip_sha256": asset_meta.get("zip_sha256"),
                "gzip_sha256": asset_meta.get("gzip_sha256"),
                "dat_sha256": asset_meta.get("dat_sha256"),
                "local_dat_path": asset_meta.get("local_dat_path"),
                "local_zip_path": asset_meta.get("local_zip_path"),
                "local_gzip_path": asset_meta.get("local_gzip_path"),
                "layout_year_used": layout_year,
                "layout_url": layout_url,
            }
        )

    for y, m in sorted(ALLOW_MISSING_MONTHS):
        if month_index(y, m) < month_index(2019, 1):
            continue
        if (y, m) in months:
            continue
        skipped_missing.append(f"{y}-{m:02d}")

    if not rows:
        raise RuntimeError("No monthly aggregates produced.")

    out = pd.concat(rows, ignore_index=True)
    ter_order = ["low", "middle", "high"]
    out["ai_relevance_tercile"] = pd.Categorical(
        out["ai_relevance_tercile"], categories=ter_order, ordered=True
    )
    out = out.sort_values(["month", "ai_relevance_tercile"])
    out["ai_relevance_tercile"] = out["ai_relevance_tercile"].astype(str)
    for c in ("mean_usual_weekly_hours", "sum_composite_weight"):
        out[c] = out[c].astype(float).round(12)

    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)

    meta = {
        "output_csv": str(OUT_CSV.relative_to(ROOT)),
        "first_month": "2019-01",
        "last_month": str(out["month"].max()),
        "source_selection_mode": "rolling_latest_allowed_by_ticket",
        "source_selection_rule": (
            "Start at 2019-01 and retain each month with an official CPS Basic "
            "asset available (zip preferred, dat.gz fallback), skipping only "
            "pre-allowlisted official missing months."
        ),
        "months_processed": [f"{p['year']}-{p['month']:02d}" for p in processed],
        "skipped_missing_official": skipped_missing,
        "allow_missing_months": sorted(f"{y}-{m:02d}" for y, m in ALLOW_MISSING_MONTHS),
        "today_run_date": today.isoformat(),
        "cps_basic_base": CPS_BASIC_BASE,
        "public_use_documentation": "https://www2.census.gov/programs-surveys/cps/methodology/PublicUseDocumentation_final.pdf",
        "layout_fallback_year": FALLBACK_LAYOUT_YEAR,
        "files": processed,
    }
    META_JSON.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV} ({len(out)} rows). Metadata: {META_JSON}")


if __name__ == "__main__":
    main()
