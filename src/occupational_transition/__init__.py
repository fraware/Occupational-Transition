"""Installable package for public-data extraction (BLS, Census BTOS, O*NET, etc.)."""

from __future__ import annotations

from typing import Any

from occupational_transition import crosswalks, http
from occupational_transition.sources import btos, jolts, oews, onet

__version__ = "0.1.0"

# Public surface: prefer ``from occupational_transition.sources import btos`` etc.
# Pipeline modules (e.g. ``pipelines.figure1_panelB_t002``) load on demand via
# ``__getattr__`` so ``import occupational_transition`` stays lightweight.
__all__ = [
    "__version__",
    "crosswalks",
    "http",
    "btos",
    "jolts",
    "onet",
    "oews",
    "figure1_panelB_t002",
]


def __getattr__(name: str) -> Any:
    if name == "figure1_panelB_t002":
        from occupational_transition.pipelines import figure1_panelB_t002

        return figure1_panelB_t002
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
