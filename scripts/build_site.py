"""Build stage for GH Pages.

1. Copy accounts.yml → docs/ (so client-side JS can fetch it).
2. Copy data/ → docs/data/ (Pages only serves files inside docs/).
3. Generate per-account HTML by cloning docs/account/_template.html.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / "docs"


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    if src.exists():
        shutil.copytree(src, dst)


def load_accounts() -> list[dict]:
    with (REPO_ROOT / "accounts.yml").open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)["accounts"]


def main() -> int:
    # 1. accounts.yml
    shutil.copy(REPO_ROOT / "accounts.yml", DOCS / "accounts.yml")

    # 2. data snapshots
    copy_tree(REPO_ROOT / "data", DOCS / "data")

    # 3. per-account pages
    template = DOCS / "account" / "_template.html"
    tpl_text = template.read_text(encoding="utf-8")
    for acc in load_accounts():
        out = DOCS / "account" / f"{acc['platform']}-{acc['handle']}.html"
        out.write_text(tpl_text, encoding="utf-8")

    print(f"built docs/ with {len(list((DOCS / 'account').glob('*.html')))} account pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
