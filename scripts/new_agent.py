#!/usr/bin/env python3
"""Scaffold a new platform agent from agents/_template. Usage: python scripts/new_agent.py slack"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import AGENTS_DIR  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"[a-z][a-z0-9-]*", sys.argv[1]):
        print("usage: python scripts/new_agent.py <platform>   (lowercase, e.g. slack, instagram)")
        return 2
    platform = sys.argv[1]
    title = platform.replace("-", " ").title()
    prefix = platform[:2]
    dst = AGENTS_DIR / platform
    if dst.exists():
        print(f"agents/{platform} already exists")
        return 1
    shutil.copytree(AGENTS_DIR / "_template", dst)
    (dst / "skills" / "PLATFORM-support").rename(dst / "skills" / f"{platform}-support")
    for f in dst.rglob("*"):
        if f.is_file():
            t = f.read_text(encoding="utf-8")
            f.write_text(t.replace("PLATFORM_TITLE", title).replace("PLATFORM", platform).replace("PREFIX", prefix), encoding="utf-8")
    print(f"Created agents/{platform}. Next: edit its SKILL.md (real tasks + official help URL),")
    print(f"then: hermes profile create unstuck-{platform}  ->  hermes -p unstuck-{platform} gateway setup")
    print("      make check && make install  ->  hermes -p default gateway restart")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
