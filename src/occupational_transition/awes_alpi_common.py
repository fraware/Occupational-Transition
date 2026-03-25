"""Shared helpers used across AWES/ALPI-style metrics.

This module lives in `src/` so it is available to library users without
importing from `scripts/`.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def occ22_code_from_id(occ22_id: int) -> str:
    """Canonical occ22 key used in CPS transition states."""
    return f"occ22_{int(occ22_id):02d}"


def percentile_rank_01(s: pd.Series, method: str = "average") -> pd.Series:
    """
    Percentile rank in [0, 1] based on ascending order.

    Ties use pandas average rank. All-null yields NaN.
    """
    v = pd.to_numeric(s, errors="coerce")
    mask = v.notna()
    n = int(mask.sum())
    if n == 0:
        return pd.Series(np.nan, index=s.index, dtype=float)
    if n == 1:
        out = pd.Series(np.nan, index=s.index, dtype=float)
        out.loc[mask] = 0.5
        return out
    ranks = v[mask].rank(method=method, ascending=True)
    pct = (ranks - 1.0) / (n - 1.0)
    out = pd.Series(np.nan, index=s.index, dtype=float)
    out.loc[mask] = pct.astype(float)
    return out

