"""Repository root resolution (package lives under src/occupational_transition)."""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    """Return repository root (parent of ``src/``)."""
    return Path(__file__).resolve().parents[2]
