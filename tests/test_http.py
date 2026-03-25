from __future__ import annotations

from pathlib import Path

import occupational_transition.http as http


def test_fetch_text_cached_uses_cache(
    tmp_path: Path,
    monkeypatch,
) -> None:
    calls: list[str] = []

    def fake_fetch_text_with_retry(url: str, **_: object) -> str:
        calls.append(url)
        return '{"ok": true}'

    monkeypatch.setattr(
        http,
        "fetch_text_with_retry",
        fake_fetch_text_with_retry,
    )

    url = "https://example.com/periods"
    a = http.fetch_text_cached(url, cache_dir=tmp_path, retries=0)
    b = http.fetch_text_cached(url, cache_dir=tmp_path, retries=0)

    assert a == '{"ok": true}'
    assert b == '{"ok": true}'
    assert calls == [url]

