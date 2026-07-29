"""Telegram channel stats fetch via ScrapeCreators.

Note: For personal Telegram channels/bots ScrapeCreators offers limited coverage.
Not currently in the canonical account list — kept as scaffold for future use.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone

from _common import http_get, save_snapshot


PLATFORM = "telegram"


def fetch(handle: str) -> dict:
    channel = http_get("/v1/telegram/channel", {"handle": handle})
    return {
        "platform": PLATFORM,
        "handle": handle,
        "fetched_at": datetime.now(tz=timezone.utc).isoformat(),
        "profile": channel,
        "posts": {},
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: fetch_telegram.py <handle>", file=sys.stderr)
        return 2
    handle = sys.argv[1].lstrip("@")
    payload = fetch(handle)
    path = save_snapshot(PLATFORM, handle, payload)
    print(f"saved {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
