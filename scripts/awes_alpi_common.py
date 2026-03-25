"""
Shared helpers for AWES / ALPI metric builds (pure functions, no I/O).

Normalization and crosswalk utilities are aligned with build_crosswalks and
Figure 1–4 scripts.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# Frozen six-sector NAICS2 mapping (same rule as scripts/build_crosswalks.py).
SECTOR6_ORDER: tuple[str, ...] = ("MFG", "INF", "FAS", "PBS", "HCS", "RET")


def soc_code_to_major(soc: str) -> str:
    """Map detailed SOC 'XX-YYYY' to major group 'XX-0000'."""
    s = str(soc).strip()
    if "-" not in s:
        raise ValueError(f"Invalid SOC code: {soc}")
    left, _ = s.split("-", 1)
    if not left.isdigit():
        raise ValueError(f"Invalid SOC code: {soc}")
    return f"{int(left):02d}-0000"


def naics_string_to_n2(
    naics_field: str | float | int | None,
) -> int | None:
    """Extract NAICS 2-digit sector from OEWS/CES-style field."""
    if naics_field is None or (isinstance(naics_field, float) and np.isnan(naics_field)):
        return None
    s = str(naics_field).strip()
    if s in ("-", "", "nan", "NaN", "0"):
        return None
    first = s.split(",")[0].strip()
    digits = "".join(ch for ch in first if ch.isdigit())
    if len(digits) < 2:
        return None
    return int(digits[:2])


def naics2_to_sector6(n2: int) -> tuple[str | None, str, str]:
    """Map NAICS 2-digit sector to frozen six-sector set (sector6_code or None)."""
    if n2 in (31, 32, 33):
        return "MFG", "Manufacturing", "naics2_manufacturing"
    if n2 == 51:
        return "INF", "Information", "naics2_information"
    if n2 in (52, 53):
        return "FAS", "Financial activities", "naics2_finance_or_real_estate"
    if n2 in (54, 55, 56):
        return (
            "PBS",
            "Professional and business services",
            "naics2_professional_management_admin",
        )
    if n2 == 62:
        return "HCS", "Health care and social assistance", "naics2_health_social_assistance"
    if n2 in (44, 45):
        return "RET", "Retail trade", "naics2_retail"
    if n2 == 61:
        return (
            "PBS",
            "Professional and business services",
            "naics2_educational_services_maps_to_PBS",
        )
    return None, "", "out_of_scope_six_sector"


def occ22_code_from_id(occ22_id: int) -> str:
    """Canonical occ22 key used in CPS transition states."""
    return f"occ22_{int(occ22_id):02d}"


def percentile_rank_01(s: pd.Series, method: str = "average") -> pd.Series:
    """
    Percentile rank in [0, 1]: (rank - 1) / (n - 1) for n > 1 non-null values.

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


def zscore_panel(s: pd.Series) -> pd.Series:
    """Population z-score over non-null values; null stays null."""
    v = pd.to_numeric(s, errors="coerce")
    mu = float(v.mean(skipna=True))
    sigma = float(v.std(ddof=0))
    if sigma == 0.0 or np.isnan(sigma):
        return pd.Series(0.0, index=s.index)
    return (v - mu) / sigma
