"""BLS OEWS helpers for national baseline merges.

This module intentionally focuses on the subset of OEWS functionality needed
by reusable pipelines (e.g. Figure 1 Panel B / T-002).
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

import pandas as pd

from occupational_transition.http import download_to_path

OEWS_ZIP_URL = "https://www.bls.gov/oes/special-requests/oesm24nat.zip"
OEWS_ZIP_NAME = "oesm24nat.zip"


def ensure_oews_national_xlsx(
    raw_dir: Path,
    *,
    zip_url: str = OEWS_ZIP_URL,
    zip_name: str = OEWS_ZIP_NAME,
    extract_dir_name: str = "oesm24nat_extract",
    xlsx_regex: str = r"national_m\d+_dl\.xlsx",
    min_zip_bytes: int = 10_000,
) -> Path:
    """Ensure the May 2024 national OEWS XLSX is present under ``raw_dir``."""
    zip_path = raw_dir / zip_name
    download_to_path(
        zip_url,
        zip_path,
        extra_headers={
            "Referer": "https://www.bls.gov/oes/current/oes_stru.htm",
        },
        skip_if_exists_min_bytes=min_zip_bytes,
    )

    extract_dir = raw_dir / extract_dir_name
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)

    for p in extract_dir.rglob("*.xlsx"):
        if re.search(xlsx_regex, p.name, re.I):
            return p
    raise FileNotFoundError("No national_M*_dl.xlsx found in OEWS zip")


def load_oews_detailed_employment(xlsx_path: Path) -> pd.DataFrame:
    """Load OEWS detailed rows and return SOC-level employment weights."""
    oews = pd.read_excel(xlsx_path, sheet_name=0)
    det = oews[oews["O_GROUP"] == "detailed"].copy()
    det["soc_2018"] = det["OCC_CODE"].astype(str).str.strip()
    det["employment"] = pd.to_numeric(det["TOT_EMP"], errors="coerce")
    det = det.dropna(subset=["employment"])
    det = det[det["employment"] > 0]
    # Exclude military major group 55 (OEWS typically omits; keep rule explicit)
    det = det[~det["soc_2018"].str.startswith("55-")]
    return det[["soc_2018", "employment"]]

