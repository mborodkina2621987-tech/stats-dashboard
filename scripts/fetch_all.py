"""Iterate accounts.yml and run the matching per-platform fetch script.

Usage: python scripts/fetch_all.py
Environment: SCRAPECREATORS_API_KEY must be set.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
FETCH_DIR = REPO_ROOT / "scripts" / "fetch"


def load_accounts() -> list[dict]:
    with (REPO_ROOT / "accounts.yml").open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)["accounts"]


def main() -> int:
    failed: list[str] = []
    for acc in load_accounts():
        platform = acc["platform"]
        handle = acc["handle"]
        script = FETCH_DIR / f"fetch_{platform}.py"
        if not script.exists():
            print(f"skip {platform}/{handle}: no script")
            failed.append(f"{platform}/{handle}")
            continue
        print(f"→ {platform}/{handle}")
        result = subprocess.run(
            [sys.executable, str(script), handle],
            cwd=str(FETCH_DIR),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  FAIL: {result.stderr.strip()}")
            failed.append(f"{platform}/{handle}")
        else:
            print(f"  OK: {result.stdout.strip()}")
    if failed:
        print(f"\n{len(failed)} failures: {failed}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
