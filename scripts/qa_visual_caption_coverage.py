"""
Verify main-text figure caption and source-note files exist
(`docs/captions`, `docs/source_notes`).

Usage:
    python scripts/qa_visual_caption_coverage.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = [
    ("fig01_caption.md", "fig01_sources.md"),
    ("fig02_caption.md", "fig02_sources.md"),
    ("fig03_caption.md", "fig03_sources.md"),
    ("fig04_caption.md", "fig04_sources.md"),
    ("fig05_caption.md", "fig05_sources.md"),
]


def main() -> int:
    cap_dir = ROOT / "docs" / "captions"
    src_dir = ROOT / "docs" / "source_notes"
    errors: list[str] = []
    for cap, src in EXPECTED:
        cp = cap_dir / cap
        sp = src_dir / src
        if not cp.is_file():
            errors.append(f"missing caption: {cp}")
        elif cp.stat().st_size <= 0:
            errors.append(f"empty caption: {cp}")
        if not sp.is_file():
            errors.append(f"missing source note: {sp}")
        elif sp.stat().st_size <= 0:
            errors.append(f"empty source note: {sp}")
    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print("PASS: caption and source note coverage for Figures 1–5.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
