"""
Build occ22_crosswalk.csv and sector6_crosswalk.csv from official Census/BLS inputs.

Run from repo root: python scripts/build_crosswalks.py
"""

from __future__ import annotations

import csv
import json
import re
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
CROSS = ROOT / "crosswalks"
DOCS = ROOT / "docs"

SNAPSHOT_DATE = date.today().isoformat()

SOC_MAJOR_LABELS: dict[str, str] = {
    "11-0000": "Management Occupations",
    "13-0000": "Business and Financial Operations Occupations",
    "15-0000": "Computer and Mathematical Occupations",
    "17-0000": "Architecture and Engineering Occupations",
    "19-0000": "Life, Physical, and Social Science Occupations",
    "21-0000": "Community and Social Service Occupations",
    "23-0000": "Legal Occupations",
    "25-0000": "Educational Instruction and Library Occupations",
    "27-0000": "Arts, Design, Entertainment, Sports, and Media Occupations",
    "29-0000": "Healthcare Practitioners and Technical Occupations",
    "31-0000": "Healthcare Support Occupations",
    "33-0000": "Protective Service Occupations",
    "35-0000": "Food Preparation and Serving Related Occupations",
    "37-0000": "Building and Grounds Cleaning and Maintenance Occupations",
    "39-0000": "Personal Care and Service Occupations",
    "41-0000": "Sales and Related Occupations",
    "43-0000": "Office and Administrative Support Occupations",
    "45-0000": "Farming, Fishing, and Forestry Occupations",
    "47-0000": "Construction and Extraction Occupations",
    "49-0000": "Installation, Maintenance, and Repair Occupations",
    "51-0000": "Production Occupations",
    "53-0000": "Transportation and Material Moving Occupations",
    "55-0000": "Military Specific Occupations",
}

SECTOR6 = {
    "MFG": "Manufacturing",
    "INF": "Information",
    "FAS": "Financial activities",
    "PBS": "Professional and business services",
    "HCS": "Health care and social assistance",
    "RET": "Retail trade",
}

PRDTOCC1_ROWS = [
    (1, "Management occupations", "0010-0440", "11-0000"),
    (2, "Business and financial operations occupations", "0500-0960", "13-0000"),
    (3, "Computer and mathematical science occupations", "1005-1240", "15-0000"),
    (4, "Architecture and engineering occupations", "1305-1560", "17-0000"),
    (5, "Life, physical, and social science occupations", "1600-1980", "19-0000"),
    (6, "Community and social service occupation", "2001-2060", "21-0000"),
    (7, "Legal occupations", "2100-2180", "23-0000"),
    (8, "Education, training, and library occupations", "2205-2550", "25-0000"),
    (9, "Arts, design, entertainment, sports, and media occupations", "2600-2970", "27-0000"),
    (10, "Healthcare practitioner and technical occupations", "3000-3550", "29-0000"),
    (11, "Healthcare support occupations", "3600-3655", "31-0000"),
    (12, "Protective service occupations", "3700-3960", "33-0000"),
    (13, "Food preparation and serving related occupations", "4000-4160", "35-0000"),
    (14, "Building and grounds cleaning and maintenance occupations", "4200-4255", "37-0000"),
    (15, "Personal care and service occupations", "4300-4655", "39-0000"),
    (16, "Sales and related occupations", "4700-4965", "41-0000"),
    (17, "Office and administrative support occupations", "5000-5940", "43-0000"),
    (18, "Farming, fishing, and forestry occupations", "6005-6130", "45-0000"),
    (19, "Construction and extraction occupations", "6200-6950", "47-0000"),
    (20, "Installation, maintenance, and repair occupations", "7000-7640", "49-0000"),
    (21, "Production occupations", "7700-8990", "51-0000"),
    (22, "Transportation and material moving occupations", "9005-9760", "53-0000"),
    (23, "Armed Forces", "9840", "55-0000"),
]


def soc_detail_to_major(soc_raw: str | float) -> str | None:
    if soc_raw is None or (isinstance(soc_raw, float) and pd.isna(soc_raw)):
        return None
    s = str(soc_raw).strip().upper()
    if not s or s == "NAN":
        return None
    if " - " in s and len(s.split(" - ")[0]) <= 7:
        return None
    token = re.split(r"\s+", s)[0]
    if "-" not in token:
        return None
    left, _right = token.split("-", 1)
    left = left.strip()
    if not left.isdigit():
        return None
    prefix = int(left)
    if prefix < 11 or prefix > 55:
        return None
    return f"{prefix:02d}-0000"


def occ22_from_soc_major(major: str | None) -> tuple[int | None, str | None, bool]:
    if major is None:
        return None, None, False
    if major == "55-0000":
        return None, None, True
    ordered = [m for m in SOC_MAJOR_LABELS if m != "55-0000"]
    if major not in ordered:
        return None, None, False
    idx = ordered.index(major) + 1
    return idx, SOC_MAJOR_LABELS[major], False


def load_bls_tsv(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if not lines:
        return []
    header = lines[0].split("\t")
    rows: list[dict[str, str]] = []
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split("\t")
        rows.append(dict(zip(header, parts)))
    return rows


def naics2_to_sector6(n2: int) -> tuple[str | None, str, str]:
    """Map NAICS 2-digit sector to frozen six-sector set."""
    if n2 in (31, 32, 33):
        return "MFG", SECTOR6["MFG"], "naics2_manufacturing"
    if n2 == 51:
        return "INF", SECTOR6["INF"], "naics2_information"
    if n2 in (52, 53):
        return "FAS", SECTOR6["FAS"], "naics2_finance_or_real_estate"
    if n2 in (54, 55, 56):
        return "PBS", SECTOR6["PBS"], "naics2_professional_management_admin"
    if n2 == 62:
        return "HCS", SECTOR6["HCS"], "naics2_health_social_assistance"
    if n2 in (44, 45):
        return "RET", SECTOR6["RET"], "naics2_retail"
    if n2 == 61:
        return "PBS", SECTOR6["PBS"], "naics2_educational_services_maps_to_PBS"
    return None, "", "out_of_scope_six_sector"


def naics_string_to_n2(naics_field: str) -> int | None:
    """Extract leading NAICS digits from CES-style field (may list multiple codes)."""
    if not naics_field or naics_field.strip() in ("-", "", "nan"):
        return None
    first = naics_field.split(",")[0].strip()
    digits = "".join(ch for ch in first if ch.isdigit())
    if len(digits) < 2:
        return None
    return int(digits[:2])


def bed_industry_to_naics_n2(code: str) -> int | None:
    """BED industry_code 300xxx encodes NAICS as industry_code - 300000 (BLS file convention)."""
    if not code.isdigit() or len(code) != 6:
        return None
    ci = int(code)
    if 300000 <= ci <= 399999:
        naics_val = ci - 300000
        s = str(naics_val)
        if len(s) >= 2:
            return int(s[:2])
    return None


def build_occ22_rows() -> list[dict[str, str]]:
    out: list[dict[str, str]] = []

    for prdt, desc, crange, soc_major in PRDTOCC1_ROWS:
        occ22_id, occ22_label, is_mil = occ22_from_soc_major(soc_major)
        out.append(
            {
                "source_system": "CPS_PRDTOCC1",
                "source_occ_code": str(prdt),
                "source_occ_title": desc,
                "census_occ_code_range": crange,
                "soc_major_group_code": soc_major,
                "soc_major_group_title": SOC_MAJOR_LABELS.get(soc_major, ""),
                "occ22_id": str(occ22_id) if occ22_id is not None else "",
                "occ22_label": occ22_label or "",
                "is_military_excluded": "true" if (is_mil or prdt == 23) else "false",
                "notes": "Census CPS Occupation Codes PDF Appendix 10; PRDTOCC1 Basic CPS",
            }
        )

    xlsx_path = RAW / "table-a1_a2.xlsx"
    df = pd.read_excel(xlsx_path, sheet_name="2018 Census Occ Code List", header=None)
    seen_census: set[str] = set()
    soc_codes_for_detail: set[str] = set()

    for _, r in df.iterrows():
        title = r[1]
        ccode = r[2]
        soc = r[3]
        if pd.isna(ccode) or pd.isna(soc):
            continue
        cstr = str(ccode).strip()
        if not re.fullmatch(r"\d{4}", cstr):
            continue
        major = soc_detail_to_major(soc)
        if major is None:
            continue
        occ22_id, occ22_label, is_mil = occ22_from_soc_major(major)
        if cstr not in seen_census:
            seen_census.add(cstr)
            out.append(
                {
                    "source_system": "CPS_PEIO1OCD_2018",
                    "source_occ_code": cstr,
                    "source_occ_title": "" if pd.isna(title) else str(title).strip(),
                    "census_occ_code_range": "",
                    "soc_major_group_code": major,
                    "soc_major_group_title": SOC_MAJOR_LABELS.get(major, ""),
                    "occ22_id": str(occ22_id) if occ22_id is not None else "",
                    "occ22_label": occ22_label or "",
                    "is_military_excluded": "true" if is_mil else "false",
                    "notes": "2018 Census occupation code Table A2 (TP-78); PEIO1OCD detailed",
                }
            )

        token = re.split(r"\s+", str(soc).strip())[0]
        if soc_detail_to_major(soc):
            soc_codes_for_detail.add(token)

    for soc_token in sorted(soc_codes_for_detail):
        major = soc_detail_to_major(soc_token)
        if major is None:
            continue
        occ22_id, occ22_label, is_mil = occ22_from_soc_major(major)
        out.append(
            {
                "source_system": "SOC_2018_DETAIL",
                "source_occ_code": soc_token,
                "source_occ_title": "",
                "census_occ_code_range": "",
                "soc_major_group_code": major,
                "soc_major_group_title": SOC_MAJOR_LABELS.get(major, ""),
                "occ22_id": str(occ22_id) if occ22_id is not None else "",
                "occ22_label": occ22_label or "",
                "is_military_excluded": "true" if is_mil else "false",
                "notes": "SOC 2018 detail; major group from prefix; OEWS/O*NET alignment",
            }
        )

    return out


def jolts_row_to_sector6(code: str) -> tuple[str | None, str, int, str]:
    c = code.strip()
    if c in ("300000", "320000", "340000"):
        return "MFG", SECTOR6["MFG"], 1, "jolts_manufacturing_family"
    if c == "510000":
        return "INF", SECTOR6["INF"], 1, "jolts_information"
    if c == "510099":
        return "FAS", SECTOR6["FAS"], 1, "jolts_financial_activities"
    if c in ("520000", "530000"):
        return "FAS", SECTOR6["FAS"], 1, "jolts_finance_or_real_estate"
    if c == "540099":
        return "PBS", SECTOR6["PBS"], 1, "jolts_professional_business_services"
    if c == "610000":
        return "PBS", SECTOR6["PBS"], 1, "jolts_private_educational_services"
    if c == "620000":
        return "HCS", SECTOR6["HCS"], 1, "jolts_health_care_social_assistance"
    if c == "440000":
        return "RET", SECTOR6["RET"], 1, "jolts_retail_trade"
    if c in (
        "000000",
        "100000",
        "110099",
        "230000",
        "400000",
        "420000",
        "480099",
        "600000",
        "700000",
        "710000",
        "720000",
        "810000",
        "900000",
        "910000",
        "920000",
        "923000",
        "929000",
    ):
        return None, "", 0, "jolts_aggregate_outside_frozen_six"
    return None, "", 0, "jolts_not_in_frozen_six"


def ces_supersector_to_sector6(code: str) -> tuple[str | None, str, int, str]:
    m = {
        "30": ("MFG", SECTOR6["MFG"], "ces_supersector_manufacturing"),
        "31": ("MFG", SECTOR6["MFG"], "ces_supersector_durable_mfg"),
        "32": ("MFG", SECTOR6["MFG"], "ces_supersector_nondurable_mfg"),
        "50": ("INF", SECTOR6["INF"], "ces_supersector_information"),
        "55": ("FAS", SECTOR6["FAS"], "ces_supersector_financial_activities"),
        "60": ("PBS", SECTOR6["PBS"], "ces_supersector_professional_business_services"),
        "65": ("HCS", SECTOR6["HCS"], "ces_supersector_private_education_health"),
        "42": ("RET", SECTOR6["RET"], "ces_supersector_retail_trade"),
    }
    if code in m:
        sc, lab, ru = m[code]
        return sc, lab, 1, ru
    if code in ("00", "05", "06", "07", "08", "10", "20", "40", "41", "43", "44", "70", "80", "90"):
        return None, "", 0, "ces_supersector_aggregate_outside_frozen_six"
    return None, "", 0, "ces_supersector_unmapped"


def bed_row_to_sector6(code: str, name: str) -> tuple[str | None, str, int, str]:
    n2 = bed_industry_to_naics_n2(code)
    if n2 is not None:
        s6, lab, rule = naics2_to_sector6(n2)
        if s6:
            return s6, lab, 1, f"bed_naics_derived_{rule}"
        return None, "", 0, f"bed_naics_out_of_scope_{rule}"

    c = code.strip()
    if c == "100030":
        return "MFG", SECTOR6["MFG"], 1, "bed_goods_producing_manufacturing"
    if c == "200050":
        return "INF", SECTOR6["INF"], 1, "bed_service_information"
    if c == "200060":
        return "FAS", SECTOR6["FAS"], 1, "bed_service_financial_activities"
    if c == "200070":
        return "PBS", SECTOR6["PBS"], 1, "bed_service_professional_business"
    if c == "200080":
        return "HCS", SECTOR6["HCS"], 1, "bed_service_education_health_combined_nearest_hcs"
    if c == "200020":
        return "RET", SECTOR6["RET"], 1, "bed_service_retail_trade"
    if c.startswith(("000000", "100000", "200000")):
        return None, "", 0, "bed_top_level_aggregate"
    return None, "", 0, "bed_unmapped"


def build_sector6_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    jpath = RAW / "btos_api_strata.json"
    if jpath.exists():
        strata = json.loads(jpath.read_text(encoding="utf-8"))
        for s in strata:
            st = s.get("STRATA_TYPE")
            sv = s.get("STRATA_VALUE")
            if st == "naics2" and sv:
                sv_s = str(sv).strip()
                if sv_s in ("XX", "XXX") or not sv_s[0].isdigit():
                    rows.append(
                        {
                            "source_program": "BTOS",
                            "source_code": sv_s,
                            "source_label": "",
                            "source_level": "naics2",
                            "naics_reference": sv_s,
                            "sector6_code": "",
                            "sector6_label": "",
                            "mapping_rule": "btos_suppressed_or_invalid_sector",
                            "is_in_scope": "0",
                        }
                    )
                    continue
                n2 = int(sv_s[:2]) if len(sv_s) >= 2 else None
                if n2 is None:
                    continue
                s6, lab, rule = naics2_to_sector6(n2)
                rows.append(
                    {
                        "source_program": "BTOS",
                        "source_code": sv_s,
                        "source_label": "",
                        "source_level": "naics2",
                        "naics_reference": sv_s,
                        "sector6_code": s6 or "",
                        "sector6_label": lab,
                        "mapping_rule": rule,
                        "is_in_scope": "1" if s6 else "0",
                    }
                )
            elif st == "naics3" and sv:
                v = str(sv).replace("X", "0")
                digits = "".join(ch for ch in v if ch.isdigit())
                n2 = int(digits[:2]) if len(digits) >= 2 else None
                if n2 is None:
                    s6, lab, rule = None, "", "naics3_unparsed"
                else:
                    s6, lab, rule = naics2_to_sector6(n2)
                rows.append(
                    {
                        "source_program": "BTOS",
                        "source_code": str(sv),
                        "source_label": "",
                        "source_level": "naics3",
                        "naics_reference": str(sv),
                        "sector6_code": s6 or "",
                        "sector6_label": lab,
                        "mapping_rule": rule + "_from_naics3",
                        "is_in_scope": "1" if s6 else "0",
                    }
                )

    jt = RAW / "jt.industry.txt"
    if jt.exists():
        for r in load_bls_tsv(jt):
            code = r.get("industry_code", "").strip()
            label = r.get("industry_text", "")
            sc, lab, ins, rule = jolts_row_to_sector6(code)
            rows.append(
                {
                    "source_program": "JOLTS",
                    "source_code": code,
                    "source_label": label,
                    "source_level": "jolts_industry",
                    "naics_reference": "",
                    "sector6_code": sc or "",
                    "sector6_label": lab,
                    "mapping_rule": rule,
                    "is_in_scope": str(ins),
                }
            )

    ce = RAW / "ce.supersector.txt"
    if ce.exists():
        for r in load_bls_tsv(ce):
            code = r.get("supersector_code", "").strip()
            label = r.get("supersector_name", "")
            sc, lab, ins, rule = ces_supersector_to_sector6(code)
            rows.append(
                {
                    "source_program": "CES",
                    "source_code": code,
                    "source_label": label,
                    "source_level": "ces_supersector",
                    "naics_reference": "",
                    "sector6_code": sc or "",
                    "sector6_label": lab,
                    "mapping_rule": rule,
                    "is_in_scope": str(ins),
                }
            )

    cei = RAW / "ce.industry.txt"
    if cei.exists():
        for r in load_bls_tsv(cei):
            code = r.get("industry_code", "").strip()
            name = r.get("industry_name", "")
            naics_f = r.get("naics_code", "")
            n2 = naics_string_to_n2(naics_f)
            if n2 is None:
                rows.append(
                    {
                        "source_program": "CES",
                        "source_code": code,
                        "source_label": name,
                        "source_level": "ces_industry",
                        "naics_reference": naics_f,
                        "sector6_code": "",
                        "sector6_label": "",
                        "mapping_rule": "ces_no_naics_or_total",
                        "is_in_scope": "0",
                    }
                )
                continue
            s6, lab, rule = naics2_to_sector6(n2)
            rows.append(
                {
                    "source_program": "CES",
                    "source_code": code,
                    "source_label": name,
                    "source_level": "ces_industry",
                    "naics_reference": naics_f,
                    "sector6_code": s6 or "",
                    "sector6_label": lab,
                    "mapping_rule": rule + "_from_ces_naics",
                    "is_in_scope": "1" if s6 else "0",
                }
            )

        # QCEW uses the same NAICS industry definitions as CES/BLS; map unique NAICS 2-digit from CES file
        seen_n2: set[int] = set()
        for r in load_bls_tsv(cei):
            naics_f = r.get("naics_code", "")
            n2 = naics_string_to_n2(naics_f)
            if n2 is None or n2 in seen_n2:
                continue
            seen_n2.add(n2)
            s6, lab, rule = naics2_to_sector6(n2)
            rows.append(
                {
                    "source_program": "QCEW",
                    "source_code": f"NAICS2_{n2:02d}",
                    "source_label": f"NAICS sector {n2:02d} (via CES naics_code prefix; QCEW uses NAICS)",
                    "source_level": "qcew_naics2_via_ces",
                    "naics_reference": f"{n2:02d}",
                    "sector6_code": s6 or "",
                    "sector6_label": lab,
                    "mapping_rule": rule + "_qcew_naics_equivalence",
                    "is_in_scope": "1" if s6 else "0",
                }
            )

    bdi = RAW / "bd.industry.txt"
    if bdi.exists():
        for r in load_bls_tsv(bdi):
            code = r.get("industry_code", "").strip()
            name = r.get("industry_name", "")
            sc, lab, ins, rule = bed_row_to_sector6(code, name)
            rows.append(
                {
                    "source_program": "BED",
                    "source_code": code,
                    "source_label": name,
                    "source_level": "bed_industry",
                    "naics_reference": "",
                    "sector6_code": sc or "",
                    "sector6_label": lab,
                    "mapping_rule": rule,
                    "is_in_scope": str(ins),
                }
            )

    return rows


def write_registry() -> None:
    rows = [
        {
            "dataset_id": "census_tp78_table_a1_a2",
            "program": "Census_ACS_TP78",
            "source_url": "https://www2.census.gov/programs-surveys/demo/tables/industry-occupation/time-series/tp78/table-a1_a2.xlsx",
            "download_url": "https://www2.census.gov/programs-surveys/demo/tables/industry-occupation/time-series/tp78/table-a1_a2.xlsx",
            "file_name": "table-a1_a2.xlsx",
            "file_format": "xlsx",
            "release_date_reported": "",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT_DATE,
            "notes_on_version": "2018 Census occupation codes Table A2",
        },
        {
            "dataset_id": "census_cps_occupation_codes_pdf",
            "program": "Census_CPS",
            "source_url": "https://www2.census.gov/programs-surveys/cps/methodology/Occupation%20Codes.pdf",
            "download_url": "https://www2.census.gov/programs-surveys/cps/methodology/Occupation%20Codes.pdf",
            "file_name": "Occupation_Codes_Jan2025.pdf",
            "file_format": "pdf",
            "release_date_reported": "",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT_DATE,
            "notes_on_version": "Appendix 10 PRDTOCC1 recodes",
        },
        {
            "dataset_id": "bls_soc_2018_structure",
            "program": "BLS_SOC",
            "source_url": "https://www.bls.gov/soc/2018/soc_2018_class_and_coding_structure.pdf",
            "download_url": "https://www.bls.gov/soc/2018/soc_2018_class_and_coding_structure.pdf",
            "file_name": "",
            "file_format": "pdf",
            "release_date_reported": "",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT_DATE,
            "notes_on_version": "2018 SOC major groups",
        },
        {
            "dataset_id": "bls_jt_industry",
            "program": "BLS_JOLTS",
            "source_url": "https://download.bls.gov/pub/time.series/jt/jt.industry",
            "download_url": "https://download.bls.gov/pub/time.series/jt/jt.industry",
            "file_name": "jt.industry.txt",
            "file_format": "tsv",
            "release_date_reported": "",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT_DATE,
            "notes_on_version": "LABSTAT JOLTS industry",
        },
        {
            "dataset_id": "bls_ce_supersector",
            "program": "BLS_CES",
            "source_url": "https://download.bls.gov/pub/time.series/ce/ce.supersector",
            "download_url": "https://download.bls.gov/pub/time.series/ce/ce.supersector",
            "file_name": "ce.supersector.txt",
            "file_format": "tsv",
            "release_date_reported": "",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT_DATE,
            "notes_on_version": "CES supersector",
        },
        {
            "dataset_id": "bls_ce_industry",
            "program": "BLS_CES",
            "source_url": "https://download.bls.gov/pub/time.series/ce/ce.industry",
            "download_url": "https://download.bls.gov/pub/time.series/ce/ce.industry",
            "file_name": "ce.industry.txt",
            "file_format": "tsv",
            "release_date_reported": "",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT_DATE,
            "notes_on_version": "CES NAICS industry codes; used for NAICS-to-sector6 and QCEW NAICS alignment",
        },
        {
            "dataset_id": "bls_bd_industry",
            "program": "BLS_BED",
            "source_url": "https://download.bls.gov/pub/time.series/bd/bd.industry",
            "download_url": "https://download.bls.gov/pub/time.series/bd/bd.industry",
            "file_name": "bd.industry.txt",
            "file_format": "tsv",
            "release_date_reported": "",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT_DATE,
            "notes_on_version": "BED industry classification",
        },
        {
            "dataset_id": "census_btos_api_strata",
            "program": "Census_BTOS",
            "source_url": "https://www.census.gov/hfp/btos/api/strata",
            "download_url": "https://www.census.gov/hfp/btos/api/strata",
            "file_name": "btos_api_strata.json",
            "file_format": "json",
            "release_date_reported": "",
            "source_last_modified_observed": "",
            "snapshot_download_date": SNAPSHOT_DATE,
            "notes_on_version": "BTOS strata naics2/naics3",
        },
        {
            "dataset_id": "bls_qcew_industry_titles",
            "program": "BLS_QCEW",
            "source_url": "https://www.bls.gov/cew/classifications/industry/industry-titles.htm",
            "download_url": "https://www.bls.gov/cew/classifications/industry/industry-titles.csv",
            "file_name": "industry-titles.csv",
            "file_format": "csv",
            "release_date_reported": "",
            "source_last_modified_observed": "BLS page Last Modified May 5 2022",
            "snapshot_download_date": SNAPSHOT_DATE,
            "notes_on_version": "QCEW NAICS industry titles; crosswalk uses NAICS 2-digit mapping consistent with BLS industry classification",
        },
    ]
    DOCS.mkdir(parents=True, exist_ok=True)
    reg_path = DOCS / "data_registry.csv"
    with reg_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    CROSS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    occ_rows = build_occ22_rows()
    fieldnames = [
        "source_system",
        "source_occ_code",
        "source_occ_title",
        "census_occ_code_range",
        "soc_major_group_code",
        "soc_major_group_title",
        "occ22_id",
        "occ22_label",
        "is_military_excluded",
        "notes",
    ]
    with (CROSS / "occ22_crosswalk.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in occ_rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})

    sec_rows = build_sector6_rows()
    sfields = [
        "source_program",
        "source_code",
        "source_label",
        "source_level",
        "naics_reference",
        "sector6_code",
        "sector6_label",
        "mapping_rule",
        "is_in_scope",
    ]
    with (CROSS / "sector6_crosswalk.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=sfields)
        w.writeheader()
        for row in sec_rows:
            w.writerow({k: row.get(k, "") for k in sfields})

    write_registry()
    print(f"Wrote {len(occ_rows)} occ22 rows, {len(sec_rows)} sector6 rows.")


if __name__ == "__main__":
    main()
