# Architecture

```mermaid
flowchart TB
  OP[Operator / maintainer] --> C
  subgraph Control plane
    C[Central agent<br/>SOUL.md: PART A base + PART B duties<br/>skills: fleet-monitor, memory-audit]
  end
  C -. inherits base behavior (install.py) .-> W
  C -. inherits base behavior .-> T
  C -. inherits base behavior .-> D
  subgraph Workers - independent Hermes profiles
    W[WhatsApp agent<br/>own SOUL, SKILL, MEMORY, bot token]
    T[Telegram agent<br/>own SOUL, SKILL, MEMORY, bot token]
    D[Discord agent<br/>own SOUL, SKILL, MEMORY, bot token]
  end
  U1[WhatsApp user] --> W
  U2[Telegram user] --> T
  U3[Discord user] --> D
  C -- reads reports only --> H[fleet_health.py / memory_audit.py]
  H -- metadata, sizes, tags, drift --> W & T & D
```

## Design rules
1. **One platform, one agent.** Each worker is a separate Hermes profile (`<hermes home>/profiles/<name>/`) with its own
   `SOUL.md`, `skills/`, `memories/` and its own bot token. Recent Hermes versions run **one host gateway per machine**
   that serves every profile and routes each platform's messages to that profile's own agent. Because of this, a bot token
   must be configured in exactly one profile (two pollers on one token conflict). A bad lesson in one agent cannot
   affect another.
2. **Inherited behavior, private memory.** Every worker's SOUL.md is generated as
   `central BASE block + its own PERSONA.md`. So all agents solve problems the same way (the Unstuck loop, the safety
   rules) while knowing only their platform. Memory is never copied or shared.
3. **Agents own their skills and memory.** `install.py` never overwrites an agent's memory and, by default, never
   overwrites a skill the agent has refined.
4. **The central agent governs, it does not chat with end users.** It monitors health, detects SOUL drift, audits memory
   for isolation and sensitive data, and tracks skill freshness.
5. **Coordination is through files and reports, not agent-to-agent chat.** Hermes profiles are isolated by design and
   (at the time of writing) have no native agent-to-agent calls. That is a feature here: it keeps memory isolation honest.
   If you later want live bot-to-bot messaging, look at the Hermes Bot Mode plugin (verify its current status first).

## Data flow of one support conversation
1. User messages the platform's bot. 2. The worker runs CLARIFY, LOCATE (its SKILL.md), GUIDE, CONFIRM.
3. On failure it RECOVERS via the task's "If it doesn't work" branches. 4. On close it writes an anonymous lesson to its own
MEMORY.md; a lesson that fails twice is tagged `[STALE?]`. 5. The central agent's audit counts `[STALE?]` tags and
reports which tasks to re-verify.

## Scripts
| Script | Purpose |
| --- | --- |
| `install.py` | Compose and install SOUL/skills into Hermes profiles; seed memory; dry-run supported |
| `fleet_health.py` | Profile/gateway/SOUL-sync/skills/memory status plus host load, RAM, disk; JSON and HTML output |
| `memory_audit.py` | Isolation, bloat, stale tags, sensitive-data scan; optional redaction with backup |
| `validate.py` | Repo structure and safety-wording checks (CI) |
| `run_evals.py` | Offline knowledge-coverage evals and live evals against real agents |
| `new_agent.py` | Scaffold a new platform agent (e.g. Slack) in seconds |
