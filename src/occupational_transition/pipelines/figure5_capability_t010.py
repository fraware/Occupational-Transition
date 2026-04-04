"""T-010: synthesis-only capability matrix (frozen lineage docs)."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

# Seven empirical-object columns for the retained synthesis matrix.
# Include the worker-firm linkage object explicitly so Claim 5's core
# architecture gap is directly encoded in the output matrix.
EMPIRICAL_OBJECT_KEYS: list[str] = [
    "worker_outcomes",
    "worker_occupational_transitions",
    "firm_ai_adoption",
    "labor_demand_turnover",
    "occupational_structure_wages",
    "task_exposure_mechanism",
    "worker_firm_ai_linkage",
]

# T-010 five core datasets, in stable display order.
DATASET_ORDER: list[str] = [
    "CPS (basic monthly)",
    "BTOS",
    "JOLTS",
    "OEWS",
    "O*NET",
]

# Frozen symbols from docs/lineage/t010_paper_notes_matrix.md,
# mapped to issue vocabulary.
# direct = check, partial = triangle, none = x-mark.
_CAPABILITY: dict[str, tuple[str, ...]] = {
    "CPS (basic monthly)": (
        "direct",
        "direct",
        "none",
        "partial",
        "partial",
        "none",
        "none",
    ),
    "BTOS": (
        "partial",
        "none",
        "direct",
        "partial",
        "none",
        "partial",
        "none",
    ),
    "JOLTS": (
        "none",
        "none",
        "none",
        "direct",
        "none",
        "none",
        "none",
    ),
    "OEWS": (
        "none",
        "none",
        "none",
        "none",
        "direct",
        "none",
        "none",
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


def run(root: Path) -> None:
    """T-010 build entrypoint for ``run_step``."""
    fig = root / "figures"
    inter = root / "intermediate"
    issues = root / "docs" / "lineage" / "t010_issues.md"
    paper_notes = root / "docs" / "lineage" / "t010_paper_notes_matrix.md"
    out_csv = fig / "figure5_capability_matrix.csv"
    out_meta = inter / "figure5_capability_matrix_run_metadata.json"

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

    fig.mkdir(parents=True, exist_ok=True)
    inter.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(rows, columns=OUT_COLS).to_csv(out_csv, index=False)

    meta: dict[str, Any] = {
        "ticket": "T-010",
        "generated_at_utc": generated_at,
        "assertion_synthesis_only": (
            "This output encodes categorical capability judgments from "
            "docs/lineage/t010_paper_notes_matrix.md; it does not compute new "
            "statistics or estimates."
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
                "file_name": str(issues.relative_to(root)).replace("\\", "/"),
                "path": str(issues),
                "sha256": sha256_file(issues),
            },
            {
                "file_name": str(paper_notes.relative_to(root)).replace(
                    "\\", "/"
                ),
                "path": str(paper_notes),
                "sha256": sha256_file(paper_notes),
            },
        ],
        "matrix_reference": (
            "docs/lineage/t010_paper_notes_matrix.md Dataset-to-claim matrix "
            "adapted to retained seven empirical objects, including "
            "worker_firm_ai_linkage; rows CPS (basic monthly), BTOS, JOLTS, "
            "OEWS, O*NET"
        ),
        "row_count": len(rows),
        "output_csv": str(out_csv.relative_to(root)).replace("\\", "/"),
    }

    out_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Wrote {out_csv} ({len(rows)} rows)")
    print(f"Wrote {out_meta}")
