"""Thin wrapper for T-001 baseline pipeline."""

from __future__ import annotations

from pathlib import Path

from occupational_transition.pipelines.figure1_panelA_t001 import run


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out_csv, meta_csv, run_meta, n = run(root)
    print(f"Wrote {out_csv} ({n} rows)")
    print(f"Meta: {meta_csv}")
    print(f"Run metadata: {run_meta}")


if __name__ == "__main__":
    main()
