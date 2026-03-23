"""
Figure 3 robustness: basic consistency checks on BTOS outputs.

Writes `intermediate/robustness/figure3_btos_consistency.md`.

Run from repo root:
    python scripts/robustness/figure3_btos_consistency.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))

from _report import write_report  # noqa: E402

PANELA = ROOT / "figures" / "figure3_panelA_btos_ai_trends.csv"
PANELB = ROOT / "figures" / "figure3_panelB_btos_workforce_effects.csv"
META_A = ROOT / "intermediate" / "figure3_panelA_btos_ai_trends_run_metadata.json"


def main() -> int:
    lines: list[str] = ["## Panel A (trends)"]

    if not PANELA.is_file():
        lines.append(f"SKIP: missing `{PANELA}`")
    else:
        df = pd.read_csv(PANELA)
        for col in ("ai_use_current_rate", "ai_use_expected_6m_rate"):
            if col in df.columns:
                lo = float(df[col].min())
                hi = float(df[col].max())
                bad = df[(df[col] < 0) | (df[col] > 1)]
                lines.append(
                    f"- `{col}` range [{lo:.4f}, {hi:.4f}], "
                    f"rows outside [0,1]: {len(bad)}"
                )
        if "btos_period_id" in df.columns:
            lines.append(
                f"- distinct periods: {df['btos_period_id'].nunique()} "
                f"(rows={len(df)})"
            )
        if "period_start_date" in df.columns:
            d = pd.to_datetime(df["period_start_date"], errors="coerce")
            lines.append(
                f"- period_start_date parseable: {d.notna().sum()}/{len(df)}"
            )

    lines.extend(["", "## Panel B (workforce effects)"])
    if not PANELB.is_file():
        lines.append(f"SKIP: missing `{PANELB}`")
    else:
        b = pd.read_csv(PANELB)
        if "weighted_share" in b.columns:
            lo = float(b["weighted_share"].min())
            hi = float(b["weighted_share"].max())
            lines.append(f"- `weighted_share` range [{lo:.4f}, {hi:.4f}]")
        lines.append(f"- rows: {len(b)}")

    lines.extend(["", "## Run metadata (Panel A)"])
    if META_A.is_file():
        meta = json.loads(META_A.read_text(encoding="utf-8"))
        lines.append(
            "- metadata keys (sample): "
            + ", ".join(sorted(meta.keys())[:10])
        )
    else:
        lines.append(f"- missing `{META_A.name}`")

    write_report("figure3_btos_consistency.md", "\n".join(lines))
    print("Wrote intermediate/robustness/figure3_btos_consistency.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
