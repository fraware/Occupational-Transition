from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.image as mpimg

ROOT = Path(__file__).resolve().parents[1]
PNG = ROOT / "visuals" / "png"
PDF = ROOT / "visuals" / "vector"

REQUIRED = [
    "awes_top20_latest",
    "alpi_top20_latest",
    "awes_alpi_monthly_median",
    "awes_vs_alpi_latest_scatter",
]


def _check_png(path: Path, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing png: {path}")
        return
    if path.stat().st_size <= 0:
        errors.append(f"empty png: {path}")
        return
    try:
        arr = mpimg.imread(path)
        if arr.size == 0:
            errors.append(f"unreadable png: {path}")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"unreadable png {path}: {exc}")


def _check_pdf(path: Path, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing pdf: {path}")
        return
    if path.stat().st_size <= 0:
        errors.append(f"empty pdf: {path}")


def main() -> int:
    errors: list[str] = []
    for stem in REQUIRED:
        _check_png(PNG / f"{stem}.png", errors)
        _check_pdf(PDF / f"{stem}.pdf", errors)

    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("QA OK: AWES/ALPI visuals")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
