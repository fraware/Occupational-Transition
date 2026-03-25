"""
Regenerate intermediate/audit/02_provenance_reconciliation.csv and
intermediate/audit/02_provenance_reconciliation_summary.json by comparing
each intermediate/*run_metadata.json source_files_sha256 entry to local files.

Usage (repo root):
    python scripts/rebuild_audit_provenance_tables.py
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTER = ROOT / "intermediate"
AUDIT = INTER / "audit"
OUT_CSV = AUDIT / "02_provenance_reconciliation.csv"
OUT_SUMMARY = AUDIT / "02_provenance_reconciliation_summary.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_local_path(p: str) -> Path | None:
    if not p or not str(p).strip():
        return None
    raw = Path(p)
    try:
        if raw.is_absolute():
            try:
                rel = raw.relative_to(ROOT)
                return ROOT / rel
            except ValueError:
                return raw if raw.is_file() else None
        cand = ROOT / raw
        return cand if cand.is_file() else None
    except OSError:
        return None


def iter_source_entries(meta: dict) -> list[dict]:
    raw = meta.get("source_files_sha256")
    if raw is None:
        return []
    if isinstance(raw, list):
        return [x for x in raw if isinstance(x, dict)]
    if isinstance(raw, dict):
        out: list[dict] = []
        for rel, h in raw.items():
            if not isinstance(rel, str) or not isinstance(h, str):
                continue
            out.append(
                {
                    "file_name": rel,
                    "local_cache_path": rel,
                    "url": "",
                    "sha256": h,
                }
            )
        return out
    return []


def main() -> int:
    AUDIT.mkdir(parents=True, exist_ok=True)

    meta_files = sorted(INTER.rglob("*run_metadata.json"))
    rows: list[list[str]] = []
    header = [
        "metadata_file",
        "url",
        "local_path",
        "recorded_sha256",
        "local_exists",
        "computed_sha256",
        "status",
    ]

    for mf in meta_files:
        rel_meta = mf.relative_to(ROOT).as_posix()
        try:
            meta = json.loads(mf.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            rows.append(
                [
                    rel_meta,
                    "",
                    "",
                    "",
                    "False",
                    "",
                    f"json_error:{e}",
                ]
            )
            continue

        for ent in iter_source_entries(meta):
            url = str(ent.get("url") or "")
            lp = ent.get("local_cache_path") or ent.get("path") or ent.get("file_name")
            lp_s = str(lp).strip() if lp is not None else ""
            recorded = str(ent.get("sha256") or "").strip()

            path_obj = normalize_local_path(lp_s) if lp_s else None
            exists = path_obj is not None and path_obj.is_file()
            computed = ""
            status = "no_local_path"

            if exists and path_obj is not None:
                computed = sha256_file(path_obj)
                if recorded and computed == recorded:
                    status = "match"
                elif recorded:
                    status = "mismatch"
                else:
                    status = "match" if not recorded else "mismatch"

            display_path = lp_s
            if exists and path_obj is not None:
                try:
                    display_path = path_obj.relative_to(ROOT).as_posix()
                except ValueError:
                    display_path = str(path_obj)

            rows.append(
                [
                    rel_meta,
                    url,
                    display_path,
                    recorded,
                    str(exists),
                    computed,
                    status,
                ]
            )

    counts = Counter(r[6] for r in rows)
    summary = {
        "captured_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status_counts": dict(sorted(counts.items())),
        "row_count": len(rows),
    }

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

    OUT_SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_CSV} ({len(rows)} rows)")
    print(f"Wrote {OUT_SUMMARY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
