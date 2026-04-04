"""Structured bundle description for docs and CLI (no PyYAML dependency)."""

from __future__ import annotations

from pathlib import Path

from occupational_transition.manifests import ANALYSIS_BUNDLES, FULL_REBUILD_STEPS


def _steps_by_ticket() -> dict[str, tuple[str, ...]]:
    return {s.ticket: s.outputs for s in FULL_REBUILD_STEPS}


def format_analysis_bundles_yaml() -> str:
    lines: list[str] = [
        "# Generated from occupational_transition.manifests",
        "# Regenerate: python scripts/build_bundle_manifest.py",
        "",
        "bundles:",
    ]
    by_t = _steps_by_ticket()
    for b in ANALYSIS_BUNDLES:
        lines.append(f"  - name: {b.name}")
        lines.append(f"    description: {b.description!r}")
        lines.append("    tickets:")
        for t in b.tickets:
            lines.append(f"      - id: {t}")
            outs = by_t.get(t, ())
            lines.append("        outputs:")
            for o in outs:
                lines.append(f"          - {o}")
    lines.append("")
    return "\n".join(lines)


def write_analysis_bundles_yaml(root: Path) -> Path:
    dest = root / "docs" / "meta" / "analysis_bundles.yaml"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(format_analysis_bundles_yaml(), encoding="utf-8")
    return dest
