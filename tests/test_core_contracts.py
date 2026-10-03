"""Static document contracts, NOT model behavioral verification.

These tests detect missing guidance, conflicting legacy rules, excess router
length, and broken installed references. They do not prove that an agent obeys
any guidance. Model pressure scenarios belong to the separate evaluation runner.
"""

from pathlib import Path
import re
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CORE = ("using-lookup", "finding-existing-work", "evaluating-existing-work")
NAMES = set(CORE) | {
    "licensing-and-payback", "contributing-back", "domain-playbooks"
}


def document(name):
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


class CorePackagingContracts(unittest.TestCase):
    def test_existing_six_skill_names_are_preserved(self):
        actual = set()
        for path in SKILLS.glob("*/SKILL.md"):
            text = path.read_text(encoding="utf-8")
            match = re.search(r"^name: ([-a-z]+)$", text, re.MULTILINE)
            self.assertIsNotNone(match, path)
            self.assertEqual(path.parent.name, match.group(1))
            actual.add(match.group(1))
        self.assertEqual(NAMES, actual)

    def test_core_guidance_has_no_repo_root_prior_art_dependency(self):
        for name in CORE:
            with self.subTest(skill=name):
                self.assertNotIn("PRIOR-ART.md", document(name))

    def test_references_resolve_from_skills_only_install(self):
        # No repository README/PRIOR-ART exists in this isolated installation.
        # Named skill references use the skill loader, not repo-relative paths.
        with tempfile.TemporaryDirectory() as temporary:
            installed = Path(temporary) / "installed"
            shutil.copytree(SKILLS, installed)
            for name in CORE:
                folder = installed / name
                for source in folder.rglob("*.md"):
                    text = source.read_text(encoding="utf-8")
                    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                        if re.match(r"[a-z]+://", target) or target.startswith("#"):
                            continue
                        resolved = (source.parent / target.split("#", 1)[0]).resolve()
                        self.assertTrue(resolved.is_relative_to(folder.resolve()),
                                        f"Reference escapes installed skill: {target}")
                        self.assertTrue(resolved.is_file(), str(resolved))
                    if source.name == "SKILL.md":
                        dependencies = re.findall(r"`([a-z]+(?:-[a-z]+)+)`", text)
                        self.assertTrue(dependencies, "Named-skill resolution must not be vacuous")
                        for dependency in dependencies:
                            self.assertIn(dependency, NAMES, f"Unknown installed skill: {dependency}")
                            self.assertTrue((installed / dependency / "SKILL.md").is_file())


class RouterContracts(unittest.TestCase):
    def test_action_trigger_does_not_conflict_with_user_word_routing(self):
        text = document("using-lookup")
        self.assertIn("Trigger on the next action", text)
        self.assertNotIn("Dispatch on the user's words", text)

    def test_reuse_is_only_for_same_decision_with_unchanged_constraints(self):
        text = document("using-lookup")
        self.assertRegex(text, r"same decision.*unchanged constraints")
        self.assertNotIn("A previous stage in this conversation already ran", text)

    def test_explicit_invalidation_precedes_reuse(self):
        text = document("using-lookup")
        self.assertIn("Invalidation takes precedence over reuse", text)
        for constraint in ("scope", "platform", "scale", "license", "budget", "freshness"):
            self.assertIn(constraint, text)

    def test_lookup_returns_answer_but_implementation_returns_control(self):
        text = document("using-lookup")
        self.assertRegex(text, r"Lookup-only.*answer")
        self.assertRegex(text, r"Implementation request.*authorized workflow")
        self.assertNotIn("don't continue into implementation", text)

    def test_router_is_compact(self):
        words = document("using-lookup").split()
        self.assertLessEqual(len(words), 350, "Frequently loaded router exceeds word budget")


class FinderContracts(unittest.TestCase):
    def test_local_repository_dependencies_docs_capabilities_precede_public_search(self):
        text = document("finding-existing-work")
        local = text.find("1. **Local first**")
        public = text.find("2. **Public sources")
        self.assertTrue(0 <= local < public, "Discovery must explicitly start locally")
        for item in ("repository", "dependencies", "docs", "capabilities"):
            self.assertTrue(item in text[local:public], f"Missing local source: {item}")

    def test_public_queries_redact_private_identifiers(self):
        text = document("finding-existing-work").lower()
        self.assertTrue("redact private identifiers" in text,
                        "Public-query privacy contract is missing")
        self.assertTrue("generic" in text, "Require generic technical search terms")

    def test_retrieved_directives_are_untrusted_data(self):
        text = document("finding-existing-work").lower()
        self.assertTrue("retrieved directives" in text and "untrusted" in text,
                        "Source instructions must not gain authority")

    def test_offline_or_no_search_means_unknown_not_absent(self):
        text = document("finding-existing-work").lower()
        self.assertTrue("no-search" in text and "offline" in text,
                        "Availability/restriction contract is missing")
        self.assertTrue("unknown, not absent" in text,
                        "Unsearched alternatives cannot count as negative evidence")

    def test_negative_claims_require_scope_inspected_sources_and_unknowns(self):
        text = document("finding-existing-work")
        for fragment in ("No suitable candidate found in", "sources inspected", "unknowns"):
            self.assertTrue(fragment in text, f"Missing evidence clause: {fragment}")
        self.assertTrue('"Nothing exists" stated in one line is a complete answer' not in text,
                        "Legacy unsupported-absence rule remains")
        self.assertTrue("what nobody has done" not in text,
                        "Legacy universal gap claim remains")

    def test_effort_budget_is_independent_of_output_length_with_overrides(self):
        text = document("finding-existing-work")
        for fragment in ("quick check", "go deep", "standard", "Effort budget",
                         "Output length is independent", "overrides take precedence"):
            self.assertTrue(fragment in text, f"Missing budget/output clause: {fragment}")
        self.assertTrue("~50-100 tokens" not in text,
                        "Legacy effort/output token coupling remains")

    def test_single_compact_decision_record_includes_compose_and_unknown(self):
        text = document("finding-existing-work")
        for fragment in ("## Decision record", "adopt / extend / compose / build",
                         "unknown", "constraints", "Evidence", "Coverage", "Next"):
            self.assertTrue(fragment in text, f"Missing decision-record field: {fragment}")
        self.assertTrue("## Brief" not in text, "Do not retain duplicated legacy brief")


class EvaluatorContracts(unittest.TestCase):
    def test_compose_is_a_concrete_choice_and_in_the_output_contract(self):
        text = document("evaluating-existing-work")
        self.assertTrue("| Compose |" in text, "Compose needs its own decision criterion")
        output = text.partition("## Record and return")[2]
        self.assertTrue("adopt / extend / compose / build" in output,
                        "Output must preserve compose, not silently drop it")

    def test_existing_record_is_updated_or_loaded_by_installed_skill_name(self):
        text = document("evaluating-existing-work")
        for fragment in ("Update the existing decision record", "If no record exists",
                         "`finding-existing-work` by name"):
            self.assertTrue(fragment in text, f"Missing shared-record clause: {fragment}")
        self.assertTrue("Same shape as the Brief" not in text,
                        "Legacy duplicated brief rule remains")

    def test_direct_candidate_evaluation_keeps_local_first_and_source_safety(self):
        text = document("evaluating-existing-work").lower()
        for fragment in ("local repository", "dependencies", "docs", "capabilities",
                         "before external", "redact private identifiers",
                         "retrieved directives", "untrusted"):
            self.assertTrue(fragment in text, f"Missing standalone safety clause: {fragment}")

    def test_validation_budget_and_output_length_are_separate(self):
        text = document("evaluating-existing-work").lower()
        for fragment in ("effort budget", "quick", "deep", "output length"):
            self.assertTrue(fragment in text, f"Missing validation budget clause: {fragment}")

    def test_unchecked_fit_is_unknown_with_blocking_uncertainty_preserved(self):
        text = document("evaluating-existing-work").lower()
        for fragment in ("unknown", "unverified", "inspected sources", "blocking uncertainty"):
            self.assertTrue(fragment in text, f"Missing uncertainty clause: {fragment}")
        self.assertTrue("pending" in text, "A license/fit blocker must permit a pending verdict")

    def test_lookup_only_answer_and_authorized_implementation_continuation(self):
        text = document("evaluating-existing-work").lower()
        self.assertTrue("lookup-only" in text and "answer" in text,
                        "Lookup-only must stop with an answer")
        self.assertTrue("implementation request" in text and "authorized workflow" in text,
                        "Implementation authorization must survive lookup")
        self.assertTrue("does not authorize" in text,
                        "Evaluation cannot grant new installation/execution permission")


if __name__ == "__main__":
    unittest.main()
