"""Figure 1 Panel B pipeline: O*NET Work Activities -> AI Task Index.

This module is intentionally reusable: it fetches/loads the required public
inputs (O*NET, OEWS, crosswalks) and returns CSV-ready dataframes plus the
run metadata contract expected by `scripts/qa_figure1_panelB.py`.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from occupational_transition.awes_alpi_common import (
    occ22_code_from_id,
    percentile_rank_01,
)
from occupational_transition.crosswalks import load_occ22_labels
from occupational_transition.sources.oews import (
    OEWS_ZIP_NAME,
    OEWS_ZIP_URL,
    ensure_oews_national_xlsx,
    load_oews_detailed_employment,
)
from occupational_transition.sources.onet import (
    ONET_DB_PAGE,
    ONET_RELEASES_ARCHIVE,
    ONET_SOC_XWALK_URL,
    ensure_onet_text_zip,
    ensure_soc_crosswalk,
    load_soc_crosswalk,
    onet_version_to_zip_token,
    read_work_activities_im,
)

FROZEN_ELEMENTS: tuple[str, ...] = (
    "Analyzing Data or Information",
    "Processing Information",
    "Documenting/Recording Information",
    "Working with Computers",
    "Assisting and Caring for Others",
    "Handling and Moving Objects",
)

DIGITAL_INFO_ELEMENTS: tuple[str, ...] = FROZEN_ELEMENTS[:4]

Z_OUT_RENAME: dict[str, str] = {
    "Analyzing Data or Information": "onet_analyzing_data_z",
    "Processing Information": "onet_processing_information_z",
    "Documenting/Recording Information": "onet_documenting_recording_z",
    "Working with Computers": "onet_working_with_computers_z",
    "Assisting and Caring for Others": "onet_assisting_caring_z",
    "Handling and Moving Objects": "onet_handling_moving_z",
}


def soc_code_to_major(soc: str) -> str:
    """Map detailed SOC 'XX-YYYY' to major group 'XX-0000'."""
    s = str(soc).strip()
    if "-" not in s:
        raise ValueError(f"Invalid SOC code: {soc!r}")
    left, _ = s.split("-", 1)
    if not left.isdigit():
        raise ValueError(f"Invalid SOC code: {soc!r}")
    return f"{int(left):02d}-0000"


def onet_to_soc_means(wa: pd.DataFrame, xwalk: pd.DataFrame) -> pd.DataFrame:
    """Mean O*NET IM score per (2018 SOC detail, element) across O*NET-SOC rows."""
    m = wa.merge(xwalk, on="onet_soc_code", how="inner")
    if m.empty:
        raise ValueError("No overlap between Work Activities and SOC crosswalk")
    g = (
        m.groupby(["soc_2018", "element_name"], as_index=False)["data_value"]
        .mean()
        .reset_index(drop=True)
    )
    return g


def aggregate_to_occ22(
    soc_element_scores: pd.DataFrame,
    oews_emp: pd.DataFrame,
    labels: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate SOC-level element scores to 22 occ22 groups (employment weighted)."""
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
        raise ValueError(
            f"Unmapped SOC majors for OEWS/O*NET merge: {bad}"
        )

    merged["weighted"] = merged["data_value"] * merged["employment"]
    out_rows: list[pd.DataFrame] = []
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
    return wide.reset_index()


def zscore_22(s: pd.Series) -> pd.Series:
    mu = s.mean()
    sigma = s.std(ddof=0)
    if sigma == 0 or np.isnan(sigma):
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - mu) / sigma


def assign_terciles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deterministic terciles on AI Task Index.

    Sort by (ai_task_index asc, occ22_id asc). For 22 rows:
    low=7, middle=7, high=8.
    """
    d = df.sort_values(["ai_task_index", "occ22_id"]).reset_index(drop=True)
    labels_terc = np.empty(len(d), dtype=object)
    labels_terc[0:7] = "low"
    labels_terc[7:14] = "middle"
    labels_terc[14:22] = "high"
    d["ai_relevance_tercile"] = labels_terc
    return d


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _zcol_name(elem: str) -> str:
    safe = (
        elem.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace(",", "")
    )
    return f"z_{safe}"


@dataclass(frozen=True)
class Figure1PanelB_T002_Result:
    heatmap_out: pd.DataFrame
    terc_out: pd.DataFrame
    exposure_df: pd.DataFrame
    meta_df: pd.DataFrame
    run_metadata: dict[str, Any]
    registry_rows: list[dict[str, str]]


def build_figure1_panelB_t002(
    *,
    onet_version: str = "30.2",
    repo_root: Path | None = None,
    raw_dir: Path | None = None,
    figures_dir: Path | None = None,
    intermediate_dir: Path | None = None,
    crosswalk_csv: Path | None = None,
    snapshot_date: str | None = None,
) -> Figure1PanelB_T002_Result:
    """
    Build the T-002 artifacts in-memory.

    The returned `run_metadata` is aligned to what `scripts/qa_figure1_panelB.py`
    validates.
    """
    repo_root = repo_root or Path.cwd()
    raw_dir = raw_dir or (repo_root / "raw")
    figures_dir = figures_dir or (repo_root / "figures")
    intermediate_dir = intermediate_dir or (repo_root / "intermediate")
    crosswalk_csv = (
        crosswalk_csv or (repo_root / "crosswalks" / "occ22_crosswalk.csv")
    )
    snapshot_date = snapshot_date or date.today().isoformat()

    heatmap_path = figures_dir / "figure1_panelB_task_heatmap.csv"
    tercile_path = intermediate_dir / "ai_relevance_terciles.csv"
    expo_path = intermediate_dir / "occ22_exposure_components.csv"
    meta_path = intermediate_dir / "figure1_panelB_meta.csv"

    labels = load_occ22_labels(crosswalk_csv)

    onet_zip = ensure_onet_text_zip(onet_version, raw_dir)
    wa = read_work_activities_im(onet_zip, FROZEN_ELEMENTS)
    xw_path = ensure_soc_crosswalk(raw_dir)
    xw = load_soc_crosswalk(xw_path)
    soc_elem = onet_to_soc_means(wa, xw)

    xlsx = ensure_oews_national_xlsx(raw_dir)
    oews_det = load_oews_detailed_employment(xlsx)
    wide = aggregate_to_occ22(soc_elem, oews_det, labels)

    # Z-scores across 22 groups for each of six dimensions.
    zcols: dict[str, str] = {}
    for elem in FROZEN_ELEMENTS:
        zcols[elem] = _zcol_name(elem)
        wide[zcols[elem]] = zscore_22(wide[elem])

    wide = wide.merge(labels[["occ22_id", "occ22_label"]], on="occ22_id")
    wide["occupation_group"] = wide["occ22_label"]

    z_digital = [wide[zcols[e]] for e in DIGITAL_INFO_ELEMENTS]
    wide["ai_task_index"] = pd.concat(z_digital, axis=1).mean(axis=1)

    # Exposure components (AWES input artifact).
    exposure_pct = percentile_rank_01(wide["ai_task_index"])
    expo_cols: dict[str, Any] = {
        "occ22_code": wide["occ22_id"].map(occ22_code_from_id),
        "occ22_label": wide["occ22_label"].astype(str),
        "ai_task_index_raw": wide["ai_task_index"].astype(float),
        "exposure_pct": exposure_pct.astype(float),
    }
    for elem, outc in Z_OUT_RENAME.items():
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
    exposure_df = exposure_df[exposure_cols_order]

    # Terciles.
    terc = assign_terciles(
        wide[["occ22_id", "occupation_group", "ai_task_index"]].copy()
    )
    heatmap_cols = ["occupation_group", "occ22_id"] + [
        zcols[e] for e in FROZEN_ELEMENTS
    ]
    heatmap_out = wide[heatmap_cols].sort_values("occ22_id")
    terc_out = terc.sort_values("occ22_id")[
        ["occupation_group", "occ22_id", "ai_task_index", "ai_relevance_tercile"]
    ]

    # Legacy meta CSV (inputs description; does not replace run metadata JSON).
    meta_df = pd.DataFrame(
        [
            {
                "onet_version": onet_version,
                "onet_text_zip": str(onet_zip.relative_to(repo_root)),
                "scale_id": "IM",
                "scale_name": "Importance",
                "oews_file": str(xlsx.relative_to(repo_root)),
                "oews_zip_url": OEWS_ZIP_URL,
                "crosswalk_file": str(xw_path.relative_to(repo_root)),
                "snapshot_date": snapshot_date,
                "zscore_scope": "22 occupation groups; population std (ddof=0)",
                "ai_task_index": (
                    "mean of z-scores for four digital-information work "
                    "activities"
                ),
                "tercile_rule": (
                    "sort by ai_task_index ascending then occ22_id; "
                    "ranks 1-7 low, 8-14 middle, 15-22 high"
                ),
            }
        ]
    )

    def rel(p: Path) -> str:
        return str(p.relative_to(repo_root)).replace("\\", "/")

    onet_zip_url = (
        "https://www.onetcenter.org/dl_files/database/"
        f"db_{onet_version_to_zip_token(onet_version)}_text.zip"
    )

    run_metadata: dict[str, Any] = {
        "ticket": "T-002",
        "output_heatmap_csv": rel(heatmap_path),
        "output_terciles_csv": rel(tercile_path),
        "legacy_meta_csv": rel(meta_path),
        "source_selection_mode": "pinned_vintage_required_by_ticket",
        "source_selection_rule": (
            "Pinned O*NET version parameter and pinned OEWS May 2024 zip for "
            "cross-sectional baseline."
        ),
        "onet_version": onet_version,
        "sources": [
            {
                "file_name": onet_zip.name,
                "url": onet_zip_url,
                "local_cache_path": rel(onet_zip),
                "sha256": _sha256_file(onet_zip),
            },
            {
                "file_name": xw_path.name,
                "url": ONET_SOC_XWALK_URL,
                "local_cache_path": rel(xw_path),
                "sha256": _sha256_file(xw_path),
            },
            {
                "file_name": OEWS_ZIP_NAME,
                "url": OEWS_ZIP_URL,
                "local_cache_path": rel(raw_dir / OEWS_ZIP_NAME),
                "sha256": _sha256_file(raw_dir / OEWS_ZIP_NAME),
            },
        ],
        "crosswalk_sha256": _sha256_file(crosswalk_csv),
        "row_count_heatmap": int(len(heatmap_out)),
        "row_count_terciles": int(len(terc_out)),
        "output_exposure_components_csv": rel(expo_path),
        "exposure_components_note": (
            "occ22_exposure_components.csv: ATI mean of four digital-information "
            "z-scores; exposure_pct is percentile rank across 22 groups."
        ),
    }

    # Registry rows (optional side-effect handled by caller).
    registry_rows: list[dict[str, str]] = [
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
            "snapshot_download_date": snapshot_date,
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
            "snapshot_download_date": snapshot_date,
            "notes_on_version": "Historical O*NET database release versions",
        },
        {
            "dataset_id": f"onet_{onet_version.replace('.', '_')}_text_database_zip",
            "program": "O_NET",
            "source_url": ONET_DB_PAGE,
            "download_url": onet_zip_url,
            "file_name": f"db_{onet_version_to_zip_token(onet_version)}_text.zip",
            "file_format": "zip",
            "release_date_reported": "",
            "source_last_modified_observed": "",
            "snapshot_download_date": snapshot_date,
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
            "snapshot_download_date": snapshot_date,
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
            "snapshot_download_date": snapshot_date,
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
            "snapshot_download_date": snapshot_date,
            "notes_on_version": "O*NET-SOC 2019 to 2018 SOC crosswalk",
        },
    ]

    return Figure1PanelB_T002_Result(
        heatmap_out=heatmap_out.reset_index(drop=True),
        terc_out=terc_out.reset_index(drop=True),
        exposure_df=exposure_df,
        meta_df=meta_df,
        run_metadata=run_metadata,
        registry_rows=registry_rows,
    )

