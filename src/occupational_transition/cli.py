"""Unified CLI for source discovery and pipeline execution."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from occupational_transition.http import fetch_text_cached, raw_cache_root
from occupational_transition.manifests import ANALYSIS_BUNDLES, list_sources, selectable_steps
from occupational_transition.orchestration import (
    env_for_source_mode,
    latest_acceptance_log,
    parse_csv_list,
    parse_profile,
    run_acceptance_steps,
    run_shell,
)
from occupational_transition.sources.btos import BTOS_API_BASE
from occupational_transition.sources.jolts import (
    JOLTS_BASE,
    PROVENANCE_FILES,
    ensure_jt_file,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ot",
        description=(
            "Run and discover Occupational Transition pipelines and sources."
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

    p_list_analyses = sub.add_parser(
        "list-analyses",
        help="List predefined analysis bundles and included tickets.",
    )
    p_list_analyses.set_defaults(func=_cmd_list_analyses)

    p_list_sources = sub.add_parser(
        "list-sources",
        help="List available source families and mode hints.",
    )
    p_list_sources.set_defaults(func=_cmd_list_sources)

    p_run = sub.add_parser(
        "run",
        help="Run selected analyses with CLI flags and/or a TOML profile.",
    )
    p_run.add_argument(
        "--profile",
        type=str,
        default="",
        help="Path to TOML profile. Values can be overridden by explicit flags.",
    )
    p_run.add_argument(
        "--bundle",
        type=str,
        default="",
        help="Analysis bundle name (quick-start, core-paper, full-replication, release-signoff).",
    )
    p_run.add_argument(
        "--tickets",
        type=str,
        default="",
        help="Comma-separated ticket IDs to run (overrides bundle), e.g. T-001,T-002.",
    )
    p_run.add_argument(
        "--source-selection-mode",
        choices=["latest_mode", "freeze_mode"],
        default="latest_mode",
        help="latest_mode for monitoring; freeze_mode for comparability/release.",
    )
    p_run.add_argument("--skip-install", action="store_true", help="Skip pip install -r requirements.txt.")
    p_run.add_argument("--with-visuals", action="store_true", help="Run visuals build and QA.")
    p_run.add_argument("--with-audit-summary", action="store_true", help="Build acceptance audit summary.")
    p_run.add_argument("--require-signoff", action="store_true", help="Run release signoff QA gate.")
    p_run.set_defaults(func=_cmd_run)

    args = parser.parse_args()
    kwargs: dict[str, Any] = {}
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


def _cmd_list_analyses() -> None:
    for b in ANALYSIS_BUNDLES:
        print(f"{b.name}: {b.description}")
        print(f"  tickets: {', '.join(b.tickets)}")


def _cmd_list_sources() -> None:
    for row in list_sources():
        print(f"{row['source']}: {row['mode_hint']}")


def _cmd_run(
    *,
    profile: str = "",
    bundle: str = "",
    tickets: str = "",
    source_selection_mode: str = "latest_mode",
    skip_install: bool = False,
    with_visuals: bool = False,
    with_audit_summary: bool = False,
    require_signoff: bool = False,
) -> None:
    root = Path(__file__).resolve().parents[2]

    profile_data: dict[str, Any] = {}
    if profile:
        profile_data = parse_profile(Path(profile))

    run_cfg = profile_data.get("run", {}) if isinstance(profile_data.get("run"), dict) else {}
    selected_bundle = bundle or str(run_cfg.get("bundle", "")).strip()
    selected_tickets = parse_csv_list(tickets) if tickets else parse_csv_list(str(run_cfg.get("tickets", "")))
    source_mode = source_selection_mode or str(run_cfg.get("source_selection_mode", "latest_mode"))
    if source_mode not in {"latest_mode", "freeze_mode"}:
        raise ValueError("source_selection_mode must be latest_mode or freeze_mode")

    step_list = selectable_steps(selected_bundle or None, selected_tickets or None)
    if not step_list:
        raise ValueError("No steps selected. Provide --bundle or --tickets.")

    env = env_for_source_mode(source_mode)
    install_skip_effective = skip_install or bool(run_cfg.get("skip_install", False))
    visuals_effective = with_visuals or bool(run_cfg.get("with_visuals", False))
    audit_effective = with_audit_summary or bool(run_cfg.get("with_audit_summary", False))
    signoff_effective = require_signoff or bool(run_cfg.get("require_signoff", False))

    if not install_skip_effective:
        rc, _ = run_shell(
            root,
            "python -m pip install -r requirements.txt && python -m pip install -e .",
            env_overrides=env,
        )
        if rc != 0:
            raise SystemExit(rc)

    # Run chosen steps with no post gates (this command is analysis-centric).
    rc = run_acceptance_steps(root=root, steps=step_list, gates=[], env_overrides=env)
    if rc != 0:
        raise SystemExit(rc)

    if visuals_effective:
        for cmd in ("python scripts/run_visuals_all.py", "python scripts/qa_visuals.py"):
            rc, _ = run_shell(root, cmd, env_overrides=env)
            if rc != 0:
                raise SystemExit(rc)

    if audit_effective:
        log = latest_acceptance_log(root)
        if log is not None:
            rc, _ = run_shell(
                root,
                "python scripts/build_acceptance_audit_summary.py "
                f'--log "{log.relative_to(root).as_posix()}"',
                env_overrides=env,
            )
            if rc != 0:
                raise SystemExit(rc)

    if signoff_effective:
        rc, _ = run_shell(root, "python scripts/qa_release_signoff.py", env_overrides=env)
        if rc != 0:
            raise SystemExit(rc)


if __name__ == "__main__":
    main()


def main_run_full() -> None:
    """Convenience entrypoint: equivalent to `ot run --bundle full-replication`."""
    _cmd_run(bundle="full-replication")


def main_run_visuals() -> None:
    """Convenience entrypoint for visual build + QA."""
    root = Path(__file__).resolve().parents[2]
    for cmd in ("python scripts/run_visuals_all.py", "python scripts/qa_visuals.py"):
        rc, _ = run_shell(root, cmd)
        if rc != 0:
            raise SystemExit(rc)
