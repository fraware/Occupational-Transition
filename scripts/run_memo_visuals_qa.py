from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCRIPTS = [
    "scripts/qa_memo_dashboard_kpis.py",
    "scripts/qa_memo_occ_bubble_scatter.py",
    "scripts/qa_memo_cps_transition_flows.py",
    "scripts/qa_memo_capability_matrix.py",
    "scripts/qa_memo_resolution_ladder.py",
    "scripts/qa_memo_policy_roadmap.py",
    "scripts/qa_memo_btos_state_ai_use_latest.py",
    "scripts/qa_state_qcew_deep_dive.py",
    "scripts/qa_virginia_memo_visuals.py",
    "scripts/build_drift_dashboard.py",
    "scripts/qa_drift_dashboard.py",
]


def main() -> int:
    for s in SCRIPTS:
        print(f"[qa] {s}")
        rc = subprocess.call([sys.executable, str(ROOT / s)])
        if rc != 0:
            print(f"FAILED: {s} (exit {rc})", file=sys.stderr)
            return rc
    print("Memo visuals QA complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
