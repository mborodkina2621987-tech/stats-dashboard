"""http_get retries transient ScrapeCreators errors (fetch-daily failed 22.11 on one 500).

Offline: requests.get and time.sleep are faked.
Run: python3 -m pytest tests/test_http_get_retry.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "fetch"))
import _common  # noqa: E402


class Resp:
    def __init__(self, status: int, body: dict | None = None) -> None:
        self.status_code = status
        self._body = body or {}

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error", response=self)

    def json(self) -> dict:
        return self._body


@pytest.fixture(autouse=True)
def no_sleep_key(monkeypatch) -> None:
    monkeypatch.setenv(_common.API_KEY_ENV, "test")
    monkeypatch.setattr(_common.time, "sleep", lambda s: None, raising=False)


def fake_get(monkeypatch, statuses: list[int]) -> list[int]:
    seen: list[int] = []

    def get(*a, **kw):
        code = statuses[len(seen)]
        seen.append(code)
        return Resp(code, {"ok": True})

    monkeypatch.setattr(_common.requests, "get", get)
    return seen


def test_one_500_then_ok_returns_data(monkeypatch) -> None:
    seen = fake_get(monkeypatch, [500, 200])
    assert _common.http_get("/x", {}) == {"ok": True}
    assert seen == [500, 200]


def test_persistent_500_raises_after_retries(monkeypatch) -> None:
    seen = fake_get(monkeypatch, [500] * 10)
    with pytest.raises(requests.HTTPError):
        _common.http_get("/x", {})
    assert len(seen) == len(_common.RETRY_DELAYS_S) + 1


def test_404_not_retried(monkeypatch) -> None:
    seen = fake_get(monkeypatch, [404, 200])
    with pytest.raises(requests.HTTPError):
        _common.http_get("/x", {})
    assert seen == [404]
