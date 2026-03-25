"""
Build Figure 1 Panel B: O*NET work-activity task heatmap and AI Task Index (T-002).

Uses official O*NET Work Activities (Importance scale) and OEWS national
employment weights,
aggregated to the 22 occ22 groups from crosswalks/occ22_crosswalk.csv.

Run from repo root: python scripts/build_figure1_panelB.py
Optional: python scripts/build_figure1_panelB.py --onet-version 30.2
"""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from occupational_transition.http import download_to_path
from occupational_transition.sources.onet import (
    ONET_DB_PAGE,
    ONET_RELEASES_ARCHIVE,
    ONET_SOC_XWALK_URL,
    onet_version_to_zip_token,
)

ROOT = Path(__file__).resolve().parents[1]

RAW = ROOT / "raw"
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
CROSS = ROOT / "crosswalks" / "occ22_crosswalk.csv"
DOCS = ROOT / "docs" / "data_registry.csv"

OEWS_ZIP_URL = "https://www.bls.gov/oes/special-requests/oesm24nat.zip"
OEWS_ZIP_NAME = "oesm24nat.zip"

# Official O*NET landing URLs for registry rows.

FROZEN_ELEMENTS: tuple[str, ...] = (
    "Analyzing Data or Information",
    "Processing Information",
    "Documenting/Recording Information",
    "Working with Computers",
    "Assisting and Caring for Others",
    "Handling and Moving Objects",
)

DIGITAL_INFO_ELEMENTS = FROZEN_ELEMENTS[:4]

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


def onet_to_soc_means(wa: pd.DataFrame, xwalk: pd.DataFrame) -> pd.DataFrame:
    """Mean O*NET IM score per (2018 SOC detail, element) across O*NET-SOC rows."""
    m = wa.merge(xwalk, on="onet_soc_code", how="inner")
    if m.empty:
        raise ValueError("No overlap between Work Activities and SOC crosswalk")
    g = m.groupby(["soc_2018", "element_name"], as_index=False)["data_value"].mean()
    return g


def ensure_oews_national_xlsx() -> Path:
    zip_path = RAW / OEWS_ZIP_NAME
    download_to_path(
        OEWS_ZIP_URL,
        zip_path,
        extra_headers={
            "Referer": "https://www.bls.gov/oes/current/oes_stru.htm",
        },
        skip_if_exists_min_bytes=10_000,
    )
    extract_dir = RAW / "oesm24nat_extract"
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)
    for p in extract_dir.rglob("*.xlsx"):
        if re.search(r"national_m\d+_dl\.xlsx", p.name, re.I):
            return p
    raise FileNotFoundError("No national_M*_dl.xlsx found in OEWS zip")


def load_oews_detailed_employment(xlsx_path: Path) -> pd.DataFrame:
    oews = pd.read_excel(xlsx_path, sheet_name=0)
    det = oews[oews["O_GROUP"] == "detailed"].copy()
    det["soc_2018"] = det["OCC_CODE"].astype(str).str.strip()
    det["employment"] = pd.to_numeric(det["TOT_EMP"], errors="coerce")
    det = det.dropna(subset=["employment"])
    det = det[det["employment"] > 0]
    # Exclude military major group 55 (OEWS typically omits; keep rule explicit)
    det = det[~det["soc_2018"].str.startswith("55-")]
    return det[["soc_2018", "employment"]]


def aggregate_to_occ22(
    soc_element_scores: pd.DataFrame,
    oews_emp: pd.DataFrame,
    labels: pd.DataFrame,
) -> pd.DataFrame:
    """
    soc_element_scores: soc_2018, element_name, data_value (mean at SOC detail).
    oews_emp: soc_2018, employment (may have one row per SOC).
    """
    merged = soc_element_scores.merge(oews_emp, on="soc_2018", how="inner")
    if merged.empty:
        raise ValueError(
            "No SOC overlap between O*NET aggregates and OEWS detailed rows"
        )
    merged["soc_major"] = merged["soc_2018"].map(soc_code_to_major)
    merged = merged.merge(
        labels,
        left_on="soc_major",
        right_on="soc_major_group_code",
        how="left",
    )
    if merged["occ22_id"].isna().any():
        bad = merged[merged["occ22_id"].isna()]["soc_major"].unique()
        raise ValueError(f"Unmapped SOC majors for OEWS/O*NET merge: {bad}")

    merged["weighted"] = merged["data_value"] * merged["employment"]
    out_rows = []
    for elem in FROZEN_ELEMENTS:
        sub = merged[merged["element_name"] == elem]
        g = sub.groupby("occ22_id", as_index=False).agg(
            wsum=("weighted", "sum"),
            emp=("employment", "sum"),
        )
        g["score"] = g["wsum"] / g["emp"]
        g["element_name"] = elem
        out_rows.append(g[["occ22_id", "element_name", "score"]])
    long_df = pd.concat(out_rows, ignore_index=True)
    wide = long_df.pivot(index="occ22_id", columns="element_name", values="score")
    wide = wide.reset_index()
    return wide


def zscore_22(s: pd.Series) -> pd.Series:
    mu = s.mean()
    sigma = s.std(ddof=0)
    if sigma == 0 or np.isnan(sigma):
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - mu) / sigma


def assign_terciles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deterministic terciles on AI Task Index: sort by (index asc, occ22_id asc).
    22 rows -> 7 lowest = low, next 7 = middle, top 8 = high.
    """
    d = df.sort_values(["ai_task_index", "occ22_id"]).reset_index(drop=True)
    labels_terc = np.empty(len(d), dtype=object)
    labels_terc[0:7] = "low"
    labels_terc[7:14] = "middle"
    labels_terc[14:22] = "high"
    d["ai_relevance_tercile"] = labels_terc
    return d


def append_registry_rows_t002(onet_version: str) -> None:
    rows = [
        {
            "dataset_id": "onet_database_landing",
            "program": "O_NET",
            "source_url": ONET_DB_PAGE,
            "download_url": ONET_DB_PAGE,
            "file_name": "",
            "file_format": "html",
            "release_date_reported": "",
            "source_last_modified_observed": (
                "February 24 2026 per O*NET Resource Center page"
            ),
            "snapshot_download_date": SNAPSHOT,
            "notes_on_version": (
                f"O*NET database downloads; production release {onet_version}"
            ),
        },
        {
            "dataset_id": "onet_database_releases_archive",
            "program": "O_NET",
            "source_url": ONET_RELEASES_ARCHIVE,
            "download_url": ONET_RELEASES_ARCHIVE,
            "file_name": "",
            "file_format": "html",
            "release_date_reported": "",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT,
            "notes_on_version": "Historical O*NET database release versions",
        },
        {
            "dataset_id": f"onet_{onet_version.replace('.', '_')}_text_database_zip",
            "program": "O_NET",
            "source_url": ONET_DB_PAGE,
            "download_url": f"https://www.onetcenter.org/dl_files/database/db_{onet_version_to_zip_token(onet_version)}_text.zip",
            "file_name": f"db_{onet_version_to_zip_token(onet_version)}_text.zip",
            "file_format": "zip",
            "release_date_reported": "",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT,
            "notes_on_version": "O*NET core database tab-delimited text files",
        },
        {
            "dataset_id": (
                f"onet_{onet_version.replace('.', '_')}_work_activities_dictionary"
            ),
            "program": "O_NET",
            "source_url": f"https://www.onetcenter.org/dictionary/{onet_version}/excel/work_activities.html",
            "download_url": f"https://www.onetcenter.org/dictionary/{onet_version}/excel/work_activities.html",
            "file_name": "",
            "file_format": "html",
            "release_date_reported": "",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT,
            "notes_on_version": "Work Activities file schema; IM/LV scales",
        },
        {
            "dataset_id": (
                f"onet_{onet_version.replace('.', '_')}_scales_reference_dictionary"
            ),
            "program": "O_NET",
            "source_url": f"https://www.onetcenter.org/dictionary/{onet_version}/excel/scales_reference.html",
            "download_url": f"https://www.onetcenter.org/dictionary/{onet_version}/excel/scales_reference.html",
            "file_name": "",
            "file_format": "html",
            "release_date_reported": "",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT,
            "notes_on_version": "Scale IDs IM Importance LV Level",
        },
        {
            "dataset_id": "onet_soc2019_to_soc2018_crosswalk",
            "program": "O_NET",
            "source_url": "https://www.onetcenter.org/taxonomy/2019/soc.html",
            "download_url": ONET_SOC_XWALK_URL,
            "file_name": "2019_to_SOC_Crosswalk.csv",
            "file_format": "csv",
            "release_date_reported": "",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT,
            "notes_on_version": "O*NET-SOC 2019 to 2018 SOC crosswalk",
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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--onet-version",
        default="30.2",
        help="O*NET database version string matching db_<version>_text.zip",
    )
    args = parser.parse_args()
    onet_v = args.onet_version

    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    from occupational_transition.pipelines.figure1_panelB_t002 import (
        build_figure1_panelB_t002,
    )

    result = build_figure1_panelB_t002(
        onet_version=onet_v,
        repo_root=ROOT,
        raw_dir=RAW,
        figures_dir=FIG,
        intermediate_dir=INTER,
        crosswalk_csv=CROSS,
    )

    heatmap_path = FIG / "figure1_panelB_task_heatmap.csv"
    tercile_path = INTER / "ai_relevance_terciles.csv"
    exposure_path = INTER / "occ22_exposure_components.csv"
    meta_path = INTER / "figure1_panelB_meta.csv"
    meta_json_path = INTER / "figure1_panelB_run_metadata.json"

    result.heatmap_out.to_csv(heatmap_path, index=False)
    result.exposure_df.to_csv(exposure_path, index=False)
    result.terc_out.to_csv(tercile_path, index=False)
    result.meta_df.to_csv(meta_path, index=False)
    meta_json_path.write_text(
        json.dumps(result.run_metadata, indent=2), encoding="utf-8"
    )

    existing = pd.read_csv(DOCS)
    have = set(existing["dataset_id"].astype(str))
    for r in result.registry_rows:
        if r["dataset_id"] in have:
            continue
        existing = pd.concat([existing, pd.DataFrame([r])], ignore_index=True)
    existing.to_csv(DOCS, index=False)

    print(f"Wrote {heatmap_path} ({len(result.heatmap_out)} rows)")
    print(f"Wrote {exposure_path} ({len(result.exposure_df)} rows)")
    print(f"Wrote {tercile_path} ({len(result.terc_out)} rows)")
    print(f"Meta: {meta_path}")
    print(f"Run metadata: {meta_json_path}")


if __name__ == "__main__":
    main()
