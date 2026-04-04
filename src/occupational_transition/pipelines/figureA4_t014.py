"""
Build Figure A4 ABS structural heterogeneity from official
Census ABS technology tables.

Output:
- figures/figureA4_abs_structural_adoption.csv
- intermediate/figureA4_abs_structural_adoption_run_metadata.json
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class FigureA4Layout:
    root: Path
    raw: Path
    fig: Path
    inter: Path
    out_csv: Path
    out_meta: Path


def _figure_a4_layout(root: Path) -> FigureA4Layout:
    fig = root / "figures"
    inter = root / "intermediate"
    return FigureA4Layout(
        root=root,
        raw=root / "raw" / "abs",
        fig=fig,
        inter=inter,
        out_csv=fig / "figureA4_abs_structural_adoption.csv",
        out_meta=inter / "figureA4_abs_structural_adoption_run_metadata.json",
    )


def run(root: Path) -> None:
    build_figure_a4_abs_structural_adoption(_figure_a4_layout(root))


ABS_DATA_HUB_URL = "https://www.census.gov/programs-surveys/abs/data.html"
ABS_TABLES_HUB_URL = (
    "https://www.census.gov/programs-surveys/abs/data/tables.html"
)
FALLBACK_TECH_PAGE_URL = (
    "https://www.census.gov/data/tables/2019/econ/abs/2019-abs-automation-technology-module.html"
)
API_BASE_URL = "https://api.census.gov/data/2018/abstcb"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

OUT_COLS = [
    "abs_reference_year",
    "industry_code",
    "industry_label",
    "firm_size_class",
    "measure_key",
    "measure_label",
    "weighted_share",
    "source_table_id",
]

TOTAL_FILTERS = {
    "SEX": "001",
    "ETH_GROUP": "001",
    "RACE_GROUP": "00",
    "VET_GROUP": "001",
}

ADOPTION_LABEL = "Artificial Intelligence: Total use"
WORKFORCE_LABELS = {
    "ai_workforce_increased": (
        "Artificial Intelligence: Increased number of workers employed by this "
        "business"
    ),
    "ai_workforce_decreased": (
        "Artificial Intelligence: Decreased number of workers employed by this "
        "business"
    ),
    "ai_workforce_unchanged": (
        "Artificial Intelligence: Did not change number of workers employed by "
        "this business"
    ),
}


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def fetch_bytes(url: str) -> bytes:
    with urlopen(_request(url), timeout=180) as resp:
        return resp.read()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def discover_technology_page() -> str:
    try:
        html = fetch_bytes(ABS_TABLES_HUB_URL).decode(
            "utf-8", errors="replace"
        )
    except Exception:
        return FALLBACK_TECH_PAGE_URL

    matches = re.findall(
        (
            r"https://www\\.census\\.gov/data/tables/\\d{4}/econ/abs/"
            r"\\d{4}-abs-automation-technology-module\\.html"
        ),
        html,
    )
    if not matches:
        return FALLBACK_TECH_PAGE_URL
    return sorted(set(matches))[-1]


def load_api_rows() -> tuple[list[dict[str, str]], bytes, str]:
    query = (
        "get="
        "YEAR,NAICS2017,NAICS2017_LABEL,NSFSZFI,NSFSZFI_LABEL,"
        "TECHUSE,TECHUSE_LABEL,IMPACTWF_U,IMPACTWF_U_LABEL,FIRMPDEMP_PCT"
        "&for=us:*"
        "&SEX=001&ETH_GROUP=001&RACE_GROUP=00&VET_GROUP=001"
    )
    api_url = f"{API_BASE_URL}?{query}"
    raw = fetch_bytes(api_url)
    data = json.loads(raw.decode("utf-8"))
    header = data[0]
    rows = [dict(zip(header, r)) for r in data[1:]]
    return rows, raw, api_url


def parse_pct_to_share(v: str) -> float:
    x = float(v)
    if x < 0.0 or x > 100.0:
        raise ValueError(f"Percent out of bounds: {v}")
    return x / 100.0


def is_two_digit_industry(code: str) -> bool:
    return len(code) == 2 and code != "00" and code.isdigit()


def build_rows(rows: list[dict[str, str]]) -> list[dict[str, str | float]]:
    out: list[dict[str, str | float]] = []

    # Industry cut: 2-digit NAICS, all firms only.
    industry_rows = [
        r
        for r in rows
        if is_two_digit_industry(r["NAICS2017"]) and r["NSFSZFI"] == "001"
    ]

    # Firm-size cut: all sectors (00), non-total firm sizes.
    size_rows = [
        r for r in rows if r["NAICS2017"] == "00" and r["NSFSZFI"] != "001"
    ]

    # AI adoption measure
    for bucket_name, bucket_rows in [
        ("industry", industry_rows),
        ("firm_size", size_rows),
    ]:
        for r in bucket_rows:
            if r["TECHUSE_LABEL"] != ADOPTION_LABEL:
                continue
            industry_code = r["NAICS2017"] if bucket_name == "industry" else "00"
            industry_label = (
                r["NAICS2017_LABEL"]
                if bucket_name == "industry"
                else "All sectors"
            )
            firm_size = (
                r["NSFSZFI_LABEL"] if bucket_name == "firm_size" else "All firms"
            )
            out.append(
                {
                    "abs_reference_year": r["YEAR"],
                    "industry_code": industry_code,
                    "industry_label": industry_label,
                    "firm_size_class": firm_size,
                    "measure_key": "ai_total_use",
                    "measure_label": ADOPTION_LABEL,
                    "weighted_share": parse_pct_to_share(r["FIRMPDEMP_PCT"]),
                    "source_table_id": "ABSTCB2018",
                }
            )

    # AI workforce impact measures
    inv_workforce = {v: k for k, v in WORKFORCE_LABELS.items()}
    for bucket_name, bucket_rows in [
        ("industry", industry_rows),
        ("firm_size", size_rows),
    ]:
        for r in bucket_rows:
            label = r["IMPACTWF_U_LABEL"]
            if label not in inv_workforce:
                continue
            industry_code = r["NAICS2017"] if bucket_name == "industry" else "00"
            industry_label = (
                r["NAICS2017_LABEL"]
                if bucket_name == "industry"
                else "All sectors"
            )
            firm_size = (
                r["NSFSZFI_LABEL"] if bucket_name == "firm_size" else "All firms"
            )
            out.append(
                {
                    "abs_reference_year": r["YEAR"],
                    "industry_code": industry_code,
                    "industry_label": industry_label,
                    "firm_size_class": firm_size,
                    "measure_key": inv_workforce[label],
                    "measure_label": label,
                    "weighted_share": parse_pct_to_share(r["FIRMPDEMP_PCT"]),
                    "source_table_id": "ABSTCB2018",
                }
            )

    if not out:
        raise RuntimeError("No rows built from ABS API response.")
    return out


def build_figure_a4_abs_structural_adoption(layout: FigureA4Layout) -> None:
    layout.raw.mkdir(parents=True, exist_ok=True)
    layout.fig.mkdir(parents=True, exist_ok=True)
    layout.inter.mkdir(parents=True, exist_ok=True)

    tech_page_url = discover_technology_page()
    tech_page_bytes = fetch_bytes(tech_page_url)
    rows, api_bytes, api_url = load_api_rows()

    raw_json_path = layout.raw / "abstcb_2018_us_national.json"
    raw_json_path.write_bytes(api_bytes)

    out_rows = build_rows(rows)
    out_rows = sorted(
        out_rows,
        key=lambda r: (
            str(r["abs_reference_year"]),
            str(r["industry_code"]),
            str(r["firm_size_class"]),
            str(r["measure_key"]),
        ),
    )

    with layout.out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUT_COLS)
        writer.writeheader()
        for r in out_rows:
            rr = dict(r)
            rr["weighted_share"] = round(float(rr["weighted_share"]), 6)
            writer.writerow(rr)

    meta = {
        "task_id": "T-014",
        "output_csv": str(layout.out_csv.relative_to(layout.root)),
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "geography": "national",
        "grouping_scope": "industry_and_firm_size_only",
        "selected_module_page_url": tech_page_url,
        "abs_reference_year": "2018",
        "source_table_id": "ABSTCB2018",
        "sources": [
            {"name": "abs_data_hub", "url": ABS_DATA_HUB_URL},
            {"name": "abs_tables_hub", "url": ABS_TABLES_HUB_URL},
            {"name": "abs_technology_module_page", "url": tech_page_url},
            {"name": "abs_api_query", "url": api_url},
        ],
        "downloaded_artifacts": [
            {
                "path": str(raw_json_path.relative_to(layout.root)),
                "sha256": sha256_bytes(api_bytes),
            },
            {"url": tech_page_url, "sha256": sha256_bytes(tech_page_bytes)},
        ],
        "total_filters_applied": TOTAL_FILTERS,
        "scale": {
            "input_unit": "percent",
            "output_unit": "share",
            "transformation": "weighted_share = FIRMPDEMP_PCT / 100.0",
        },
        "measure_dictionary": [
            {"measure_key": "ai_total_use", "measure_label": ADOPTION_LABEL},
            *[
                {"measure_key": k, "measure_label": v}
                for k, v in WORKFORCE_LABELS.items()
            ],
        ],
        "transformation_notes": (
            "Rows are restricted to national totals and either (a) 2-digit NAICS by all firms "
            "or (b) all sectors by firm-size class, using published ABS percentages only."
        ),
        "provenance_statement": (
            "Official U.S. Census Bureau ABS published technology tables/API "
            "only."
        ),
    }
    layout.out_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {layout.out_csv} and {layout.out_meta}")

