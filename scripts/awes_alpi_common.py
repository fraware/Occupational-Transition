"""
Backward-compatible import path for repo scripts.

Implementation lives in ``occupational_transition.awes_alpi_common``. When you run
``python scripts/<name>.py``, Python puts ``scripts/`` on ``sys.path`` first, so
``from awes_alpi_common import ...`` resolves here; this module ensures ``src/``
is visible and re-exports the package API.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
_src_s = str(_SRC)
if _src_s not in sys.path:
    sys.path.insert(0, _src_s)

from occupational_transition.awes_alpi_common import (  # noqa: E402
    SECTOR6_ORDER,
    naics2_to_sector6,
    naics_string_to_n2,
    occ22_code_from_id,
    percentile_rank_01,
    soc_code_to_major,
    zscore_panel,
)

__all__ = [
    "SECTOR6_ORDER",
    "naics2_to_sector6",
    "naics_string_to_n2",
    "occ22_code_from_id",
    "percentile_rank_01",
    "soc_code_to_major",
    "zscore_panel",
]
