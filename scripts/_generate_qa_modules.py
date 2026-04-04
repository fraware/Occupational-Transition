"""Generate src/occupational_transition/qa/* from scripts/qa_*.py using repo_root()."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
DEST = REPO / "src" / "occupational_transition" / "qa"

PAIRS: list[tuple[str, str]] = [
    ("qa_figure2_panelA.py", "figure2_panelA_t003.py"),
    ("qa_figure2_panelB_counts.py", "figure2_panelB_counts_t004.py"),
    ("qa_figure2_panelB_probs.py", "figure2_panelB_probs_t005.py"),
    ("qa_figure3_panelB_btos_workforce_effects.py", "figure3_panelB_t007.py"),
    ("qa_figure4_panelB_ces_sector_index.py", "figure4_panelB_t009.py"),
    ("qa_figure5_capability_matrix.py", "figure5_capability_t010.py"),
    ("qa_figureA1_asec_welfare_by_ai_tercile.py", "figureA1_t011.py"),
    ("qa_figureA2_sipp_event_study.py", "figureA2_t012.py"),
    ("qa_figureA3_cps_supp_validation.py", "figureA3_t013.py"),
    ("qa_figureA4_abs_structural_adoption.py", "figureA4_t014.py"),
    ("qa_figureA5_ces_payroll_hours.py", "figureA5_t015.py"),
    ("qa_figureA6_bed_churn.py", "figureA6_t016.py"),
    ("qa_figureA7_qcew_state_benchmark.py", "figureA7_t017.py"),
    ("qa_figureA8_lehd_benchmark.py", "figureA8_t018.py"),
    ("qa_figureA9_acs_local_composition.py", "figureA9_t019.py"),
    ("qa_figureA10_nls_longrun.py", "figureA10_t020.py"),
    ("qa_occ22_sector_weights.py", "occ22_sector_weights_t021.py"),
    ("qa_btos_sector_ai_use_monthly.py", "btos_sector_ai_use_t022.py"),
    ("qa_awes_occ22_monthly.py", "awes_occ22_monthly_t023.py"),
    ("qa_sector6_stress_monthly.py", "sector6_stress_monthly_t024.py"),
    ("qa_cps_occ22_exit_risk_monthly.py", "cps_occ22_exit_risk_t025.py"),
    ("qa_alpi_occ22_monthly.py", "alpi_occ22_monthly_t026.py"),
]


def _extract_path_blocks(lines: list[str]) -> tuple[list[str], list[str]]:
    """Remove top-level assignments that use ``root`` (``CONST = root`` or ``CONST = (`` + root)."""
    kept: list[str] = []
    extracted: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"^[A-Z][A-Z0-9_]* = root ", line):
            block = [line]
            depth = line.count("(") - line.count(")")
            i += 1
            while i < len(lines) and depth > 0:
                block.append(lines[i])
                depth += lines[i].count("(") - lines[i].count(")")
                i += 1
            extracted.extend(block)
            continue
        if re.match(r"^[A-Z][A-Z0-9_]* = \(\s*$", line):
            block = [line]
            depth = line.count("(") - line.count(")")
            j = i + 1
            while j < len(lines) and depth > 0:
                block.append(lines[j])
                depth += lines[j].count("(") - lines[j].count(")")
                j += 1
            if any("root" in x for x in block):
                extracted.extend(block)
                i = j
                continue
            kept.extend(block)
            i = j
            continue
        kept.append(line)
        i += 1
    return kept, extracted


def _split_at_main(lines: list[str]) -> tuple[list[str], list[str]]:
    for idx, ln in enumerate(lines):
        if re.match(r"^def main\(\)", ln):
            return lines[:idx], lines[idx:]
    raise ValueError("def main() not found")


def _stderr_report_fn(name: str) -> str:
    return (
        f"\ndef {name}(errors: list[str]) -> int:\n"
        '    import sys\n\n'
        '    print("QA failures:", file=sys.stderr)\n'
        "    for e in errors:\n"
        '        print(f"  - {e}", file=sys.stderr)\n'
        "    return 1\n"
    )


def _post_t007(full: str) -> str:
    full = full.replace("def main() -> None:", "def main() -> int:", 1)
    full = full.replace(
        "    if not FIG_CSV.is_file():\n        raise SystemExit(f\"missing {FIG_CSV}\")",
        "    if not FIG_CSV.is_file():\n        errors.append(f\"missing {FIG_CSV}\")\n        return 1",
    )
    full = full.replace(
        "    if not META_JSON.is_file():\n        raise SystemExit(f\"missing {META_JSON}\")",
        "    if not META_JSON.is_file():\n        errors.append(f\"missing {META_JSON}\")\n        return 1",
    )
    full = full.replace(
        '    if errors:\n        raise SystemExit("QA failures:\\n- " + "\\n- ".join(errors))\n\n    print("QA OK: figure3_panelB_btos_workforce_effects.csv")',
        '    if errors:\n        return _qa_report_stderr(errors)\n\n    print("QA OK: figure3_panelB_btos_workforce_effects.csv")\n    return 0',
    )
    full = re.sub(
        r'\nif __name__ == "__main__":',
        _stderr_report_fn("_qa_report_stderr")
        + '\nif __name__ == "__main__":',
        full,
        count=1,
    )
    return full


def _post_t014(full: str) -> str:
    full = full.replace("def main() -> None:", "def main() -> int:", 1)
    full = full.replace(
        "    if not FIG_CSV.is_file():\n        raise SystemExit(f\"missing {FIG_CSV}\")",
        "    if not FIG_CSV.is_file():\n        return _qa_report_stderr([f\"missing {FIG_CSV}\"])",
    )
    full = full.replace(
        "    if not META_JSON.is_file():\n        raise SystemExit(f\"missing {META_JSON}\")",
        "    if not META_JSON.is_file():\n        return _qa_report_stderr([f\"missing {META_JSON}\"])",
    )
    full = full.replace(
        '    if errors:\n        raise SystemExit("QA failures:\\n- " + "\\n- ".join(errors))\n\n    print("QA OK: figureA4_abs_structural_adoption.csv")',
        '    if errors:\n        return _qa_report_stderr(errors)\n\n    print("QA OK: figureA4_abs_structural_adoption.csv")\n    return 0',
    )
    full = re.sub(
        r'\nif __name__ == "__main__":',
        _stderr_report_fn("_qa_report_stderr")
        + '\nif __name__ == "__main__":',
        full,
        count=1,
    )
    return full


def _post_t020(full: str) -> str:
    full = full.replace(
        "def fail(msg: str) -> None:\n"
        '    print(f"QA failure: {msg}", file=sys.stderr)\n'
        "    raise SystemExit(1)",
        "def _fail_a10(msg: str) -> int:\n"
        '    print(f"QA failure: {msg}", file=sys.stderr)\n'
        "    return 1",
    )
    full = re.sub(r"\bfail\(", "return _fail_a10(", full)
    full = full.replace("def main() -> None:", "def main() -> int:", 1)
    full = full.replace(
        '    print("QA OK: figureA10_nls_longrun.csv")\n\n\nif __name__',
        '    print("QA OK: figureA10_nls_longrun.csv")\n    return 0\n\n\nif __name__',
    )
    return full


POST: dict[str, Callable[[str], str]] = {
    "qa_figure3_panelB_btos_workforce_effects.py": _post_t007,
    "qa_figureA4_abs_structural_adoption.py": _post_t014,
    "qa_figureA10_nls_longrun.py": _post_t020,
}


def transform(raw: str, src: str) -> str:
    text = re.sub(
        r"^ROOT = Path\(__file__\)\.resolve\(\)\.parents\[1\]\s*\n",
        "",
        raw,
        flags=re.M,
    )
    text = text.replace("ROOT", "root")
    text = text.replace(
        "from awes_alpi_common import",
        "from occupational_transition.awes_alpi_common import",
    )

    lines = text.splitlines(keepends=True)
    bare = [x.rstrip("\n") for x in lines]
    pre, post_lines = _split_at_main(bare)
    pre_kept, path_block = _extract_path_blocks(pre)
    prelude = "\n".join(pre_kept) + "\n"

    if "from occupational_transition.paths import repo_root" not in prelude:
        prelude = prelude.replace(
            "from __future__ import annotations",
            "from __future__ import annotations\n\n"
            "from occupational_transition.paths import repo_root",
            1,
        )

    post_s = "\n".join(post_lines) + "\n"
    indent = "    "
    inject = indent + "root = repo_root()\n"
    for pl in path_block:
        inject += indent + pl.strip() + "\n"

    m = re.search(r"(def main\(\)[^:]*:\n)", post_s)
    if not m:
        raise ValueError(f"no def main in {src}")
    insert_at = m.end()
    post_s = post_s[:insert_at] + inject + post_s[insert_at:]

    prelude = re.sub(
        r'^"""[^"]*"""',
        f'"""Ticket QA (from scripts/{src})."""',
        prelude,
        count=1,
        flags=re.M,
    )

    full = prelude + post_s
    hook = POST.get(src)
    if hook:
        full = hook(full)
    return full


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    for src, dst in PAIRS:
        raw = (SCRIPTS / src).read_text(encoding="utf-8")
        new = transform(raw, src)
        (DEST / dst).write_text(new, encoding="utf-8")
        print("wrote", dst)


if __name__ == "__main__":
    main()
