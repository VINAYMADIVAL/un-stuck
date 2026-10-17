# Install guide (Hermes Desktop + CLI)

```mermaid
flowchart TD
  A[Install Hermes Agent<br/>Desktop first-run installer or CLI] --> B[Clone this repo]
  B --> C{Existing profile with all platforms<br/>e.g. gemma?}
  C -- yes --> C1[Keep it as a fallback.<br/>Do NOT reuse its bot tokens in new profiles<br/>unless you remove them from it first]
  C -- no --> D
  C1 --> D[Create 4 profiles<br/>Desktop: Agents tab, or CLI:<br/>hermes profile create unstuck-central<br/>... unstuck-whatsapp / telegram / discord]
  D --> E[Set model + API key in each profile<br/>Desktop: Models, or profile .env]
  E --> F[Configure ONE platform per worker<br/>hermes -p unstuck-telegram gateway setup<br/>same for whatsapp, discord]
  F --> G{Windows?}
  G -- yes --> G1[copy fleet.local.json.example to fleet.local.json<br/>set profiles_dir to AppData/Local/hermes/profiles]
  G -- no --> H
  G1 --> H[python scripts/install.py --dry-run<br/>then python scripts/install.py<br/>SOUL = base + persona, skills, memory seed]
  H --> I[Restart host gateway<br/>hermes -p default gateway restart<br/>or wait for its profile rescan]
  I --> J[Message each bot on its platform]
  J --> K[python scripts/fleet_health.py<br/>python scripts/memory_audit.py]
  K --> L[Verify tasks vs official help pages<br/>set last_verified, re-run install]
```

Notes
- `install.py` never creates Hermes profiles; create them first.
- One bot token belongs to one profile. The host gateway serves all profiles, so a duplicate token means two pollers.
- Do not enable `gateway.standalone` (Hermes marks it a temporary shim).
- Adding a platform: `python scripts/new_agent.py slack`, `hermes profile create unstuck-slack`,
  `hermes -p unstuck-slack gateway setup`, `python scripts/install.py --only slack`, restart the host gateway.
