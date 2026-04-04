"""Load docs/data_registry.csv and fetch rows into raw/."""

from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Any, Iterable

from occupational_transition.http import (
    download_to_path,
    fetch_text_cached,
    raw_cache_root,
)
from occupational_transition.sources.jolts import ensure_jt_file


def data_registry_path(root: Path) -> Path:
    return root / "docs" / "data_registry.csv"


def load_data_registry(root: Path) -> list[dict[str, str]]:
    path = data_registry_path(root)
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _row_by_id(
    rows: Iterable[dict[str, str]],
    dataset_id: str,
) -> dict[str, str] | None:
    for r in rows:
        if (r.get("dataset_id") or "").strip() == dataset_id:
            return r
    return None


def _dest_for_http(row: dict[str, str], raw_dir: Path) -> Path:
    fn = (row.get("file_name") or "").strip()
    if fn:
        return raw_dir / fn
    url = (row.get("download_url") or "").strip()
    safe = "".join(c if c.isalnum() else "_" for c in url[:48])
    return raw_dir / f"download_{safe}.bin"


def fetch_dataset_row(
    row: dict[str, str],
    *,
    raw_dir: Path,
    force: bool = False,
) -> Path | list[Path] | None:
    """
    Fetch one registry row. Returns path(s) written, or None for no-op (reference).

    Raises ValueError if extractor is missing or download cannot proceed.
    """
    ext = (row.get("extractor") or "").strip()
    if ext == "":
        return None
    skip = None if force else 10_000

    if ext == "http_download":
        url = (row.get("download_url") or "").strip()
        if not url.startswith("https://"):
            raise ValueError(
                f"{row.get('dataset_id')}: http_download requires HTTPS download_url"
            )
        dest = _dest_for_http(row, raw_dir)
        download_to_path(
            url,
            dest,
            skip_if_exists_min_bytes=0 if force else skip,
            extra_headers=_extra_headers_for_url(url),
        )
        return dest

    if ext == "jolts_labstat_file":
        fn = (row.get("file_name") or "").strip()
        if not fn:
            raise ValueError(
                f"{row.get('dataset_id')}: jolts_labstat_file needs file_name"
            )
        return ensure_jt_file(
            fn,
            raw_dir=raw_dir,
            skip_if_exists_min_bytes=0 if force else skip,
        )

    if ext == "btos_api_json":
        url = (row.get("download_url") or "").strip()
        if not url.startswith("https://"):
            raise ValueError(f"{row.get('dataset_id')}: btos_api_json needs HTTPS URL")
        fetch_text_cached(
            url,
            cache_dir=raw_dir,
            skip_if_exists_min_bytes=0 if force else 1,
        )
        return raw_dir

    raise ValueError(f"Unknown extractor {ext!r} for {row.get('dataset_id')}")


def _extra_headers_for_url(url: str) -> dict[str, str] | None:
    if "download.bls.gov" in url:
        return {"Referer": "https://www.bls.gov/"}
    return None


def fetch_by_dataset_id(
    root: Path,
    dataset_id: str,
    *,
    raw_dir: Path | None = None,
    force: bool = False,
) -> Path | list[Path] | None:
    rows = load_data_registry(root)
    row = _row_by_id(rows, dataset_id)
    if row is None:
        raise KeyError(f"Unknown dataset_id: {dataset_id}")
    cache = raw_dir if raw_dir is not None else raw_cache_root()
    return fetch_dataset_row(row, raw_dir=cache, force=force)


def rows_matching(
    rows: list[dict[str, str]],
    *,
    program: str | None = None,
    cadence: str | None = None,
    fetchable_only: bool = True,
) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for r in rows:
        if fetchable_only and not (r.get("extractor") or "").strip():
            continue
        if program and (r.get("program") or "").strip() != program.strip():
            continue
        if cadence and (r.get("update_cadence") or "").strip() != cadence.strip():
            continue
        out.append(r)
    return out


def refresh_catalog_rows(
    rows: list[dict[str, str]],
    *,
    raw_dir: Path,
    force: bool = False,
    dry_run: bool = False,
) -> list[dict[str, Any]]:
    """Fetch each row; return log lines as dicts."""
    log: list[dict[str, Any]] = []
    for row in rows:
        did = row.get("dataset_id", "")
        if dry_run:
            log.append(
                {
                    "dataset_id": did,
                    "status": "dry_run",
                    "extractor": row.get("extractor"),
                }
            )
            continue
        try:
            res = fetch_dataset_row(row, raw_dir=raw_dir, force=force)
            log.append({"dataset_id": did, "status": "ok", "result": str(res)})
        except Exception as e:  # noqa: BLE001
            log.append({"dataset_id": did, "status": "error", "error": str(e)})
    return log


def source_selection_mode_from_environ() -> str:
    return (os.environ.get("SOURCE_SELECTION_MODE") or "latest_mode").strip()


def refresh_blocked_by_freeze(*, force_refresh_in_freeze: bool) -> bool:
    if force_refresh_in_freeze:
        return False
    return source_selection_mode_from_environ() == "freeze_mode"
