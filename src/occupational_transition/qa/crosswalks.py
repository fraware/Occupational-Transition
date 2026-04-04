"""QA checks for PR-000 crosswalk outputs and ``docs/data_registry.csv``."""

from __future__ import annotations

import sys

import pandas as pd

from occupational_transition.paths import repo_root


def main() -> int:
    root = repo_root()
    occ_path = root / "crosswalks" / "occ22_crosswalk.csv"
    sec_path = root / "crosswalks" / "sector6_crosswalk.csv"
    reg_path = root / "docs" / "data_registry.csv"

    errors: list[str] = []

    o = pd.read_csv(occ_path)
    dup_occ = o.duplicated(subset=["source_system", "source_occ_code"]).any()
    if dup_occ:
        errors.append("occ22_crosswalk: duplicate (source_system, source_occ_code)")

    prdt = o[o["source_system"] == "CPS_PRDTOCC1"]
    if len(prdt) != 23:
        errors.append(f"occ22: expected 23 PRDTOCC1 rows, got {len(prdt)}")
    for i in range(1, 23):
        row = prdt[prdt["source_occ_code"].astype(str) == str(i)]
        if row.empty or str(row.iloc[0]["occ22_id"]) == "":
            errors.append(f"occ22: PRDTOCC1={i} missing occ22_id")
    mil = prdt[prdt["source_occ_code"].astype(str) == "23"]
    if mil.empty:
        errors.append("occ22: PRDTOCC1=23 (Armed Forces) missing")
    else:
        mil_ex = str(mil.iloc[0]["is_military_excluded"]).lower()
        if mil_ex not in ("true", "1"):
            errors.append("occ22: PRDTOCC1=23 should be is_military_excluded true")

    s = pd.read_csv(sec_path)
    dup_sec = s.duplicated(subset=["source_program", "source_code"]).any()
    if dup_sec:
        errors.append("sector6_crosswalk: duplicate (source_program, source_code)")

    ins = s[s["is_in_scope"].astype(str) == "1"]
    empty_code = ins["sector6_code"].isna() | (ins["sector6_code"].astype(str) == "")
    bad = ins[empty_code]
    if len(bad) > 0:
        msg = f"sector6: {len(bad)} in-scope rows missing sector6_code"
        errors.append(msg)

    r = pd.read_csv(reg_path)
    required_cols = [
        "dataset_id",
        "program",
        "source_url",
        "download_url",
        "file_format",
        "release_date_reported",
        "source_last_modified_observed",
        "snapshot_download_date",
        "extractor",
        "update_cadence",
        "notes_for_users",
    ]
    for c in required_cols:
        if c not in r.columns:
            errors.append(f"data_registry: missing column {c}")

    if not r.empty:
        if r["dataset_id"].astype(str).str.strip().eq("").any():
            errors.append("data_registry: blank dataset_id values")
        if r["dataset_id"].duplicated().any():
            errors.append("data_registry: duplicate dataset_id values")
        if r["source_url"].astype(str).str.startswith("http://").any():
            errors.append("data_registry: source_url contains non-HTTPS links")
        if r["download_url"].astype(str).str.startswith("http://").any():
            errors.append("data_registry: download_url contains non-HTTPS links")
        for c in ["release_date_reported", "source_last_modified_observed"]:
            blank = r[c].astype(str).str.strip().eq("")
            if blank.any():
                errors.append(f"data_registry: blank values in {c}")

        cadence_ok = {"static", "annual", "rolling", "reference"}
        cadence_vals = r["update_cadence"].astype(str).str.strip()
        bad_c = ~cadence_vals.isin(cadence_ok)
        if bad_c.any():
            bad_ids = r.loc[bad_c, "dataset_id"].tolist()
            errors.append(
                "data_registry: update_cadence must be one of "
                f"{sorted(cadence_ok)} (bad rows: {bad_ids})"
            )

        extractor_ok = {
            "",
            "http_download",
            "jolts_labstat_file",
            "btos_api_json",
        }
        ext_vals = r["extractor"].fillna("").astype(str).str.strip()
        bad_e = ~ext_vals.isin(extractor_ok)
        if bad_e.any():
            errors.append(
                "data_registry: unknown extractor value "
                f"(bad rows: {r.loc[bad_e, 'dataset_id'].tolist()})"
            )

        nu_blank = r["notes_for_users"].astype(str).str.strip().eq("")
        if nu_blank.any():
            errors.append(
                "data_registry: notes_for_users must be non-blank for each row"
            )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print("QA OK: occ22_crosswalk.csv, sector6_crosswalk.csv, data_registry.csv")
    return 0
