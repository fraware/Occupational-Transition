from __future__ import annotations

import hashlib
import json
import re
import urllib.request
import zipfile
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from occupational_transition.crosswalks import load_occ22_labels

OEWS_ZIP_URL = "https://www.bls.gov/oes/special-requests/oesm24nat.zip"
OEWS_ZIP_NAME = "oesm24nat.zip"


def soc_code_to_major(soc: str) -> str:
    s = str(soc).strip()
    if "-" not in s:
        raise ValueError(f"Invalid SOC code: {soc}")
    left, _ = s.split("-", 1)
    if not left.isdigit():
        raise ValueError(f"Invalid SOC code: {soc}")
    return f"{int(left):02d}-0000"


def wage_proxy_row(row: pd.Series) -> float:
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


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def download_oews_zip(raw: Path) -> Path:
    raw.mkdir(parents=True, exist_ok=True)
    dest = raw / OEWS_ZIP_NAME
    if dest.exists() and dest.stat().st_size > 10000:
        return dest
    req = urllib.request.Request(
        OEWS_ZIP_URL,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bls.gov/oes/current/oes_stru.htm",
        },
    )
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as out:
        out.write(resp.read())
    return dest


def find_national_xlsx(zip_path: Path, raw: Path) -> Path:
    extract_dir = raw / "oesm24nat_extract"
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)
    for p in extract_dir.rglob("*.xlsx"):
        if re.search(r"national_m\d+_dl\.xlsx", p.name, re.I):
            return p
    raise FileNotFoundError("No national_M*_dl.xlsx found in OEWS zip")


def build_baseline(xlsx_path: Path, crosswalk: Path) -> pd.DataFrame:
    oews = pd.read_excel(xlsx_path, sheet_name=0)
    det = oews[oews["O_GROUP"] == "detailed"].copy()
    det["soc_major"] = det["OCC_CODE"].map(soc_code_to_major)
    total_emp = float(oews[oews["OCC_CODE"] == "00-0000"]["TOT_EMP"].iloc[0])
    det["wage_proxy"] = det.apply(wage_proxy_row, axis=1)
    det["emp_wage"] = det["TOT_EMP"] * det["wage_proxy"]
    labels = load_occ22_labels(crosswalk)
    merged = det.merge(labels, left_on="soc_major", right_on="soc_major_group_code", how="left")
    if merged["occ22_id"].isna().any():
        bad = merged[merged["occ22_id"].isna()]["soc_major"].unique()
        raise ValueError(f"Unmapped SOC majors: {bad}")
    g = merged.groupby("occ22_id", as_index=False).agg(employment=("TOT_EMP", "sum"), emp_wage_sum=("emp_wage", "sum"))
    g = g.merge(labels[["occ22_id", "occ22_label"]], on="occ22_id", how="left")
    g["employment_share"] = g["employment"] / total_emp
    g["median_annual_wage"] = g["emp_wage_sum"] / g["employment"]
    out = g.sort_values("occ22_id")[["occ22_label", "employment", "employment_share", "median_annual_wage"]].copy()
    out = out.rename(columns={"occ22_label": "occupation_group"})
    out.loc[:, "median_annual_wage"] = out["median_annual_wage"].round(0).astype(int)
    out.loc[:, "employment"] = out["employment"].astype(int)
    return out


def append_registry_rows(registry_path: Path, snapshot: str) -> None:
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
            "snapshot_download_date": snapshot,
            "notes_on_version": "OEWS data tables index; national May 2024 XLSX zip",
            "extractor": "",
            "update_cadence": "reference",
            "notes_for_users": "Landing page only; fetch specific zip rows for files.",
        },
        {
            "dataset_id": "bls_oews_may2024_national_zip",
            "program": "BLS_OEWS",
            "source_url": OEWS_ZIP_URL,
            "download_url": OEWS_ZIP_URL,
            "file_name": OEWS_ZIP_NAME,
            "file_format": "zip",
            "release_date_reported": "April 2 2025",
            "source_last_modified_observed": "",
            "snapshot_download_date": snapshot,
            "notes_on_version": "May 2024 national occupational employment and wage estimates",
            "extractor": "http_download",
            "update_cadence": "annual",
            "notes_for_users": "Large zip; T-001/T-002 national weights.",
        },
    ]
    existing = pd.read_csv(registry_path)
    have = set(existing["dataset_id"].astype(str))
    for r in rows:
        if r["dataset_id"] not in have:
            existing = pd.concat([existing, pd.DataFrame([r])], ignore_index=True)
    existing.to_csv(registry_path, index=False)


def run(root: Path) -> tuple[Path, Path, Path, int]:
    raw = root / "raw"
    fig = root / "figures"
    inter = root / "intermediate"
    cross = root / "crosswalks" / "occ22_crosswalk.csv"
    docs = root / "docs" / "data_registry.csv"
    snapshot = date.today().isoformat()

    fig.mkdir(parents=True, exist_ok=True)
    inter.mkdir(parents=True, exist_ok=True)

    zip_path = download_oews_zip(raw)
    xlsx = find_national_xlsx(zip_path, raw)
    out_df = build_baseline(xlsx, cross)
    out_path = fig / "figure1_panelA_occ_baseline.csv"
    meta_path = inter / "figure1_panelA_occ_baseline_meta.csv"
    run_meta_path = inter / "figure1_panelA_run_metadata.json"

    out_df.to_csv(out_path, index=False)
    oews_full = pd.read_excel(xlsx, sheet_name=0)
    total_emp = float(oews_full.query("OCC_CODE == '00-0000'")["TOT_EMP"].iloc[0])
    det_sum = float(oews_full.query("O_GROUP == 'detailed'")["TOT_EMP"].sum())
    pd.DataFrame(
        [
            {
                "oews_reference_period": "May 2024",
                "oews_release_date": "April 2 2025",
                "national_total_employment_00_0000": int(total_emp),
                "detailed_occupation_employment_sum": int(det_sum),
                "employment_reconciliation_diff": int(total_emp - det_sum),
                "oews_file": str(xlsx.relative_to(root)),
                "zip_source": OEWS_ZIP_URL,
                "snapshot_date": snapshot,
            }
        ]
    ).to_csv(meta_path, index=False)
    run_meta = {
        "ticket": "T-001",
        "output_csv": str(out_path.relative_to(root)).replace("\\", "/"),
        "legacy_meta_csv": str(meta_path.relative_to(root)).replace("\\", "/"),
        "source_selection_mode": "pinned_vintage_required_by_ticket",
        "source_selection_rule": "Pinned OEWS May 2024 national zip per T-001.",
        "sources": [
            {
                "file_name": OEWS_ZIP_NAME,
                "url": OEWS_ZIP_URL,
                "local_cache_path": str(zip_path.relative_to(root)).replace("\\", "/"),
                "sha256": _sha(zip_path),
            }
        ],
        "crosswalk_sha256": _sha(cross),
        "snapshot_date": snapshot,
        "row_count": int(len(out_df)),
    }
    run_meta_path.write_text(json.dumps(run_meta, indent=2), encoding="utf-8")
    append_registry_rows(docs, snapshot)
    return out_path, meta_path, run_meta_path, len(out_df)
