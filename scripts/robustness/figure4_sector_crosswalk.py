"""
Figure 4 robustness: sector codes in figure outputs appear in sector6 crosswalk.

Writes `intermediate/robustness/figure4_sector_crosswalk.md`.

Run from repo root:
    python scripts/robustness/figure4_sector_crosswalk.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))

from _report import write_report  # noqa: E402

JOLTS = ROOT / "figures" / "figure4_panelA_jolts_sector_rates.csv"
CES = ROOT / "figures" / "figure4_panelB_ces_sector_index.csv"
SECTOR = ROOT / "crosswalks" / "sector6_crosswalk.csv"


def main() -> int:
    if not SECTOR.is_file():
        write_report(
            "figure4_sector_crosswalk.md",
            f"FAIL: missing crosswalk {SECTOR}",
        )
        return 1

    cw = pd.read_csv(SECTOR)
    code_col = "sector6_code" if "sector6_code" in cw.columns else None
    if code_col is None:
        write_report("figure4_sector_crosswalk.md", "FAIL: sector6_code not in crosswalk")
        return 1
    valid = set(cw[code_col].astype(str).unique())

    lines = ["## sector6 crosswalk", f"- `{SECTOR.relative_to(ROOT)}`", ""]

    for label, path in (("JOLTS", JOLTS), ("CES", CES)):
        lines.append(f"## {label}")
        if not path.is_file():
            lines.append(f"- SKIP: missing `{path}`")
            continue
        df = pd.read_csv(path)
        if "sector6_code" not in df.columns:
            lines.append("- FAIL: no sector6_code column")
            continue
        codes = set(df["sector6_code"].astype(str).unique())
        bad = sorted(codes - valid)
        lines.append(
            f"- distinct sector6_code in figure: {len(codes)}; "
            f"not in crosswalk: {bad if bad else 'none'}"
        )

    write_report("figure4_sector_crosswalk.md", "\n".join(lines))
    print("Wrote intermediate/robustness/figure4_sector_crosswalk.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
