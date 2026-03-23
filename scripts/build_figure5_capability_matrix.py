"""
Build figures/figure5_capability_matrix.csv — synthesis-only capability matrix.

Coding is frozen from paper-notes.md (Dataset-to-claim matrix, first seven
claim columns) for the five core datasets listed in T-010. No empirical
estimation.

Run from repo root: python scripts/build_figure5_capability_matrix.py
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
ISSUES = ROOT / "issues.md"
PAPER_NOTES = ROOT / "paper-notes.md"

OUT_CSV = FIG / "figure5_capability_matrix.csv"
OUT_META = INTER / "figure5_capability_matrix_run_metadata.json"

# First seven empirical-object columns in paper-notes.md (excludes
# Worker–firm AI causal claims). Slugs match column headers.
EMPIRICAL_OBJECT_KEYS: list[str] = [
    "worker_outcomes",
    "worker_occupational_transitions",
    "firm_ai_adoption",
    "labor_demand_turnover",
    "occupational_structure_wages",
    "task_exposure_mechanism",
    "local_geographic_exposure",
]

# T-010 five core datasets, in stable display order.
DATASET_ORDER: list[str] = [
    "CPS (basic monthly)",
    "BTOS",
    "JOLTS",
    "OEWS",
    "O*NET",
]

# Frozen symbols from paper-notes.md lines 517–650, mapped to issue vocabulary.
# direct = check, partial = triangle, none = x-mark.
_CAPABILITY: dict[str, tuple[str, ...]] = {
    "CPS (basic monthly)": (
        "direct",
        "direct",
        "none",
        "partial",
        "partial",
        "none",
        "partial",
    ),
    "BTOS": (
        "partial",
        "none",
        "direct",
        "partial",
        "none",
        "partial",
        "direct",
    ),
    "JOLTS": (
        "none",
        "none",
        "none",
        "direct",
        "none",
        "none",
        "partial",
    ),
    "OEWS": (
        "none",
        "none",
        "none",
        "none",
        "direct",
        "none",
        "direct",
    ),
    "O*NET": (
        "none",
        "none",
        "none",
        "none",
        "partial",
        "direct",
        "none",
    ),
}

LEGEND_DIRECT = (
    "can directly support this claim with public data "
    "(paper-notes symbol check)"
)
LEGEND_PARTIAL = (
    "can support it only indirectly, partially, or with important caveats "
    "(paper-notes symbol triangle)"
)
LEGEND_NONE = (
    "cannot support this claim with public data (paper-notes symbol x-mark)"
)

OUT_COLS = (
    ["dataset_label"]
    + EMPIRICAL_OBJECT_KEYS
    + ["legend_direct", "legend_partial", "legend_none"]
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat()

    if len(DATASET_ORDER) != 5:
        raise RuntimeError("DATASET_ORDER must contain exactly 5 datasets")
    for ds in DATASET_ORDER:
        if ds not in _CAPABILITY:
            raise RuntimeError(f"missing frozen matrix row for {ds!r}")
        if len(_CAPABILITY[ds]) != len(EMPIRICAL_OBJECT_KEYS):
            raise RuntimeError(f"wrong column count for {ds!r}")

    rows: list[dict[str, Any]] = []
    for ds in DATASET_ORDER:
        codes = _CAPABILITY[ds]
        row: dict[str, Any] = {"dataset_label": ds}
        for k, v in zip(EMPIRICAL_OBJECT_KEYS, codes, strict=True):
            row[k] = v
        row["legend_direct"] = LEGEND_DIRECT
        row["legend_partial"] = LEGEND_PARTIAL
        row["legend_none"] = LEGEND_NONE
        rows.append(row)

    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(rows, columns=OUT_COLS).to_csv(OUT_CSV, index=False)

    meta: dict[str, Any] = {
        "ticket": "T-010",
        "generated_at_utc": generated_at,
        "assertion_synthesis_only": (
            "This output encodes categorical capability judgments from "
            "paper-notes.md; it does not compute new statistics or estimates."
        ),
        "symbol_mapping": {
            "check_mark": "direct",
            "triangle": "partial",
            "x_mark": "none",
        },
        "empirical_object_keys": list(EMPIRICAL_OBJECT_KEYS),
        "dataset_order": list(DATASET_ORDER),
        "source_files_sha256": [
            {
                "file_name": str(ISSUES.relative_to(ROOT)).replace("\\", "/"),
                "path": str(ISSUES),
                "sha256": sha256_file(ISSUES),
            },
            {
                "file_name": str(PAPER_NOTES.relative_to(ROOT)).replace(
                    "\\", "/"
                ),
                "path": str(PAPER_NOTES),
                "sha256": sha256_file(PAPER_NOTES),
            },
        ],
        "matrix_reference": (
            "paper-notes.md Dataset-to-claim matrix; first seven claim "
            "columns; rows CPS (basic monthly), BTOS, JOLTS, OEWS, O*NET"
        ),
        "row_count": len(rows),
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
    }

    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Wrote {OUT_CSV} ({len(rows)} rows)")
    print(f"Wrote {OUT_META}")


if __name__ == "__main__":
    main()
