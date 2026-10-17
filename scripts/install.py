#!/usr/bin/env python3
"""Install the Unstuck fleet into Hermes profile directories.

- central profile gets the full central/SOUL.md plus central skills.
- each sub-agent gets: SOUL.md = inherited BASE block + its own PERSONA.md, its skills, and a seed MEMORY.md.
- Memory is NEVER overwritten. Existing agent-owned skills are NOT overwritten unless --force-skills (backup made).
"""
from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (CENTRAL_DIR, agent_dirs, central_profile_name, compose_subagent_soul,  # noqa: E402
                    load_agent, profiles_dir)


def write(path: Path, text: str, dry: bool, label: str) -> None:
    print(f"  {'[dry] ' if dry else ''}write {label}: {path}")
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def copy_skills(src: Path, dst: Path, dry: bool, force: bool) -> None:
    if not src.exists():
        return
    for skill in sorted(p for p in src.iterdir() if p.is_dir()):
        target = dst / skill.name
        new = (skill / "SKILL.md").read_text(encoding="utf-8")
        if (target / "SKILL.md").exists():
            old = (target / "SKILL.md").read_text(encoding="utf-8")
            if old == new:
                print(f"  skill {skill.name}: up to date")
                continue
            if not force:
                print(f"  skill {skill.name}: agent-owned copy differs -> kept (use --force-skills to overwrite)")
                continue
            backup = target / f"SKILL.md.bak-{int(time.time())}"
            print(f"  {'[dry] ' if dry else ''}backup -> {backup.name}")
            if not dry:
                shutil.copy2(target / "SKILL.md", backup)
        print(f"  {'[dry] ' if dry else ''}install skill {skill.name} -> {target}")
        if not dry:
            shutil.copytree(skill, target, dirs_exist_ok=True)


def seed_memory(src: Path, dst: Path, dry: bool) -> None:
    mem = dst / "memories" / "MEMORY.md"
    if mem.exists():
        print("  memory: exists -> untouched (memory is agent-owned)")
        return
    seed = src / "memories" / "MEMORY.md"
    if seed.exists():
        write(mem, seed.read_text(encoding="utf-8"), dry, "memory seed")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="show what would change, write nothing")
    ap.add_argument("--force-skills", action="store_true", help="overwrite agent-owned SKILL.md (backup is made)")
    ap.add_argument("--only", help="install only this agent key (e.g. whatsapp) or 'central'")
    args = ap.parse_args()

    root = profiles_dir()
    central_soul = (CENTRAL_DIR / "SOUL.md").read_text(encoding="utf-8")
    print(f"Profiles dir: {root}")

    if args.only in (None, "central"):
        name = central_profile_name()
        dst = root / name
        print(f"\n[central] profile '{name}'")
        write(dst / "SOUL.md", central_soul, args.dry_run, "SOUL.md")
        copy_skills(CENTRAL_DIR / "skills", dst / "skills", args.dry_run, args.force_skills)
        seed_memory(CENTRAL_DIR, dst, args.dry_run)

    for adir in agent_dirs():
        if args.only not in (None, adir.name):
            continue
        meta = load_agent(adir)
        dst = root / meta["profile"]
        print(f"\n[{adir.name}] profile '{meta['profile']}'")
        persona = (adir / "PERSONA.md").read_text(encoding="utf-8")
        write(dst / "SOUL.md", compose_subagent_soul(central_soul, persona, adir.name),
              args.dry_run, "SOUL.md (inherited base + persona)")
        copy_skills(adir / "skills", dst / "skills", args.dry_run, args.force_skills)
        seed_memory(adir, dst, args.dry_run)

    print("\nDone." + (" (dry run, nothing written)" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
