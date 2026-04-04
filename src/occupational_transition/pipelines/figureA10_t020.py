"""
Build Figure A10 (NLS long-run career adaptation).

Output:
- figures/figureA10_nls_longrun.csv
- intermediate/figureA10_nls_longrun_run_metadata.json
"""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd


@dataclass(frozen=True)
class FigureA10Layout:
    root: Path
    raw: Path
    fig: Path
    inter: Path
    cross: Path
    terciles: Path
    out_csv: Path
    out_meta: Path


def _figure_a10_layout(root: Path) -> FigureA10Layout:
    fig = root / "figures"
    inter = root / "intermediate"
    return FigureA10Layout(
        root=root,
        raw=root / "raw" / "nls",
        fig=fig,
        inter=inter,
        cross=root / "crosswalks" / "occ22_crosswalk.csv",
        terciles=inter / "ai_relevance_terciles.csv",
        out_csv=fig / "figureA10_nls_longrun.csv",
        out_meta=inter / "figureA10_nls_longrun_run_metadata.json",
    )


def run(root: Path) -> None:
    build_figure_a10_nls_longrun(_figure_a10_layout(root))


NLS_ZIP_URL = "https://www.bls.gov/nls/getting-started/nlsy97_all_1997-2019.zip"
NLS_ZIP_NAME = "nlsy97_all_1997-2019.zip"

ZIP_CDB_MEMBER = "nlsy97_all_1997-2019.cdb"
ZIP_CSV_MEMBER = "nlsy97_all_1997-2019.csv"

SOURCE_PROGRAM = "BLS_NLSY97_PUBLIC_USE"
SOURCE_SERIES_ID = "nlsy97_all_1997_2019_release20_public_use"

USER_AGENT = "Mozilla/5.0"
REFERER = "https://www.bls.gov/nls/getting-started/accessing-data.htm"

OUT_COLS = [
    "survey_round",
    "baseline_ai_tercile",
    "weighted_n",
    "occupation_switch_rate",
    "employment_rate",
    "unemployment_rate",
    "nilf_rate",
    "mean_annual_earnings",
    "training_participation_rate",
    "source_program",
    "source_series_id",
]

TERCILE_ORDER = {"low": 0, "middle": 1, "high": 2}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def fetch_to_cache(url: str, dst: Path) -> str:
    if dst.exists():
        return sha256_file(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha256()
    req = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Referer": REFERER,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urlopen(req, timeout=600) as r, dst.open("wb") as out:
        while True:
            b = r.read(1024 * 1024)
            if not b:
                break
            out.write(b)
            h.update(b)
    return h.hexdigest()


def parse_occ22_intervals(path: Path) -> list[tuple[int, int, int]]:
    df = pd.read_csv(path)
    intervals: list[tuple[int, int, int]] = []
    for occ22_id, g in df.groupby("occ22_id", dropna=False):
        if pd.isna(occ22_id):
            continue
        vals = [str(x).strip() for x in g["census_occ_code_range"].tolist()]
        vals = [v for v in vals if v and v.lower() != "nan"]
        if not vals:
            continue
        rng = next((v for v in vals if "-" in v), vals[0])
        if "-" in rng:
            a, b = rng.split("-", 1)
            lo, hi = int(a), int(b)
        else:
            lo = hi = int(rng)
        intervals.append((lo, hi, int(occ22_id)))
    intervals.sort(key=lambda x: x[0])
    return intervals


def map_occ22(occ_code: int, intervals: list[tuple[int, int, int]]) -> int | None:
    for lo, hi, oid in intervals:
        if lo <= occ_code <= hi:
            return oid
    return None


def parse_cdb_catalog_stream(cdb_file) -> list[tuple[str, str, str]]:
    pat = re.compile(r"^([A-Z0-9]+\.\d+)\s+\[([^\]]+)\]\s+Survey Year:\s*(.+)$")
    rows: list[tuple[str, str, str]] = []
    for raw in cdb_file:
        line = raw.decode("latin-1", errors="ignore").rstrip("\r\n")
        m = pat.match(line)
        if m:
            rows.append((m.group(1), m.group(2), m.group(3).strip()))
    return rows


def parse_int(v: str) -> int | None:
    s = str(v).strip()
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        s = s[1:-1].strip()
    if not s:
        return None
    try:
        return int(float(s))
    except ValueError:
        return None


def parse_weight(v: str) -> float | None:
    n = parse_int(v)
    if n is None or n <= 0:
        return None
    return n / 100.0


def parse_income(v: str) -> float | None:
    n = parse_int(v)
    if n is None or n <= 0:
        return None
    return float(n)


def build_figure_a10_nls_longrun(layout: FigureA10Layout) -> None:
    layout.raw.mkdir(parents=True, exist_ok=True)
    layout.fig.mkdir(parents=True, exist_ok=True)
    layout.inter.mkdir(parents=True, exist_ok=True)

    if not layout.cross.exists():
        raise RuntimeError(f"missing {layout.cross}")
    if not layout.terciles.exists():
        raise RuntimeError(f"missing {layout.terciles}")

    intervals = parse_occ22_intervals(layout.cross)
    ai_df = pd.read_csv(layout.terciles)
    ai_map = {
        int(r["occ22_id"]): str(r["ai_relevance_tercile"]).strip()
        for _, r in ai_df.iterrows()
    }
    if set(ai_map.keys()) != set(range(1, 23)):
        raise RuntimeError("ai_relevance_terciles coverage is not occ22 1..22")

    local_zip = layout.raw / NLS_ZIP_NAME
    zip_sha = fetch_to_cache(NLS_ZIP_URL, local_zip)

    with zipfile.ZipFile(local_zip) as zf:
        with zf.open(ZIP_CDB_MEMBER, "r") as cdbf:
            catalog = parse_cdb_catalog_stream(cdbf)

        code_by_name_year: dict[tuple[str, str], str] = {}
        emp_status_cols_by_year: dict[int, list[tuple[int, str]]] = defaultdict(list)

        for code_dot, qname, syear in catalog:
            code = code_dot.replace(".", "")
            code_by_name_year[(qname, syear)] = code
            m = re.match(r"EMP_STATUS_(\d{4})\.(\d+)$", qname)
            if m:
                yr = int(m.group(1))
                wk = int(m.group(2))
                emp_status_cols_by_year[yr].append((wk, code))

        for yr in emp_status_cols_by_year:
            emp_status_cols_by_year[yr].sort(key=lambda t: t[0])

        years: list[int] = []
        for yr in range(1997, 2020):
            y = str(yr)
            if ("SAMPLING_WEIGHT_CC", y) not in code_by_name_year:
                continue
            if ("YEMP_OCCODE-2002.01", y) not in code_by_name_year:
                continue
            if ("CV_ENROLLSTAT", y) not in code_by_name_year:
                continue
            if yr not in emp_status_cols_by_year:
                continue
            income_ok = (
                ("CV_INCOME_GROSS_YR", y) in code_by_name_year
                or ("CV_INCOME_FAMILY", y) in code_by_name_year
            )
            if not income_ok:
                continue
            years.append(yr)

        if not years:
            raise RuntimeError("no valid survey years resolved for T-020 build")

        var_codes: set[str] = set()
        required_core_codes: set[str] = set()
        pid_code = code_by_name_year[("PUBID", "1997")]
        var_codes.add(pid_code)
        required_core_codes.add(pid_code)
        for yr in years:
            y = str(yr)
            w_code = code_by_name_year[("SAMPLING_WEIGHT_CC", y)]
            occ_code = code_by_name_year[("YEMP_OCCODE-2002.01", y)]
            en_code = code_by_name_year[("CV_ENROLLSTAT", y)]
            var_codes.update([w_code, occ_code, en_code])
            required_core_codes.update([w_code, occ_code, en_code])
            if ("CV_INCOME_FAMILY", y) in code_by_name_year:
                i_code = code_by_name_year[("CV_INCOME_FAMILY", y)]
                var_codes.add(i_code)
                required_core_codes.add(i_code)
            if ("CV_INCOME_GROSS_YR", y) in code_by_name_year:
                i_code = code_by_name_year[("CV_INCOME_GROSS_YR", y)]
                var_codes.add(i_code)
                required_core_codes.add(i_code)
            for _, c in emp_status_cols_by_year[yr]:
                var_codes.add(c)

        with zf.open(ZIP_CSV_MEMBER, "r") as fb:
            header_line = fb.readline()
            header = (
                header_line.decode("latin-1", errors="ignore")
                .rstrip("\r\n")
                .split(",")
            )
            header = [h.strip().strip('"') for h in header]
            idx_by_code = {name: i for i, name in enumerate(header)}

            missing = sorted([c for c in required_core_codes if c not in idx_by_code])
            if missing:
                raise RuntimeError(f"missing required columns in NLS csv: {missing[:20]}")

            # Keep only EMP_STATUS columns that are actually present in this full extract.
            for yr in list(emp_status_cols_by_year.keys()):
                filtered = [(wk, c) for wk, c in emp_status_cols_by_year[yr] if c in idx_by_code]
                emp_status_cols_by_year[yr] = filtered

            pid_col = code_by_name_year[("PUBID", "1997")]
            pid_idx = idx_by_code[pid_col]

            # Weighted aggregators keyed by (survey_round, baseline_tercile)
            agg_weight: defaultdict[tuple[int, str], float] = defaultdict(float)
            agg_switch_num: defaultdict[tuple[int, str], float] = defaultdict(float)
            agg_switch_den: defaultdict[tuple[int, str], float] = defaultdict(float)
            agg_emp_num: defaultdict[tuple[int, str], float] = defaultdict(float)
            agg_emp_den: defaultdict[tuple[int, str], float] = defaultdict(float)
            agg_unemp_num: defaultdict[tuple[int, str], float] = defaultdict(float)
            agg_unemp_den: defaultdict[tuple[int, str], float] = defaultdict(float)
            agg_nilf_num: defaultdict[tuple[int, str], float] = defaultdict(float)
            agg_nilf_den: defaultdict[tuple[int, str], float] = defaultdict(float)
            agg_income_num: defaultdict[tuple[int, str], float] = defaultdict(float)
            agg_income_den: defaultdict[tuple[int, str], float] = defaultdict(float)
            agg_train_num: defaultdict[tuple[int, str], float] = defaultdict(float)
            agg_train_den: defaultdict[tuple[int, str], float] = defaultdict(float)

            needed_idx: set[int] = {idx_by_code[c] for c in var_codes}

            for line in fb:
                parts = line.decode("latin-1", errors="ignore").rstrip("\r\n").split(",")
                row = {i: parts[i] for i in needed_idx}
                _pid = parse_int(row.get(pid_idx, ""))
                if _pid is None:
                    continue

                occ22_by_year: dict[int, int] = {}
                for yr in years:
                    occ_idx = idx_by_code[code_by_name_year[("YEMP_OCCODE-2002.01", str(yr))]]
                    occ = parse_int(row.get(occ_idx, ""))
                    if occ is None or occ <= 0:
                        continue
                    occ22 = map_occ22(occ, intervals)
                    if occ22 is None:
                        continue
                    occ22_by_year[yr] = occ22

                if not occ22_by_year:
                    continue

                baseline_year = min(occ22_by_year.keys())
                baseline_occ22 = occ22_by_year[baseline_year]
                baseline_tercile = ai_map.get(baseline_occ22)
                if baseline_tercile not in TERCILE_ORDER:
                    continue

                for yr in years:
                    key = (yr, baseline_tercile)
                    w_idx = idx_by_code[code_by_name_year[("SAMPLING_WEIGHT_CC", str(yr))]]
                    w = parse_weight(row.get(w_idx, ""))
                    if w is None or w <= 0:
                        continue

                    agg_weight[key] += w

                    current_occ22 = occ22_by_year.get(yr)
                    if current_occ22 is not None:
                        agg_switch_den[key] += w
                        if current_occ22 != baseline_occ22:
                            agg_switch_num[key] += w

                    # Labor-force status from weekly EMP_STATUS_{year}.*
                    emp_codes = [idx_by_code[c] for _, c in emp_status_cols_by_year[yr]]
                    employed_w = 0
                    unemployed_w = 0
                    nilf_w = 0
                    lfs_denom = 0
                    for cidx in emp_codes:
                        st = parse_int(row.get(cidx, ""))
                        if st is None or st < 0 or st == 0:
                            continue
                        if st >= 9701:
                            employed_w += 1
                            lfs_denom += 1
                        elif st == 4:
                            unemployed_w += 1
                            lfs_denom += 1
                        elif st in (1, 5):
                            nilf_w += 1
                            lfs_denom += 1
                        elif st in (2, 3, 6):
                            lfs_denom += 1

                    if lfs_denom > 0:
                        agg_emp_num[key] += w * (employed_w / lfs_denom)
                        agg_emp_den[key] += w
                        agg_unemp_num[key] += w * (unemployed_w / lfs_denom)
                        agg_unemp_den[key] += w
                        agg_nilf_num[key] += w * (nilf_w / lfs_denom)
                        agg_nilf_den[key] += w

                    # Income variable: prefer CV_INCOME_FAMILY when present.
                    income = None
                    if ("CV_INCOME_FAMILY", str(yr)) in code_by_name_year:
                        income_idx = idx_by_code[
                            code_by_name_year[("CV_INCOME_FAMILY", str(yr))]
                        ]
                        income = parse_income(row.get(income_idx, ""))
                    if income is None and ("CV_INCOME_GROSS_YR", str(yr)) in code_by_name_year:
                        income_idx = idx_by_code[
                            code_by_name_year[("CV_INCOME_GROSS_YR", str(yr))]
                        ]
                        income = parse_income(row.get(income_idx, ""))
                    if income is not None:
                        agg_income_num[key] += w * income
                        agg_income_den[key] += w

                    enroll_idx = idx_by_code[code_by_name_year[("CV_ENROLLSTAT", str(yr))]]
                    enroll = parse_int(row.get(enroll_idx, ""))
                    if enroll is not None and enroll > 0:
                        in_school = 1.0 if 8 <= enroll <= 11 else 0.0
                        agg_train_num[key] += w * in_school
                        agg_train_den[key] += w

    out_rows: list[dict[str, object]] = []
    for yr in years:
        for tercile in ["low", "middle", "high"]:
            key = (yr, tercile)
            wsum = agg_weight.get(key, 0.0)
            if wsum <= 0:
                continue
            row = {
                "survey_round": str(yr),
                "baseline_ai_tercile": tercile,
                "weighted_n": wsum,
                "occupation_switch_rate": (
                    agg_switch_num[key] / agg_switch_den[key]
                    if agg_switch_den[key] > 0
                    else float("nan")
                ),
                "employment_rate": (
                    agg_emp_num[key] / agg_emp_den[key]
                    if agg_emp_den[key] > 0
                    else float("nan")
                ),
                "unemployment_rate": (
                    agg_unemp_num[key] / agg_unemp_den[key]
                    if agg_unemp_den[key] > 0
                    else float("nan")
                ),
                "nilf_rate": (
                    agg_nilf_num[key] / agg_nilf_den[key]
                    if agg_nilf_den[key] > 0
                    else float("nan")
                ),
                "mean_annual_earnings": (
                    agg_income_num[key] / agg_income_den[key]
                    if agg_income_den[key] > 0
                    else float("nan")
                ),
                "training_participation_rate": (
                    agg_train_num[key] / agg_train_den[key]
                    if agg_train_den[key] > 0
                    else float("nan")
                ),
                "source_program": SOURCE_PROGRAM,
                "source_series_id": SOURCE_SERIES_ID,
            }
            out_rows.append(row)

    if not out_rows:
        raise RuntimeError("no output rows produced for T-020")

    out_df = pd.DataFrame(out_rows, columns=OUT_COLS)
    out_df["survey_round"] = out_df["survey_round"].astype(int)
    out_df = out_df.sort_values(
        by=["survey_round", "baseline_ai_tercile"],
        key=lambda s: s.map(TERCILE_ORDER) if s.name == "baseline_ai_tercile" else s,
    )
    out_df["survey_round"] = out_df["survey_round"].astype(str)
    out_df.to_csv(layout.out_csv, index=False)

    meta = {
        "ticket": "T-020",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "output_csv": str(layout.out_csv.relative_to(layout.root)).replace("\\", "/"),
        "source_program": SOURCE_PROGRAM,
        "source_series_id": SOURCE_SERIES_ID,
        "source_urls": [
            "https://www.bls.gov/nls/getting-started/accessing-data.htm",
            "https://www.bls.gov/nls/notices/2024/nlsy97-data-release-20.htm",
            NLS_ZIP_URL,
        ],
        "source_files_sha256": [
            {
                "file_name": NLS_ZIP_NAME,
                "url": NLS_ZIP_URL,
                "local_cache_path": str(local_zip.relative_to(layout.root)).replace("\\", "/"),
                "sha256": zip_sha,
            }
        ],
        "crosswalk_file": str(layout.cross.relative_to(layout.root)).replace("\\", "/"),
        "crosswalk_sha256": sha256_file(layout.cross),
        "ai_terciles_file": str(layout.terciles.relative_to(layout.root)).replace("\\", "/"),
        "ai_terciles_sha256": sha256_file(layout.terciles),
        "retained_rounds": [str(y) for y in years],
        "cohort_selection_rule": (
            "Use official BLS NLSY97 public-use full extract "
            "(nlsy97_all_1997-2019.zip) as available from BLS access page."
        ),
        "baseline_classification_lineage": "YEMP_OCCODE-2002.01 -> occ22_crosswalk -> ai_relevance_terciles",
        "weighting": {
            "weight_variable": "SAMPLING_WEIGHT_CC",
            "implied_decimals": 2,
            "normalization": "weighted means by survey_round x baseline_ai_tercile",
        },
        "outcome_definitions": {
            "occupation_switch_rate": "Weighted share with valid current occ22 and current_occ22 != baseline_occ22",
            "employment_rate": "Weighted mean of annual weekly employment share from EMP_STATUS_{year}.*",
            "unemployment_rate": "Weighted mean of annual weekly unemployment share from EMP_STATUS_{year}.*",
            "nilf_rate": "Weighted mean of annual weekly NILF share from EMP_STATUS_{year}.*",
            "mean_annual_earnings": "Weighted mean of CV_INCOME_FAMILY when available, else CV_INCOME_GROSS_YR",
            "training_participation_rate": "Weighted share with CV_ENROLLSTAT in enrolled statuses 8..11",
        },
        "interpretation_note": (
            "Figure A10 is long-run descriptive context from public NLS data and "
            "is not a near-real-time AI-shock or causal-identification series."
        ),
        "row_count": int(len(out_df)),
    }
    layout.out_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Wrote {layout.out_csv} ({len(out_df)} rows)")
    print(f"Wrote {layout.out_meta}")


