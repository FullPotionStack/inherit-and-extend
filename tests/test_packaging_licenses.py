"""Packaging/content regressions, not a certification of legal compliance.

Run: python3 -m unittest discover -s tests -p test_packaging_licenses.py -v
Only stdlib is required. Copies are isolated under Hermes scratch, never profiles.
"""
import hashlib
import os
import re
from urllib.parse import unquote, urlsplit
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "using-lookup", "finding-existing-work", "evaluating-existing-work",
    "licensing-and-payback", "contributing-back", "domain-playbooks",
)
# Pin the baseline text while allowing Git's platform-specific checkout line endings.
ROOT_LICENSE_SHA256 = "50efd1e43910d910a18ba3bee9e4ffcc0f6d030063f11b7a6d0ba2ae21072023"
SCRATCH = Path(os.environ.get("TMPDIR") or (
    Path.home() / "AppData/Local/hermes/cache/scratch"
))


class PackagingLicensesTests(unittest.TestCase):
    def test_manual_skill_folder_copy_preserves_full_license_and_provenance(self):
        expected_license = (ROOT / "LICENSE").read_bytes()
        self.assertEqual(hashlib.sha256(expected_license.replace(b"\r\n", b"\n")).hexdigest(),
                         ROOT_LICENSE_SHA256)
        SCRATCH.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="skill-license-copy-", dir=SCRATCH) as work:
            copied_skills = Path(work) / "skills"
            for name in SKILLS:
                with self.subTest(skill=name):
                    # Equivalent to copying skills/<name> recursively; no root files copied.
                    target = copied_skills / name
                    shutil.copytree(ROOT / "skills" / name, target)
                    self.assertTrue((target / "SKILL.md").is_file())
                    self.assertFalse((copied_skills / "LICENSE").exists())
                    self.assertTrue((target / "LICENSE").is_file(), "standalone copy loses MIT notice")
                    self.assertEqual((target / "LICENSE").read_bytes(), expected_license)
                    provenance = target / "PROVENANCE.md"
                    self.assertTrue(provenance.is_file(), "standalone copy loses source attribution")
                    text = provenance.read_text(encoding="utf-8")
                    self.assertIn("https://github.com/FullPotionStack/look-before-build", text)
                    self.assertIn(f"skills/{name}", text)
                    self.assertIn("Copyright (c) 2026 FullPotionStack", text)
                    self.assertIn("[LICENSE](LICENSE)", text)
                    self.assertNotIn("../../", text, "attribution must survive folder-only copying")

    def test_license_triage_does_not_treat_families_as_legal_verdicts(self):
        text = (ROOT / "skills/licensing-and-payback/SKILL.md").read_text(encoding="utf-8")
        lower = " ".join(text.lower().split())  # Ignore Markdown line wrapping.
        for concept in ("exact license", "version", "private use", "distribution",
                        "network interaction", "integration", "inventory",
                        "not legal judgments", "legal counsel", "uncertain"):
            with self.subTest(concept=concept):
                self.assertIn(concept, lower)
        for obsolete in ("your project inherits the license", "nothing else",
                         "minimum correct form", "zero license implications",
                         "no risk to your product", "a quick forum post now beats"):
            with self.subTest(obsolete=obsolete):
                self.assertNotIn(obsolete, lower)
        # Separate triage rows force review of the distinct library/file and network triggers.
        rows = {line.split("|")[1].strip(): line.lower()
                for line in text.splitlines() if line.startswith("|") and line.count("|") >= 3}
        for label, concepts in {
            "LGPL-3.0": ("relink", "reverse engineering", "source"),
            "MPL-2.0": ("file", "distribution", "source"),
            "GPL-3.0": ("convey", "private", "aggregate"),
            "AGPL-3.0": ("modified", "network", "source"),
            "Apache-2.0": ("if", "notice", "changed"),
        }.items():
            with self.subTest(license=label):
                self.assertIn(label, rows)
                if label in rows:
                    for concept in concepts:
                        self.assertIn(concept, rows[label])
        self.assertRegex(lower, r"credit line.{0,60}not.{0,30}license compliance")
        for url in (
            "https://opensource.org/license/mit",
            "https://www.apache.org/licenses/LICENSE-2.0",
            "https://www.gnu.org/licenses/lgpl-3.0.html",
            "https://www.mozilla.org/en-US/MPL/2.0/",
            "https://www.gnu.org/licenses/gpl-3.0.html",
            "https://www.gnu.org/licenses/agpl-3.0.html",
        ):
            with self.subTest(primary_text=url):
                self.assertIn(url, text)

    def test_contribution_is_opt_in_and_checks_rights_before_publication(self):
        text = (ROOT / "skills/contributing-back/SKILL.md").read_text(encoding="utf-8")
        lower = " ".join(text.lower().split())
        for concept in ("optional", "declining", "ownership", "employer", "nda",
                        "credentials", "private data", "cla", "dco", "approval",
                        "exact material", "destination", "draft"):
            with self.subTest(concept=concept):
                self.assertIn(concept, lower)
        for obsolete in ("paying that forward is fair", "rough share beats",
                         "no code shared, pure value", "40+ harnesses",
                         "does **not** require your product's code to be public"):
            with self.subTest(obsolete=obsolete):
                self.assertNotIn(obsolete, lower)
        self.assertIn("[LICENSE](LICENSE)", text)
        self.assertIn("[PROVENANCE.md](PROVENANCE.md)", text)

    def test_owned_document_references_survive_isolated_folder_copies(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="skill-reference-copy-", dir=SCRATCH) as work:
            checked_links = 0
            for name in SKILLS:
                target = Path(work) / name
                shutil.copytree(ROOT / "skills" / name, target)
                docs = [target / "PROVENANCE.md"]
                if name in ("licensing-and-payback", "contributing-back"):
                    docs += list(target.rglob("*.md"))
                for doc in set(docs):
                    with self.subTest(document=f"{name}/{doc.name}"):
                        text = doc.read_text(encoding="utf-8")
                        links = re.findall(r"\[[^\]]+\]\(([^\s)]+)\)", text)
                        self.assertTrue(links, "reference check must not be vacuous")
                        for link in links:
                            checked_links += 1
                            parts = urlsplit(link)
                            if parts.scheme:
                                self.assertEqual(parts.scheme, "https")
                                self.assertTrue(parts.netloc, f"malformed URL: {link}")
                                # Online availability is not asserted by this offline test.
                            else:
                                destination = (doc.parent / unquote(parts.path)).resolve()
                                self.assertTrue(destination.is_relative_to(target.resolve()),
                                                f"reference escapes copied folder: {link}")
                                self.assertTrue(destination.is_file(), f"broken reference: {link}")
                # Bare handoff identifiers name real suite skills, but their availability
                # is explicitly conditional; these folders need not contain siblings.
                if name in ("licensing-and-payback", "contributing-back"):
                    text = (target / "SKILL.md").read_text(encoding="utf-8")
                    for identifier in re.findall(r"`([a-z]+(?:-[a-z]+)+)`", text):
                        if identifier in SKILLS:
                            self.assertTrue((ROOT / "skills" / identifier / "SKILL.md").is_file())
                    self.assertIn("unavailable", text)
            self.assertGreaterEqual(checked_links, 20)


if __name__ == "__main__":
    unittest.main()
