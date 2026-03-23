from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTER = ROOT / "intermediate"
MANIFEST = INTER / "visuals_run_manifest.json"


def _run(cmd: str) -> tuple[int, str]:
    p = subprocess.run(
        cmd,
        cwd=ROOT,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return p.returncode, p.stdout


def main() -> int:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log = INTER / f"visuals_acceptance_log_{ts}.md"
    lines: list[str] = []
    lines.append("# Visuals Acceptance Log")
    lines.append("")
    lines.append(
        f"- Started UTC: {dt.datetime.now(dt.timezone.utc).isoformat()}"
    )

    rc1, out1 = _run("python scripts/run_visuals_all.py")
    rc2, out2 = _run("python scripts/qa_visuals.py")
    lines.append(f"- run_visuals_all exit: `{rc1}`")
    lines.append(f"- qa_visuals exit: `{rc2}`")
    lines.append("")
    lines.append("## run_visuals_all output")
    lines.append("```text")
    lines.append(out1.rstrip() if out1.strip() else "(no output)")
    lines.append("```")
    lines.append("")
    lines.append("## qa_visuals output")
    lines.append("```text")
    lines.append(out2.rstrip() if out2.strip() else "(no output)")
    lines.append("```")
    lines.append("")

    if MANIFEST.is_file():
        obj = json.loads(MANIFEST.read_text(encoding="utf-8"))
        outputs = obj.get("outputs", [])
        lines.append(f"- Manifest: `{MANIFEST.relative_to(ROOT).as_posix()}`")
        lines.append(f"- Visual stems validated: `{len(outputs)}`")
        lines.append("")
        lines.append("| Stem | PNG bytes | PDF bytes |")
        lines.append("|---|---:|---:|")
        for o in outputs:
            lines.append(
                f"| {o['stem']} | {o['png_bytes']} | {o['pdf_bytes']} |"
            )
        lines.append("")

    lines.append(
        f"- Finished UTC: {dt.datetime.now(dt.timezone.utc).isoformat()}"
    )
    result = "PASS" if rc1 == 0 and rc2 == 0 else "FAIL"
    lines.append(f"- Result: `{result}`")
    log.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{result}. Log written: {log}")
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
