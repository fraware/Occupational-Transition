from __future__ import annotations

import numpy as np
import pandas as pd

RELIABILITY_COLUMNS = [
    "weighted_n",
    "effective_n",
    "cv",
    "se",
    "ci_lower",
    "ci_upper",
    "ci_level",
    "variance_method",
    "reliability_tier",
    "publish_flag",
    "suppression_reason",
    "pooling_applied",
    "evidence_directness",
]


def evaluate_publishability(
    df: pd.DataFrame,
    *,
    min_weighted_n: float,
    min_effective_n: float,
    max_cv: float,
) -> pd.DataFrame:
    out = df.copy()
    weighted = pd.to_numeric(out["weighted_n"], errors="coerce")
    effective = pd.to_numeric(out["effective_n"], errors="coerce")
    cv = pd.to_numeric(out["cv"], errors="coerce")

    reasons: list[str] = []
    flags: list[bool] = []
    tiers: list[str] = []

    for w, e, c in zip(weighted, effective, cv):
        local = []
        if pd.isna(w) or w < min_weighted_n:
            local.append("weighted_n_below_min")
        if pd.isna(e) or e < min_effective_n:
            local.append("effective_n_below_min")
        if pd.isna(c):
            local.append("cv_missing")
        elif c > max_cv:
            local.append("cv_above_max")

        publish = len(local) == 0
        flags.append(publish)
        reasons.append("" if publish else ";".join(local))
        if publish and c <= 0.15:
            tiers.append("high")
        elif publish:
            tiers.append("medium")
        else:
            tiers.append("low")

    out["publish_flag"] = flags
    out["suppression_reason"] = reasons
    out["reliability_tier"] = tiers
    out["pooling_applied"] = out.get("pooling_applied", 1)
    pa = pd.to_numeric(out["pooling_applied"], errors="coerce").fillna(1).astype(int)
    out["pooling_applied"] = pa

    directness = out.get("evidence_directness")
    if directness is None:
        out["evidence_directness"] = "derived_transform"
    else:
        out["evidence_directness"] = (
            out["evidence_directness"]
            .astype(str)
            .replace({"": "derived_transform", "nan": "derived_transform"})
        )
    return out


def ensure_reliability_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in RELIABILITY_COLUMNS:
        if col not in out.columns:
            out[col] = np.nan
    return out
