#!/usr/bin/env python3
"""Static checks for the repo itself (run in CI): structure, frontmatter, safety wording."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import BASE_BEGIN, BASE_END, CENTRAL_DIR, agent_dirs, extract_base, parse_frontmatter  # noqa: E402

BAD_PHRASES = re.compile(r"(?i)\b(tell|send|share|give|type|read out|enter)\b[^.\n]{0,15}\bme\b[^.\n]{0,20}\b(pin|otp|password|passcode|code)\b")
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)
    print(f"FAIL  {msg}")


def main() -> int:
    soul = (CENTRAL_DIR / "SOUL.md").read_text(encoding="utf-8")
    if soul.count(BASE_BEGIN) != 1 or soul.count(BASE_END) != 1 or extract_base(soul) is None:
        err("central/SOUL.md must contain exactly one BASE:BEGIN / BASE:END pair")
    for needle in ("Never ask for", "Scam check", "Your memory is private"):
        if needle not in (extract_base(soul) or ""):
            err(f"central SOUL base missing required rule: {needle}")
    for sk in sorted((CENTRAL_DIR / "skills").iterdir()):
        f = sk / "SKILL.md"
        fm = parse_frontmatter(f.read_text(encoding="utf-8")) if f.exists() else {}
        if fm.get("name") != sk.name or not fm.get("description"):
            err(f"central skill {sk.name}: frontmatter needs name == folder and a description")

    agents = agent_dirs()
    if len(agents) < 3:
        err("expected at least 3 agents (whatsapp, telegram, discord)")
    for a in agents:
        meta_file = a / "agent.json"
        if not meta_file.exists():
            err(f"{a.name}: agent.json missing")
            continue
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        for k in ("platform", "profile", "skill", "help_center"):
            if not meta.get(k):
                err(f"{a.name}: agent.json missing '{k}'")
        if not (a / "PERSONA.md").exists():
            err(f"{a.name}: PERSONA.md missing")
        if not (a / "memories" / "MEMORY.md").exists():
            err(f"{a.name}: memories/MEMORY.md seed missing")
        skill = a / "skills" / meta.get("skill", "?") / "SKILL.md"
        if not skill.exists():
            err(f"{a.name}: skill file {skill.relative_to(a)} missing")
            continue
        text = skill.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm.get("name") != meta["skill"]:
            err(f"{a.name}: skill frontmatter name must equal '{meta['skill']}'")
        for k in ("description", "version", "platform", "last_verified", "official_help"):
            if not fm.get(k):
                err(f"{a.name}: skill frontmatter missing '{k}'")
        tasks = re.findall(r"^## TASK: (\S+)", text, re.M)
        if len(tasks) < 3:
            err(f"{a.name}: needs at least 3 tasks, found {len(tasks)}")
        for i, block in enumerate(re.split(r"^## TASK: ", text, flags=re.M)[1:]):
            if "**Source:**" not in block and "**Safety:**" not in block:
                err(f"{a.name}: task {tasks[i]} has no **Source:** line")
            if "**Goal:**" not in block:
                err(f"{a.name}: task {tasks[i]} has no **Goal:** line")
        if "## Change log" not in text:
            err(f"{a.name}: skill needs a '## Change log' section")
        for m in BAD_PHRASES.finditer(text):
            err(f"{a.name}: skill appears to ask the user for a secret: '{m.group(0)}'")
    print(f"\n{len(errors)} problem(s)." if errors else "All static checks passed.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
