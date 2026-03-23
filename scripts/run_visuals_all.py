from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CMDS = [
    "python scripts/visualize_figure1.py",
    "python scripts/visualize_figure2.py",
    "python scripts/visualize_figure3.py",
    "python scripts/visualize_figure4.py",
    "python scripts/visualize_figure5.py",
    "python scripts/visualize_figureA.py",
]


def main() -> int:
    for cmd in CMDS:
        print(f"RUN {cmd}")
        r = subprocess.run(cmd, cwd=ROOT, shell=True)
        if r.returncode != 0:
            print(f"FAIL {cmd}")
            return r.returncode
    print("DONE visuals build")
    return 0


if __name__ == "__main__":
    sys.exit(main())
