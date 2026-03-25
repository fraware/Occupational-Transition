from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCRIPTS = [
    "scripts/build_figure1_panelA.py",
    "scripts/build_figure1_panelB.py",
    "scripts/build_figure2_panelA.py",
    "scripts/build_figure2_panelB_counts.py",
    "scripts/build_figure2_panelB_probs.py",
    "scripts/build_figure3_panelA_btos_ai_trends.py",
    "scripts/build_figure3_panelB_btos_workforce_effects.py",
    "scripts/build_figure4_panelA_jolts_sector_rates.py",
    "scripts/build_figure4_panelB_ces_sector_index.py",
    "scripts/build_figure5_capability_matrix.py",
    "scripts/build_memo_dashboard_kpis.py",
    "scripts/build_memo_dashboard_png.py",
    "scripts/visualize_memo.py",
    "scripts/build_memo_occ_bubble_scatter.py",
    "scripts/build_memo_cps_transition_flows.py",
    "scripts/build_memo_btos_state_ai_map.py",
    "scripts/build_memo_resolution_ladder.py",
    "scripts/build_memo_policy_roadmap.py",
    "scripts/build_state_qcew_deep_dive.py",
    "scripts/build_virginia_memo_kpis.py",
    "scripts/visualize_virginia_memo.py",
]


def main() -> int:
    for s in SCRIPTS:
        print(f"[build] {s}")
        rc = subprocess.call([sys.executable, str(ROOT / s)])
        if rc != 0:
            print(f"FAILED: {s} (exit {rc})", file=sys.stderr)
            return rc
    print("Memo visuals build complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
