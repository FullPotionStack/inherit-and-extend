"""Focused review regressions; not legal advice or model-behavior verification.

Run: python3 -m unittest discover -s tests -p test_license_packaging_review.py -v
"""
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import unquote, urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LicensePackagingReviewTests(unittest.TestCase):
    def test_lgpl_combined_work_review_includes_both_license_texts(self):
        text = (ROOT / "skills/licensing-and-payback/SKILL.md").read_text(encoding="utf-8")
        rows = {line.split("|")[1].strip(): line.lower()
                for line in text.splitlines() if line.startswith("|") and line.count("|") >= 3}
        self.assertIn("LGPL-3.0", rows)
        row = rows["LGPL-3.0"]
        self.assertRegex(row, r"copies of both.{0,30}gplv3.{0,30}lgplv3")
        for duty in ("relink", "shared-library", "reverse engineering", "installation"):
            with self.subTest(duty=duty):
                self.assertIn(duty, row)


    def test_version_selection_records_only_or_later_permission(self):
        text = (ROOT / "skills/licensing-and-payback/SKILL.md").read_text(encoding="utf-8")
        facts = " ".join(text.partition("## Establish the facts")[2]
                         .partition("## Inventory with tools, then review")[0].lower().split())
        self.assertIn("version-only", facts)
        self.assertIn("or any later version", facts)
        self.assertIn("chosen license", facts)


    def test_folder_only_copy_is_self_contained_without_online_research_notes(self):
        # Do not trust TMPDIR: some shells still point it at the system temp directory.
        scratch = Path.home() / "AppData/Local/hermes/cache/scratch"
        scratch.mkdir(parents=True, exist_ok=True)
        expected_license = (ROOT / "LICENSE").read_bytes()
        with tempfile.TemporaryDirectory(prefix="license-review-copy-", dir=scratch) as work:
            installed = Path(work) / "skills"
            for name in ("licensing-and-payback", "contributing-back"):
                with self.subTest(skill=name):
                    target = installed / name
                    shutil.copytree(ROOT / "skills" / name, target)
                    self.assertEqual((target / "LICENSE").read_bytes(), expected_license)
                    self.assertIn(b"Copyright (c) 2026 FullPotionStack", expected_license)
                    self.assertFalse((installed / "LICENSE").exists())
                    self.assertFalse((installed / "PRIOR-ART.md").exists())
                    provenance = (target / "PROVENANCE.md").read_text(encoding="utf-8")
                    self.assertIn("optional", provenance.lower())
                    self.assertIn("not required", provenance.lower())
                    self.assertIn(f"skills/{name}", provenance)
                    self.assertIn("Copyright (c) 2026 FullPotionStack", provenance)
                    local_links = []
                    for doc in (target / "SKILL.md", target / "PROVENANCE.md"):
                        for link in re.findall(r"\[[^\]]+\]\(([^\s)]+)\)",
                                               doc.read_text(encoding="utf-8")):
                            parts = urlsplit(link)
                            if not parts.scheme and parts.path:
                                resolved = (doc.parent / unquote(parts.path)).resolve()
                                local_links.append(resolved)
                                self.assertTrue(resolved.is_relative_to(target.resolve()))
                                self.assertTrue(resolved.is_file(), f"missing local reference: {link}")
                    self.assertEqual(set(local_links),
                                     {target.resolve() / "LICENSE", target.resolve() / "PROVENANCE.md"})


if __name__ == "__main__":
    unittest.main()
