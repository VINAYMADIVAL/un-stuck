#!/usr/bin/env python3
"""Memory governance for the central agent.

Checks every agent's memories/ for: isolation (no shared/symlinked memory), size/bloat, [STALE?] tags,
and sensitive data (PIN/OTP-like codes, phone numbers, emails, tokens, passwords).
Findings never print the secret: only type, file and line number.
--redact replaces matches with [REDACTED:<type>] after writing a .bak backup (needs the operator's approval).
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MEMORY_WARN_BYTES, agent_dirs, central_profile_name, load_agent, profiles_dir, sha  # noqa: E402

PATTERNS = {
    "pin-or-otp": re.compile(r"(?i)\b(pin|otp|passcode|verification code|login code|code)\b[^\n\d]{0,20}\b\d{4,8}\b"),
    "phone-number": re.compile(r"(?<!\w)\+?\d[\d\s\-()]{8,14}\d(?!\w)"),
    "email": re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"),
    "secret-assignment": re.compile(r"(?i)\b(api[_-]?key|token|secret|password|passwd)\b\s*[:=]\s*\S+"),
    "api-key": re.compile(r"\b(sk|pk|ghp|xox[bp])[-_][A-Za-z0-9\-_]{16,}\b"),
    "discord-token": re.compile(r"\b[A-Za-z0-9_\-]{23,28}\.[A-Za-z0-9_\-]{6,7}\.[A-Za-z0-9_\-]{27,}\b"),
}


def memory_files(pdir: Path) -> list[Path]:
    m = pdir / "memories"
    return sorted(m.glob("*.md")) if m.exists() else []


def scan_file(path: Path) -> list[tuple[str, int]]:
    hits = []
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        if line.lstrip().startswith("#") and "Format:" in line:
            continue  # the seed header contains an example format line
        for kind, rx in PATTERNS.items():
            if rx.search(line):
                hits.append((kind, i))
    return hits


def redact(path: Path) -> int:
    shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
    text, n = path.read_text(encoding="utf-8"), 0
    for kind, rx in PATTERNS.items():
        text, c = rx.subn(f"[REDACTED:{kind}]", text)
        n += c
    path.write_text(text, encoding="utf-8")
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--redact", action="store_true", help="redact findings in place (backup .bak is written)")
    args = ap.parse_args()

    root = profiles_dir()
    profiles = {"central": central_profile_name()}
    profiles.update({a.name: load_agent(a)["profile"] for a in agent_dirs()})

    problems = 0
    seen_hash: dict[str, str] = {}
    seen_inode: dict[tuple, str] = {}
    for key, prof in profiles.items():
        pdir = root / prof
        files = memory_files(pdir)
        print(f"[{key}] {pdir / 'memories'}  ({len(files)} file(s))")
        if not files:
            print("  no memory files yet")
        for f in files:
            if f.is_symlink():
                print(f"  ISOLATION: {f.name} is a symlink -> {f.resolve()}")
                problems += 1
            st = f.stat()
            ino = (st.st_dev, st.st_ino)
            if ino in seen_inode and seen_inode[ino] != key:
                print(f"  ISOLATION: {f.name} is the same file as {seen_inode[ino]}'s memory")
                problems += 1
            seen_inode[ino] = key
            body = f.read_text(encoding="utf-8", errors="ignore")
            lessons = [l for l in body.splitlines() if l.startswith("- [")]
            if lessons:
                h = sha(body)
                if h in seen_hash and seen_hash[h] != key:
                    print(f"  ISOLATION: {f.name} has identical content to {seen_hash[h]}'s memory (copied/shared?)")
                    problems += 1
                seen_hash[h] = key
            if st.st_size > MEMORY_WARN_BYTES:
                print(f"  SIZE: {f.name} is {st.st_size // 1024} KB (>{MEMORY_WARN_BYTES // 1024} KB), prune or merge duplicates")
                problems += 1
            dupes = len(lessons) - len(set(lessons))
            if dupes:
                print(f"  DUPLICATES: {dupes} repeated lesson line(s) in {f.name}")
                problems += 1
            stale = body.count("[STALE?]")
            if stale:
                print(f"  STALE: {stale} [STALE?] tag(s) in {f.name}: re-verify related tasks")
            for kind, line in scan_file(f):
                print(f"  SENSITIVE: {kind} at {f.name}:{line} (value hidden)")
                problems += 1
            if args.redact:
                n = redact(f)
                print(f"  REDACTED {n} match(es) in {f.name}; backup: {f.name}.bak")
    print(f"\nAudit complete: {problems} issue(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
