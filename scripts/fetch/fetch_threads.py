"""Threads profile + recent posts fetch via ScrapeCreators."""
from __future__ import annotations

import sys
from datetime import datetime, timezone

from _common import http_get, save_snapshot


PLATFORM = "threads"


def fetch(handle: str) -> dict:
    profile = http_get("/v1/threads/profile", {"handle": handle})
    posts = http_get("/v1/threads/user/posts", {"handle": handle, "amount": 20})
    return {
        "platform": PLATFORM,
        "handle": handle,
        "fetched_at": datetime.now(tz=timezone.utc).isoformat(),
        "profile": profile,
        "posts": posts,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: fetch_threads.py <handle>", file=sys.stderr)
        return 2
    handle = sys.argv[1].lstrip("@")
    payload = fetch(handle)
    path = save_snapshot(PLATFORM, handle, payload)
    print(f"saved {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
