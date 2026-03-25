"""
Build figures/figure1_panelA_occ_baseline.csv from BLS OEWS national file and occ22 taxonomy.

Run from repo root: python scripts/build_figure1_panelA.py
"""

from __future__ import annotations

import re
import zipfile
import json
import hashlib
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
CROSS = ROOT / "crosswalks" / "occ22_crosswalk.csv"
DOCS = ROOT / "docs" / "data_registry.csv"

OEWS_ZIP_URL = "https://www.bls.gov/oes/special-requests/oesm24nat.zip"
OEWS_ZIP_NAME = "oesm24nat.zip"
SNAPSHOT = date.today().isoformat()


def soc_code_to_major(soc: str) -> str:
    """Map detailed SOC 'XX-YYYY' to major group 'XX-0000'."""
    s = str(soc).strip()
    if "-" not in s:
        raise ValueError(f"Invalid SOC code: {soc}")
    left, _ = s.split("-", 1)
    if not left.isdigit():
        raise ValueError(f"Invalid SOC code: {soc}")
    return f"{int(left):02d}-0000"


def load_occ22_labels() -> pd.DataFrame:
    """occ22_id and label from CPS_PRDTOCC1 rows (22 civilian groups)."""
    cx = pd.read_csv(CROSS)
    pr = cx[cx["source_system"] == "CPS_PRDTOCC1"].copy()
    pr = pr[pr["source_occ_code"].astype(str) != "23"]
    pr["occ22_id"] = pr["occ22_id"].astype(int)
    return pr[["occ22_id", "occ22_label", "soc_major_group_code"]].drop_duplicates()


def wage_proxy_row(row: pd.Series) -> float:
    """
    Row-level wage proxy for aggregation (documented in docs).
    Prefer A_MEDIAN, else A_MEAN, else H_MEDIAN * 2080 (OEWS typical annualization).
    """
    am = pd.to_numeric(row.get("A_MEDIAN"), errors="coerce")
    if pd.notna(am):
        return float(am)
    amean = pd.to_numeric(row.get("A_MEAN"), errors="coerce")
    if pd.notna(amean):
        return float(amean)
    hm = pd.to_numeric(row.get("H_MEDIAN"), errors="coerce")
    if pd.notna(hm):
        return float(hm) * 2080.0
    return np.nan


def download_oews_zip() -> Path:
    import urllib.request

    RAW.mkdir(parents=True, exist_ok=True)
    dest = RAW / OEWS_ZIP_NAME
    if dest.exists() and dest.stat().st_size > 10000:
        return dest
    req = urllib.request.Request(
        OEWS_ZIP_URL,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.bls.gov/oes/current/oes_stru.htm",
        },
    )
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as out:
        out.write(resp.read())
    return dest


def find_national_xlsx(zip_path: Path) -> Path:
    extract_dir = RAW / "oesm24nat_extract"
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)
    for p in extract_dir.rglob("*.xlsx"):
        if re.search(r"national_m\d+_dl\.xlsx", p.name, re.I):
            return p
    raise FileNotFoundError("No national_M*_dl.xlsx found in OEWS zip")


def build_baseline(xlsx_path: Path) -> pd.DataFrame:
    oews = pd.read_excel(xlsx_path, sheet_name=0)
    det = oews[oews["O_GROUP"] == "detailed"].copy()
    det["soc_major"] = det["OCC_CODE"].map(soc_code_to_major)

    total_row = oews[oews["OCC_CODE"] == "00-0000"]
    total_emp = float(total_row["TOT_EMP"].iloc[0])

    det["wage_proxy"] = det.apply(wage_proxy_row, axis=1)
    det["emp_wage"] = det["TOT_EMP"] * det["wage_proxy"]

    labels = load_occ22_labels()
    merged = det.merge(
        labels,
        left_on="soc_major",
        right_on="soc_major_group_code",
        how="left",
    )
    if merged["occ22_id"].isna().any():
        bad = merged[merged["occ22_id"].isna()]["soc_major"].unique()
        raise ValueError(f"Unmapped SOC majors: {bad}")

    g = merged.groupby("occ22_id", as_index=False).agg(
        employment=("TOT_EMP", "sum"),
        emp_wage_sum=("emp_wage", "sum"),
    )
    g = g.merge(labels[["occ22_id", "occ22_label"]], on="occ22_id", how="left")
    g["employment_share"] = g["employment"] / total_emp
    g["median_annual_wage"] = g["emp_wage_sum"] / g["employment"]
    g["occupation_group"] = g["occ22_label"]

    g = g.sort_values("occ22_id")
    out = g[
        [
            "occupation_group",
            "employment",
            "employment_share",
            "median_annual_wage",
        ]
    ].copy()
    out.loc[:, "median_annual_wage"] = (
        out["median_annual_wage"].round(0).astype(int)
    )
    out.loc[:, "employment"] = out["employment"].astype(int)
    return out


def append_registry_rows() -> None:
    rows = [
        {
            "dataset_id": "bls_oews_tables_hub",
            "program": "BLS_OEWS",
            "source_url": "https://www.bls.gov/oes/current/oes_stru.htm",
            "download_url": "https://www.bls.gov/oes/current/oes_stru.htm",
            "file_name": "",
            "file_format": "html",
            "release_date_reported": "",
            "source_last_modified_observed": "July 23 2025 per BLS page",
            "snapshot_download_date": SNAPSHOT,
            "notes_on_version": "OEWS data tables index; national May 2024 XLSX zip",
        },
        {
            "dataset_id": "bls_oews_may2024_national_zip",
            "program": "BLS_OEWS",
            "source_url": "https://www.bls.gov/oes/special-requests/oesm24nat.zip",
            "download_url": "https://www.bls.gov/oes/special-requests/oesm24nat.zip",
            "file_name": "oesm24nat.zip",
            "file_format": "zip",
            "release_date_reported": "April 2 2025",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT,
            "notes_on_version": "May 2024 national occupational employment and wage estimates",
        },
        {
            "dataset_id": "bls_oews_may2024_technical_notes",
            "program": "BLS_OEWS",
            "source_url": "https://www.bls.gov/oes/2024/may/oes_tec.htm",
            "download_url": "https://www.bls.gov/oes/2024/may/oes_tec.htm",
            "file_name": "",
            "file_format": "html",
            "release_date_reported": "",
            "source_last_modified_observed": "April 2 2025",
            "snapshot_download_date": SNAPSHOT,
            "notes_on_version": "OEWS scope, 2018 SOC, MB3 methodology",
        },
        {
            "dataset_id": "bls_oews_may2024_news_release",
            "program": "BLS_OEWS",
            "source_url": "https://www.bls.gov/news.release/archives/ocwage_04022025.htm",
            "download_url": "https://www.bls.gov/news.release/archives/ocwage_04022025.htm",
            "file_name": "",
            "file_format": "html",
            "release_date_reported": "April 2 2025",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT,
            "notes_on_version": "OEWS news release May 2024 reference period",
        },
    ]
    existing = pd.read_csv(DOCS)
    have = set(existing["dataset_id"].astype(str))
    for r in rows:
        if r["dataset_id"] in have:
            continue
        existing = pd.concat([existing, pd.DataFrame([r])], ignore_index=True)
    existing.to_csv(DOCS, index=False)


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    zip_path = download_oews_zip()
    xlsx = find_national_xlsx(zip_path)
    out_df = build_baseline(xlsx)

    out_path = FIG / "figure1_panelA_occ_baseline.csv"
    meta_path = INTER / "figure1_panelA_occ_baseline_meta.csv"
    meta_json_path = INTER / "figure1_panelA_run_metadata.json"

    oews_full = pd.read_excel(xlsx, sheet_name=0)
    total_emp = float(oews_full.query("OCC_CODE == '00-0000'")["TOT_EMP"].iloc[0])
    det_sum = float(oews_full.query("O_GROUP == 'detailed'")["TOT_EMP"].sum())
    meta = pd.DataFrame(
        [
            {
                "oews_reference_period": "May 2024",
                "oews_release_date": "April 2 2025",
                "national_total_employment_00_0000": int(total_emp),
                "detailed_occupation_employment_sum": int(det_sum),
                "employment_reconciliation_diff": int(total_emp - det_sum),
                "oews_file": str(xlsx.relative_to(ROOT)),
                "zip_source": OEWS_ZIP_URL,
                "snapshot_date": SNAPSHOT,
                "wage_rule": (
                    "employment-weighted mean of row wage_proxy; "
                    "A_MEDIAN else A_MEAN else H_MEDIAN*2080"
                ),
            }
        ]
    )
    meta.to_csv(meta_path, index=False)

    def _sha(path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            while True:
                b = f.read(1024 * 1024)
                if not b:
                    break
                h.update(b)
        return h.hexdigest()

    run_meta = {
        "ticket": "T-001",
        "output_csv": str(out_path.relative_to(ROOT)).replace("\\", "/"),
        "legacy_meta_csv": str(meta_path.relative_to(ROOT)).replace("\\", "/"),
        "source_selection_mode": "pinned_vintage_required_by_ticket",
        "source_selection_rule": "Pinned OEWS May 2024 national zip per T-001.",
        "sources": [
            {
                "file_name": OEWS_ZIP_NAME,
                "url": OEWS_ZIP_URL,
                "local_cache_path": str(zip_path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": _sha(zip_path),
            }
        ],
        "crosswalk_sha256": _sha(CROSS),
        "snapshot_date": SNAPSHOT,
        "row_count": int(len(out_df)),
    }
    meta_json_path.write_text(json.dumps(run_meta, indent=2), encoding="utf-8")

    out_df.to_csv(out_path, index=False)
    append_registry_rows()
    print(f"Wrote {out_path} ({len(out_df)} rows)")
    print(f"Meta: {meta_path}")
    print(f"Run metadata: {meta_json_path}")


if __name__ == "__main__":
    main()
