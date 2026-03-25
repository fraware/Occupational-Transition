"""Fail if known pre-reorganization doc paths appear in source or docs (CI guard)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Substrings that should not appear outside the migration map file.
STALE_SUBSTRINGS = [
    "docs/api/README.md",
    "docs/replication.md",
    "docs/library_overview.md",
    "docs/figure_catalog.md",
    "docs/claim_audit.md",
    "docs/captions/",
    "docs/source_notes/",
    "docs/figure_memos/",
    "docs/paper_final.md",
    "docs/methods_data.md",
    "docs/evidence_snapshot.md",
    "docs/appendix_draft.md",
    "docs/appendix_outline.md",
    "docs/memo_visual_precision.md",
    "docs/visual_style_guide.md",
    "docs/reliability_framework.md",
    "docs/replication_checklist.md",
    "docs/acceptance_matrix.md",
    "docs/committed_outputs.md",
    "docs/release_process.md",
    "docs/git_history_hygiene.md",
    "docs/pr000_crosswalk_methodology.md",
    # Briefing pack moved under docs/policy/briefing/
    "docs/policy/senate_briefing_memo.md",
    "docs/policy/senate_briefing_evidence_baseline_va.md",
    "docs/policy/senate_briefing_lineage_va.md",
    "docs/policy/senate_briefing_script_va.md",
    "docs/policy/senate_briefing_qa_va.md",
    "docs/policy/senator_handout_1page_va.md",
    "docs/policy/senator_packet_order_va.md",
    "docs/policy/senator_cps_condensed_brief.md",
    "docs/policy/virginia_deep_dive.md",
]

# Ticket markdown at docs root (should live under methodology/tickets).
_TICKET_AT_ROOT = re.compile(r"docs/t\d{3}_[^)\s`'\"]+\.md")

SKIP_NAMES = {
    "path_migration_map.json",
    "check_stale_doc_paths.py",
    "rewrite_docs_paths.py",
}
TEXT_SUFFIXES = {".md", ".py", ".toml", ".txt", ".yaml", ".yml", ".csv"}


def main() -> int:
    bad: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.name in SKIP_NAMES:
            continue
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("docs/sphinx/_build/"):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if rel == "docs/meta/path_migration_map.json":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")
        for sub in STALE_SUBSTRINGS:
            if sub in text:
                bad.append(f"{rel}: contains stale substring {sub!r}")
        for m in _TICKET_AT_ROOT.finditer(text):
            if "docs/methodology/tickets/" in text[max(0, m.start() - 30) : m.start()]:
                continue
            bad.append(f"{rel}: stale ticket path pattern {m.group(0)!r}")
    if bad:
        print("Stale docs/ path references:\n", file=sys.stderr)
        for line in bad:
            print(line, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
