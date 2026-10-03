"""Offline documentation checks; these do not test agent behavior or efficacy."""
from pathlib import Path
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "using-lookup", "finding-existing-work", "evaluating-existing-work",
    "licensing-and-payback", "contributing-back", "domain-playbooks",
)


def text(relative):
    path = ROOT / relative
    return path.read_text(encoding="utf-8") if path.exists() else ""


class DocumentationConsistencyTests(unittest.TestCase):
    def test_removed_unsupported_claims(self):
        combined = text("README.md") + text("PRIOR-ART.md")
        for claim in (
            "it will write one, every time", "It fires right before",
            "Most runs touch two", "none cover the brief-format",
            "None addresses bias", "none of which have an equivalent",
            "The gap is real", "Runs on anything that reads",
        ):
            with self.subTest(claim=claim):
                self.assertNotIn(claim, combined)

    def test_installation_has_all_six_and_explicit_scope(self):
        readme = text("README.md")
        self.assertIn("Install all six", readme)
        for name in SKILLS:
            self.assertTrue((ROOT / "skills" / name / "SKILL.md").is_file())
            self.assertRegex(readme, rf"(?m)^\s*{name}\s*\\?$")
        self.assertIn("--agent claude-code", readme)
        self.assertIn("--global", readme)
        self.assertIn("project scope", readme)
        self.assertIn("LICENSE", readme)
        self.assertIn("PROVENANCE.md", readme)

    def test_hermes_profile_and_native_windows_paths(self):
        readme = text("README.md")
        for required in (
            "HERMES_HOME", "hermes profile", "%LOCALAPPDATA%\\hermes",
            "profiles/<name>/skills/", "profile home", "not tested",
        ):
            self.assertIn(required, readme)
        self.assertIn('test -n "$HERMES_HOME"', readme)
        self.assertIn("Test-Path", readme)

    def test_readme_describes_bounded_search_and_implementation_handback(self):
        readme = text("README.md").lower()
        for required in (
            "local", "adopt / extend / compose / build", "search scope",
            "research effort", "output length", "original request",
            "not found in the inspected sources", "not a hook",
        ):
            self.assertIn(required, readme)

    def test_prior_art_records_evidence_limits_and_overlapping_work(self):
        prior = text("PRIOR-ART.md")
        for required in (
            "2026-10-02", "2026-09-30", "primary", "historical",
            "Quick Mode", "Full Mode", "local", "exit", "bias",
            "unverified", "not exhaustive", "contribution",
        ):
            self.assertIn(required, prior)

    def test_worked_examples_have_evidence_and_unexecuted_status(self):
        for name in ("study-path.md", "creative-work.md"):
            example = text(f"docs/examples/{name}")
            with self.subTest(example=name):
                self.assertGreater(len(example.split()), 450)
                for heading in (
                    "## Constraints", "## Search scope", "## Examined options",
                    "## Lessons and failure modes", "## Comparison",
                    "## Bounded decision", "## Learning versus copying", "## Sources",
                ):
                    self.assertIn(heading, example)
                self.assertIn("Illustrative", example)
                self.assertIn("not executed", example)
                self.assertIn("2026-10-02", example)
                self.assertGreaterEqual(len(re.findall(r"https://", example)), 2)

    def test_domain_body_is_concise_and_references_are_on_demand(self):
        body = text("skills/domain-playbooks/SKILL.md")
        self.assertLessEqual(len(body.split()), 500)
        self.assertIn("Load only", body)
        for reference in ("software-and-infrastructure.md", "games.md", "study-and-learning.md", "creative-work.md"):
            self.assertIn(f"references/{reference}", body)
            self.assertTrue((ROOT / "skills/domain-playbooks/references" / reference).is_file())
        self.assertIn("learning", body.lower())
        self.assertIn("copying", body.lower())

    def test_local_markdown_links_and_fences(self):
        files = [ROOT / "README.md", ROOT / "PRIOR-ART.md", ROOT / "skills/domain-playbooks/SKILL.md"]
        files += list((ROOT / "docs/examples").glob("*.md"))
        files += list((ROOT / "skills/domain-playbooks/references").glob("*.md"))
        for path in files:
            content = path.read_text(encoding="utf-8")
            with self.subTest(path=str(path.relative_to(ROOT))):
                fences = re.findall(r"(?m)^```", content)
                self.assertEqual(len(fences) % 2, 0, "Unbalanced code fences")
                for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
                    if "://" in target or target.startswith(("#", "mailto:")):
                        continue
                    target = unquote(target.split("#", 1)[0])
                    self.assertTrue((path.parent / target).exists(), f"Broken local link: {target}")
                self.assertNotRegex(content, r"(?m)^\|\s*\|\s*\|\s*$", "Empty table headers")


class ManualInstallRecipeTests(unittest.TestCase):
    """Run the documented copy recipes only against disposable fake homes."""

    def setUp(self):
        scratch = os.environ.get("TMPDIR")
        if not scratch:
            if os.name == "nt":
                scratch = str(Path(os.environ["LOCALAPPDATA"]) / "hermes/cache/scratch")
            else:
                scratch = str(Path.home() / ".cache/look-before-build")
        Path(scratch).mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="docs-copy-probe-", dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.fake_home = Path(temporary.name) / "fake profile home"
        self.fake_home.mkdir()
        self.environment = os.environ.copy()
        self.environment["HERMES_HOME"] = self.fake_home.as_posix()
        self.environment["MSYS_NO_PATHCONV"] = "1"

    def recipe(self, language, marker):
        blocks = re.findall(rf"```{language}\n(.*?)\n```", text("README.md"), re.S)
        matches = [block for block in blocks if marker in block]
        self.assertEqual(len(matches), 1, "Must locate exactly one documented copy recipe")
        return matches[0]

    def inventory(self):
        destination = self.fake_home / "skills"
        self.assertFalse((destination / "skills").exists(), "Unexpected extra skills/ layer")
        self.assertEqual(sorted(path.name for path in destination.iterdir()), sorted(SKILLS))
        copied = {}
        for name in SKILLS:
            source = ROOT / "skills" / name
            self.assertTrue((source / "LICENSE").is_file())
            self.assertTrue((source / "PROVENANCE.md").is_file())
            source_files = {path.relative_to(source) for path in source.rglob("*") if path.is_file()}
            target = destination / name
            self.assertEqual(source_files, {path.relative_to(target) for path in target.rglob("*") if path.is_file()})
            for relative in source_files:
                original = (source / relative).read_bytes()
                actual = (target / relative).read_bytes()
                self.assertEqual(original, actual, f"Copy differs: {name}/{relative}")
                copied[f"{name}/{relative.as_posix()}"] = actual
        return copied

    def run_recipe(self, argv, environment=None):
        return subprocess.run(
            argv, cwd=ROOT, env=self.environment if environment is None else environment,
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=45,
        )

    @unittest.skipUnless(shutil.which("bash"), "Bash is not installed")
    def test_bash_copy_preserves_all_files_and_refuses_existing_destinations(self):
        command = [shutil.which("bash"), "--noprofile", "--norc", "-c",
                   self.recipe("bash", 'test -n "$HERMES_HOME"')]
        first = self.run_recipe(command)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        before = self.inventory()
        second = self.run_recipe(command)
        self.assertNotEqual(second.returncode, 0)
        self.assertIn("Already exists:", second.stdout + second.stderr)
        self.assertEqual(before, self.inventory())

    @unittest.skipUnless(shutil.which("powershell"), "Windows PowerShell is not installed")
    def test_powershell_copy_preserves_all_files_and_refuses_existing_destinations(self):
        command = [shutil.which("powershell"), "-NoProfile", "-NonInteractive", "-Command",
                   '$ErrorActionPreference = "Stop"; ' + self.recipe("powershell", "Test-Path")]
        first = self.run_recipe(command)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        before = self.inventory()
        second = self.run_recipe(command)
        self.assertNotEqual(second.returncode, 0)
        self.assertIn("Already exists:", second.stdout + second.stderr)
        self.assertEqual(before, self.inventory())

    @unittest.skipUnless(shutil.which("bash"), "Bash is not installed")
    def test_bash_copy_stops_when_profile_home_is_unset(self):
        environment = self.environment.copy()
        environment.pop("HERMES_HOME")
        result = self.run_recipe(
            [shutil.which("bash"), "--noprofile", "--norc", "-c",
             self.recipe("bash", 'test -n "$HERMES_HOME"')], environment,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Resolve HERMES_HOME first", result.stdout + result.stderr)
        self.assertFalse((self.fake_home / "skills").exists())


if __name__ == "__main__":
    unittest.main()
