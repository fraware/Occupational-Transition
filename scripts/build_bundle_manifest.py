"""Write docs/meta/analysis_bundles.yaml from manifest ticket lists."""

from __future__ import annotations

import sys
from pathlib import Path

if str(Path(__file__).resolve().parents[1] / "src") not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from occupational_transition.bundle_manifest import write_analysis_bundles_yaml
from occupational_transition.paths import repo_root


def main() -> None:
    root = repo_root()
    path = write_analysis_bundles_yaml(root)
    print(f"Wrote {path.relative_to(root)}")


if __name__ == "__main__":
    main()
