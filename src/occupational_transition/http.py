"""HTTP helpers for public data endpoints (BLS, Census BTOS, O*NET, etc.)."""

from __future__ import annotations

import hashlib
import os
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# Maximum retries for transient failures when using fetch_text_with_retry.
_DEFAULT_RETRIES = 3
_DEFAULT_BACKOFF_S = 1.0


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _request(
    url: str,
    user_agent: str | None = None,
    extra_headers: dict[str, str] | None = None,
) -> Request:
    ua = user_agent if user_agent is not None else DEFAULT_USER_AGENT
    headers: dict[str, str] = {"User-Agent": ua}
    if extra_headers:
        headers.update(extra_headers)
    return Request(url, headers=headers)


def fetch_text(
    url: str,
    *,
    timeout: float = 180.0,
    user_agent: str | None = None,
    extra_headers: dict[str, str] | None = None,
) -> str:
    with urlopen(_request(url, user_agent, extra_headers), timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def fetch_bytes(
    url: str,
    *,
    timeout: float = 300.0,
    user_agent: str | None = None,
    extra_headers: dict[str, str] | None = None,
) -> bytes:
    with urlopen(_request(url, user_agent, extra_headers), timeout=timeout) as resp:
        return resp.read()


def fetch_text_with_retry(
    url: str,
    *,
    timeout: float = 180.0,
    user_agent: str | None = None,
    extra_headers: dict[str, str] | None = None,
    retries: int = _DEFAULT_RETRIES,
    backoff_s: float = _DEFAULT_BACKOFF_S,
) -> str:
    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return fetch_text(
                url,
                timeout=timeout,
                user_agent=user_agent,
                extra_headers=extra_headers,
            )
        except (HTTPError, URLError, OSError, TimeoutError) as e:
            last = e
            if attempt < retries:
                time.sleep(backoff_s * (2**attempt))
    assert last is not None
    raise last


def fetch_bytes_with_retry(
    url: str,
    *,
    timeout: float = 300.0,
    user_agent: str | None = None,
    extra_headers: dict[str, str] | None = None,
    retries: int = _DEFAULT_RETRIES,
    backoff_s: float = _DEFAULT_BACKOFF_S,
) -> bytes:
    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return fetch_bytes(
                url,
                timeout=timeout,
                user_agent=user_agent,
                extra_headers=extra_headers,
            )
        except (HTTPError, URLError, OSError, TimeoutError) as e:
            last = e
            if attempt < retries:
                time.sleep(backoff_s * (2**attempt))
    assert last is not None
    raise last


def download_to_path(
    url: str,
    dest: Path,
    *,
    timeout: float = 300.0,
    user_agent: str | None = None,
    extra_headers: dict[str, str] | None = None,
    skip_if_exists_min_bytes: int | None = 10_000,
) -> Path:
    """
    Download URL to dest. If dest exists and is larger than skip_if_exists_min_bytes,
    skip the download (caller can pass 0 to always re-fetch).
    """
    dest = dest.resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)
    if (
        skip_if_exists_min_bytes is not None
        and dest.exists()
        and dest.stat().st_size >= skip_if_exists_min_bytes
    ):
        return dest
    data = fetch_bytes(
        url, timeout=timeout, user_agent=user_agent, extra_headers=extra_headers
    )
    dest.write_bytes(data)
    return dest


def raw_cache_root(env: dict[str, str] | None = None) -> Path:
    """Default root for large downloads: env OT_RAW_DIR or ./raw relative to cwd."""
    env = env if env is not None else os.environ
    raw = env.get("OT_RAW_DIR", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    return Path.cwd() / "raw"


def _url_cache_path(
    url: str,
    cache_dir: Path,
    *,
    default_suffix: str = ".txt",
) -> Path:
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix or default_suffix
    key = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return cache_dir / f"{key}{suffix}"


def fetch_text_cached(
    url: str,
    *,
    cache_dir: Path | None = None,
    timeout: float = 180.0,
    user_agent: str | None = None,
    extra_headers: dict[str, str] | None = None,
    retries: int = _DEFAULT_RETRIES,
    backoff_s: float = _DEFAULT_BACKOFF_S,
    skip_if_exists_min_bytes: int = 1,
) -> str:
    """
    Fetch and cache decoded text for a URL.

    Cache file stores the decoded/normalized UTF-8 text, which matches how the
    pipeline currently hashes by re-encoding the decoded string.
    """
    cache_dir = cache_dir if cache_dir is not None else raw_cache_root()
    cache_dir.mkdir(parents=True, exist_ok=True)

    cache_path = _url_cache_path(url, cache_dir, default_suffix=".json")
    if (
        skip_if_exists_min_bytes is not None
        and cache_path.exists()
        and cache_path.stat().st_size >= skip_if_exists_min_bytes
    ):
        return cache_path.read_text(encoding="utf-8", errors="replace")

    text = fetch_text_with_retry(
        url,
        timeout=timeout,
        user_agent=user_agent,
        extra_headers=extra_headers,
        retries=retries,
        backoff_s=backoff_s,
    )
    cache_path.write_text(text, encoding="utf-8")
    return text
