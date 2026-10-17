---
name: fleet-monitor
description: Check the health of all Unstuck platform agents (profile, gateway, SOUL sync, skills, memory size, host CPU/RAM/disk) and report a fleet status. Use when the operator asks for status, a health check, or resource usage.
version: 1.0.0
---

# Fleet Monitor Skill

## When to use
The operator asks "how are the agents?", "health check", "status", "is anything down?", or "resource usage".

## Procedure
1. From the repository root (`$UNSTUCK_HOME`, the folder containing `scripts/`), run:
   `python scripts/fleet_health.py`
   Add `--html status/dashboard.html` if the operator wants a shareable dashboard.
2. Read the output. Each agent has a status:
   - **OK**: all good.
   - **WARN**: works, but needs attention (drift, stale lessons, gateway down, unverified skill, bloated memory).
   - **FAIL**: profile or SOUL.md missing.
3. Report in the format from SOUL.md section B5. Keep it under 15 lines.
4. Recommend at most three actions, in priority order. Typical fixes:
   - `soul-sync: drift` -> `make install` (re-syncs base behavior; never touches memory).
   - `gateway: down` -> `hermes -p <profile> gateway start` (confirm with operator first).
   - skill unverified -> verify tasks against the official help center, then update `last_verified`.
5. Resource thresholds: load above 80% of cores, memory above 85%, disk above 90% -> flag as HOST WARN.

## Rules
- Read-only. Never restart, edit or delete anything without the operator's explicit OK.
- Do not read conversation history of sub-agents.
