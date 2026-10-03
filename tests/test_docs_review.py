"""Documentation regression probes, not evidence of model effectiveness.

Only disposable profile homes are touched. Reuse the existing recipe fixture
so the tested commands are extracted from the README, not rewritten here.
"""
from pathlib import Path
import shutil
import subprocess
import unittest
import test_docs_examples as examples


ROOT = Path(__file__).resolve().parents[1]


class CopyCollisionReviewTests(unittest.TestCase):
    def setUp(self):
        self.fixture = examples.ManualInstallRecipeTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.destination = self.fixture.fake_home / "skills"
        existing = self.destination / "research" / "domain-playbooks"
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text(
            "---\nname: domain-playbooks\n---\nExisting private edits\n",
            encoding="utf-8",
        )
        (existing / "sentinel.txt").write_text("do not change", encoding="utf-8")
        self.before = self.snapshot()

    def snapshot(self):
        return {
            str(path.relative_to(self.destination)): path.read_bytes()
            for path in self.destination.rglob("*") if path.is_file()
        }

    def assert_collision_refused(self, command):
        result = self.fixture.run_recipe(command)
        self.assertNotEqual(result.returncode, 0, "A categorized installed skill must block copying")
        self.assertIn("Already exists:", result.stdout + result.stderr)
        self.assertEqual(self.before, self.snapshot(), "Preflight must stop before any skill is copied")
        self.assertEqual([path.name for path in self.destination.iterdir()], ["research"])

    @unittest.skipUnless(shutil.which("bash"), "Bash is not installed")
    def test_bash_refuses_categorized_installed_skill_before_any_copy(self):
        self.assert_collision_refused([
            shutil.which("bash"), "--noprofile", "--norc", "-c",
            self.fixture.recipe("bash", 'test -n "$HERMES_HOME"'),
        ])

    @unittest.skipUnless(shutil.which("powershell"), "PowerShell is not installed")
    def test_powershell_refuses_categorized_installed_skill_before_any_copy(self):
        self.assert_collision_refused([
            shutil.which("powershell"), "-NoProfile", "-NonInteractive", "-Command",
            '$ErrorActionPreference = "Stop"; ' + self.fixture.recipe("powershell", "Test-Path"),
        ])


class CheckoutPreflightReviewTests(unittest.TestCase):
    def setUp(self):
        self.fixture = examples.ManualInstallRecipeTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.checkout = self.fixture.fake_home.parent / "incomplete checkout"
        shutil.copytree(ROOT / "skills", self.checkout / "skills")
        # A late-listed missing file must stop the entire copy before any writes.
        (self.checkout / "skills/domain-playbooks/PROVENANCE.md").unlink()

    def assert_incomplete_checkout_refused(self, command):
        result = subprocess.run(
            command, cwd=self.checkout, env=self.fixture.environment,
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=45,
        )
        self.assertNotEqual(result.returncode, 0, "Incomplete skill copies must not be installed")
        self.assertIn("Missing source:", result.stdout + result.stderr)
        self.assertFalse((self.fixture.fake_home / "skills").exists())

    @unittest.skipUnless(shutil.which("bash"), "Bash is not installed")
    def test_bash_incomplete_checkout_stops_before_any_copy(self):
        self.assert_incomplete_checkout_refused([
            shutil.which("bash"), "--noprofile", "--norc", "-c",
            self.fixture.recipe("bash", 'test -n "$HERMES_HOME"'),
        ])

    @unittest.skipUnless(shutil.which("powershell"), "PowerShell is not installed")
    def test_powershell_incomplete_checkout_stops_before_any_copy(self):
        self.assert_incomplete_checkout_refused([
            shutil.which("powershell"), "-NoProfile", "-NonInteractive", "-Command",
            '$ErrorActionPreference = "Stop"; ' + self.fixture.recipe("powershell", "Test-Path"),
        ])


if __name__ == "__main__":
    unittest.main()
