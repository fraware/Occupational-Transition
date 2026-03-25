"""
Build Figure A9 local occupational composition from ACS PUMS.

Outputs:
- figures/figureA9_acs_local_composition.csv
- intermediate/figureA9_acs_local_composition_run_metadata.json
"""

from __future__ import annotations

import bisect
import csv
import hashlib
import io
import json
import re
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "acs" / "pums"
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"

OUT_CSV = FIG / "figureA9_acs_local_composition.csv"
OUT_META = INTER / "figureA9_acs_local_composition_run_metadata.json"

SOURCE_DIR_URL = (
    "https://www2.census.gov/programs-surveys/acs/data/pums/"
)
PUMS_PERSON_ZIP_NAME = "csv_pus.zip"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

CROSSWALK_FILE = ROOT / "crosswalks" / "occ22_crosswalk.csv"
AI_TERCILES_FILE = INTER / "ai_relevance_terciles.csv"

OUT_COLS_PREFIX = [
    "acs_year",
    "puma",
    "population_weight_sum",
    "high_ai_tercile_share",
    "middle_ai_tercile_share",
    "low_ai_tercile_share",
    "occ22_share_sum_check",
]

SECTER_ORD = [str(i) for i in range(1, 23)]
OCC22_SHARE_COLS = [f"occ22_share_{i}" for i in SECTER_ORD]

OUT_COLS = OUT_COLS_PREFIX + OCC22_SHARE_COLS

AI_TERCILE_ORDER = ["low", "middle", "high"]


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def sha256_file_stream(path: Path, chunk_size: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def download_to_cache_stream(url: str, local_path: Path, timeout_s: int = 600) -> str:
    local_path.parent.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha256()
    with urlopen(_request(url), timeout=timeout_s) as resp, local_path.open("wb") as f:
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
            h.update(chunk)
    return h.hexdigest()


def select_latest_acs_pums_person_zip() -> tuple[int, str, str]:
    """
    Returns (acs_year, variant_dir, full_zip_url).
    Selection rule:
    - Consider year directories under /programs-surveys/acs/data/pums/
    - Prefer 1-Year over 5-Year for the chosen latest year.
    """
    import re

    html = urlopen(_request(SOURCE_DIR_URL), timeout=60).read().decode(
        "utf-8", errors="replace"
    )
    years = [int(m.group(1)) for m in re.finditer(r"href=['\"](\d{4})/['\"]", html)]
    if not years:
        raise RuntimeError("could not parse ACS PUMS year directories")

    for year in sorted(set(years), reverse=True):
        for variant in ["1-Year", "5-Year"]:
            zip_url = f"{SOURCE_DIR_URL}{year}/{variant}/{PUMS_PERSON_ZIP_NAME}"
            try:
                # Only validate existence; do not download the full payload here.
                # Use a tiny byte-range request when supported.
                req = Request(
                    zip_url,
                    headers={"User-Agent": USER_AGENT, "Range": "bytes=0-1"},
                )
                with urlopen(req, timeout=60) as resp:
                    resp.read(2)
                    return year, variant, zip_url
            except Exception:
                continue

    raise RuntimeError("could not resolve an ACS PUMS person zip")


def parse_range(range_s: str) -> tuple[int, int]:
    s = str(range_s).strip()
    if not s:
        raise ValueError("empty range")
    if "-" in s:
        a, b = s.split("-", 1)
        return int(a), int(b)
    if s.isdigit():
        v = int(s)
        return v, v
    raise ValueError(f"unrecognized range format: {s!r}")


def build_occ22_interval_index(crosswalk_df: pd.DataFrame) -> list[tuple[int, int, int]]:
    """
    Build sorted list of (start_code, end_code, occ22_id) intervals.
    Assumes the 22-group mapping is a clean non-overlapping partition over
    the Census occupation code universe.
    """
    intervals: list[tuple[int, int, int]] = []
    # The crosswalk has many rows per occupation title code, but it should
    # define exactly one Census occupation-code interval per occ22_id.
    for oid, g in crosswalk_df.groupby("occ22_id", dropna=False):
        if pd.isna(oid):
            continue
        vals = [str(x).strip() for x in g["census_occ_code_range"].tolist()]
        vals = [v for v in vals if v and v.lower() != "nan"]
        if not vals:
            raise RuntimeError(f"missing census_occ_code_range for occ22_id={oid}")
        # Prefer explicit hyphenated ranges when present.
        chosen = next((v for v in vals if "-" in v), vals[0])
        start, end = parse_range(chosen)
        intervals.append((start, end, int(oid)))

    intervals.sort(key=lambda x: x[0])
    return intervals


def select_pums_person_csv_members(all_members: list[str]) -> list[str]:
    """
    Identify all person-level PUMS CSV/TXT members inside csv_pus.zip.

    Census typically ships national person microdata as split files
    (e.g. psam_pusa.csv, psam_pusb.csv). Older or single-file releases may
    expose one psam_pus.csv. Using only the first lexicographic member would
    silently drop geography splits.
    """
    csv_txt = [m for m in all_members if m.lower().endswith((".csv", ".txt"))]
    split_pat = re.compile(r"psam_pus[a-z]\.(csv|txt)$", re.IGNORECASE)
    split_members = [m for m in csv_txt if split_pat.search(m.split("/")[-1])]
    if split_members:
        return sorted(split_members)
    single_pat = re.compile(r"^psam_pus\.(csv|txt)$", re.IGNORECASE)
    single = [m for m in csv_txt if single_pat.match(m.split("/")[-1])]
    if single:
        return sorted(single)
    if len(csv_txt) == 1:
        return csv_txt
    raise RuntimeError(
        "could not identify PUMS person CSV members in csv_pus.zip "
        f"(expected psam_pus*.csv split files or a single table); got {csv_txt!r}"
    )


def accumulate_pums_rows_from_reader(
    rdr: csv.DictReader,
    intervals: list[tuple[int, int, int]],
    ai_map: dict[int, str],
    use_esr_filter: bool,
    total_w_by_puma: defaultdict[str, float],
    occ_w_by_puma: dict[str, list[float]],
    ai_w_by_puma: dict[str, dict[str, float]],
) -> None:
    for row in rdr:
        puma_raw = str(row.get("PUMA", "")).strip()
        if not puma_raw or not puma_raw.isdigit():
            continue
        puma = puma_raw.zfill(5)
        if puma == "00000":
            continue

        pwgt_raw = str(row.get("PWGTP", "")).strip()
        if not pwgt_raw:
            continue
        try:
            pwgt = float(pwgt_raw)
        except ValueError:
            continue
        if pwgt <= 0:
            continue

        if use_esr_filter:
            esr_raw = str(row.get("ESR", "")).strip()
            if esr_raw and esr_raw.isdigit() and int(esr_raw) != 1:
                continue

        occ_raw = str(row.get("OCCP", "")).strip()
        if not occ_raw or not occ_raw.isdigit():
            continue
        try:
            occ_code = int(occ_raw)
        except ValueError:
            continue

        occ22_id = occ22_id_from_code(occ_code, intervals)
        if occ22_id is None:
            continue

        total_w_by_puma[puma] += pwgt
        if puma not in occ_w_by_puma:
            occ_w_by_puma[puma] = [0.0] * 22
        idx = occ22_id - 1
        occ_w_by_puma[puma][idx] += pwgt

        terc = ai_map[occ22_id]
        if puma not in ai_w_by_puma:
            ai_w_by_puma[puma] = {t: 0.0 for t in AI_TERCILE_ORDER}
        ai_w_by_puma[puma][terc] += pwgt


def occ22_id_from_code(occ_code: int, intervals: list[tuple[int, int, int]]) -> int | None:
    starts = [s for s, _, _ in intervals]
    idx = bisect.bisect_right(starts, occ_code) - 1
    if idx < 0:
        return None
    start, end, occ22_id = intervals[idx]
    if start <= occ_code <= end:
        return occ22_id
    return None


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).isoformat()

    if not CROSSWALK_FILE.is_file():
        raise RuntimeError(f"missing crosswalk: {CROSSWALK_FILE}")
    if not AI_TERCILES_FILE.is_file():
        raise RuntimeError(f"missing ai terciles: {AI_TERCILES_FILE}")

    crosswalk_df = pd.read_csv(CROSSWALK_FILE)
    required_cols = {"census_occ_code_range", "occ22_id"}
    if not required_cols.issubset(set(crosswalk_df.columns)):
        raise RuntimeError(f"occ22 crosswalk missing columns {required_cols}")

    intervals = build_occ22_interval_index(crosswalk_df)
    occ22_ids = sorted({int(x[2]) for x in intervals})
    if occ22_ids != list(range(1, 23)):
        raise RuntimeError(f"expected occ22_id 1..22, got {occ22_ids}")

    ai_df = pd.read_csv(AI_TERCILES_FILE)
    if "occ22_id" not in ai_df.columns or "ai_relevance_tercile" not in ai_df.columns:
        raise RuntimeError("ai_relevance_terciles.csv missing required columns")
    ai_map = {int(r["occ22_id"]): str(r["ai_relevance_tercile"]) for _, r in ai_df.iterrows()}
    if set(ai_map.keys()) != set(range(1, 23)):
        raise RuntimeError("ai tercile mapping must cover occ22_id 1..22")

    acs_year, acs_variant_dir, zip_url = select_latest_acs_pums_person_zip()
    suffix = "1yr" if acs_variant_dir == "1-Year" else "5yr"
    local_zip = RAW / f"acs_pums_{acs_year}_{suffix}_{PUMS_PERSON_ZIP_NAME}"
    if local_zip.is_file():
        zip_sha = sha256_file_stream(local_zip)
    else:
        zip_sha = download_to_cache_stream(zip_url, local_zip)

    with zipfile.ZipFile(local_zip) as zf:
        members = zf.namelist()
        person_members = select_pums_person_csv_members(members)

        total_w_by_puma: defaultdict[str, float] = defaultdict(float)
        occ_w_by_puma: dict[str, list[float]] = {}
        ai_w_by_puma: dict[str, dict[str, float]] = {}

        needed = {"PUMA", "PWGTP", "OCCP"}
        use_esr_filter = False
        fieldnames_set: set[str] | None = None

        for data_name in person_members:
            with zf.open(data_name, "r") as f:
                text = io.TextIOWrapper(f, encoding="utf-8", errors="replace")
                rdr = csv.DictReader(text)
                if not rdr.fieldnames:
                    raise RuntimeError(
                        f"ACS PUMS reader missing fieldnames in {data_name!r}"
                    )
                fn = set(rdr.fieldnames)
                if fieldnames_set is None:
                    fieldnames_set = fn
                    if not needed.issubset(fn):
                        missing = sorted(needed - fn)
                        raise RuntimeError(
                            f"ACS PUMS missing required columns: {missing}"
                        )
                    use_esr_filter = "ESR" in fn
                elif fn != fieldnames_set:
                    raise RuntimeError(
                        "ACS PUMS column set differs between zip members: "
                        f"{sorted(fn ^ fieldnames_set)}"
                    )

                accumulate_pums_rows_from_reader(
                    rdr,
                    intervals,
                    ai_map,
                    use_esr_filter,
                    total_w_by_puma,
                    occ_w_by_puma,
                    ai_w_by_puma,
                )

    if not total_w_by_puma:
        raise RuntimeError("ACS aggregation produced zero PUMA totals")

    pumas = sorted(total_w_by_puma.keys())

    out_rows: list[dict[str, Any]] = []
    for puma in pumas:
        tot = float(total_w_by_puma[puma])
        if tot <= 0:
            continue

        occ_shares = [w / tot for w in occ_w_by_puma[puma]]
        occ_sum_check = float(sum(occ_shares))
        ai_shares = {t: ai_w_by_puma[puma].get(t, 0.0) / tot for t in AI_TERCILE_ORDER}

        row: dict[str, Any] = {
            "acs_year": acs_year,
            "puma": puma,
            "population_weight_sum": tot,
            "high_ai_tercile_share": ai_shares["high"],
            "middle_ai_tercile_share": ai_shares["middle"],
            "low_ai_tercile_share": ai_shares["low"],
            "occ22_share_sum_check": occ_sum_check,
        }
        for i, share in enumerate(occ_shares, start=1):
            row[f"occ22_share_{i}"] = share
        out_rows.append(row)

    if not out_rows:
        raise RuntimeError("no output rows after filtering totals")

    out_df = pd.DataFrame(out_rows, columns=OUT_COLS)
    out_df = out_df.sort_values(["puma"]).reset_index(drop=True)
    out_df.to_csv(OUT_CSV, index=False)

    meta = {
        "ticket": "T-019",
        "generated_at_utc": generated_at,
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "acs_year": acs_year,
        "selected_acs_source": {
            "source_dir_url": SOURCE_DIR_URL,
            "acs_variant_dir": acs_variant_dir,
            "person_file_name": PUMS_PERSON_ZIP_NAME,
            "person_csv_members": person_members,
            "person_file_member": person_members[0],
            "person_zip_url": zip_url,
        },
        "source_selection_mode": "rolling_latest_allowed_by_ticket",
        "source_selection_rule": (
            "From ACS PUMS year directories, choose the latest available year "
            "and prefer 1-Year over 5-Year when both exist."
        ),
        "crosswalk_file": str(CROSSWALK_FILE.relative_to(ROOT)).replace("\\", "/"),
        "crosswalk_sha256": sha256_file_stream(CROSSWALK_FILE),
        "ai_terciles_file": str(AI_TERCILES_FILE.relative_to(ROOT)).replace("\\", "/"),
        "ai_terciles_sha256": sha256_file_stream(AI_TERCILES_FILE),
        "source_files_sha256": [
            {
                "file_name": local_zip.name,
                "url": zip_url,
                "sha256": zip_sha,
                "local_cache_path": str(local_zip.relative_to(ROOT)).replace("\\", "/"),
            },
        ],
        "filters": {
            "employment_filter": "ESR==1 if ESR exists in input; otherwise no ESR filter",
            "puma_filter": "PUMA is 5-digit numeric and != 00000",
            "occupation_filter": "OCCP mapped to frozen occ22 via census_occ_code_range intervals",
        },
        "weighting": {
            "weight_variable": "PWGTP",
            "normalization": "shares computed as category_weight / total_valid_person_weight_per_PUMA",
        },
        "row_count": int(len(out_df)),
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV} ({len(out_df)} rows)")
    print(f"Wrote {OUT_META}")


if __name__ == "__main__":
    main()

