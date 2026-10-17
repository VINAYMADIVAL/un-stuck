#!/usr/bin/env python3
"""Fleet health check for the central agent: profiles, SOUL sync, skills, memory, gateway, host resources."""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (CENTRAL_DIR, MEMORY_WARN_BYTES, agent_dirs, central_profile_name, extract_base,  # noqa: E402
                    load_agent, parse_frontmatter, profiles_dir, sha)

SKILL_MAX_AGE_DAYS = 30


def gateway_state(profile: str) -> str:
    if shutil.which("hermes") is None:
        return "unknown"
    try:
        r = subprocess.run(["hermes", "-p", profile, "gateway", "status"], capture_output=True, text=True, timeout=8)
    except (subprocess.TimeoutExpired, OSError):
        return "unknown"
    out = (r.stdout + r.stderr).lower()
    if re.search(r"not running|inactive|stopped|not installed|dead", out):
        return "down"
    if r.returncode == 0 and re.search(r"running|active|up", out):
        return "up"
    return "unknown"


def skill_info(skills_dir: Path) -> dict:
    """Count skills; flag invalid frontmatter; report the staleest verification age (9999 = never verified)."""
    count, invalid, worst = 0, [], None
    if skills_dir.exists():
        for s in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            f = s / "SKILL.md"
            if not f.exists():
                continue
            count += 1
            fm = parse_frontmatter(f.read_text(encoding="utf-8"))
            if not fm.get("name") or not fm.get("description"):
                invalid.append(s.name)
            try:
                age = (date.today() - datetime.strptime(fm.get("last_verified", ""), "%Y-%m-%d").date()).days
            except ValueError:
                age = 9999 if fm.get("platform") else None  # platform skills with no real date are unverified
            if age is not None:
                worst = age if worst is None else max(worst, age)
    return {"count": count, "invalid": invalid, "oldest_verified_days": worst}


def memory_info(mem_dir: Path) -> dict:
    size, stale, mtime = 0, 0, None
    if mem_dir.exists():
        for f in mem_dir.glob("*.md"):
            size += f.stat().st_size
            stale += f.read_text(encoding="utf-8", errors="ignore").count("[STALE?]")
            m = f.stat().st_mtime
            mtime = m if mtime is None else max(mtime, m)
    return {"bytes": size, "stale": stale, "last_modified": datetime.fromtimestamp(mtime).isoformat(timespec="minutes") if mtime else None}


def host_info() -> dict:
    cores = os.cpu_count() or 1
    load = os.getloadavg()[0] if hasattr(os, "getloadavg") else 0.0
    mem_pct = None
    try:
        mi = {l.split(":")[0]: int(l.split()[1]) for l in Path("/proc/meminfo").read_text().splitlines()}
        mem_pct = round(100 * (1 - mi["MemAvailable"] / mi["MemTotal"]))
    except (OSError, KeyError, ValueError):
        pass
    du = shutil.disk_usage(Path.home())
    return {"load": round(load, 2), "cores": cores, "mem_pct": mem_pct, "disk_pct": round(100 * du.used / du.total)}


def check_agent(key: str, profile: str, expect_base: str, root: Path, is_central: bool) -> dict:
    pdir = root / profile
    row = {"agent": key, "profile": profile, "status": "OK", "notes": []}
    if not pdir.exists():
        row.update(status="FAIL", soul="missing", skills=None, memory=None, gateway="n/a")
        row["notes"].append("profile directory not found (run `make install`)")
        return row
    soul = pdir / "SOUL.md"
    if not soul.exists():
        row["soul"] = "missing"
        row["status"] = "FAIL"
        row["notes"].append("SOUL.md missing")
    else:
        got = extract_base(soul.read_text(encoding="utf-8"))
        row["soul"] = "ok" if got is not None and sha(got) == sha(expect_base) else "drift"
        if row["soul"] == "drift":
            row["notes"].append("inherited BASE differs from central/SOUL.md (run `make install`)")
    row["skills"] = skill_info(pdir / "skills")
    row["memory"] = memory_info(pdir / "memories")
    row["gateway"] = gateway_state(profile)
    if row["skills"]["count"] == 0:
        row["notes"].append("no skills installed")
    if row["skills"]["invalid"]:
        row["notes"].append(f"invalid skill frontmatter: {', '.join(row['skills']['invalid'])}")
    age = row["skills"]["oldest_verified_days"]
    if age is not None and age > SKILL_MAX_AGE_DAYS and not is_central:
        row["notes"].append("skill not verified in 30+ days (or still DRAFT)")
    if row["memory"]["bytes"] > MEMORY_WARN_BYTES:
        row["notes"].append("memory file is large; consider pruning")
    if row["memory"]["stale"]:
        row["notes"].append(f"{row['memory']['stale']} [STALE?] lesson(s): re-verify the related task")
    if row["gateway"] == "down":
        row["notes"].append("gateway is down")
    if row["status"] != "FAIL" and row["notes"]:
        row["status"] = "WARN"
    return row


def render_text(rows: list[dict], host: dict) -> str:
    lines = [f"FLEET STATUS  {datetime.now().isoformat(timespec='seconds')}"]
    for r in rows:
        mem = f"{(r['memory'] or {}).get('bytes', 0) / 1024:.1f} KB" if r.get("memory") else "-"
        stale = (r.get("memory") or {}).get("stale", 0)
        lines.append(f"{r['agent']:<10} {r['status']:<5} gateway: {r.get('gateway', '-'):<8} soul-sync: {r.get('soul', '-'):<7} memory: {mem:<8} stale: {stale}")
        for n in r["notes"]:
            lines.append(f"           - {n}")
    mem = f"{host['mem_pct']}%" if host["mem_pct"] is not None else "n/a"
    lines.append(f"HOST       load {host['load']}/{host['cores']}  mem {mem}  disk {host['disk_pct']}%")
    warns = []
    if host["load"] > 0.8 * host["cores"]:
        warns.append("CPU load high")
    if host["mem_pct"] is not None and host["mem_pct"] > 85:
        warns.append("memory above 85%")
    if host["disk_pct"] > 90:
        warns.append("disk above 90%")
    if warns:
        lines.append("HOST WARN  " + ", ".join(warns))
    return "\n".join(lines)


def render_html(rows: list[dict], host: dict) -> str:
    color = {"OK": "#1a7f37", "WARN": "#9a6700", "FAIL": "#cf222e"}
    trs = ""
    for r in rows:
        mem = f"{(r['memory'] or {}).get('bytes', 0) / 1024:.1f} KB" if r.get("memory") else "-"
        notes = "<br>".join(html.escape(n) for n in r["notes"]) or "-"
        trs += (f"<tr><td>{html.escape(r['agent'])}</td><td style='color:{color[r['status']]};font-weight:700'>{r['status']}</td>"
                f"<td>{r.get('gateway','-')}</td><td>{r.get('soul','-')}</td><td>{mem}</td>"
                f"<td>{(r.get('memory') or {}).get('stale',0)}</td><td>{notes}</td></tr>")
    return f"""<!doctype html><meta charset=utf-8><title>Unstuck fleet</title>
<style>body{{font:15px system-ui;margin:2rem;max-width:960px}}table{{border-collapse:collapse;width:100%}}
td,th{{border:1px solid #d0d7de;padding:.5rem;text-align:left;vertical-align:top}}th{{background:#f6f8fa}}</style>
<h1>Unstuck fleet status</h1><p>{datetime.now().isoformat(timespec='seconds')} &middot; host load {host['load']}/{host['cores']},
mem {host['mem_pct']}%, disk {host['disk_pct']}%</p>
<table><tr><th>Agent</th><th>Status</th><th>Gateway</th><th>SOUL sync</th><th>Memory</th><th>Stale</th><th>Notes</th></tr>{trs}</table>"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    ap.add_argument("--html", metavar="FILE", help="also write a static HTML dashboard")
    args = ap.parse_args()

    root = profiles_dir()
    expect = extract_base((CENTRAL_DIR / "SOUL.md").read_text(encoding="utf-8"))
    rows = [check_agent("central", central_profile_name(), expect, root, True)]
    # central keeps the full SOUL, so compare base block (works the same way)
    for adir in agent_dirs():
        meta = load_agent(adir)
        rows.append(check_agent(adir.name, meta["profile"], expect, root, False))
    host = host_info()

    status_dir = Path(__file__).resolve().parent.parent / "status"
    status_dir.mkdir(exist_ok=True)
    (status_dir / "health.json").write_text(json.dumps({"time": time.time(), "agents": rows, "host": host}, indent=2))
    if args.html:
        Path(args.html).write_text(render_html(rows, host), encoding="utf-8")
    print(json.dumps({"agents": rows, "host": host}, indent=2) if args.json else render_text(rows, host))
    return 1 if any(r["status"] == "FAIL" for r in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
