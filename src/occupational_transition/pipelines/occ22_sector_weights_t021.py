"""
Build intermediate/occ22_sector_weights.csv from OEWS industry-specific occupational
employment (BLS special request oesmYYin4.zip) plus national cross-industry totals
for coverage denominators.

Run from repo root: python scripts/build_occ22_sector_weights.py
"""

from __future__ import annotations

import json
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

from occupational_transition.awes_alpi_common import (
    SECTOR6_ORDER,
    naics2_to_sector6,
    naics_string_to_n2,
    occ22_code_from_id,
    soc_code_to_major,
)

OEWS_IN4_ZIP_NAME = "oesm24in4.zip"
OEWS_IN4_ZIP_URL = "https://www.bls.gov/oes/special-requests/oesm24in4.zip"


@dataclass(frozen=True)
class Occ22SectorWeightsPaths:
    root: Path
    raw: Path
    inter: Path
    cross: Path
    extract_dir: Path
    out_csv: Path
    out_meta: Path


def _occ22_sector_weights_paths(root: Path) -> Occ22SectorWeightsPaths:
    raw = root / "raw"
    inter = root / "intermediate"
    return Occ22SectorWeightsPaths(
        root=root,
        raw=raw,
        inter=inter,
        cross=root / "crosswalks" / "occ22_crosswalk.csv",
        extract_dir=raw / "oesm24in4_extract",
        out_csv=inter / "occ22_sector_weights.csv",
        out_meta=inter / "occ22_sector_weights_run_metadata.json",
    )


def run(root: Path) -> None:
    build_occ22_sector_weights(_occ22_sector_weights_paths(root))


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


def _request(url: str) -> Request:
    return Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Referer": "https://www.bls.gov/oes/current/oes_stru.htm",
        },
    )


def download_file(url: str, dest: Path, timeout_s: int = 45) -> None:
    """Fetch with bounded wait; BLS may block or stall from some networks."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urlopen(_request(url), timeout=timeout_s) as resp, open(dest, "wb") as out:
            out.write(resp.read())
    except OSError:
        if dest.exists():
            dest.unlink(missing_ok=True)
        raise


def find_national_m_dl_xlsx(root: Path) -> Path:
    for p in root.glob("raw/oesm24nat_extract/**/national_M*_dl.xlsx"):
        if p.is_file():
            return p
    raise FileNotFoundError(
        "National OEWS workbook not found. Run scripts/build_figure1_panelA.py or "
        "extract oesm24nat.zip under raw/oesm24nat_extract/."
    )


def load_occ22_labels(cross: Path) -> pd.DataFrame:
    cx = pd.read_csv(cross)
    pr = cx[cx["source_system"] == "CPS_PRDTOCC1"].copy()
    pr = pr[pr["source_occ_code"].astype(str) != "23"]
    pr["occ22_id"] = pr["occ22_id"].astype(int)
    return pr[["occ22_id", "occ22_label", "soc_major_group_code"]].drop_duplicates()


def occ22_totals_from_national(xlsx_path: Path, labels: pd.DataFrame) -> pd.DataFrame:
    """National cross-industry detailed occupation employment by occ22."""
    oews = pd.read_excel(xlsx_path, sheet_name=0)
    det = oews[oews["O_GROUP"] == "detailed"].copy()
    det["soc_2018"] = det["OCC_CODE"].astype(str).str.strip()
    det["employment"] = pd.to_numeric(det["TOT_EMP"], errors="coerce")
    det = det.dropna(subset=["employment"])
    det = det[det["employment"] > 0]
    det = det[~det["soc_2018"].str.startswith("55-")]
    det["soc_major"] = det["soc_2018"].map(soc_code_to_major)
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
        oews_occ_total_employment=("employment", "sum"),
    )
    g = g.merge(labels[["occ22_id", "occ22_label"]], on="occ22_id", how="right")
    g["oews_occ_total_employment"] = g["oews_occ_total_employment"].fillna(0.0)
    return g


def ensure_in4_zip(raw: Path, extract_dir: Path) -> Path:
    dest = raw / OEWS_IN4_ZIP_NAME
    if dest.exists() and dest.stat().st_size > 10_000:
        return dest
    try:
        download_file(OEWS_IN4_ZIP_URL, dest, timeout_s=45)
    except OSError as e:
        raise FileNotFoundError(
            f"Could not download {OEWS_IN4_ZIP_URL} ({e}). "
            f"Manually download the BLS OEWS May 2024 national "
            f"industry-specific occupational employment zip (in4 / M2024) "
            f"from https://www.bls.gov/oes/current/oes_stru.htm and save as "
            f"raw/{OEWS_IN4_ZIP_NAME}, or place an extracted workbook tree "
            f"under {extract_dir}."
        ) from e
    return dest


def extract_in4_zip(zip_path: Path, extract_dir: Path) -> Path:
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)
    return extract_dir


def iter_in4_worksheets(extract_root: Path) -> list[Path]:
    """
    Use one OEWS IN4 hierarchy level only. Reading nat3d + nat4d + natsector together
    nests industries and double-counts employment (coverage_share >> 1).

    Prefer BLS national 4-digit NAICS × occupation file; fall back to 3-digit only
    if 4-digit is absent. Skip *owner* and description workbooks.
    """
    skip = (
        "field description",
        "file_descriptions",
        "~$",
    )
    candidates = sorted(
        p
        for p in extract_root.rglob("*.xlsx")
        if p.is_file()
        and not any(s in p.name.lower() for s in skip)
        and "_owner_" not in p.name.lower()
        and p.name.startswith("nat4d_")
    )
    if not candidates:
        candidates = sorted(
            p
            for p in extract_root.rglob("*.xlsx")
            if p.is_file()
            and not any(s in p.name.lower() for s in skip)
            and "_owner_" not in p.name.lower()
            and p.name.startswith("nat3d_")
        )
    if not candidates:
        raise FileNotFoundError(
            f"No nat4d_/nat3d_ industry OEWS xlsx under {extract_root} "
            f"(expected e.g. nat4d_M2024_dl.xlsx; do not mix hierarchy levels)."
        )
    return candidates


def _read_in4_frame(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=0)
    df.columns = [str(c).strip() for c in df.columns]
    req = {"OCC_CODE", "TOT_EMP", "O_GROUP"}
    if not req.issubset(set(df.columns)):
        raise ValueError(f"{path.name} missing columns {req}: have {list(df.columns)}")
    return df


def load_in4_long(extract_root: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in iter_in4_worksheets(extract_root):
        try:
            df = _read_in4_frame(path)
        except ValueError:
            continue
        if "NAICS" not in df.columns:
            continue
        sub = df[df["O_GROUP"].astype(str) == "detailed"].copy()
        if "AREA" in sub.columns:
            sub = sub[pd.to_numeric(sub["AREA"], errors="coerce") == 99]
        sub["TOT_EMP"] = pd.to_numeric(sub["TOT_EMP"], errors="coerce")
        sub = sub.dropna(subset=["TOT_EMP"])
        sub = sub[sub["TOT_EMP"] > 0]
        sub["soc_2018"] = sub["OCC_CODE"].astype(str).str.strip()
        sub = sub[~sub["soc_2018"].str.startswith("55-")]
        sub["naics_raw"] = sub["NAICS"]
        n2 = sub["naics_raw"].map(naics_string_to_n2)
        sub["naics2"] = n2
        sub = sub.dropna(subset=["naics2"])
        sec = sub["naics2"].astype(int).map(lambda x: naics2_to_sector6(int(x))[0])
        sub["sector6_code"] = sec
        sub = sub[sub["sector6_code"].notna()]
        if sub.empty:
            continue
        frames.append(sub[["soc_2018", "naics_raw", "sector6_code", "TOT_EMP"]])
    if not frames:
        raise RuntimeError(
            "No usable industry-by-occupation rows parsed from IN4 extracts."
        )
    long_df = pd.concat(frames, ignore_index=True)
    long_df = long_df.groupby(
        ["soc_2018", "naics_raw", "sector6_code"],
        as_index=False,
    ).agg(oews_cell_employment=("TOT_EMP", "max"))
    long_df = long_df.rename(columns={"oews_cell_employment": "TOT_EMP"})
    return long_df


def build_occ22_sector_weights(p: Occ22SectorWeightsPaths) -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    p.inter.mkdir(parents=True, exist_ok=True)

    labels = load_occ22_labels(p.cross)
    nat_xlsx = find_national_m_dl_xlsx(p.root)
    occ_tot = occ22_totals_from_national(nat_xlsx, labels)

    zip_path = p.raw / OEWS_IN4_ZIP_NAME
    has_prefill = any(p.extract_dir.rglob("*.xlsx"))
    if not has_prefill:
        if zip_path.exists() and zip_path.stat().st_size > 10_000:
            extract_in4_zip(zip_path, p.extract_dir)
        else:
            try:
                ensure_in4_zip(p.raw, p.extract_dir)
                extract_in4_zip(zip_path, p.extract_dir)
            except OSError as e:
                raise FileNotFoundError(
                    "Missing industry OEWS inputs. Provide either "
                    f"(a) {zip_path}, or (b) extracted *.xlsx workbooks under "
                    f"{p.extract_dir} (see BLS OEWS May 2024 industry-specific "
                    f"occupational employment downloads). Last error: {e}"
                ) from e
    long_df = load_in4_long(p.extract_dir)
    long_df["soc_major"] = long_df["soc_2018"].map(soc_code_to_major)
    merged = long_df.merge(
        labels[["occ22_id", "occ22_label", "soc_major_group_code"]],
        left_on="soc_major",
        right_on="soc_major_group_code",
        how="inner",
    )
    g = merged.groupby(
        ["occ22_id", "occ22_label", "sector6_code"],
        as_index=False,
    ).agg(oews_occ_sector_employment=("TOT_EMP", "sum"))

    s6_labels = {
        "MFG": "Manufacturing",
        "INF": "Information",
        "FAS": "Financial activities",
        "PBS": "Professional and business services",
        "HCS": "Health care and social assistance",
        "RET": "Retail trade",
    }

    rows: list[dict[str, object]] = []
    for row in labels.sort_values("occ22_id").itertuples(index=False):
        oid = int(row.occ22_id)
        olabel = str(row.occ22_label)
        sub = g[g["occ22_id"] == oid]
        tot_denom = float(
            occ_tot.loc[occ_tot["occ22_id"] == oid, "oews_occ_total_employment"].iloc[0]
        )
        emp_by_s = {
            str(r.sector6_code): float(r.oews_occ_sector_employment)
            for r in sub.itertuples()
        }
        sum_s = sum(emp_by_s.get(s, 0.0) for s in SECTOR6_ORDER)
        coverage = float(sum_s / tot_denom) if tot_denom > 0 else 0.0
        cov_flag = 1 if coverage < 0.60 else 0
        w_denom = sum_s
        for s in SECTOR6_ORDER:
            emp = emp_by_s.get(s, 0.0)
            w = (emp / w_denom) if w_denom > 0 else 0.0
            rows.append(
                {
                    "occ22_code": occ22_code_from_id(oid),
                    "occ22_label": str(olabel),
                    "sector6_code": s,
                    "sector6_label": s6_labels[s],
                    "oews_occ_sector_employment": emp,
                    "oews_occ_total_employment": tot_denom,
                    "sector_weight": w,
                    "sector6_coverage_share": coverage,
                    "coverage_flag_low": cov_flag,
                }
            )

    out = pd.DataFrame(rows)
    out.to_csv(p.out_csv, index=False)

    meta = {
        "output_csv": str(p.out_csv.relative_to(p.root)).replace("\\", "/"),
        "generated_at_utc": generated_at,
        "formula_version": "AWES-ALPI sector weights v1",
        "oews_in4_zip": OEWS_IN4_ZIP_URL,
        "oews_national_xlsx": str(nat_xlsx.relative_to(p.root)).replace("\\", "/"),
        "coverage_threshold_rule": "coverage_flag_low=1 iff sector6_coverage_share < 0.60",
        "weight_rule": (
            "w_{o,s} = Emp_{o,s} / sum_{s' in S6} Emp_{o,s'}; "
            "S6 is frozen six sectors; no occupations dropped."
        ),
        "normalization_rule": (
            "Emp from OEWS IN4 detailed SOC rows at a single hierarchy file "
            "(nat4d preferred; nat3d fallback); national AREA=99 only; "
            "NAICS mapped to sector6 via leading NAICS2 as in build_crosswalks. "
            "(soc, naics, sector6) cells de-duplicated with max() per workbook set."
        ),
        "row_count": int(len(out)),
        "crosswalk_file": str(p.cross.relative_to(p.root)).replace("\\", "/"),
    }
    p.out_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {p.out_csv} ({len(out)} rows)")
    print(f"Wrote {p.out_meta}")
