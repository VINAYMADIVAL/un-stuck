import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable


def run(script, *args, env=None):
    e = dict(os.environ, **(env or {}))
    return subprocess.run([PY, str(ROOT / "scripts" / script), *args], capture_output=True, text=True, env=e)


class FleetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = {"HERMES_PROFILES_DIR": self.tmp.name}
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_validate_passes(self):
        self.assertEqual(run("validate.py").returncode, 0)

    def test_install_composes_inherited_soul(self):
        r = run("install.py", env=self.env)
        self.assertEqual(r.returncode, 0, r.stderr)
        soul = (self.root / "unstuck-whatsapp" / "SOUL.md").read_text()
        self.assertIn("BASE:BEGIN", soul)
        self.assertIn("Never ask for", soul)
        self.assertIn("Unstuck for WhatsApp", soul)
        self.assertNotIn("PART B", soul)  # central-only duties are not inherited
        self.assertTrue((self.root / "unstuck-telegram" / "skills" / "telegram-support" / "SKILL.md").exists())

    def test_install_never_overwrites_memory_or_agent_skills(self):
        run("install.py", env=self.env)
        mem = self.root / "unstuck-discord" / "memories" / "MEMORY.md"
        mem.write_text(mem.read_text() + "- [2026-10-18] dc-2fa | any | clock fix | confidence: med\n")
        skill = self.root / "unstuck-discord" / "skills" / "discord-support" / "SKILL.md"
        skill.write_text(skill.read_text() + "\n- agent edit\n")
        run("install.py", env=self.env)
        self.assertIn("clock fix", mem.read_text())
        self.assertIn("agent edit", skill.read_text())

    def test_drift_detected(self):
        run("install.py", env=self.env)
        soul = self.root / "unstuck-telegram" / "SOUL.md"
        soul.write_text(soul.read_text().replace("Never ask for", "Feel free to ask for"))
        r = run("fleet_health.py", "--json", env=self.env)
        data = json.loads(r.stdout)
        row = next(a for a in data["agents"] if a["agent"] == "telegram")
        self.assertEqual(row["soul"], "drift")

    def test_missing_profile_fails(self):
        r = run("fleet_health.py", env=self.env)
        self.assertEqual(r.returncode, 1)
        self.assertIn("FAIL", r.stdout)

    def test_audit_finds_sensitive_without_printing_it(self):
        run("install.py", env=self.env)
        mem = self.root / "unstuck-whatsapp" / "memories" / "MEMORY.md"
        mem.write_text(mem.read_text() + "- user said pin: 482913 and email a.b@example.com\n")
        r = run("memory_audit.py", env=self.env)
        self.assertEqual(r.returncode, 1)
        self.assertIn("SENSITIVE: pin-or-otp", r.stdout)
        self.assertNotIn("482913", r.stdout)
        self.assertNotIn("a.b@example.com", r.stdout)
        run("memory_audit.py", "--redact", env=self.env)
        self.assertNotIn("482913", mem.read_text())
        self.assertTrue(mem.with_suffix(".md.bak").exists())

    def test_audit_flags_shared_memory(self):
        run("install.py", env=self.env)
        a = self.root / "unstuck-whatsapp" / "memories" / "MEMORY.md"
        b = self.root / "unstuck-telegram" / "memories" / "MEMORY.md"
        a.write_text(a.read_text() + "- [2026-10-18] x | any | same lesson | confidence: low\n")
        b.unlink()
        b.symlink_to(a)
        r = run("memory_audit.py", env=self.env)
        self.assertIn("ISOLATION", r.stdout)

    def test_clean_audit_passes(self):
        run("install.py", env=self.env)
        self.assertEqual(run("memory_audit.py", env=self.env).returncode, 0)

    def test_offline_evals_pass(self):
        self.assertEqual(run("run_evals.py").returncode, 0)


if __name__ == "__main__":
    unittest.main()
