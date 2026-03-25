"""One-shot rewriter: update docs/ path strings after folder reorganization."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_REL = frozenset({"docs/meta/path_migration_map.json"})
TEXT_SUFFIXES = frozenset({".md", ".py", ".toml", ".txt", ".yaml", ".yml"})


def build_pairs() -> list[tuple[str, str]]:
    with open(ROOT / "docs/meta/path_migration_map.json", encoding="utf-8") as f:
        data = json.load(f)
    pairs: list[tuple[str, str]] = [(k, v) for k, v in data["moves"].items()]
    for old_dir, new_dir in data["directory_moves"].items():
        o = old_dir.rstrip("/") + "/"
        n = new_dir.rstrip("/") + "/"
        pairs.append((o, n))
    tickets = ROOT / "docs/methodology/tickets"
    if tickets.is_dir():
        for p in sorted(tickets.glob("t*.md")):
            pairs.append((f"docs/{p.name}", f"docs/methodology/tickets/{p.name}"))
    # Longest keys first to avoid partial replacements
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    out: list[tuple[str, str]] = []
    for o, n in pairs:
        out.append((o, n))
        if "/" in o:
            out.append((o.replace("/", "\\"), n.replace("/", "\\")))
    return out


def should_process(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel in SKIP_REL:
        return False
    if ".git" in path.parts:
        return False
    suf = path.suffix.lower()
    return suf in TEXT_SUFFIXES


def main() -> None:
    pairs = build_pairs()
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or not should_process(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")
        new_text = text
        for old, new in pairs:
            if old in new_text:
                new_text = new_text.replace(old, new)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            changed += 1
    print(f"Updated {changed} files.")


if __name__ == "__main__":
    main()
