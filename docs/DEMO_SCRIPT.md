# 3-minute demo video script

Record on a laptop plus a phone screen. Keep each beat short.

1. **The problem (20s).** "Ever lost ten minutes finding one setting? My mom couldn't set a PIN on WhatsApp."
2. **WhatsApp agent (45s).** On WhatsApp: "How do I set a PIN?" The agent asks Android or iPhone, then gives one step at a time with exact labels, confirms each, and cites the official page. Show it never asks for the PIN.
3. **Safety (25s).** Message: "A man on the phone asked for the code I just got." The agent warns it is a scam pattern and does not proceed.
4. **Same brain, different platforms (30s).** Ask Telegram "how do I add a password so nobody steals my account?" and Discord "turn on 2FA". Same loop, same tone, different expertise.
5. **Central agent (40s).** In the terminal run `make health`: all agents, soul-sync ok, gateway up, memory sizes. Edit the base SOUL (one line), run `make health` to show `drift`, run `make install`, show `ok`. Then `make audit`: memories private, no sensitive data.
6. **Learning and quality (15s).** Show `make check` (18/18) and a `[STALE?]` lesson in an agent's memory.
7. **Extend (10s).** `make new-agent P=slack` creates a new platform agent skeleton.
8. **Close (5s).** "Unstuck: ten minutes back, for everyone."

Before recording: run `make audit`, verify every task you plan to show against the official help page, and set `last_verified`.
