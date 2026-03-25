"""BLS LABSTAT JOLTS time-series helpers (national SA published rates)."""

from __future__ import annotations

import csv
from io import StringIO
from pathlib import Path

from occupational_transition.http import download_to_path, raw_cache_root

JOLTS_BASE = "https://download.bls.gov/pub/time.series/jt/"

# All LABSTAT inputs required for provenance (including reference files for QA).
PROVENANCE_FILES: list[str] = [
    "jt.series",
    "jt.industry",
    "jt.period",
    "jt.seasonal",
    "jt.data.2.JobOpenings",
    "jt.data.3.Hires",
    "jt.data.5.Quits",
    "jt.data.6.LayoffsDischarges",
]

# JOLTS data files (LABSTAT) keyed by two-character dataelement_code.
DATA_FILE_BY_DATAELEMENT: dict[str, str] = {
    "JO": "jt.data.2.JobOpenings",
    "HI": "jt.data.3.Hires",
    "QU": "jt.data.5.Quits",
    "LD": "jt.data.6.LayoffsDischarges",
}

DATAELEMENT_TO_RATE_NAME: dict[str, str] = {
    "JO": "job_openings_rate",
    "HI": "hires_rate",
    "QU": "quits_rate",
    "LD": "layoffs_discharges_rate",
}


def normalize_jt_row(row: dict[str, str]) -> dict[str, str]:
    return {
        k.strip(): (v.strip() if isinstance(v, str) else v)
        for k, v in row.items()
    }


def load_jt_series_table(text: str) -> list[dict[str, str]]:
    rows = list(csv.DictReader(StringIO(text), delimiter="\t"))
    return [normalize_jt_row(r) for r in rows]


def period_to_month(year_s: str, period: str) -> str | None:
    if not period.startswith("M") or len(period) != 3:
        return None
    try:
        m = int(period[1:], 10)
    except ValueError:
        return None
    if m < 1 or m > 12:
        return None
    try:
        y = int(year_s, 10)
    except ValueError:
        return None
    return f"{y:04d}-{m:02d}"


def parse_data_line(line: str) -> tuple[str, str, str, str] | None:
    """Return (series_id, year, period, value_raw) or None."""
    if not line.strip():
        return None
    parts = line.split("\t")
    if len(parts) < 4:
        return None
    return (
        parts[0].strip(),
        parts[1].strip(),
        parts[2].strip(),
        parts[3].strip(),
    )

def jt_file_path(file_name: str, *, raw_dir: Path | None = None) -> Path:
    raw_dir = raw_dir if raw_dir is not None else raw_cache_root()
    return raw_dir / file_name


def ensure_jt_file(
    file_name: str,
    *,
    raw_dir: Path | None = None,
    timeout: float = 300.0,
    skip_if_exists_min_bytes: int = 10_000,
) -> Path:
    raw_dir = raw_dir if raw_dir is not None else raw_cache_root()
    dest = jt_file_path(file_name, raw_dir=raw_dir)
    url = f"{JOLTS_BASE}{file_name}"
    download_to_path(
        url,
        dest,
        timeout=timeout,
        extra_headers={"Referer": "https://www.bls.gov/"},
        skip_if_exists_min_bytes=skip_if_exists_min_bytes,
    )
    return dest


def fetch_jolts_file_bytes(
    file_name: str,
    *,
    timeout: float = 300.0,
    raw_dir: Path | None = None,
) -> bytes:
    dest = ensure_jt_file(
        file_name,
        raw_dir=raw_dir,
        timeout=timeout,
        skip_if_exists_min_bytes=1,
    )
    return dest.read_bytes()


def fetch_provenance_payloads(
    file_names: list[str] | None = None,
    *,
    timeout: float = 300.0,
    raw_dir: Path | None = None,
) -> list[tuple[str, bytes]]:
    """Return (file_name, raw_bytes) for each LABSTAT file."""
    names = file_names if file_names is not None else PROVENANCE_FILES
    out: list[tuple[str, bytes]] = []
    for fname in names:
        out.append(
            (
                fname,
                fetch_jolts_file_bytes(
                    fname,
                    timeout=timeout,
                    raw_dir=raw_dir,
                ),
            )
        )
    return out


def stream_data_file_observations(
    file_name: str,
    series_ids: set[str],
    *,
    min_month: str | None = None,
    timeout: float = 300.0,
    raw_dir: Path | None = None,
) -> dict[str, list[tuple[str, float]]]:
    """
    Parse a JOLTS jt.data.* file and return series_id -> [(month, value), ...].

    The implementation is streaming at the TSV line level (no whole-file
    dataframe materialization).
    """
    raw = fetch_jolts_file_bytes(
        file_name,
        timeout=timeout,
        raw_dir=raw_dir,
    )
    text = raw.decode("utf-8", "replace")
    values_by_series: dict[str, list[tuple[str, float]]] = {}
    for line in text.splitlines()[1:]:
        parsed = parse_data_line(line)
        if parsed is None:
            continue
        sid, year_s, period, val_raw = parsed
        if sid not in series_ids:
            continue
        month = period_to_month(year_s, period)
        if month is None:
            continue
        if min_month is not None and month < min_month:
            continue
        try:
            val = float(val_raw)
        except ValueError as e:
            raise RuntimeError(
                f"non-numeric value for {sid} {year_s} {period}: {val_raw!r}"
            ) from e
        values_by_series.setdefault(sid, []).append((month, val))
    return values_by_series
