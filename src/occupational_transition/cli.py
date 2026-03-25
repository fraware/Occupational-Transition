"""Command-line helpers for discovering public data endpoints (read-only pointers)."""

from __future__ import annotations

import argparse
from pathlib import Path

from occupational_transition.http import fetch_text_cached, raw_cache_root
from occupational_transition.sources.btos import BTOS_API_BASE
from occupational_transition.sources.jolts import (
    JOLTS_BASE,
    PROVENANCE_FILES,
    ensure_jt_file,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ot-fetch",
        description=(
            "Print canonical URLs and file lists for US public labor data sources "
            "(no downloads unless you use other pipeline scripts)."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_btos = sub.add_parser("btos", help="Census BTOS API base and catalog endpoints")
    p_btos.add_argument(
        "--download",
        action="store_true",
        help="Download/cache periods and questions JSON endpoints.",
    )
    p_btos.add_argument(
        "--raw-dir",
        type=str,
        default="",
        help="Override cache root (default: OT_RAW_DIR or ./raw).",
    )
    p_btos.set_defaults(func=_cmd_btos)

    p_jolts = sub.add_parser(
        "jolts",
        help="BLS LABSTAT JOLTS base and provenance files",
    )
    p_jolts.add_argument(
        "--download",
        action="store_true",
        help="Download/cache all JOLTS provenance files into raw/.",
    )
    p_jolts.add_argument(
        "--raw-dir",
        type=str,
        default="",
        help="Override cache root (default: OT_RAW_DIR or ./raw).",
    )
    p_jolts.set_defaults(func=_cmd_jolts)

    args = parser.parse_args()
    kwargs: dict[str, object] = {}
    if hasattr(args, "download"):
        kwargs["download"] = args.download
    if hasattr(args, "raw_dir"):
        kwargs["raw_dir"] = args.raw_dir
    args.func(**kwargs)


def _cmd_btos(*, download: bool = False, raw_dir: str = "") -> None:
    cache_root = Path(raw_dir).expanduser().resolve() if raw_dir else raw_cache_root()
    if not download:
        print("btos_api_base", BTOS_API_BASE)
        print("periods", f"{BTOS_API_BASE}/periods")
        print("questions", f"{BTOS_API_BASE}/questions")
        return

    fetch_text_cached(f"{BTOS_API_BASE}/periods", cache_dir=cache_root)
    fetch_text_cached(f"{BTOS_API_BASE}/questions", cache_dir=cache_root)
    print(f"BTOS cached into {cache_root}")


def _cmd_jolts(*, download: bool = False, raw_dir: str = "") -> None:
    cache_root = Path(raw_dir).expanduser().resolve() if raw_dir else raw_cache_root()
    if not download:
        print("jolts_labstat_base", JOLTS_BASE)
        for fname in PROVENANCE_FILES:
            print("file", f"{JOLTS_BASE}{fname}")
        return

    for fname in PROVENANCE_FILES:
        ensure_jt_file(fname, raw_dir=cache_root)
    print(f"JOLTS cached into {cache_root}")


if __name__ == "__main__":
    main()
