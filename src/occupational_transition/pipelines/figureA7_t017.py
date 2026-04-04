"""
Build Figure A7 QCEW state benchmark (T-017).

Output:
- figures/figureA7_qcew_state_benchmark.csv
- intermediate/figureA7_qcew_state_benchmark_run_metadata.json
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

import pandas as pd


@dataclass(frozen=True)
class FigureA7Layout:
    root: Path
    raw: Path
    fig: Path
    inter: Path
    cross: Path
    out_csv: Path
    out_meta: Path


def _figure_a7_layout(root: Path) -> FigureA7Layout:
    fig = root / "figures"
    inter = root / "intermediate"
    return FigureA7Layout(
        root=root,
        raw=root / "raw" / "bls" / "qcew",
        fig=fig,
        inter=inter,
        cross=root / "crosswalks" / "sector6_crosswalk.csv",
        out_csv=fig / "figureA7_qcew_state_benchmark.csv",
        out_meta=inter / "figureA7_qcew_state_benchmark_run_metadata.json",
    )


def run(root: Path) -> None:
    build_figure_a7_qcew_state_benchmark(_figure_a7_layout(root))


QCEW_DOWNLOADS = "https://www.bls.gov/cew/downloadable-data-files.htm"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

SECTOR6_ORDER = ["MFG", "INF", "FAS", "PBS", "HCS", "RET"]
OUT_COLS = [
    "qcew_year",
    "qcew_quarter",
    "state_fips",
    "state_name",
    "sector6_code",
    "sector6_label",
    "sector_employment",
    "state_total_employment",
    "state_sector_employment_share",
    "average_weekly_wage",
    "source_industry_aggregation_note",
]

STATE_NAME_BY_FIPS = {
    "01": "Alabama",
    "02": "Alaska",
    "04": "Arizona",
    "05": "Arkansas",
    "06": "California",
    "08": "Colorado",
    "09": "Connecticut",
    "10": "Delaware",
    "11": "District of Columbia",
    "12": "Florida",
    "13": "Georgia",
    "15": "Hawaii",
    "16": "Idaho",
    "17": "Illinois",
    "18": "Indiana",
    "19": "Iowa",
    "20": "Kansas",
    "21": "Kentucky",
    "22": "Louisiana",
    "23": "Maine",
    "24": "Maryland",
    "25": "Massachusetts",
    "26": "Michigan",
    "27": "Minnesota",
    "28": "Mississippi",
    "29": "Missouri",
    "30": "Montana",
    "31": "Nebraska",
    "32": "Nevada",
    "33": "New Hampshire",
    "34": "New Jersey",
    "35": "New Mexico",
    "36": "New York",
    "37": "North Carolina",
    "38": "North Dakota",
    "39": "Ohio",
    "40": "Oklahoma",
    "41": "Oregon",
    "42": "Pennsylvania",
    "44": "Rhode Island",
    "45": "South Carolina",
    "46": "South Dakota",
    "47": "Tennessee",
    "48": "Texas",
    "49": "Utah",
    "50": "Vermont",
    "51": "Virginia",
    "53": "Washington",
    "54": "West Virginia",
    "55": "Wisconsin",
    "56": "Wyoming",
}


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def fetch_bytes(url: str) -> bytes:
    with urlopen(_request(url), timeout=600) as resp:
        return resp.read()


def fetch_with_cache(url: str, path: Path) -> bytes:
    if path.is_file():
        return path.read_bytes()
    data = fetch_bytes(url)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_latest_qtrly_singlefile_url(download_page_html: str) -> tuple[str, int]:
    matches = re.findall(
        r"https://data\.bls\.gov/cew/data/files/(\d{4})/csv/\1_qtrly_singlefile\.zip",
        download_page_html,
    )
    if not matches:
        raise RuntimeError("could not locate qtrly_singlefile links on QCEW page")
    years = sorted({int(y) for y in matches})
    y = years[-1]
    url = f"https://data.bls.gov/cew/data/files/{y}/csv/{y}_qtrly_singlefile.zip"
    return url, y


def load_qcew_sector6_map(cross: Path) -> dict[str, tuple[str, str]]:
    df = pd.read_csv(cross)
    sub = df[
        (df["source_program"] == "QCEW")
        & (df["source_level"] == "qcew_naics2_via_ces")
        & (df["is_in_scope"] == 1)
    ][["source_code", "sector6_code", "sector6_label"]].copy()
    out: dict[str, tuple[str, str]] = {}
    for _, row in sub.iterrows():
        raw_src = str(row["source_code"]).strip()
        src = raw_src.split("_")[-1]
        sec = str(row["sector6_code"]).strip()
        lbl = str(row["sector6_label"]).strip()
        out[src] = (sec, lbl)
    expected = set(SECTOR6_ORDER)
    got = {v[0] for v in out.values()}
    if got != expected:
        raise RuntimeError(
            "QCEW crosswalk sector set mismatch: "
            f"expected {sorted(expected)}, got {sorted(got)}"
        )
    return out


def state_fips_from_area(area_fips: str) -> str | None:
    code = area_fips.strip()
    if len(code) != 5 or not code.isdigit():
        return None
    if code[2:] != "000":
        return None
    if code == "00000":
        return None
    return code[:2]


def naics2_from_industry_code(industry_code: str) -> str | None:
    s = industry_code.strip()
    if len(s) >= 2 and s[:2].isdigit():
        return s[:2]
    return None


def quarter_rank(q: str) -> int:
    try:
        qq = int(q)
    except ValueError:
        return -1
    if qq < 1 or qq > 4:
        return -1
    return qq


def parse_qtrly_singlefile(
    zip_bytes: bytes,
    sector_map: dict[str, tuple[str, str]],
) -> tuple[list[dict[str, Any]], int, str]:
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        names = zf.namelist()
        if not names:
            raise RuntimeError("empty qtrly_singlefile zip")
        data_name = names[0]
        with zf.open(data_name, "r") as f:
            txt = io.TextIOWrapper(f, encoding="utf-8", errors="replace")
            rdr = csv.DictReader(txt)
            required = {
                "area_fips",
                "own_code",
                "industry_code",
                "year",
                "qtr",
                "month3_emplvl",
                "avg_wkly_wage",
            }
            if not rdr.fieldnames or not required.issubset(set(rdr.fieldnames)):
                raise RuntimeError(
                    "qcew quarterly header missing required columns; "
                    f"got={rdr.fieldnames}"
                )

            top_year = -1
            top_q = -1
            rows: list[dict[str, str]] = []
            for r in rdr:
                own = str(r.get("own_code", "")).strip()
                if own != "1":
                    continue
                st = state_fips_from_area(str(r.get("area_fips", "")))
                if st is None:
                    continue
                naics2 = naics2_from_industry_code(str(r.get("industry_code", "")))
                if naics2 is None or naics2 not in sector_map:
                    continue
                y_s = str(r.get("year", "")).strip()
                q_s = str(r.get("qtr", "")).strip()
                try:
                    y = int(y_s)
                except ValueError:
                    continue
                q = quarter_rank(q_s)
                if q < 1:
                    continue
                if (y > top_year) or (y == top_year and q > top_q):
                    top_year = y
                    top_q = q
                rows.append(r)

    if top_year < 0 or top_q < 0:
        raise RuntimeError("failed to resolve retained QCEW year/quarter")

    kept: list[dict[str, Any]] = []
    for r in rows:
        y = int(str(r.get("year", "0")).strip())
        q = quarter_rank(str(r.get("qtr", "")).strip())
        if y != top_year or q != top_q:
            continue
        st = state_fips_from_area(str(r.get("area_fips", "")))
        if st is None:
            continue
        naics2 = naics2_from_industry_code(str(r.get("industry_code", "")))
        if naics2 is None:
            continue
        sec_code, sec_label = sector_map[naics2]
        try:
            emp = float(str(r.get("month3_emplvl", "")).strip())
            wage = float(str(r.get("avg_wkly_wage", "")).strip())
        except ValueError:
            continue
        if emp <= 0 or wage <= 0:
            continue
        state_name = STATE_NAME_BY_FIPS.get(st, "")
        if not state_name:
            continue
        kept.append(
            {
                "qcew_year": top_year,
                "qcew_quarter": top_q,
                "state_fips": st,
                "state_name": state_name,
                "sector6_code": sec_code,
                "sector6_label": sec_label,
                "naics2": naics2,
                "employment": emp,
                "wage": wage,
            }
        )
    return kept, top_year, f"Q{top_q}"


def build_figure_a7_qcew_state_benchmark(layout: FigureA7Layout) -> None:
    layout.raw.mkdir(parents=True, exist_ok=True)
    layout.fig.mkdir(parents=True, exist_ok=True)
    layout.inter.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).isoformat()
    sector_map = load_qcew_sector6_map(layout.cross)

    page_path = layout.raw / "downloadable-data-files.html"
    page_raw = fetch_with_cache(QCEW_DOWNLOADS, page_path)
    page_html = page_raw.decode("utf-8", "replace")
    qtrly_url, latest_link_year = parse_latest_qtrly_singlefile_url(page_html)
    qzip_name = qtrly_url.rstrip("/").split("/")[-1]
    qtrly_raw = fetch_with_cache(qtrly_url, layout.raw / qzip_name)
    parsed, retained_year, retained_quarter = parse_qtrly_singlefile(
        qtrly_raw, sector_map
    )
    if not parsed:
        raise RuntimeError("no QCEW rows retained after filtering")

    df = pd.DataFrame(parsed)
    grouped = (
        df.groupby(
            ["qcew_year", "qcew_quarter", "state_fips", "state_name", "sector6_code"],
            as_index=False,
        )
        .apply(
            lambda g: pd.Series(
                {
                    "sector6_label": g["sector6_label"].iloc[0],
                    "sector_employment": float(g["employment"].sum()),
                    "average_weekly_wage": float(
                        (g["wage"] * g["employment"]).sum() / g["employment"].sum()
                    ),
                }
            ),
            include_groups=False,
        )
    )

    counts = grouped.groupby("state_fips")["sector6_code"].nunique()
    complete_states = set(counts[counts == 6].index.tolist())
    grouped = grouped[grouped["state_fips"].isin(complete_states)].copy()
    if grouped.empty:
        raise RuntimeError("no complete state x 6-sector rows after aggregation")

    totals = grouped.groupby("state_fips", as_index=False)["sector_employment"].sum()
    totals = totals.rename(columns={"sector_employment": "state_total_employment"})
    out = grouped.merge(totals, on="state_fips", how="left")
    out["state_sector_employment_share"] = (
        out["sector_employment"] / out["state_total_employment"]
    )
    out["source_industry_aggregation_note"] = (
        "QCEW own_code=1 state rows, NAICS2 mapped via frozen sector6 crosswalk; "
        "average_weekly_wage aggregated as employment-weighted mean across in-scope "
        "NAICS rows within each state-sector."
    )

    out["qcew_year"] = out["qcew_year"].astype(int)
    out["qcew_quarter"] = out["qcew_quarter"].astype(int)
    out["state_fips"] = out["state_fips"].astype(str).str.zfill(2)
    out["sector6_code"] = pd.Categorical(
        out["sector6_code"], categories=SECTOR6_ORDER, ordered=True
    )
    out = out.sort_values(["state_fips", "sector6_code"]).reset_index(drop=True)
    out = out[OUT_COLS]
    out.to_csv(layout.out_csv, index=False)

    cross_sha = sha256_bytes(layout.cross.read_bytes())
    meta = {
        "ticket": "T-017",
        "generated_at_utc": generated_at,
        "output_csv": str(layout.out_csv.relative_to(layout.root)).replace("\\", "/"),
        "crosswalk_file": str(layout.cross.relative_to(layout.root)).replace("\\", "/"),
        "crosswalk_sha256": cross_sha,
        "source_files_sha256": [
            {
                "file_name": "downloadable-data-files.html",
                "url": QCEW_DOWNLOADS,
                "sha256": sha256_bytes(page_raw),
                "local_cache_path": str(page_path.relative_to(layout.root)).replace("\\", "/"),
            },
            {
                "file_name": qzip_name,
                "url": qtrly_url,
                "sha256": sha256_bytes(qtrly_raw),
                "local_cache_path": str((layout.raw / qzip_name).relative_to(layout.root)).replace(
                    "\\", "/"
                ),
            },
        ],
        "source_selection_mode": "rolling_latest_allowed_by_ticket",
        "selection_rule": (
            "Latest available qtrly_singlefile link year from official BLS QCEW "
            "download page, then latest observed quarter within that file."
        ),
        "latest_qtrly_singlefile_link_year": latest_link_year,
        "retained_period": {"qcew_year": retained_year, "qcew_quarter": retained_quarter},
        "filters": {
            "ownership_code": "1",
            "geography": "state only via area_fips ending 000 and not 00000",
            "industry_mapping": "NAICS2 prefix from industry_code mapped via frozen sector6 crosswalk",
            "require_complete_state_sector_coverage": True,
            "state_fips_reference": "USPS/FIPS standard state code list (50 states + DC)",
        },
        "state_total_definition": (
            "state_total_employment is the sum of sector_employment over the six "
            "in-scope sectors within each state for the retained period."
        ),
        "wage_aggregation_rule": (
            "average_weekly_wage is employment-weighted mean of published QCEW "
            "avg_wkly_wage across retained in-scope NAICS rows within state-sector."
        ),
        "row_count": int(len(out)),
    }
    layout.out_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {layout.out_csv} ({len(out)} rows)")
    print(f"Wrote {layout.out_meta}")

