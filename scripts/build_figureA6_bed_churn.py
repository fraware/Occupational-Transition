"""
Build Figure A6 BED establishment churn (T-016).

Output:
- figures/figureA6_bed_churn.csv
- intermediate/figureA6_bed_churn_run_metadata.json
"""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "bls" / "bd"
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
CROSS = ROOT / "crosswalks" / "sector6_crosswalk.csv"

OUT_CSV = FIG / "figureA6_bed_churn.csv"
OUT_META = INTER / "figureA6_bed_churn_run_metadata.json"

BD_BASE = "https://download.bls.gov/pub/time.series/bd/"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

MIN_QUARTER = "2019-Q1"

SECTOR6_ORDER = ["MFG", "INF", "FAS", "PBS", "HCS", "RET"]

# Broadest BED-compatible industry groups from frozen crosswalk.
CANONICAL_BED_INDUSTRY_BY_SECTOR6: dict[str, str] = {
    "MFG": "100030",
    "RET": "200020",
    "INF": "200050",
    "FAS": "200060",
    "PBS": "200070",
    "HCS": "200080",
}

# BED employment-rate churn measures (dataclass codes),
# per bd.series title definitions.
MEASURE_MAP = {
    "gross_job_gains_rate": "01",
    "openings_rate": "03",
    "gross_job_losses_rate": "04",
    "closings_rate": "06",
}

META_FILES = [
    "bd.txt",
    "bd.series",
    "bd.industry",
    "bd.ratelevel",
    "bd.periodicity",
    "bd.dataelement",
    "bd.unitanalysis",
    "bd.ownership",
    "bd.seasonal",
]

DATA_CURRENT = "bd.data.0.Current"
DATA_ALL = "bd.data.1.AllItems"

OUT_COLS = [
    "quarter",
    "sector6_code",
    "sector6_label",
    "gross_job_gains_rate",
    "gross_job_losses_rate",
    "openings_rate",
    "closings_rate",
    "gains_series_id",
    "losses_series_id",
    "openings_series_id",
    "closings_series_id",
]


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def fetch_bytes(url: str) -> bytes:
    with urlopen(_request(url), timeout=300) as resp:
        return resp.read()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_row(row: dict[str, str]) -> dict[str, str]:
    return {
        k.strip(): (v.strip() if isinstance(v, str) else v)
        for k, v in row.items()
    }


def load_tsv(text: str) -> list[dict[str, str]]:
    rows = list(csv.DictReader(StringIO(text), delimiter="\t"))
    return [normalize_row(r) for r in rows]


def parse_data_line(line: str) -> tuple[str, str, str, str] | None:
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


def parse_quarter(year_s: str, period: str) -> str | None:
    if not period.startswith("Q") or len(period) != 3:
        return None
    try:
        year = int(year_s)
        q = int(period[1:])
    except ValueError:
        return None
    if q < 1 or q > 4:
        return None
    return f"{year:04d}-Q{q}"


def load_sector6_labels_from_crosswalk() -> dict[str, str]:
    df = pd.read_csv(CROSS)
    sub = df[
        (df["source_program"] == "BED")
        & (df["source_level"] == "bed_industry")
        & (df["is_in_scope"] == 1)
    ][["source_code", "sector6_code", "sector6_label"]].copy()
    out: dict[str, str] = {}
    for sec in SECTOR6_ORDER:
        code = CANONICAL_BED_INDUSTRY_BY_SECTOR6[sec]
        hit = sub[sub["source_code"].astype(str).str.strip() == code]
        if hit.empty:
            raise RuntimeError(
                "missing BED crosswalk mapping row for "
                f"source_code={code}"
            )
        out[sec] = str(hit.iloc[0]["sector6_label"]).strip()
    return out


def resolve_series(
    series_rows: list[dict[str, str]]
) -> dict[str, dict[str, str]]:
    """
    Returns map sector6 -> {measure_key: series_id}.
    """
    out: dict[str, dict[str, str]] = {s: {} for s in SECTOR6_ORDER}
    for sec in SECTOR6_ORDER:
        ind = CANONICAL_BED_INDUSTRY_BY_SECTOR6[sec]
        for measure_key, dataclass in MEASURE_MAP.items():
            hits: list[str] = []
            for r in series_rows:
                if r.get("seasonal") != "S":
                    continue
                if r.get("state_code") != "00":
                    continue
                if r.get("msa_code") != "00000":
                    continue
                if r.get("county_code") != "000":
                    continue
                if r.get("industry_code") != ind:
                    continue
                if r.get("unitanalysis_code") != "1":
                    continue
                if r.get("dataelement_code") != "1":
                    continue
                if r.get("sizeclass_code") != "00":
                    continue
                if r.get("dataclass_code") != dataclass:
                    continue
                if r.get("ratelevel_code") != "R":
                    continue
                if r.get("periodicity_code") != "Q":
                    continue
                if r.get("ownership_code") != "5":
                    continue
                sid = r.get("series_id", "").strip()
                if sid:
                    hits.append(sid)
            if len(hits) != 1:
                raise RuntimeError(
                    "expected one series for "
                    f"sector={sec} measure={measure_key}, "
                    f"got {len(hits)}"
                )
            out[sec][measure_key] = hits[0]
    return out


def load_values_for_series(
    series_ids: set[str], data_text: str
) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {sid: {} for sid in series_ids}
    for line in data_text.splitlines()[1:]:
        parsed = parse_data_line(line)
        if parsed is None:
            continue
        sid_raw, year_s, period, value_raw = parsed
        sid = sid_raw.strip()
        if sid not in series_ids:
            continue
        quarter = parse_quarter(year_s, period)
        if quarter is None or quarter < MIN_QUARTER:
            continue
        try:
            value = float(value_raw)
        except ValueError as exc:
            raise RuntimeError(
                f"non-numeric BED value for {sid} {year_s} {period}: "
                f"{value_raw!r}"
            ) from exc
        out[sid][quarter] = value
    return out


def choose_data_payload(
    series_resolved: dict[str, dict[str, str]]
) -> tuple[str, bytes, dict[str, dict[str, float]], str]:
    needed = {
        sid
        for sec_map in series_resolved.values()
        for sid in sec_map.values()
    }
    cur_url = f"{BD_BASE}{DATA_CURRENT}"
    cur_raw = fetch_bytes(cur_url)
    cur_text = cur_raw.decode("utf-8", "replace")
    cur_vals = load_values_for_series(needed, cur_text)

    # Require at least one retained 2019+ quarter per needed series.
    if all(cur_vals[sid] for sid in needed):
        return DATA_CURRENT, cur_raw, cur_vals, "current"

    all_url = f"{BD_BASE}{DATA_ALL}"
    all_raw = fetch_bytes(all_url)
    all_text = all_raw.decode("utf-8", "replace")
    all_vals = load_values_for_series(needed, all_text)
    missing = [sid for sid in needed if not all_vals[sid]]
    if missing:
        raise RuntimeError(
            "missing series observations in both BED payloads: "
            f"{missing[:6]}"
        )
    return DATA_ALL, all_raw, all_vals, "fallback_to_allitems"


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).isoformat()
    sector_labels = load_sector6_labels_from_crosswalk()

    source_hashes: list[dict[str, str]] = []
    series_text: str | None = None
    for fname in META_FILES:
        url = f"{BD_BASE}{fname}"
        raw = fetch_bytes(url)
        source_hashes.append(
            {"file_name": fname, "url": url, "sha256": sha256_bytes(raw)}
        )
        (RAW / fname).write_bytes(raw)
        if fname == "bd.series":
            series_text = raw.decode("utf-8", "replace")

    if series_text is None:
        raise RuntimeError("bd.series not loaded")

    series_rows = load_tsv(series_text)
    resolved = resolve_series(series_rows)
    payload_name, payload_raw, values_by_sid, payload_mode = (
        choose_data_payload(resolved)
    )
    payload_url = f"{BD_BASE}{payload_name}"
    source_hashes.append(
        {
            "file_name": payload_name,
            "url": payload_url,
            "sha256": sha256_bytes(payload_raw),
        }
    )
    (RAW / payload_name).write_bytes(payload_raw)

    # Keep intersection of available quarters across all sectors and all measures.
    all_quarter_sets: list[set[str]] = []
    for sec in SECTOR6_ORDER:
        for mk in MEASURE_MAP:
            sid = resolved[sec][mk]
            all_quarter_sets.append(set(values_by_sid[sid].keys()))
    common_quarters = (
        sorted(set.intersection(*all_quarter_sets))
        if all_quarter_sets
        else []
    )
    common_quarters = [q for q in common_quarters if q >= MIN_QUARTER]
    if not common_quarters:
        raise RuntimeError(
            "no common quarter coverage across all sector-measure series"
        )

    out_rows: list[dict[str, Any]] = []
    for q in common_quarters:
        for sec in SECTOR6_ORDER:
            sid_g = resolved[sec]["gross_job_gains_rate"]
            sid_l = resolved[sec]["gross_job_losses_rate"]
            sid_o = resolved[sec]["openings_rate"]
            sid_c = resolved[sec]["closings_rate"]
            out_rows.append(
                {
                    "quarter": q,
                    "sector6_code": sec,
                    "sector6_label": sector_labels[sec],
                    "gross_job_gains_rate": values_by_sid[sid_g][q],
                    "gross_job_losses_rate": values_by_sid[sid_l][q],
                    "openings_rate": values_by_sid[sid_o][q],
                    "closings_rate": values_by_sid[sid_c][q],
                    "gains_series_id": sid_g,
                    "losses_series_id": sid_l,
                    "openings_series_id": sid_o,
                    "closings_series_id": sid_c,
                }
            )

    out_rows.sort(
        key=lambda r: (r["quarter"], SECTOR6_ORDER.index(r["sector6_code"]))
    )
    pd.DataFrame(out_rows, columns=OUT_COLS).to_csv(OUT_CSV, index=False)

    measure_mapping = {
        "gross_job_gains_rate": {
            "dataclass_code": "01",
            "ratelevel_code": "R",
            "dataelement_code": "1",
        },
        "openings_rate": {
            "dataclass_code": "03",
            "ratelevel_code": "R",
            "dataelement_code": "1",
        },
        "gross_job_losses_rate": {
            "dataclass_code": "04",
            "ratelevel_code": "R",
            "dataelement_code": "1",
        },
        "closings_rate": {
            "dataclass_code": "06",
            "ratelevel_code": "R",
            "dataelement_code": "1",
        },
    }

    retained_series: list[dict[str, str]] = []
    for sec in SECTOR6_ORDER:
        retained_series.append(
            {
                "sector6_code": sec,
                "bed_industry_code": CANONICAL_BED_INDUSTRY_BY_SECTOR6[sec],
                "gains_series_id": resolved[sec]["gross_job_gains_rate"],
                "losses_series_id": resolved[sec]["gross_job_losses_rate"],
                "openings_series_id": resolved[sec]["openings_rate"],
                "closings_series_id": resolved[sec]["closings_rate"],
            }
        )

    meta = {
        "ticket": "T-016",
        "generated_at_utc": generated_at,
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "crosswalk_file": str(CROSS.relative_to(ROOT)).replace("\\", "/"),
        "assertion_published_bed_only": (
            "Only published BLS BED national seasonally adjusted quarterly rate series "
            "were retained; no reconstruction from microdata."
        ),
        "series_filters": {
            "seasonal": "S",
            "state_code": "00",
            "msa_code": "00000",
            "county_code": "000",
            "unitanalysis_code": "1",
            "dataelement_code": "1",
            "sizeclass_code": "00",
            "ratelevel_code": "R",
            "periodicity_code": "Q",
            "ownership_code": "5",
        },
        "measure_code_mapping": measure_mapping,
        "canonical_bed_industry_by_sector6": CANONICAL_BED_INDUSTRY_BY_SECTOR6,
        "data_payload_used": payload_name,
        "data_payload_mode": payload_mode,
        "quarter_window": {
            "min_requested": MIN_QUARTER,
            "first_quarter_in_output": common_quarters[0],
            "last_quarter_in_output": common_quarters[-1],
        },
        "source_files_sha256": source_hashes,
        "retained_series": retained_series,
        "row_count": len(out_rows),
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV} ({len(out_rows)} rows)")
    print(f"Wrote {OUT_META}")


if __name__ == "__main__":
    main()
