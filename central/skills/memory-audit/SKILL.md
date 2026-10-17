---
name: memory-audit
description: Audit every platform agent's private memory for isolation, bloat, stale lessons and sensitive data (PIN/OTP-like codes, phone numbers, emails, tokens). Use when the operator asks about memory health, privacy, or before a demo.
version: 1.0.0
---

# Memory Audit Skill

## When to use
The operator asks about memory health or privacy, or before any public demo or recording.

## Procedure
1. From the repository root run: `python scripts/memory_audit.py`
2. Interpret findings (the script never prints secret values, only type, file and line):
   - **ISOLATION**: memory shared or copied between agents. This breaks the design (memory is private per agent). Report as critical.
   - **SENSITIVE**: personal or secret data in memory. Report as high priority; agents must not store user data.
   - **SIZE / DUPLICATES**: ask the owning agent to prune and merge (do not edit its memory yourself).
   - **STALE**: count of `[STALE?]` tags. Name the related platform and recommend re-verifying that task.
3. If there are SENSITIVE findings, propose redaction and wait for explicit approval, then run:
   `python scripts/memory_audit.py --redact` (writes a `.bak` backup next to each file).
4. Summarize: issues by severity, then a short action list.

## Rules
- Never display, quote or copy memory contents in your report.
- Never move or copy memory from one agent to another. Memory stays private per agent.
- Redaction and pruning require operator approval.
