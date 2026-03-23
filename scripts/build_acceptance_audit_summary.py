"""
Build a short audit-summary table from a strict acceptance log.

Usage:
    python scripts/build_acceptance_audit_summary.py \
      --log intermediate/full_clean_rebuild_acceptance_YYYYMMDDTHHMMSSZ.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_log(log_text: str) -> list[dict[str, str]]:
    lines = log_text.splitlines()
    out: list[dict[str, str]] = []
    cur: dict[str, str] | None = None
    in_build_block = False
    build_block_lines: list[str] = []

    for line in lines:
        m_ticket = re.match(r"## (PR-000|T-\d{3})$", line.strip())
        if m_ticket:
            if cur is not None:
                out.append(cur)
            cur = {
                "ticket": m_ticket.group(1),
                "duration_seconds": "",
                "row_counts": "n/a",
                "result": "",
            }
            in_build_block = False
            build_block_lines = []
            continue

        if cur is None:
            continue

        if line.strip() == "### Build Output":
            in_build_block = False
            build_block_lines = []
            continue

        if line.strip() == "```text":
            in_build_block = not in_build_block
            if not in_build_block and build_block_lines:
                txt = " ".join(build_block_lines)
                matches = re.findall(r"\((\d+)\s+rows\)", txt)
                if matches:
                    if len(matches) == 1:
                        cur["row_counts"] = matches[0]
                    else:
                        cur["row_counts"] = ", ".join(matches)
                build_block_lines = []
            continue

        if in_build_block:
            build_block_lines.append(line.strip())
            continue

        m_elapsed = re.search(r"- Elapsed seconds: `([^`]+)`", line)
        if m_elapsed:
            cur["duration_seconds"] = m_elapsed.group(1)
            continue

        m_result = re.search(r"- Checkpoint result: `([^`]+)`", line)
        if m_result:
            cur["result"] = m_result.group(1)
            continue

    if cur is not None:
        out.append(cur)
    return out


def build_summary_md(rows: list[dict[str, str]], src_log: Path) -> str:
    md: list[str] = []
    md.append("# Acceptance Audit Summary")
    md.append("")
    md.append(f"- Source log: `{src_log.as_posix()}`")
    md.append("")
    md.append("| Ticket | Duration (s) | Row counts | Pass/Fail |")
    md.append("|---|---:|---:|---|")
    for r in rows:
        md.append(
            f"| {r['ticket']} | {r['duration_seconds'] or 'n/a'} | "
            f"{r['row_counts']} | {r['result'] or 'n/a'} |"
        )
    md.append("")
    return "\n".join(md)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True, help="Path to acceptance log")
    args = parser.parse_args()

    src_log = (ROOT / args.log).resolve() if not Path(args.log).is_absolute() else Path(args.log)
    if not src_log.exists():
        raise FileNotFoundError(f"log not found: {src_log}")

    log_text = src_log.read_text(encoding="utf-8")
    rows = parse_log(log_text)
    if not rows:
        raise RuntimeError("no ticket rows parsed from acceptance log")

    out_path = src_log.with_name(src_log.stem + "_audit_summary.md")
    out_path.write_text(build_summary_md(rows, src_log), encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
