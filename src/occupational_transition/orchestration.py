from __future__ import annotations

import argparse
import datetime as dt
import glob
import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PipelineStep:
    ticket: str
    build_cmd: str
    qa_cmd: str
    outputs: tuple[str, ...]
    build_module: str | None = None
    qa_module: str | None = None


@dataclass(frozen=True)
class GateStep:
    name: str
    command: str


@dataclass(frozen=True)
class AnalysisBundle:
    name: str
    description: str
    tickets: tuple[str, ...]


def run_shell(
    root: Path,
    cmd: str,
    *,
    env_overrides: dict[str, str] | None = None,
    capture_output: bool = False,
) -> tuple[int, str]:
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
    proc = subprocess.run(
        cmd,
        cwd=root,
        shell=True,
        text=True,
        stdout=subprocess.PIPE if capture_output else None,
        stderr=subprocess.STDOUT if capture_output else None,
        env=env,
    )
    return proc.returncode, proc.stdout or ""


def delete_outputs(root: Path, outputs: tuple[str, ...]) -> list[str]:
    deleted: list[str] = []
    for rel in outputs:
        p = root / rel
        if p.exists():
            p.unlink()
            deleted.append(rel)
    return deleted


def latest_acceptance_log(root: Path) -> Path | None:
    pattern = str(root / "intermediate" / "full_clean_rebuild_acceptance_*.md")
    paths = [
        Path(p)
        for p in glob.glob(pattern)
        if "_audit_summary" not in p and p.endswith(".md")
    ]
    if not paths:
        return None
    return max(paths, key=lambda p: p.stat().st_mtime)


def run_acceptance_steps(
    *,
    root: Path,
    steps: list[PipelineStep],
    gates: list[GateStep],
    env_overrides: dict[str, str] | None = None,
) -> int:
    inter = root / "intermediate"
    inter.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = inter / f"full_clean_rebuild_acceptance_{ts}.md"

    lines: list[str] = []
    lines.append("# Full Clean Rebuild Acceptance Log")
    lines.append("")
    lines.append(f"- Started UTC: {dt.datetime.now(dt.timezone.utc).isoformat()}")
    lines.append(f"- Scope: {steps[0].ticket} through {steps[-1].ticket}")
    lines.append("- Mode: strict ticket-by-ticket rebuild with checkpoints")
    lines.append("")

    failures = 0
    start_all = time.time()

    for step in steps:
        t0 = time.time()
        lines.append(f"## {step.ticket}")
        lines.append("")
        deleted = delete_outputs(root, step.outputs)
        lines.append(f"- Checkpoint cleanup deleted: {deleted if deleted else 'none'}")

        rc_b, out_b = run_shell(
            root,
            step.build_cmd,
            env_overrides=env_overrides,
            capture_output=True,
        )
        if "SettingWithCopyWarning" in out_b:
            rc_b = 1
            out_b += (
                "\n[STRICT WARNING POLICY] "
                "SettingWithCopyWarning escalated to failure.\n"
            )
        lines.append(f"- Build command: `{step.build_cmd}`")
        lines.append(f"- Build exit code: `{rc_b}`")
        lines.append("")
        lines.append("### Build Output")
        lines.append("```text")
        lines.append(out_b.rstrip() if out_b.strip() else "(no output)")
        lines.append("```")

        missing = [p for p in step.outputs if not (root / p).exists()]
        check = missing if missing else "all present"
        lines.append(f"- Output existence check: `{check}`")

        rc_q, out_q = run_shell(
            root,
            step.qa_cmd,
            env_overrides=env_overrides,
            capture_output=True,
        )
        lines.append(f"- QA command: `{step.qa_cmd}`")
        lines.append(f"- QA exit code: `{rc_q}`")
        lines.append("")
        lines.append("### QA Output")
        lines.append("```text")
        lines.append(out_q.rstrip() if out_q.strip() else "(no output)")
        lines.append("```")

        elapsed = round(time.time() - t0, 2)
        ticket_ok = rc_b == 0 and rc_q == 0 and not missing
        if not ticket_ok:
            failures += 1
        lines.append(f"- Checkpoint result: `{'PASS' if ticket_ok else 'FAIL'}`")
        lines.append(f"- Elapsed seconds: `{elapsed}`")
        lines.append("")
        log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        if not ticket_ok:
            lines.append("Stopping early after first failure in strict mode.")
            log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(f"FAILED at {step.ticket}. See log: {log_path}")
            return 1

    total_elapsed = round(time.time() - start_all, 2)
    lines.append("## Post-Ticket Release Gates")
    lines.append("")
    for gate in gates:
        rc_g, out_g = run_shell(
            root,
            gate.command,
            env_overrides=env_overrides,
            capture_output=True,
        )
        lines.append(f"- Gate: `{gate.name}`")
        lines.append(f"- Command: `{gate.command}`")
        lines.append(f"- Exit code: `{rc_g}`")
        lines.append("```text")
        lines.append(out_g.rstrip() if out_g.strip() else "(no output)")
        lines.append("```")
        lines.append("")
        log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        if rc_g != 0:
            lines.append("Stopping after failed post-ticket release gate.")
            log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(f"FAILED at post gate: {gate.name}. See log: {log_path}")
            return 1

    lines.append("## Final Summary")
    lines.append("")
    lines.append(f"- Failures: `{failures}`")
    lines.append(f"- Total elapsed seconds: `{total_elapsed}`")
    lines.append("- Overall result: `PASS`")
    lines.append("")
    lines.append(f"- Finished UTC: {dt.datetime.now(dt.timezone.utc).isoformat()}")
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS. Acceptance log written: {log_path}")
    return 0


def parse_profile(profile_path: Path) -> dict[str, Any]:
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile not found: {profile_path}")
    try:
        import tomllib  # py311+
    except ModuleNotFoundError:  # pragma: no cover
        import tomli as tomllib  # type: ignore
    with profile_path.open("rb") as f:
        return tomllib.load(f)


def parse_csv_list(value: str) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


def env_for_source_mode(source_mode: str) -> dict[str, str]:
    return {"SOURCE_SELECTION_MODE": source_mode}


def positive_int(value: str) -> int:
    iv = int(value)
    if iv <= 0:
        raise argparse.ArgumentTypeError("must be > 0")
    return iv
