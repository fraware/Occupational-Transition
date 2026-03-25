from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGNOFF = ROOT / "intermediate" / "release_signoff.json"

REQ = [
    "reviewer_name",
    "review_date_utc",
    "commit_hash",
    "scope_mode",
    "decision",
    "notes_sha256",
]


def main() -> int:
    if not SIGNOFF.is_file():
        print(f"FAIL: missing {SIGNOFF}", file=sys.stderr)
        return 1
    payload = json.loads(SIGNOFF.read_text(encoding="utf-8"))
    missing = [k for k in REQ if not payload.get(k)]
    if missing:
        print(f"FAIL: release signoff missing fields {missing}", file=sys.stderr)
        return 1
    if payload.get("decision") not in {"approved", "rejected"}:
        print("FAIL: decision must be approved/rejected", file=sys.stderr)
        return 1
    if payload.get("decision") != "approved":
        print("FAIL: release signoff decision is not approved", file=sys.stderr)
        return 1
    print("QA OK: release_signoff")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
