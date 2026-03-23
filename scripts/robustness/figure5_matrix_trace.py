"""
Figure 5 robustness: CSV matrix matches frozen `_CAPABILITY` in build script.

Writes `intermediate/robustness/figure5_matrix_trace.md`.

Run from repo root:
    python scripts/robustness/figure5_matrix_trace.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))

from _report import write_report  # noqa: E402

CSV_PATH = ROOT / "figures" / "figure5_capability_matrix.csv"
BUILD = ROOT / "scripts" / "build_figure5_capability_matrix.py"


def _load_build_module():
    spec = importlib.util.spec_from_file_location("bf5cap", BUILD)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {BUILD}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    if not CSV_PATH.is_file():
        write_report(
            "figure5_matrix_trace.md",
            f"SKIP: missing `{CSV_PATH}`",
        )
        return 0

    mod = _load_build_module()
    df = pd.read_csv(CSV_PATH)
    emp_keys = list(mod.EMPIRICAL_OBJECT_KEYS)
    errors: list[str] = []

    for ds in mod.DATASET_ORDER:
        row = df[df["dataset_label"].astype(str) == ds]
        if row.empty:
            errors.append(f"missing dataset row: {ds}")
            continue
        r = row.iloc[0]
        expected = mod._CAPABILITY[ds]
        for k, v in zip(emp_keys, expected, strict=True):
            if str(r[k]) != v:
                errors.append(f"{ds} {k}: csv={r[k]!r} frozen={v!r}")

    body = [
        "## Frozen build module",
        f"- `{BUILD.relative_to(ROOT)}`",
        "",
        "## Comparison result",
    ]
    if errors:
        body.append("FAIL:")
        body.extend(f"- {e}" for e in errors)
        code = 1
    else:
        body.append(
            "- PASS: all empirical-object cells match `_CAPABILITY` "
            f"for {len(mod.DATASET_ORDER)} datasets."
        )
        code = 0

    write_report("figure5_matrix_trace.md", "\n".join(body))
    print("Wrote intermediate/robustness/figure5_matrix_trace.md")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
