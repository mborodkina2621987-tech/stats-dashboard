"""Shared helpers for fetch scripts."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
API_KEY_ENV = "SCRAPECREATORS_API_KEY"
BASE_URL = "https://api.scrapecreators.com"


def get_api_key() -> str:
    key = os.environ.get(API_KEY_ENV)
    if not key:
        raise RuntimeError(f"missing env var {API_KEY_ENV}")
    return key


def http_get(path: str, params: dict) -> dict:
    headers = {"x-api-key": get_api_key()}
    resp = requests.get(f"{BASE_URL}{path}", params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def save_snapshot(platform: str, handle: str, payload: dict) -> Path:
    stamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    out_dir = DATA_DIR / platform / handle
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{stamp}.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return out_path
