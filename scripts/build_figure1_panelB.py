"""
Build Figure 1 Panel B: O*NET work-activity task heatmap and AI Task Index (T-002).

Uses official O*NET Work Activities (Importance scale) and OEWS national employment weights,
aggregated to the 22 occ22 groups from crosswalks/occ22_crosswalk.csv.

Run from repo root: python scripts/build_figure1_panelB.py
Optional: python scripts/build_figure1_panelB.py --onet-version 30.2
"""

from __future__ import annotations

import argparse
import re
import zipfile
import json
import hashlib
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

from awes_alpi_common import occ22_code_from_id, percentile_rank_01

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
CROSS = ROOT / "crosswalks" / "occ22_crosswalk.csv"
DOCS = ROOT / "docs" / "data_registry.csv"

# Official URLs (see docs/data_registry.csv)
ONET_DB_PAGE = "https://www.onetcenter.org/database.html"
ONET_RELEASES_ARCHIVE = "https://www.onetcenter.org/db_releases.html"
ONET_SOC_XWALK_URL = (
    "https://www.onetcenter.org/taxonomy/2019/soc/2019_to_SOC_Crosswalk.csv?fmt=csv"
)
OEWS_ZIP_URL = "https://www.bls.gov/oes/special-requests/oesm24nat.zip"
OEWS_ZIP_NAME = "oesm24nat.zip"

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


def load_occ22_labels() -> pd.DataFrame:
    cx = pd.read_csv(CROSS)
    pr = cx[cx["source_system"] == "CPS_PRDTOCC1"].copy()
    pr = pr[pr["source_occ_code"].astype(str) != "23"]
    pr["occ22_id"] = pr["occ22_id"].astype(int)
    return pr[["occ22_id", "occ22_label", "soc_major_group_code"]].drop_duplicates()


def download_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; Occupational-Transition/1.0)",
        },
    )
    with urlopen(req) as resp, open(dest, "wb") as out:
        out.write(resp.read())


def onet_version_to_zip_token(version: str) -> str:
    """Map '30.2' to '30_2' for official zip filenames (db_30_2_text.zip)."""
    return version.strip().replace(".", "_")


def ensure_onet_text_zip(version: str) -> Path:
    """Download O*NET db_<version>_text.zip if missing."""
    token = onet_version_to_zip_token(version)
    fname = f"db_{token}_text.zip"
    dest = RAW / fname
    if dest.exists() and dest.stat().st_size > 10_000:
        return dest
    url = f"https://www.onetcenter.org/dl_files/database/{fname}"
    download_file(url, dest)
    return dest


def read_work_activities_im(zip_path: Path) -> pd.DataFrame:
    """Parse Work Activities.txt; keep Importance (IM) scale only."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        inner = [n for n in zf.namelist() if n.endswith("Work Activities.txt")][0]
        raw = zf.read(inner).decode("utf-8", errors="replace")
    lines = raw.splitlines()
    if not lines:
        raise ValueError("Empty Work Activities file")
    header = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 6:
            continue
        row = dict(zip(header, parts + [""] * (len(header) - len(parts))))
        rows.append(row)
    df = pd.DataFrame(rows)
    df = df.rename(
        columns={
            "O*NET-SOC Code": "onet_soc_code",
            "Element Name": "element_name",
            "Scale ID": "scale_id",
            "Data Value": "data_value",
        }
    )
    df = df[df["scale_id"] == "IM"].copy()
    df["data_value"] = pd.to_numeric(df["data_value"], errors="coerce")
    df = df[df["element_name"].isin(FROZEN_ELEMENTS)]
    df = df.dropna(subset=["data_value", "onet_soc_code"])
    return df[["onet_soc_code", "element_name", "data_value"]]


def ensure_soc_crosswalk() -> Path:
    dest = RAW / "onet_2019_to_soc2018_crosswalk.csv"
    if not dest.exists():
        download_file(ONET_SOC_XWALK_URL, dest)
    return dest


def load_crosswalk(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.rename(
        columns={
            "O*NET-SOC 2019 Code": "onet_soc_code",
            "2018 SOC Code": "soc_2018",
        }
    )
    df["soc_2018"] = df["soc_2018"].astype(str).str.strip()
    return df[["onet_soc_code", "soc_2018"]]


def onet_to_soc_means(wa: pd.DataFrame, xwalk: pd.DataFrame) -> pd.DataFrame:
    """Mean O*NET IM score per (2018 SOC detail, element) across O*NET-SOC rows."""
    m = wa.merge(xwalk, on="onet_soc_code", how="inner")
    if m.empty:
        raise ValueError("No overlap between Work Activities and SOC crosswalk")
    g = m.groupby(["soc_2018", "element_name"], as_index=False)["data_value"].mean()
    return g


def ensure_oews_national_xlsx() -> Path:
    zip_path = RAW / OEWS_ZIP_NAME
    if not zip_path.exists() or zip_path.stat().st_size < 10_000:
        download_file(OEWS_ZIP_URL, zip_path)
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
        raise ValueError("No SOC overlap between O*NET aggregates and OEWS detailed rows")
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
            "source_last_modified_observed": "February 24 2026 per O*NET Resource Center page",
            "snapshot_download_date": SNAPSHOT,
            "notes_on_version": f"O*NET database downloads; production release {onet_version}",
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
            "dataset_id": f"onet_{onet_version.replace('.', '_')}_work_activities_dictionary",
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
            "dataset_id": f"onet_{onet_version.replace('.', '_')}_scales_reference_dictionary",
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

    labels = load_occ22_labels()

    onet_zip = ensure_onet_text_zip(onet_v)
    wa = read_work_activities_im(onet_zip)
    xw_path = ensure_soc_crosswalk()
    xw = load_crosswalk(xw_path)
    soc_elem = onet_to_soc_means(wa, xw)

    xlsx = ensure_oews_national_xlsx()
    oews_det = load_oews_detailed_employment(xlsx)

    wide = aggregate_to_occ22(soc_elem, oews_det, labels)

    # Z-scores across 22 groups for each of six dimensions
    zcols: dict[str, str] = {}
    for elem in FROZEN_ELEMENTS:
        safe = (
            elem.lower()
            .replace(" ", "_")
            .replace("/", "_")
            .replace(",", "")
        )
        col_z = f"z_{safe}"
        zcols[elem] = col_z
        wide[col_z] = zscore_22(wide[elem])

    wide = wide.merge(labels[["occ22_id", "occ22_label"]], on="occ22_id", how="left")
    wide["occupation_group"] = wide["occ22_label"]

    z_digital = [wide[zcols[e]] for e in DIGITAL_INFO_ELEMENTS]
    wide["ai_task_index"] = pd.concat(z_digital, axis=1).mean(axis=1)

    # AWES input artifact (does not replace or modify AI terciles).
    z_out_rename = {
        "Analyzing Data or Information": "onet_analyzing_data_z",
        "Processing Information": "onet_processing_information_z",
        "Documenting/Recording Information": "onet_documenting_recording_z",
        "Working with Computers": "onet_working_with_computers_z",
        "Assisting and Caring for Others": "onet_assisting_caring_z",
        "Handling and Moving Objects": "onet_handling_moving_z",
    }
    exposure_pct = percentile_rank_01(wide["ai_task_index"])
    expo_cols = {
        "occ22_code": wide["occ22_id"].map(occ22_code_from_id),
        "occ22_label": wide["occ22_label"].astype(str),
        "ai_task_index_raw": wide["ai_task_index"].astype(float),
        "exposure_pct": exposure_pct.astype(float),
    }
    for elem, outc in z_out_rename.items():
        expo_cols[outc] = wide[zcols[elem]].astype(float)
    exposure_df = pd.DataFrame(expo_cols)
    exposure_df = exposure_df.sort_values("occ22_code").reset_index(drop=True)
    exposure_cols_order = [
        "occ22_code",
        "occ22_label",
        "ai_task_index_raw",
        "exposure_pct",
        "onet_analyzing_data_z",
        "onet_processing_information_z",
        "onet_documenting_recording_z",
        "onet_working_with_computers_z",
        "onet_assisting_caring_z",
        "onet_handling_moving_z",
    ]
    exposure_path = INTER / "occ22_exposure_components.csv"
    exposure_df[exposure_cols_order].to_csv(exposure_path, index=False)

    terc = assign_terciles(wide[["occ22_id", "occupation_group", "ai_task_index"]].copy())

    heatmap_cols = ["occupation_group", "occ22_id"] + [zcols[e] for e in FROZEN_ELEMENTS]
    heatmap_out = wide[heatmap_cols].sort_values("occ22_id")

    terc_out = terc.sort_values("occ22_id")[
        ["occupation_group", "occ22_id", "ai_task_index", "ai_relevance_tercile"]
    ]

    meta = pd.DataFrame(
        [
            {
                "onet_version": onet_v,
                "onet_text_zip": str(onet_zip.relative_to(ROOT)),
                "scale_id": "IM",
                "scale_name": "Importance",
                "oews_file": str(xlsx.relative_to(ROOT)),
                "oews_zip_url": OEWS_ZIP_URL,
                "crosswalk_file": str(xw_path.relative_to(ROOT)),
                "snapshot_date": SNAPSHOT,
                "zscore_scope": "22 occupation groups; population std (ddof=0)",
                "ai_task_index": "mean of z-scores for four digital-information work activities",
                "tercile_rule": "sort by ai_task_index ascending then occ22_id; ranks 1-7 low, 8-14 middle, 15-22 high",
            }
        ]
    )
    meta_path = INTER / "figure1_panelB_meta.csv"
    meta.to_csv(meta_path, index=False)
    meta_json_path = INTER / "figure1_panelB_run_metadata.json"

    heatmap_path = FIG / "figure1_panelB_task_heatmap.csv"
    tercile_path = INTER / "ai_relevance_terciles.csv"
    heatmap_out.to_csv(heatmap_path, index=False)
    terc_out.to_csv(tercile_path, index=False)

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
        "ticket": "T-002",
        "output_heatmap_csv": str(heatmap_path.relative_to(ROOT)).replace("\\", "/"),
        "output_terciles_csv": str(tercile_path.relative_to(ROOT)).replace("\\", "/"),
        "legacy_meta_csv": str(meta_path.relative_to(ROOT)).replace("\\", "/"),
        "source_selection_mode": "pinned_vintage_required_by_ticket",
        "source_selection_rule": (
            "Pinned O*NET version parameter and pinned OEWS May 2024 zip for "
            "cross-sectional baseline."
        ),
        "onet_version": onet_v,
        "sources": [
            {
                "file_name": onet_zip.name,
                "url": f"https://www.onetcenter.org/dl_files/database/db_{onet_version_to_zip_token(onet_v)}_text.zip",
                "local_cache_path": str(onet_zip.relative_to(ROOT)).replace("\\", "/"),
                "sha256": _sha(onet_zip),
            },
            {
                "file_name": xw_path.name,
                "url": ONET_SOC_XWALK_URL,
                "local_cache_path": str(xw_path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": _sha(xw_path),
            },
            {
                "file_name": OEWS_ZIP_NAME,
                "url": OEWS_ZIP_URL,
                "local_cache_path": str((RAW / OEWS_ZIP_NAME).relative_to(ROOT)).replace(
                    "\\", "/"
                ),
                "sha256": _sha(RAW / OEWS_ZIP_NAME),
            },
        ],
        "crosswalk_sha256": _sha(CROSS),
        "row_count_heatmap": int(len(heatmap_out)),
        "row_count_terciles": int(len(terc_out)),
        "output_exposure_components_csv": str(
            exposure_path.relative_to(ROOT)
        ).replace("\\", "/"),
        "exposure_components_note": (
            "occ22_exposure_components.csv: ATI mean of four digital-information "
            "z-scores; exposure_pct is percentile rank across 22 groups."
        ),
    }
    meta_json_path.write_text(json.dumps(run_meta, indent=2), encoding="utf-8")

    append_registry_rows_t002(onet_v)
    print(f"Wrote {heatmap_path} ({len(heatmap_out)} rows)")
    print(f"Wrote {exposure_path} ({len(exposure_df)} rows)")
    print(f"Wrote {tercile_path} ({len(terc_out)} rows)")
    print(f"Meta: {meta_path}")
    print(f"Run metadata: {meta_json_path}")


if __name__ == "__main__":
    main()
