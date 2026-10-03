"""Static regressions for reviewed workflow instructions, not agent behavior.

No model is invoked. Passing tests show that the document repairs remain present;
only separately executed behavioral evaluations can establish agent compliance.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def document(name):
    return (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


class WorkflowReviewContracts(unittest.TestCase):
    def test_router_authorization_boundary_has_complete_prose(self):
        router = document("using-lookup")
        boundary = next(line for line in router.splitlines() if "determines authorization" in line)
        self.assertIn("checking existence is not permission to build", boundary)
        self.assertNotIn("***", boundary, "A stripped placeholder must not replace the object of checking")

    def test_finder_records_failed_and_successful_empty_searches_separately(self):
        finder = document("finding-existing-work")
        evidence = finder.partition("## Evidence and claims")[2].partition("## Decision record")[0]
        self.assertIn("successful query with zero results", evidence,
                      "Zero hits need an explicit successful-search interpretation")
        self.assertIn("failed or inaccessible", evidence,
                      "Access failure cannot become a negative search observation")
        self.assertIn("Record each attempted source/query and its status", evidence,
                      "Retain the evidence needed to distinguish the two cases")
        coverage = next(line for line in finder.splitlines() if line.startswith("- **Coverage:**"))
        self.assertIn("successful-empty vs failed/inaccessible", coverage)

    def test_direct_evaluation_defines_its_default_effort_budget(self):
        evaluator = document("evaluating-existing-work")
        validation = evaluator.partition("## Bounded validation")[2].partition("## Record and return")[0]
        self.assertIn("default to standard", validation,
                      "Direct evaluation cannot rely on a nonexistent discovery budget")
        self.assertIn("if no discovery budget exists", validation)
        self.assertIn("independently of output length", validation)

    def test_direct_evaluation_checks_installed_dependencies_before_external_checks(self):
        evaluator = document("evaluating-existing-work")
        inspection = evaluator.partition("## Check fit and evidence")[2].partition("For leading candidates")[0]
        self.assertIn("declared/installed dependencies", inspection,
                      "A manifest alone cannot establish available local dependencies")
        self.assertIn("before external checks", inspection)


if __name__ == "__main__":
    unittest.main()
