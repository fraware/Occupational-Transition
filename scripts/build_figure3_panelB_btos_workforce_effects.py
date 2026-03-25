"""
Build figures/figure3_panelB_btos_workforce_effects.csv from official Census BTOS
AI supplement published tables (primary: AI_Supplement_Table.xlsx).

National, Scope 2 (AI-using firms in the last six months), pooled supplement window
documented in Census materials for the six two-week panels spanning Dec 2023–Feb 2024.

Run from repo root: python scripts/build_figure3_panelB_btos_workforce_effects.py
"""

from __future__ import annotations

import hashlib
import io
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
OUT_CSV = FIG / "figure3_panelB_btos_workforce_effects.csv"
OUT_META = INTER / "figure3_panelB_btos_workforce_effects_run_metadata.json"

PRIMARY_XLSX_URL = "https://www.census.gov/hfp/btos/downloads/AI_Supplement_Table.xlsx"
FALLBACK_ARCHIVE_URL = (
    "https://www.census.gov/hfp/btos/downloads/archive/v1/AI_Supplement_Table.xlsx"
)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# Frozen design window (T-007 / issues.md).
WINDOW_START = "2023-12-04"
WINDOW_END = "2024-02-25"

# Data dictionary Scope 2: firms that used AI to produce goods or services in last six months.
SCOPE_AI_USERS = 2

NATIONAL_SHEET = "National Response Estimates"

# Official questionnaire (AI supplement V4) item 25 is multi-select; item 28 is employment.
# The published AI_Supplement_Table.xlsx (snapshot) does not include Q25 option rows; see methodology.
Q25_QUESTION_SUBSTRING = "did this business use artificial intelligence (ai) to do any of the following"

OUT_COLS = [
    "category_key",
    "category_label",
    "weighted_share",
    "window_start",
    "window_end",
    "source_series_id",
    "evidence_directness",
]


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch_bytes(url: str) -> tuple[bytes, str | None]:
    with urlopen(_request(url), timeout=180) as resp:
        return resp.read(), resp.headers.get("Content-Type")


def parse_percent_cell(cell: Any) -> float:
    """Parse '5.0%', '0.05%', or numeric to share in [0, 1]."""
    if cell is None or (isinstance(cell, float) and pd.isna(cell)):
        raise ValueError("empty estimate cell")
    s = str(cell).strip()
    s = s.replace("\u00a0", " ")
    m = re.match(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*%\s*$", s)
    if m:
        return float(m.group(1)) / 100.0
    try:
        v = float(s)
    except ValueError as exc:
        raise ValueError(f"unrecognized estimate format: {cell!r}") from exc
    if v > 1.0 + 1e-9:
        return v / 100.0
    return v


def normalize_question(s: str) -> str:
    return re.sub(r"\s+", " ", str(s).strip().lower())


def normalize_answer(s: str) -> str:
    t = str(s).strip()
    t = t.replace("\u2019", "'").replace("\u2018", "'")
    return t


def extract_national_scope2(df: pd.DataFrame) -> pd.DataFrame:
    scope_col = "Scope (see data dictionary)"
    out = df[df[scope_col] == SCOPE_AI_USERS].copy()
    if out.empty:
        raise RuntimeError("No rows for Scope 2 (AI-using firms) in National sheet.")
    return out


def find_row(
    sub: pd.DataFrame,
    qid: float,
    answer_exact: str,
) -> pd.Series:
    m = (sub["Question ID"] == qid) & (
        sub["Answer"].map(normalize_answer) == normalize_answer(answer_exact)
    )
    hit = sub[m]
    if len(hit) != 1:
        raise RuntimeError(
            f"Expected exactly one row for QID {qid} answer {answer_exact!r}, got {len(hit)}"
        )
    return hit.iloc[0]


def find_q25_option(
    sub: pd.DataFrame, answer_label: str
) -> pd.Series | None:
    """Match questionnaire Q25-style answer text if published."""
    m = sub["Question"].map(normalize_question).str.contains(
        Q25_QUESTION_SUBSTRING, regex=False, na=False
    ) & (sub["Answer"].map(normalize_answer) == normalize_answer(answer_label))
    hit = sub[m]
    if len(hit) == 1:
        return hit.iloc[0]
    return None


def build_output_rows(sub: pd.DataFrame) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Returns rows and mapping metadata (which source row was used per category).
    """
    mapping: dict[str, Any] = {
        "primary_workbook": PRIMARY_XLSX_URL,
        "scope_code": SCOPE_AI_USERS,
        "sheet": NATIONAL_SHEET,
        "category_to_source": {},
    }

    rows: list[dict[str, Any]] = []

    # --- Employment (published Q6 / internal table Question ID 6.0) ---
    emp_answers = [
        ("employment_increased", "Increased", "Employment increased"),
        ("employment_decreased", "Decreased", "Employment decreased"),
        ("employment_did_not_change", "Did not change", "Employment did not change"),
    ]
    for key, ans, label in emp_answers:
        r = find_row(sub, 6.0, ans)
        share = parse_percent_cell(r["Estimate"])
        sid = "scope2_national_q6_ai_employment_effect_" + key.removeprefix("employment_")
        rows.append(
            {
                "category_key": key,
                "category_label": label,
                "weighted_share": share,
                "window_start": WINDOW_START,
                "window_end": WINDOW_END,
                "source_series_id": sid,
                "evidence_directness": "direct_published",
            }
        )
        mapping["category_to_source"][key] = {
            "question_id": float(r["Question ID"]),
            "answer": normalize_answer(str(r["Answer"])),
            "estimate_cell": str(r["Estimate"]),
            "match_type": "exact_published",
        }

    # --- Task categories: prefer Q25 multi-select if Census publishes it ---
    q25_specs: list[tuple[str, str, str]] = [
        (
            "perform_task_previously_done_by_employee",
            "Perform a task previously done by an employee",
            "Perform a task previously done by an employee",
        ),
        (
            "supplement_or_enhance_task_performed_by_employee",
            "Supplement or enhance a task performed by an employee",
            "Supplement or enhance a task performed by an employee",
        ),
        (
            "introduce_new_task_not_previously_done_by_employee",
            "Introduce a new task not previously done by an employee",
            "Introduce a new task not previously done by an employee",
        ),
    ]

    q25_any = False
    for key, ans_label, display_label in q25_specs:
        opt = find_q25_option(sub, ans_label)
        if opt is not None:
            q25_any = True
            share = parse_percent_cell(opt["Estimate"])
            rows.append(
                {
                    "category_key": key,
                    "category_label": display_label,
                    "weighted_share": share,
                    "window_start": WINDOW_START,
                    "window_end": WINDOW_END,
                    "source_series_id": "scope2_national_q25_multiselect_" + key,
                    "evidence_directness": "direct_published",
                }
            )
            mapping["category_to_source"][key] = {
                "question_id": float(opt["Question ID"]),
                "answer": normalize_answer(str(opt["Answer"])),
                "estimate_cell": str(opt["Estimate"]),
                "match_type": "exact_published_q25",
            }

    if q25_any:
        # If we found at least one Q25 row, require all three for consistency.
        found_keys = {r["category_key"] for r in rows if r["category_key"].startswith("perform_") or r["category_key"].startswith("supplement_") or r["category_key"].startswith("introduce_")}
        expected = {t[0] for t in q25_specs}
        if found_keys != expected:
            raise RuntimeError(
                "Partial Q25 tabulation in workbook (some options present, some missing)."
            )
        mapping["q25_multiselect_source"] = "primary_workbook"
        return rows, mapping

    # Q25 options not published: use closest published items in the same Scope 2 universe.
    mapping["q25_multiselect_source"] = "not_in_primary_workbook"
    mapping["q25_multiselect_note"] = (
        "The published AI_Supplement_Table.xlsx National sheet does not include "
        "questionnaire item 25 multi-select answer rows. Using published Scope 2 "
        "proxies from the same workbook; see docs/t007_figure3_panelB_btos_workforce_effects_methodology.md."
    )

    # Proxy 1: Q3 Yes — used AI to perform tasks previously done by employees (CES-WP discusses
    # this item as the published task-replacement incidence among AI users).
    r_q3 = find_row(sub, 3.0, "Yes")
    share_p = parse_percent_cell(r_q3["Estimate"])
    rows.append(
        {
            "category_key": "perform_task_previously_done_by_employee",
            "category_label": "Perform a task previously done by an employee",
            "weighted_share": share_p,
            "window_start": WINDOW_START,
            "window_end": WINDOW_END,
            "source_series_id": "scope2_national_q3_yes_ai_performed_tasks_previously_done_by_employees",
            "evidence_directness": "proxy_mapping",
        }
    )
    mapping["category_to_source"]["perform_task_previously_done_by_employee"] = {
        "question_id": 3.0,
        "answer": "Yes",
        "estimate_cell": str(r_q3["Estimate"]),
        "match_type": "proxy_q3_yes_not_q25_multiselect",
        "proxy_note": (
            "Published table does not include Q25 multi-select. Share is Q3 Yes: "
            "firms reporting AI used to perform tasks previously done by employees."
        ),
    }

    # Proxies for augmentation / new task: closest published organizational-change items (Q7).
    r_train = find_row(sub, 7.0, "Trained current staff to use AI")
    r_workflow = find_row(sub, 7.0, "Developed new workflows")
    share_s = parse_percent_cell(r_train["Estimate"])
    share_i = parse_percent_cell(r_workflow["Estimate"])

    rows.append(
        {
            "category_key": "supplement_or_enhance_task_performed_by_employee",
            "category_label": "Supplement or enhance a task performed by an employee",
            "weighted_share": share_s,
            "window_start": WINDOW_START,
            "window_end": WINDOW_END,
            "source_series_id": "scope2_national_q7_trained_current_staff_to_use_ai",
            "evidence_directness": "proxy_mapping",
        }
    )
    mapping["category_to_source"]["supplement_or_enhance_task_performed_by_employee"] = {
        "question_id": 7.0,
        "answer": "Trained current staff to use AI",
        "estimate_cell": str(r_train["Estimate"]),
        "match_type": "proxy_q7_training_not_q25_multiselect",
    }

    rows.append(
        {
            "category_key": "introduce_new_task_not_previously_done_by_employee",
            "category_label": "Introduce a new task not previously done by an employee",
            "weighted_share": share_i,
            "window_start": WINDOW_START,
            "window_end": WINDOW_END,
            "source_series_id": "scope2_national_q7_developed_new_workflows",
            "evidence_directness": "proxy_mapping",
        }
    )
    mapping["category_to_source"]["introduce_new_task_not_previously_done_by_employee"] = {
        "question_id": 7.0,
        "answer": "Developed new workflows",
        "estimate_cell": str(r_workflow["Estimate"]),
        "match_type": "proxy_q7_new_workflows_not_q25_multiselect",
    }

    return rows, mapping


def try_fallback_workbook() -> tuple[bytes | None, str | None]:
    """Attempt official archive/v1 URL; often returns HTML placeholder."""
    try:
        data, ctype = fetch_bytes(FALLBACK_ARCHIVE_URL)
    except Exception:
        return None, None
    if not ctype or "excel" not in ctype.lower():
        if data[:4] != b"PK\x03\x04":
            return None, None
    if data[:4] != b"PK\x03\x04":
        return None, None
    return data, FALLBACK_ARCHIVE_URL


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    primary_bytes, primary_ct = fetch_bytes(PRIMARY_XLSX_URL)
    primary_hash = sha256_bytes(primary_bytes)

    used_fallback = False
    fallback_reason: str | None = None
    workbook_bytes = primary_bytes
    workbook_url = PRIMARY_XLSX_URL
    fallback_hash: str | None = None

    df_primary = pd.read_excel(io.BytesIO(primary_bytes), sheet_name=NATIONAL_SHEET)
    sub_primary = extract_national_scope2(df_primary)

    # Detect whether Q25 rows exist in primary.
    has_q25 = bool(
        sub_primary["Question"]
        .map(normalize_question)
        .str.contains(Q25_QUESTION_SUBSTRING, regex=False, na=False)
        .any()
    )

    if not has_q25:
        fb_bytes, fb_url = try_fallback_workbook()
        if fb_bytes is not None:
            df_fb = pd.read_excel(io.BytesIO(fb_bytes), sheet_name=NATIONAL_SHEET)
            sub_fb = extract_national_scope2(df_fb)
            if sub_fb["Question"].map(normalize_question).str.contains(
                Q25_QUESTION_SUBSTRING, regex=False, na=False
            ).any():
                workbook_bytes = fb_bytes
                workbook_url = fb_url or FALLBACK_ARCHIVE_URL
                used_fallback = True
                fallback_reason = (
                    "Primary AI_Supplement_Table.xlsx lacked published Q25 multi-select rows; "
                    "archive workbook contained them."
                )
                fallback_hash = sha256_bytes(fb_bytes)
            else:
                used_fallback = False
                fallback_reason = (
                    "Primary workbook lacks Q25 multi-select rows; attempted fallback URL did "
                    "not yield a valid alternate xlsx with Q25 tabulations."
                )
        else:
            fallback_reason = (
                "Primary workbook lacks Q25 multi-select rows; official archive/v1 fallback "
                "URL did not return a valid Excel workbook (HTML or missing)."
            )

    df = pd.read_excel(io.BytesIO(workbook_bytes), sheet_name=NATIONAL_SHEET)
    sub = extract_national_scope2(df)
    rows, cat_mapping = build_output_rows(sub)

    # Deterministic order for figure output
    order = [
        "perform_task_previously_done_by_employee",
        "supplement_or_enhance_task_performed_by_employee",
        "introduce_new_task_not_previously_done_by_employee",
        "employment_increased",
        "employment_decreased",
        "employment_did_not_change",
    ]
    key_index = {r["category_key"]: r for r in rows}
    ordered = [key_index[k] for k in order]

    out_df = pd.DataFrame(ordered, columns=OUT_COLS)
    out_df["weighted_share"] = out_df["weighted_share"].round(6)
    out_df.to_csv(OUT_CSV, index=False)

    meta = {
        "output_csv": str(OUT_CSV.relative_to(ROOT)),
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "window_start": WINDOW_START,
        "window_end": WINDOW_END,
        "geography": "national",
        "universe_scope_code": SCOPE_AI_USERS,
        "universe_description": (
            "Firms that reported using Artificial Intelligence to produce goods or services "
            "in the last six months (BTOS AI supplement data dictionary Scope 2)."
        ),
        "primary_source_url": PRIMARY_XLSX_URL,
        "primary_file_sha256": primary_hash,
        "primary_content_type": primary_ct,
        "workbook_used_url": workbook_url,
        "workbook_sha256": sha256_bytes(workbook_bytes),
        "used_fallback_workbook": used_fallback,
        "fallback_url_attempted": FALLBACK_ARCHIVE_URL,
        "fallback_file_sha256": fallback_hash,
        "fallback_reason": fallback_reason,
        "category_mapping": cat_mapping,
        "notes": (
            "Pooled supplement window in Census CES-WP-24-16 Table 6 notes uses six two-week "
            "panels; frozen window endpoints follow T-007 (2023-12-04 through 2024-02-25)."
        ),
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV} and {OUT_META}")


if __name__ == "__main__":
    main()
