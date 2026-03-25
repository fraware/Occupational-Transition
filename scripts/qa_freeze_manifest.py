from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "intermediate" / "freeze_manifest.json"


def main() -> int:
    if not MAN.is_file():
        print(f"FAIL: missing {MAN}", file=sys.stderr)
        return 1
    payload = json.loads(MAN.read_text(encoding="utf-8"))
    required = {"generated_utc", "figures", "intermediate_run_metadata"}
    if not required.issubset(set(payload.keys())):
        print("FAIL: freeze manifest missing required top-level keys", file=sys.stderr)
        return 1
    if not isinstance(payload.get("figures"), dict) or not payload["figures"]:
        print("FAIL: figures section empty in freeze manifest", file=sys.stderr)
        return 1
    if not isinstance(payload.get("intermediate_run_metadata"), dict):
        print("FAIL: metadata section invalid in freeze manifest", file=sys.stderr)
        return 1
    print("QA OK: freeze_manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
