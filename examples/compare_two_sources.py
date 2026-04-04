"""
Fetch two related LABSTAT reference files and compare line counts.

Run from the repository root (requires ``pip install -e .``):

    python examples/compare_two_sources.py
"""

from __future__ import annotations

import sys
from pathlib import Path

if str(Path(__file__).resolve().parents[1] / "src") not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from occupational_transition.catalog import fetch_by_dataset_id
from occupational_transition.paths import repo_root


def main() -> None:
    root = repo_root()
    raw = root / "raw"
    raw.mkdir(parents=True, exist_ok=True)

    a = fetch_by_dataset_id(root, "bls_jt_industry", raw_dir=raw)
    b = fetch_by_dataset_id(root, "bls_ce_supersector", raw_dir=raw)
    if a is None or b is None:
        raise SystemExit("Expected paths from fetch_by_dataset_id")

    pa = a if isinstance(a, Path) else Path(str(a))
    pb = b if isinstance(b, Path) else Path(str(b))
    na = sum(1 for _ in pa.open(encoding="utf-8", errors="replace"))
    nb = sum(1 for _ in pb.open(encoding="utf-8", errors="replace"))
    print("dataset_id", "path", "lines", sep="\t")
    print("bls_jt_industry", pa.relative_to(root), na, sep="\t")
    print("bls_ce_supersector", pb.relative_to(root), nb, sep="\t")
    print(f"Line count ratio (JOLTS industry / CES supersector): {na / max(nb, 1):.4f}")


if __name__ == "__main__":
    main()
