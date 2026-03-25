from __future__ import annotations

from pathlib import Path

import pandas as pd

from occupational_transition.crosswalks import load_occ22_labels
from occupational_transition.pipelines.figure1_panelB_t002 import (
    FROZEN_ELEMENTS,
    aggregate_to_occ22,
    assign_terciles,
    onet_to_soc_means,
    soc_code_to_major,
    zscore_22,
)


def test_soc_code_to_major() -> None:
    assert soc_code_to_major("23-1000") == "23-0000"


def test_zscore_22_constant_series() -> None:
    s = pd.Series([1.0, 1.0, 1.0])
    out = zscore_22(s)
    assert out.tolist() == [0.0, 0.0, 0.0]


def test_assign_terciles_counts() -> None:
    df = pd.DataFrame(
        {
            "occ22_id": list(range(1, 23)),
            "occupation_group": ["g"] * 22,
            "ai_task_index": list(range(22)),
        }
    )
    out = assign_terciles(df)
    vc = out["ai_relevance_tercile"].value_counts().to_dict()
    assert vc["low"] == 7
    assert vc["middle"] == 7
    assert vc["high"] == 8


def test_onet_to_soc_means_basic() -> None:
    wa = pd.DataFrame(
        {
            "onet_soc_code": ["A", "B"],
            "element_name": ["Analyzing Data or Information"] * 2,
            "data_value": [1.0, 3.0],
        }
    )
    xwalk = pd.DataFrame(
        {
            "onet_soc_code": ["A", "B"],
            "soc_2018": ["11-0000", "11-0000"],
        }
    )
    out = onet_to_soc_means(wa, xwalk)
    assert len(out) == 1
    assert out.loc[0, "soc_2018"] == "11-0000"
    assert out.loc[0, "data_value"] == 2.0


def test_aggregate_to_occ22_weighted_mean() -> None:
    root = Path(__file__).resolve().parents[1]
    labels = load_occ22_labels(root / "crosswalks" / "occ22_crosswalk.csv")
    major = "11-0000"
    occ_row = labels[labels["soc_major_group_code"] == major]
    assert len(occ_row) == 1
    occ22_id = int(occ_row["occ22_id"].iloc[0])

    soc_2018 = "11-1000"
    scores = pd.DataFrame(
        {
            "soc_2018": [soc_2018] * len(FROZEN_ELEMENTS),
            "element_name": list(FROZEN_ELEMENTS),
            "data_value": [float(i + 1) for i in range(len(FROZEN_ELEMENTS))],
        }
    )
    oews_emp = pd.DataFrame({"soc_2018": [soc_2018], "employment": [10.0]})

    out = aggregate_to_occ22(scores, oews_emp, labels)
    assert len(out) == 1
    assert int(out.loc[0, "occ22_id"]) == occ22_id
    for elem in FROZEN_ELEMENTS:
        assert out.loc[0, elem] == scores[scores["element_name"] == elem][
            "data_value"
        ].iloc[0]

