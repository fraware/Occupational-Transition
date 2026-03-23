"""
Build Figure A8 LEHD public benchmark (T-018).

Output:
- figures/figureA8_lehd_benchmark.csv
- intermediate/figureA8_lehd_benchmark_run_metadata.json
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "lehd" / "j2j"
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"

OUT_CSV = FIG / "figureA8_lehd_benchmark.csv"
OUT_META = INTER / "figureA8_lehd_benchmark_run_metadata.json"

US_INDEX_URL = "https://lehd.ces.census.gov/data/j2j/latest_release/us/"
MANIFEST_URL = (
    "https://lehd.ces.census.gov/data/j2j/latest_release/us/j2jr/"
    "j2jr_us_manifest.txt"
)
DATA_URL = (
    "https://lehd.ces.census.gov/data/j2j/latest_release/us/j2jr/"
    "j2jr_us_d_f_gn_n_oslp_s.csv.gz"
)

MIN_QUARTER = "2019-Q1"

OUT_COLS = [
    "quarter",
    "benchmark_series_key",
    "benchmark_series_label",
    "benchmark_rate",
    "source_program",
    "source_series_id",
]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def fetch_bytes(url: str) -> bytes:
    with urlopen(_request(url), timeout=600) as resp:
        return resp.read()


def fetch_with_cache(url: str, path: Path) -> bytes:
    if path.is_file():
        return path.read_bytes()
    raw = fetch_bytes(url)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return raw


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _quarter_key(year_s: str, q_s: str) -> str | None:
    try:
        year = int(year_s)
        q = int(q_s)
    except ValueError:
        return None
    if q < 1 or q > 4:
        return None
    return f"{year:04d}-Q{q}"


def _qtuple(q: str) -> tuple[int, int]:
    y, qq = q.split("-Q")
    return int(y), int(qq)


def _is_contiguous_quarters(vals: list[str]) -> bool:
    if not vals:
        return False
    for i in range(1, len(vals)):
        py, pq = _qtuple(vals[i - 1])
        ny, nq = _qtuple(vals[i])
        ey, eq = (py + 1, 1) if pq == 4 else (py, pq + 1)
        if (ny, nq) != (ey, eq):
            return False
    return True


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).isoformat()

    index_raw = fetch_with_cache(
        US_INDEX_URL, RAW / "latest_release_us_index.html"
    )
    manifest_raw = fetch_with_cache(MANIFEST_URL, RAW / "j2jr_us_manifest.txt")
    data_raw = fetch_with_cache(
        DATA_URL, RAW / "j2jr_us_d_f_gn_n_oslp_s.csv.gz"
    )

    manifest_text = manifest_raw.decode("utf-8", "replace")
    if "j2jr_us_d_f_gn_n_oslp_s.csv.gz" not in manifest_text:
        raise RuntimeError("selected J2JR compact file missing from manifest")

    with gzip.GzipFile(fileobj=io.BytesIO(data_raw)) as gz:
        text = io.TextIOWrapper(gz, encoding="utf-8", errors="replace")
        rdr = csv.DictReader(text)
        required = {
            "periodicity",
            "seasonadj",
            "geo_level",
            "geography",
            "ind_level",
            "industry",
            "ownercode",
            "sex",
            "agegrp",
            "race",
            "ethnicity",
            "education",
            "firmage",
            "firmsize",
            "year",
            "quarter",
            "agg_level",
            "J2JHireR",
        }
        if not rdr.fieldnames or not required.issubset(set(rdr.fieldnames)):
            raise RuntimeError(
                "unexpected J2JR schema; missing required columns "
                f"{sorted(required - set(rdr.fieldnames or []))}"
            )

        rows: list[dict[str, str]] = []
        for row in rdr:
            if row["periodicity"] != "Q":
                continue
            if row["seasonadj"] != "S":
                continue
            if row["geo_level"] != "N" or row["geography"] != "00":
                continue
            if row["ind_level"] != "A" or row["industry"] != "00":
                continue
            if row["ownercode"] != "A00":
                continue
            if row["sex"] != "0":
                continue
            if row["agegrp"] != "A00":
                continue
            if row["race"] != "A0":
                continue
            if row["ethnicity"] != "A0":
                continue
            if row["education"] != "E0":
                continue
            if row["firmage"] != "0":
                continue
            if row["firmsize"] != "0":
                continue
            if row["agg_level"] != "1":
                continue
            q = _quarter_key(row["year"], row["quarter"])
            if q is None or q < MIN_QUARTER:
                continue
            val_s = row.get("J2JHireR", "").strip()
            if not val_s:
                continue
            try:
                val = float(val_s)
            except ValueError:
                continue
            rows.append({"quarter": q, "benchmark_rate": val})

    if not rows:
        raise RuntimeError("no benchmark rows retained from J2JR source")

    out = pd.DataFrame(rows).drop_duplicates(subset=["quarter"]).copy()
    out = out.sort_values("quarter").reset_index(drop=True)
    quarters = out["quarter"].astype(str).tolist()
    if not _is_contiguous_quarters(quarters):
        raise RuntimeError("retained quarter series is not contiguous")

    out["benchmark_series_key"] = "j2j_job_to_job_flow_rate"
    out["benchmark_series_label"] = "J2JHireR (seasonally adjusted, national)"
    out["source_program"] = "LEHD_J2JR"
    out["source_series_id"] = "j2jr_us_d_f_gn_n_oslp_s:J2JHireR"
    out = out[OUT_COLS]
    out.to_csv(OUT_CSV, index=False)

    meta = {
        "ticket": "T-018",
        "generated_at_utc": generated_at,
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "benchmark_series_key": "j2j_job_to_job_flow_rate",
        "benchmark_series_label": "J2JHireR (seasonally adjusted, national)",
        "source_series_id": "j2jr_us_d_f_gn_n_oslp_s:J2JHireR",
        "selection_rule": (
            "Use published LEHD J2JR compact seasonally adjusted file "
            "and retain J2JHireR directly for 2019-Q1 onward."
        ),
        "filters": {
            "periodicity": "Q",
            "seasonadj": "S",
            "geo_level": "N",
            "geography": "00",
            "ind_level": "A",
            "industry": "00",
            "ownercode": "A00",
            "sex": "0",
            "agegrp": "A00",
            "race": "A0",
            "ethnicity": "A0",
            "education": "E0",
            "firmage": "0",
            "firmsize": "0",
            "agg_level": "1",
        },
        "quarter_window": {
            "min_requested": MIN_QUARTER,
            "first_quarter_in_output": quarters[0],
            "last_quarter_in_output": quarters[-1],
        },
        "assertion_published_direct_rate_only": (
            "Benchmark uses published LEHD J2JR J2JHireR values directly "
            "without microdata reconstruction or synthetic ratio creation."
        ),
        "source_files_sha256": [
            {
                "file_name": "latest_release_us_index.html",
                "url": US_INDEX_URL,
                "sha256": sha256_bytes(index_raw),
            },
            {
                "file_name": "j2jr_us_manifest.txt",
                "url": MANIFEST_URL,
                "sha256": sha256_bytes(manifest_raw),
            },
            {
                "file_name": "j2jr_us_d_f_gn_n_oslp_s.csv.gz",
                "url": DATA_URL,
                "sha256": sha256_bytes(data_raw),
            },
        ],
        "row_count": int(len(out)),
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV} ({len(out)} rows)")
    print(f"Wrote {OUT_META}")


if __name__ == "__main__":
    main()
