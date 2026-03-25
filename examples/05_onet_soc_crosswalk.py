"""
Example: download the O*NET–SOC crosswalk (small CSV) and load it with pandas.

Requires network once; caches under ``raw/`` (or ``OT_RAW_DIR``).

Run::

    pip install -e .
    python examples/05_onet_soc_crosswalk.py
"""

from __future__ import annotations

from pathlib import Path

from occupational_transition.http import raw_cache_root
from occupational_transition.sources.onet import (
    ensure_soc_crosswalk,
    load_soc_crosswalk,
)


def main() -> None:
    raw_dir = raw_cache_root(Path.cwd())
    path = ensure_soc_crosswalk(raw_dir)
    df = load_soc_crosswalk(path)
    print(df.head())
    print(f"rows: {len(df)}  path: {path}")


if __name__ == "__main__":
    main()
