#!/usr/bin/env python3
"""Evaluation harness.

--offline (default, no LLM needed): every case with a `task` must find that task block in the agent's SKILL.md and
  the block must contain all `must_include` keywords. Proves the knowledge pack covers the question set.
--cmd TEMPLATE (live): run a real agent. TEMPLATE uses {profile} and {question}, e.g.
  --cmd 'hermes -p {profile} chat -q {question}'   (adjust to your Hermes CLI; see `hermes --help`)
  The reply must contain all `must_include` keywords (case-insensitive) and match none of `must_not` regexes.
Writes evals/results.json and prints a table. Exit code 1 if any case fails.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, agent_dirs, load_agent  # noqa: E402


def task_block(skill_text: str, task_id: str) -> str | None:
    m = re.search(rf"^## TASK: {re.escape(task_id)}\b.*?(?=^## |\Z)", skill_text, re.S | re.M)
    return m.group(0) if m else None


def run_case_offline(case: dict, skill_text: str) -> tuple[bool, str]:
    if case.get("offline") is False:
        return True, "skipped (live-only safety case)"
    block = task_block(skill_text, case["task"])
    if block is None:
        return False, f"task {case['task']} not found in SKILL.md"
    missing = [k for k in case.get("must_include", []) if k.lower() not in block.lower()]
    return (not missing), ("ok" if not missing else f"missing keywords: {missing}")


def run_case_live(case: dict, profile: str, template: str) -> tuple[bool, str]:
    cmd = template.format(profile=shlex.quote(profile), question=shlex.quote(case["question"]))
    try:
        out = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120).stdout
    except subprocess.TimeoutExpired:
        return False, "timeout"
    missing = [k for k in case.get("must_include", []) if k.lower() not in out.lower()]
    bad = [p for p in case.get("must_not", []) if re.search(p, out)]
    if missing or bad:
        return False, f"missing={missing} forbidden={bad}"
    return True, "ok"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cmd", help="live mode command template with {profile} and {question}")
    ap.add_argument("--offline", action="store_true", help="knowledge-coverage check (default if --cmd absent)")
    args = ap.parse_args()
    live = bool(args.cmd)

    results, failures, total = [], 0, 0
    print(f"{'mode: live' if live else 'mode: offline (knowledge coverage)'}\n")
    for adir in agent_dirs():
        meta = load_agent(adir)
        cases_file = ROOT / "evals" / "cases" / f"{adir.name}.json"
        if not cases_file.exists():
            print(f"[{adir.name}] no eval cases (add evals/cases/{adir.name}.json)")
            continue
        skill_text = (adir / "skills" / meta["skill"] / "SKILL.md").read_text(encoding="utf-8")
        cases = json.loads(cases_file.read_text(encoding="utf-8"))["cases"]
        passed = 0
        for c in cases:
            ok, why = run_case_live(c, meta["profile"], args.cmd) if live else run_case_offline(c, skill_text)
            passed += ok
            total += 1
            failures += (not ok)
            results.append({"agent": adir.name, "case": c["id"], "pass": ok, "detail": why})
            print(f"  {'PASS' if ok else 'FAIL'}  {c['id']:<14} {why}")
        print(f"[{adir.name}] {passed}/{len(cases)} passed\n")
    (ROOT / "evals" / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"TOTAL: {total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
