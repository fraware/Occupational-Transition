"""O*NET database text zip and Work Activities parsing."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pandas as pd

from occupational_transition.http import download_to_path

ONET_DB_PAGE = "https://www.onetcenter.org/database.html"
ONET_RELEASES_ARCHIVE = "https://www.onetcenter.org/db_releases.html"
ONET_SOC_XWALK_URL = (
    "https://www.onetcenter.org/taxonomy/2019/soc/2019_to_SOC_Crosswalk.csv?fmt=csv"
)


def onet_version_to_zip_token(version: str) -> str:
    """Map '30.2' to '30_2' for official zip filenames (db_30_2_text.zip)."""
    return version.strip().replace(".", "_")


def ensure_onet_text_zip(version: str, raw_dir: Path) -> Path:
    """Download O*NET db_<version>_text.zip if missing or too small."""
    token = onet_version_to_zip_token(version)
    fname = f"db_{token}_text.zip"
    dest = raw_dir / fname
    url = f"https://www.onetcenter.org/dl_files/database/{fname}"
    download_to_path(url, dest, skip_if_exists_min_bytes=10_000)
    return dest


def read_work_activities_im(
    zip_path: Path, frozen_elements: tuple[str, ...]
) -> pd.DataFrame:
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
    df = df[df["element_name"].isin(frozen_elements)]
    df = df.dropna(subset=["data_value", "onet_soc_code"])
    return df[["onet_soc_code", "element_name", "data_value"]]


def ensure_soc_crosswalk(raw_dir: Path, url: str | None = None) -> Path:
    """Download O*NET-SOC 2019 to 2018 SOC crosswalk if missing."""
    dest = raw_dir / "onet_2019_to_soc2018_crosswalk.csv"
    if dest.exists():
        return dest
    download_to_path(url or ONET_SOC_XWALK_URL, dest, skip_if_exists_min_bytes=0)
    return dest


def load_soc_crosswalk(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.rename(
        columns={
            "O*NET-SOC 2019 Code": "onet_soc_code",
            "2018 SOC Code": "soc_2018",
        }
    )
    df["soc_2018"] = df["soc_2018"].astype(str).str.strip()
    return df[["onet_soc_code", "soc_2018"]]
