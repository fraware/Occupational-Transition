from __future__ import annotations

from statistics import NormalDist

import numpy as np
import pandas as pd


def _safe_se_from_cv(value: float, cv: float) -> float:
    if np.isnan(value) or np.isnan(cv):
        return np.nan
    return abs(value) * cv


def add_basic_uncertainty_fields(
    df: pd.DataFrame,
    *,
    value_col: str = "value",
    cv_col: str = "cv",
    ci_level: float = 0.95,
    variance_method: str = "cv_approximation",
) -> pd.DataFrame:
    out = df.copy()
    alpha = 1.0 - ci_level
    z = NormalDist().inv_cdf(1.0 - alpha / 2.0)
    vals = pd.to_numeric(out[value_col], errors="coerce")
    cvs = pd.to_numeric(out[cv_col], errors="coerce")
    ses = [
        _safe_se_from_cv(float(v), float(c)) if pd.notna(v) and pd.notna(c) else np.nan
        for v, c in zip(vals, cvs)
    ]
    out["se"] = ses
    out["ci_lower"] = vals - z * pd.to_numeric(out["se"], errors="coerce")
    out["ci_upper"] = vals + z * pd.to_numeric(out["se"], errors="coerce")
    out["ci_level"] = ci_level
    out["variance_method"] = variance_method
    return out
