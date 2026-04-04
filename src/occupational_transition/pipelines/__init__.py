"""Reusable data pipeline functions (compute + return artifacts)."""

from occupational_transition.pipelines.alpi_occ22_monthly_t026 import run as run_t026
from occupational_transition.pipelines.awes_occ22_monthly_t023 import run as run_t023
from occupational_transition.pipelines.btos_sector_ai_use_t022 import run as run_t022
from occupational_transition.pipelines.cps_occ22_exit_risk_t025 import run as run_t025
from occupational_transition.pipelines.figure1_panelA_t001 import run as run_t001
from occupational_transition.pipelines.figure1_panelB_t002 import (
    build_figure1_panelB_t002 as build_t002_outputs,
)
from occupational_transition.pipelines.figure1_panelB_t002 import run as run_t002
from occupational_transition.pipelines.figure2_panelA_t003 import run as run_t003
from occupational_transition.pipelines.figure2_panelB_counts_t004 import run as run_t004
from occupational_transition.pipelines.figure2_panelB_probs_t005 import run as run_t005
from occupational_transition.pipelines.figure3_panelA_t006 import run as run_t006
from occupational_transition.pipelines.figure3_panelB_t007 import run as run_t007
from occupational_transition.pipelines.figure4_panelA_t008 import run as run_t008
from occupational_transition.pipelines.figure4_panelB_t009 import run as run_t009
from occupational_transition.pipelines.figure5_capability_t010 import run as run_t010
from occupational_transition.pipelines.figureA1_t011 import run as run_t011
from occupational_transition.pipelines.figureA2_t012 import run as run_t012
from occupational_transition.pipelines.figureA3_t013 import run as run_t013
from occupational_transition.pipelines.figureA4_t014 import run as run_t014
from occupational_transition.pipelines.figureA5_t015 import run as run_t015
from occupational_transition.pipelines.figureA6_t016 import run as run_t016
from occupational_transition.pipelines.figureA7_t017 import run as run_t017
from occupational_transition.pipelines.figureA8_t018 import run as run_t018
from occupational_transition.pipelines.figureA9_t019 import run as run_t019
from occupational_transition.pipelines.figureA10_t020 import run as run_t020
from occupational_transition.pipelines.occ22_sector_weights_t021 import run as run_t021
from occupational_transition.pipelines.pr000_crosswalks import run as run_pr000
from occupational_transition.pipelines.sector6_stress_monthly_t024 import (
    run as run_t024,
)

__all__ = [
    "build_t002_outputs",
    "run_pr000",
    "run_t001",
    "run_t002",
    "run_t003",
    "run_t004",
    "run_t005",
    "run_t006",
    "run_t007",
    "run_t008",
    "run_t009",
    "run_t010",
    "run_t011",
    "run_t012",
    "run_t013",
    "run_t014",
    "run_t015",
    "run_t016",
    "run_t017",
    "run_t018",
    "run_t019",
    "run_t020",
    "run_t021",
    "run_t022",
    "run_t023",
    "run_t024",
    "run_t025",
    "run_t026",
]
