"""QA for Figure 5 capability matrix (T-010). Exit 1 on failure."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG_CSV = ROOT / "figures" / "figure5_capability_matrix.csv"
META_JSON = ROOT / "intermediate" / "figure5_capability_matrix_run_metadata.json"
ISSUES = ROOT / "issues.md"
PAPER_NOTES = ROOT / "paper-notes.md"

ALLOWED = {"direct", "partial", "none"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []

    sys.path.insert(0, str(ROOT / "scripts"))
    import build_figure5_capability_matrix as b

    exp_cols = list(b.OUT_COLS)

    if not FIG_CSV.is_file():
        errors.append(f"missing output: {FIG_CSV}")
        return _report(errors)

    df = pd.read_csv(FIG_CSV)
    if list(df.columns) != exp_cols:
        errors.append(f"columns must be {exp_cols}, got {list(df.columns)}")

    if len(df) != 5:
        errors.append(f"expected 5 rows, got {len(df)}")

    for c in exp_cols:
        if c in df.columns and df[c].isna().any():
            errors.append(f"NaN in {c}")

    got_labels = list(df["dataset_label"].astype(str))
    if got_labels != b.DATASET_ORDER:
        errors.append(
            f"dataset_label order mismatch: {got_labels} vs {b.DATASET_ORDER}"
        )

    for _, row in df.iterrows():
        ds = str(row["dataset_label"])
        if ds not in b._CAPABILITY:
            errors.append(f"unexpected dataset_label {ds!r}")
            continue
        exp_row = b._CAPABILITY[ds]
        for i, k in enumerate(b.EMPIRICAL_OBJECT_KEYS):
            v = str(row[k]).strip()
            if v not in ALLOWED:
                errors.append(f"{ds} {k}: invalid code {v!r}")
            elif v != exp_row[i]:
                errors.append(
                    f"{ds} {k}: expected {exp_row[i]!r} got {v!r}"
                )

    for col in ("legend_direct", "legend_partial", "legend_none"):
        if col in df.columns:
            uniq = df[col].unique()
            if len(uniq) != 1:
                errors.append(f"{col} must be identical on all rows, got {uniq}")

    if not META_JSON.is_file():
        errors.append(f"missing metadata: {META_JSON}")
        return _report(errors)

    meta = json.loads(META_JSON.read_text(encoding="utf-8"))

    if meta.get("ticket") != "T-010":
        errors.append("metadata ticket must be T-010")

    if meta.get("row_count") != len(df):
        errors.append(
            f"metadata row_count {meta.get('row_count')} != csv rows {len(df)}"
        )

    if meta.get("dataset_order") != b.DATASET_ORDER:
        errors.append("metadata dataset_order mismatch")

    if meta.get("empirical_object_keys") != b.EMPIRICAL_OBJECT_KEYS:
        errors.append("metadata empirical_object_keys mismatch")

    entries = meta.get("source_files_sha256") or []
    by_name = {e.get("file_name"): e for e in entries}
    for rel, path in (
        ("issues.md", ISSUES),
        ("paper-notes.md", PAPER_NOTES),
    ):
        ex = by_name.get(rel)
        if not ex:
            errors.append(f"metadata missing sha256 entry for {rel}")
            continue
        got = sha256_file(path)
        if ex.get("sha256") != got:
            errors.append(f"sha256 mismatch for {rel}")

    return _report(errors)


def _report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("QA OK: figure5_capability_matrix.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
