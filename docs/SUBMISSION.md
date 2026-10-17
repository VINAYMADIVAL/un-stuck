# Submission cheat sheet (Hacktoberfest Hack Day Bengaluru, 18 Oct 2026)

- **Project:** Unstuck
- **Track:** Track 2, Best Open-Source AI Project
- **Primary problem statement:** O1, Autonomous Agent Swarms (supporting strengths: O2 adaptive memory, O3 verifiable answers via citations and evals)
- **Repo URL:** (paste after pushing)
- **Demo:** video (organizers said a live deployment is not required: reconfirm in the WhatsApp group, since the handbook lists a live URL)
- **Open-source AI used:** Hermes Agent (Nous Research, MIT) plus the open-weight or hosted model you configured. State exactly which model, honestly.
- **Sarvam:** if Sarvam models/APIs are really used (for example speech-to-text or translation), say exactly where. Ask a volunteer how Sarvam prizes work: the handbook lists Track 3 as its own track and says each team picks one primary track.

## One-paragraph pitch
Unstuck is a fleet of open-source AI support agents, one per messaging platform, that walk ordinary people through settings and
problems one safe step at a time. Every agent inherits the same problem-solving behavior and safety rules from a central agent,
while keeping its own platform skills and private memory. The central agent monitors health, prevents behavior drift,
and audits memory for isolation and sensitive data.

## Checklist
- [ ] Public repo pushed, CI green
- [ ] Verified each demo task against the official help center, `last_verified` updated
- [ ] `make check`, `make test`, `make audit` clean
- [ ] Demo video recorded; repo README has architecture and a GIF or link
- [ ] Submitted before 3:30 PM IST
