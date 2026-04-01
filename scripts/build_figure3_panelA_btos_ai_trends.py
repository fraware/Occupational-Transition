"""Thin wrapper for T-006 BTOS AI trends pipeline."""

from __future__ import annotations

from pathlib import Path

from occupational_transition.pipelines.figure3_panelA_t006 import run


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out_csv, out_meta, n = run(root)
    print(f"Wrote {out_csv} ({n} rows). Metadata: {out_meta}")


if __name__ == "__main__":
    main()
