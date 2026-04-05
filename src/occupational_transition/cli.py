"""Unified CLI for source discovery and pipeline execution."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from occupational_transition.bundle_manifest import write_analysis_bundles_yaml
from occupational_transition.catalog import (
    fetch_by_dataset_id,
    load_data_registry,
    refresh_blocked_by_freeze,
    refresh_catalog_rows,
    rows_matching,
)
from occupational_transition.http import fetch_text_cached, raw_cache_root
from occupational_transition.manifests import (
    ANALYSIS_BUNDLES,
    FULL_REBUILD_STEPS,
    list_sources,
    selectable_steps,
)
from occupational_transition.orchestration import (
    env_for_source_mode,
    latest_acceptance_log,
    parse_csv_list,
    parse_profile,
    run_acceptance_steps,
    run_shell,
)
from occupational_transition.paths import repo_root
from occupational_transition.sources.btos import BTOS_API_BASE
from occupational_transition.sources.jolts import (
    JOLTS_BASE,
    PROVENANCE_FILES,
    ensure_jt_file,
)


def _kwargs_for_command(args: argparse.Namespace) -> dict[str, Any]:
    fn = args.func
    out: dict[str, Any] = {}
    if fn is _cmd_btos or fn is _cmd_jolts:
        out["download"] = args.download
        out["raw_dir"] = args.raw_dir
        return out
    if fn is _cmd_list_analyses:
        out["verbose"] = args.verbose
        return out
    if fn is _cmd_catalog:
        out["program"] = args.program
        out["cadence"] = args.cadence
        out["all_rows"] = args.all_rows
        return out
    if fn is _cmd_fetch:
        out["dataset_ids"] = list(args.dataset_ids or [])
        out["program"] = args.program
        out["force"] = args.force
        out["raw_dir"] = args.raw_dir
        return out
    if fn is _cmd_refresh:
        out["cadence"] = args.cadence
        out["dataset_ids"] = list(args.dataset_ids or [])
        out["dry_run"] = args.dry_run
        out["force"] = args.force
        out["allow_in_freeze_mode"] = args.allow_in_freeze_mode
        out["raw_dir"] = args.raw_dir
        out["log"] = args.log
        return out
    if fn is _cmd_run:
        out["profile"] = args.profile
        out["bundle"] = args.bundle
        out["tickets"] = args.tickets
        out["source_selection_mode"] = args.source_selection_mode
        out["skip_install"] = args.skip_install
        out["with_visuals"] = args.with_visuals
        out["with_audit_summary"] = args.with_audit_summary
        out["require_signoff"] = args.require_signoff
        return out
    return out


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
    p_list_analyses.add_argument(
        "--verbose",
        action="store_true",
        help=(
            "Include output paths per ticket; refresh "
            "docs/meta/analysis_bundles.yaml."
        ),
    )
    p_list_analyses.set_defaults(func=_cmd_list_analyses)

    p_catalog = sub.add_parser(
        "catalog",
        help="List rows from docs/data_registry.csv (filter by program or cadence).",
    )
    p_catalog.add_argument("--program", default="", help="Filter by program column.")
    p_catalog.add_argument(
        "--cadence",
        default="",
        help="Filter by update_cadence (static, annual, rolling, reference).",
    )
    p_catalog.add_argument(
        "--all-rows",
        action="store_true",
        help="Include reference rows with no extractor (default: fetchable rows only).",
    )
    p_catalog.set_defaults(func=_cmd_catalog)

    p_fetch = sub.add_parser(
        "fetch",
        help="Download registry rows into raw/ (by dataset_id or program).",
    )
    p_fetch.add_argument(
        "--dataset-id",
        action="append",
        dest="dataset_ids",
        default=None,
        metavar="ID",
        help="Repeatable dataset_id from docs/data_registry.csv.",
    )
    p_fetch.add_argument(
        "--program",
        default="",
        help="Fetch all fetchable rows for this program (e.g. BLS_JOLTS).",
    )
    p_fetch.add_argument(
        "--force",
        action="store_true",
        help="Re-download even when cache looks populated.",
    )
    p_fetch.add_argument(
        "--raw-dir",
        type=str,
        default="",
        help="Override raw root (default OT_RAW_DIR or ./raw).",
    )
    p_fetch.set_defaults(func=_cmd_fetch)

    p_refresh = sub.add_parser(
        "refresh",
        help=(
            "Batch-fetch catalog rows (for local scheduling); "
            "respects freeze_mode unless overridden."
        ),
    )
    p_refresh.add_argument(
        "--cadence",
        default="",
        help="Only rows with this update_cadence (e.g. rolling).",
    )
    p_refresh.add_argument(
        "--dataset-id",
        action="append",
        dest="dataset_ids",
        default=None,
        metavar="ID",
        help="Repeatable dataset_id.",
    )
    p_refresh.add_argument(
        "--dry-run",
        action="store_true",
        help="Print targets without downloading.",
    )
    p_refresh.add_argument(
        "--force",
        action="store_true",
        help="Re-download even when cache looks populated.",
    )
    p_refresh.add_argument(
        "--allow-in-freeze-mode",
        action="store_true",
        help="Run refreshes even when SOURCE_SELECTION_MODE=freeze_mode.",
    )
    p_refresh.add_argument(
        "--raw-dir",
        type=str,
        default="",
        help="Override raw root.",
    )
    p_refresh.add_argument(
        "--log",
        type=str,
        default="",
        help=(
            "Append JSON lines log path under repo "
            "(default intermediate/refresh_<UTC>.jsonl)."
        ),
    )
    p_refresh.set_defaults(func=_cmd_refresh)

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
        help=(
            "Analysis bundle: quick-start, core-paper, "
            "full-replication, or release-signoff."
        ),
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
    p_run.add_argument(
        "--skip-install",
        action="store_true",
        help="Skip pip install -r requirements.txt.",
    )
    p_run.add_argument(
        "--with-visuals",
        action="store_true",
        help="Run visuals build and QA.",
    )
    p_run.add_argument(
        "--with-audit-summary",
        action="store_true",
        help="Build acceptance audit summary.",
    )
    p_run.add_argument(
        "--require-signoff",
        action="store_true",
        help="Run release signoff QA gate.",
    )
    p_run.set_defaults(func=_cmd_run)

    args = parser.parse_args()
    kwargs = _kwargs_for_command(args)
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


def _cmd_list_analyses(*, verbose: bool = False) -> None:
    root = repo_root()
    if verbose:
        write_analysis_bundles_yaml(root)
        print(f"Wrote {root / 'docs' / 'meta' / 'analysis_bundles.yaml'}")
    by_ticket = {s.ticket: s for s in FULL_REBUILD_STEPS}
    for b in ANALYSIS_BUNDLES:
        print(f"{b.name}: {b.description}")
        print(f"  tickets: {', '.join(b.tickets)}")
        if verbose:
            for t in b.tickets:
                step = by_ticket.get(t)
                if step:
                    print(f"    {t} outputs:")
                    for o in step.outputs:
                        print(f"      - {o}")


def _cmd_catalog(
    *,
    program: str = "",
    cadence: str = "",
    all_rows: bool = False,
) -> None:
    root = repo_root()
    rows = load_data_registry(root)
    sel = rows_matching(
        rows,
        program=program or None,
        cadence=cadence or None,
        fetchable_only=not all_rows,
    )
    for r in sel:
        did = r.get("dataset_id", "")
        ext = r.get("extractor", "")
        pr = r.get("program", "")
        cad = r.get("update_cadence", "")
        print(f"{did}\t{pr}\t{cad}\t{ext}")


def _cmd_fetch_jolts_program(
    *,
    raw_dir: Path,
    force: bool,
) -> None:
    skip = 0 if force else 10_000
    for fname in PROVENANCE_FILES:
        ensure_jt_file(fname, raw_dir=raw_dir, skip_if_exists_min_bytes=skip)
    print(f"JOLTS LABSTAT provenance files cached under {raw_dir}")


def _cmd_fetch(
    *,
    dataset_ids: list[str],
    program: str = "",
    force: bool = False,
    raw_dir: str = "",
) -> None:
    root = repo_root()
    cache = Path(raw_dir).expanduser().resolve() if raw_dir else raw_cache_root()
    if program.strip() == "BLS_JOLTS":
        _cmd_fetch_jolts_program(raw_dir=cache, force=force)
        rows = rows_matching(
            load_data_registry(root),
            program="BLS_JOLTS",
            fetchable_only=True,
        )
        for r in rows:
            if (r.get("extractor") or "").strip() != "jolts_labstat_file":
                continue
            fetch_by_dataset_id(
                root,
                r["dataset_id"],
                raw_dir=cache,
                force=force,
            )
        return

    if not dataset_ids and not program.strip():
        print(
            "Provide --dataset-id and/or --program (e.g. BLS_JOLTS).",
            file=sys.stderr,
        )
        raise SystemExit(2)

    if program.strip() and program.strip() != "BLS_JOLTS":
        rows = rows_matching(
            load_data_registry(root),
            program=program,
            fetchable_only=True,
        )
        for r in rows:
            fetch_by_dataset_id(root, r["dataset_id"], raw_dir=cache, force=force)
        return

    for did in dataset_ids:
        fetch_by_dataset_id(root, did, raw_dir=cache, force=force)
        print(f"Fetched {did} -> {cache}")


def _cmd_refresh(
    *,
    cadence: str = "",
    dataset_ids: list[str],
    dry_run: bool = False,
    force: bool = False,
    allow_in_freeze_mode: bool = False,
    raw_dir: str = "",
    log: str = "",
) -> None:
    root = repo_root()
    if refresh_blocked_by_freeze(force_refresh_in_freeze=allow_in_freeze_mode):
        print(
            "SOURCE_SELECTION_MODE=freeze_mode: skip refresh. "
            "Use --allow-in-freeze-mode to override.",
            file=sys.stderr,
        )
        return

    cache = Path(raw_dir).expanduser().resolve() if raw_dir else raw_cache_root()
    rows = load_data_registry(root)
    if dataset_ids:
        selected = [r for r in rows if r.get("dataset_id") in dataset_ids]
    elif cadence.strip():
        selected = rows_matching(
            rows, cadence=cadence.strip(), fetchable_only=True
        )
    else:
        print(
            "Provide --cadence and/or --dataset-id (see ot catalog).",
            file=sys.stderr,
        )
        raise SystemExit(2)

    log_path = (
        Path(log).expanduser().resolve()
        if log
        else root
        / "intermediate"
        / f"refresh_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.jsonl"
    )
    if not dry_run:
        log_path.parent.mkdir(parents=True, exist_ok=True)

    entries = refresh_catalog_rows(
        selected, raw_dir=cache, force=force, dry_run=dry_run
    )
    for e in entries:
        line = json.dumps(e, ensure_ascii=False)
        print(line)
        if not dry_run:
            with log_path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
    if not dry_run:
        print(f"Log: {log_path}", file=sys.stderr)


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

    run_section = profile_data.get("run", {})
    run_cfg = run_section if isinstance(run_section, dict) else {}
    selected_bundle = bundle or str(run_cfg.get("bundle", "")).strip()
    tickets_csv = str(run_cfg.get("tickets", ""))
    selected_tickets = (
        parse_csv_list(tickets) if tickets else parse_csv_list(tickets_csv)
    )
    source_mode = source_selection_mode or str(
        run_cfg.get("source_selection_mode", "latest_mode")
    )
    if source_mode not in {"latest_mode", "freeze_mode"}:
        raise ValueError("source_selection_mode must be latest_mode or freeze_mode")

    step_list = selectable_steps(selected_bundle or None, selected_tickets or None)
    if not step_list:
        raise ValueError("No steps selected. Provide --bundle or --tickets.")

    env = env_for_source_mode(source_mode)
    install_skip_effective = skip_install or bool(run_cfg.get("skip_install", False))
    visuals_effective = with_visuals or bool(run_cfg.get("with_visuals", False))
    audit_effective = with_audit_summary or bool(
        run_cfg.get("with_audit_summary", False)
    )
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
        for cmd in (
            "python scripts/run_visuals_all.py",
            "python scripts/qa_visuals.py",
        ):
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
        rc, _ = run_shell(
            root,
            "python scripts/qa_release_signoff.py",
            env_overrides=env,
        )
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
