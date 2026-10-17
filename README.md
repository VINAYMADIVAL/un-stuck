# Unstuck

**Ten minutes back, for everyone.** Unstuck is a fleet of open-source AI support agents, one per messaging platform
(WhatsApp, Telegram, Discord, and easy to extend), that guide ordinary people through app settings and problems one safe step at a time,
for example "set a PIN on my WhatsApp". Built on [Hermes Agent](https://github.com/NousResearch/hermes-agent) for the
Hacktoberfest Hack Day Bengaluru 2026.

## How it works

```
            Operator
               |
        +--------------+       reports only (health, drift, memory audit)
        | Central agent| ------------------------------------------+
        | SOUL.md      |                                            |
        +--------------+                                            |
     inherits BASE behavior (install.py)                            |
      |            |             |                                  |
 +----v---+  +-----v----+  +-----v----+                             |
 |WhatsApp|  | Telegram |  | Discord  |   independent Hermes        |
 | agent  |  |  agent   |  |  agent   |   profiles: own SOUL,       |
 | SKILL  |  |  SKILL   |  |  SKILL   |   SKILL, MEMORY, token <--+
 | MEMORY |  |  MEMORY  |  |  MEMORY  |
 +--------+  +----------+  +----------+
```

- **Central agent** (`central/SOUL.md`): *PART A* is base behavior inherited by every agent (the Unstuck loop, safety rules, memory discipline).
  *PART B* is central-only duties: health checks, SOUL drift detection, memory governance, resource monitoring.
- **Sub-agents** (`agents/<platform>/`): independent workers with their own `SKILL.md` task pack, private `MEMORY.md`, and bot token (a Hermes profile each).
  Memory is **never shared**; base behavior is **always inherited**.
- Full design: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## What is code here, and what is Hermes?

Hermes provides the agent runtime, model access, memory tool, skills loader, and messaging gateways. This repo is everything that makes it a product:

| Layer | Files |
| --- | --- |
| Behavior and safety design | `central/SOUL.md` (base + central duties), per-agent `PERSONA.md` |
| Platform knowledge | `agents/*/skills/*/SKILL.md` (structured task packs with official sources) |
| Fleet tooling | `scripts/install.py`, `fleet_health.py`, `memory_audit.py`, `new_agent.py`, `validate.py` |
| Quality | `evals/` + `scripts/run_evals.py`, `tests/`, GitHub Actions CI |

## Quick start

Requires Python 3.9+ (standard library only) and Hermes Agent already installed.

```bash
# 1. If your Hermes profiles already exist under other names, map them:
cp fleet.local.json.example fleet.local.json     # then edit profile names (hermes profile list)

# 2. See what would change, then install (never overwrites memory)
make install-dry
make install

# 3. Check everything
make check          # static validation + offline evals
make test           # unit tests
make health         # fleet status (add: make dashboard)
make audit          # memory isolation + sensitive-data audit
```

Profiles must exist before `make install` (it writes into them but does not create them): `hermes profile create <name>`.
Newer Hermes runs one host gateway that serves all profiles, so after configuring a platform in a profile
(`hermes -p <profile> gateway setup`) just restart the host gateway: `hermes -p default gateway restart`.
Full walkthrough with a flowchart: [docs/INSTALL.md](docs/INSTALL.md).

No `make` on Windows? Run the scripts directly: `python scripts/install.py`, `python scripts/fleet_health.py`,
`python scripts/memory_audit.py`, `python scripts/validate.py`, `python scripts/run_evals.py`.

Live evals against running agents (adjust the command to your Hermes CLI):

```bash
make evals CMD='hermes -p {profile} chat -q {question}'
```

Add a platform in seconds: `make new-agent P=slack`, fill in the SKILL.md tasks, `make check && make install`.

## Safety by design

- Agents **never ask for** PINs, OTPs, passwords or backup codes, and warn when a user is being socially engineered.
- Agents refuse to help access accounts the user does not own.
- Agent memory holds platform knowledge only; the audit script scans for PIN/OTP-like codes, phone numbers, emails and tokens and can redact them (with backup).
- Every answer points to the platform's official help page.

## Honest status

- Task packs are **drafts** (`last_verified: DRAFT-verify-before-demo`). App menus change often: verify each task against the official help center and update `last_verified`. `make health` flags unverified or old packs.
- Hermes profiles are isolated and (at the time of writing) have no native agent-to-agent calls, so coordination here is through files and reports. That is deliberate: it keeps memory isolation real.
- The gateway column is best-effort (`hermes -p <profile> gateway status`); with a multiplexed host gateway it may show `unknown`.

## Roadmap

Slack and Instagram agents, screenshot understanding with a multimodal open model, multilingual and voice replies, per-task success-rate tracking from anonymous outcomes, auto-proposed skill diffs for stale tasks.

## License

MIT
