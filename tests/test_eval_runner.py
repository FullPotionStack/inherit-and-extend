"""Runner mechanics only: these tests do not grade model behavior."""
import importlib.util
from contextlib import closing
from pathlib import Path
import unittest
import sys

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "evals" / "run.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("eval_runner", RUNNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RunnerTests(unittest.TestCase):
    def test_command_is_subscription_pinned_and_isolated(self):
        self.assertTrue(RUNNER.exists(), "missing evaluation runner")
        command = load_runner().command("hermes", Path("prompt $(bad).txt"))
        for flag, value in [("--provider", "openai-codex"), ("--model", "gpt-6.1-sol"),
                            ("--reasoning", "high"), ("--toolsets", "bot_room"),
                            ("--query-file", "prompt $(bad).txt"), ("--format", "stream-json")]:
            self.assertEqual(command[command.index(flag) + 1], value)
        for flag in ["--safe-mode", "--ignore-user-config", "--ignore-rules", "--oneshot"]:
            self.assertIn(flag, command)
        self.assertNotIn("--resume", command)
        self.assertNotIn("--continue", command)
    def test_stream_requires_one_successful_pinned_result(self):
        runner = load_runner()
        good = '{"type":"system","subtype":"init","model":"gpt-6.1-sol"}\n{"type":"result","exit_code":0,"text":"A decision", "tokens":{"input":12,"output":3}}\n'
        result = runner.parse_stream(good, "", 0)
        self.assertEqual(result["text"], "A decision")
        self.assertEqual(result["tokens"]["input"], 12)
        for raw, stderr, code in [
            (good, "", 1), (good, "Fallback activated", 0),
            (good.replace("gpt-6.1-sol", "other-model"), "", 0),
            (good.replace('"exit_code":0', '"exit_code":1'), "", 0),
            (good.replace('"A decision"', '""'), "", 0),
            (good + '{"type":"result","exit_code":0,"text":"extra"}\n', "", 0),
            ('{"type":"system","model":"gpt-6.1-sol"}\n', "", 0),
            (good + '{"type":"tool_use","name":"web_search"}\n', "", 0),
            (good + '{"type":"result","error":"rate limited"}\n', "", 0),
            ("not-json\n" + good, "", 0),
        ]:
            with self.subTest(raw=raw, stderr=stderr, code=code):
                with self.assertRaises(runner.Blocked):
                    runner.parse_stream(raw, stderr, code)
    def test_stream_fails_closed_on_untrusted_protocol_and_route(self):
        import json
        runner = load_runner()
        init = {"type": "system", "subtype": "init", "model": runner.MODEL, "session_id": "fresh"}
        result = {"type": "result", "exit_code": 0, "text": "A decision", "session_id": "fresh"}
        bad_streams = [
            [init, {**result, "text": ["not text"]}],
            [init, {**result, "session_id": "another"}],
            [init, {**result, "exit_code": False}],
            [{**init, "provider": "openai"}, result],
            [init, {**result, "model": "other-model"}],
            [init, {**result, "tool_calls": [{"name": "web_search"}]}],
            [init, {"type": "error", "message": "route failed"}, result],
            [init, {"type": "system", "subtype": "fallback", "provider": "openai"}, result],
            [result, init],
            [init, result, {"type": "text", "text": "after result"}],
            [init, {**result, "tokens": {"input": -1}}],
            [init, {"type": "unknown"}, result],
        ]
        for events in bad_streams:
            with self.subTest(events=events):
                with self.assertRaises(runner.Blocked):
                    runner.parse_stream("\n".join(json.dumps(e) for e in events), "", 0)

    def test_snapshot_is_git_object_not_concurrent_working_tree(self):
        runner = load_runner()
        snapshot = runner.snapshot(ROOT, "c94a9f6")
        self.assertEqual(len(snapshot["files"]), 6)
        self.assertIn("Stop dispatching once", snapshot["files"]["skills/using-lookup/SKILL.md"])
        self.assertEqual(snapshot["ref"], "c94a9f6c138959928b3ab2c489ecf84e07ef28ba")
        self.assertEqual(snapshot, runner.snapshot(ROOT, "c94a9f6"))
        control = runner.snapshot(ROOT, "none")
        self.assertEqual(control["files"], {})
        scenario = {"id": "example", "task": "Return a decision.", "fixtures": "Controlled input only.",
                    "rubric": ["SECRET GRADING CRITERION"]}
        prompt = runner.prompt(scenario, snapshot)
        self.assertIn("Controlled input only.", prompt)
        self.assertIn("skills/using-lookup/SKILL.md", prompt)
        self.assertNotIn("SECRET GRADING CRITERION", prompt)
        self.assertNotIn("Stop dispatching once", runner.prompt(scenario, control))
        with self.assertRaises(runner.Blocked):
            runner.snapshot(ROOT, "not-a-valid-git-revision")
    def test_snapshots_include_linked_markdown_and_exact_provenance(self):
        import hashlib
        import json
        import subprocess
        import tempfile
        runner = load_runner()
        scratch = Path.home() / "AppData/Local/hermes/cache/scratch"
        with tempfile.TemporaryDirectory(prefix="eval-snapshot-", dir=scratch) as tmp:
            repo = Path(tmp)
            body = repo / "skills/demo/SKILL.md"
            ref = repo / "skills/demo/references/topic.md"
            ref.parent.mkdir(parents=True)
            body.write_bytes(b"Consult references/topic.md\n")
            ref.write_bytes(b"DECISIVE REFERENCE\n")
            for args in [["init", "-q"], ["add", "skills"],
                         ["-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture"]]:
                subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)
            for name in ["HEAD", "working-tree"]:
                snap = runner.snapshot(repo, name)
                self.assertEqual(set(snap["files"]), {"skills/demo/SKILL.md", "skills/demo/references/topic.md"})
                self.assertEqual(snap["file_sha256"]["skills/demo/references/topic.md"],
                                 hashlib.sha256(ref.read_bytes()).hexdigest())
                self.assertIn("DECISIVE REFERENCE", runner.prompt({"task": "Decide", "fixtures": "Input"}, snap))
                canonical = json.dumps(snap["files"], sort_keys=True, ensure_ascii=False).encode("utf-8")
                self.assertEqual(snap["sha256"], hashlib.sha256(canonical).hexdigest())
            frozen = runner.snapshot(repo, "HEAD")
            ref.write_text("CHANGED\n", encoding="utf-8")
            self.assertEqual(runner.snapshot(repo, "HEAD"), frozen)
            self.assertNotEqual(runner.snapshot(repo, "working-tree")["sha256"], frozen["sha256"])

    def test_working_tree_snapshot_detects_concurrent_content_change(self):
        import tempfile
        from unittest.mock import patch
        runner = load_runner()
        scratch = Path.home() / "AppData/Local/hermes/cache/scratch"
        with tempfile.TemporaryDirectory(prefix="eval-race-", dir=scratch) as tmp:
            repo = Path(tmp)
            body = repo / "skills/demo/SKILL.md"
            body.parent.mkdir(parents=True)
            body.write_bytes(b"first\n")
            read = Path.read_bytes
            changed = []
            def racing_read(path):
                data = read(path)
                if path == body and not changed:
                    changed.append(True)
                    body.write_bytes(b"changed during snapshot\n")
                return data
            with patch.object(Path, "read_bytes", racing_read), patch.object(runner, "git", return_value="fixture-head"):
                with self.assertRaises(runner.Blocked):
                    runner.snapshot(repo, "working-tree")
            self.assertEqual(changed, [True], "the race fixture must actually execute")

    def test_attempt_preserves_actual_child_failure_and_timeout(self):
        import json
        import os
        import sys
        import tempfile
        runner = load_runner()
        scratch = Path.home() / "AppData/Local/hermes/cache/scratch"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="eval-test-", dir=scratch) as tmp:
            root = Path(tmp)
            argv = [sys.executable, "-c", "import sys; print('actual failure'); print('backend unavailable', file=sys.stderr); sys.exit(7)"]
            result = runner.attempt(argv, root / "failed", root, os.environ.copy(), timeout=10)
            self.assertEqual(result["status"], "blocked")
            self.assertEqual(result["returncode"], 7)
            self.assertEqual((root / "failed/stdout.jsonl").read_text().strip(), "actual failure")
            self.assertIn("backend unavailable", (root / "failed/stderr.txt").read_text())
            self.assertIsNone(result["scores"])
            self.assertEqual(json.loads((root / "failed/metadata.json").read_text())["status"], "blocked")
            with self.assertRaises(FileExistsError):
                runner.attempt(argv, root / "failed", root, os.environ.copy(), timeout=10)
            timed = runner.attempt([sys.executable, "-c", "import time; print('partial', flush=True); time.sleep(10)"],
                                   root / "timed", root, os.environ.copy(), timeout=1)
            self.assertEqual(timed["status"], "blocked")
            self.assertIn("timeout", timed["error"].lower())
            self.assertIn("partial", (root / "timed/stdout.jsonl").read_text())
    def test_preflight_rejects_paid_routing_fallback_or_tools(self):
        runner = load_runner()
        verified = {"provider": "openai-codex", "api_mode": "codex_responses", "host": "chatgpt.com",
                    "source": "device_code", "valid_toolset": True, "tool_count": 0,
                    "fallback_count": 0, "cli_fallback_count": 0,
                    "model": "gpt-6.1-sol", "scheme": "https", "path": "/backend-api/codex",
                    "safe_mode": True, "ignore_user_config": True, "ignore_rules": True,
                    "session_db": "fixture.db"}
        runner.validate_preflight(verified)
        for key, value in [("provider", "openai"), ("api_mode", "chat_completions"),
                           ("host", "api.openai.com"), ("source", "api_key"),
                           ("tool_count", 1), ("fallback_count", 1), ("cli_fallback_count", 1),
                           ("valid_toolset", False), ("tool_count", False), ("valid_toolset", 1),
                           ("model", "other-model"), ("scheme", "http"), ("path", "/v1"),
                           ("safe_mode", False), ("ignore_user_config", False), ("ignore_rules", False),
                           ("session_db", None), ("session_db", "")]:
            with self.subTest(key=key):
                with self.assertRaises(runner.Blocked):
                    runner.validate_preflight({**verified, key: value})

    def test_attempt_checks_subscription_session_provenance_before_completion(self):
        import json
        import os
        import sqlite3
        import tempfile
        runner = load_runner()
        scratch = Path.home() / "AppData/Local/hermes/cache/scratch"
        with tempfile.TemporaryDirectory(prefix="eval-session-", dir=scratch) as tmp:
            root = Path(tmp)
            db = root / "state.db"
            with closing(sqlite3.connect(db)) as conn, conn:
                conn.execute("CREATE TABLE sessions (id TEXT PRIMARY KEY, source TEXT, model TEXT, parent_session_id TEXT, "
                             "tool_call_count INTEGER, api_call_count INTEGER, billing_provider TEXT, billing_base_url TEXT, "
                             "billing_mode TEXT, cost_status TEXT, model_config TEXT)")
                row = ["fresh", "tool", runner.MODEL, None, 0, 1, runner.PROVIDER,
                       "https://chatgpt.com/backend-api/codex", "subscription_included", "included",
                       json.dumps({"reasoning_config": {"effort": "high"}, "api_key": "NEVER PRINT THIS"})]
                conn.execute("INSERT INTO sessions VALUES (?,?,?,?,?,?,?,?,?,?,?)", row)
            events = [{"type": "system", "subtype": "init", "model": runner.MODEL, "session_id": "fresh"},
                      {"type": "result", "exit_code": 0, "text": "Decision fixture", "session_id": "fresh"}]
            argv = [sys.executable, "-c", "print(" + repr("\n".join(json.dumps(e) for e in events)) + ")"]
            good = runner.attempt(argv, root / "good", root, os.environ.copy(), session_db=db)
            self.assertEqual(good["status"], "completed-unscored")
            self.assertEqual(good["session_provenance"]["billing_mode"], "subscription_included")
            self.assertNotIn("NEVER PRINT THIS", json.dumps(good))
            for key, value in [("billing_provider", "openai"), ("model", "other-model"),
                               ("billing_base_url", "https://api.openai.com/v1"), ("billing_mode", "api_metered"),
                               ("api_call_count", 2), ("tool_call_count", 1), ("parent_session_id", "old")]:
                with closing(sqlite3.connect(db)) as conn, conn:
                    conn.execute("DELETE FROM sessions")
                    conn.execute("INSERT INTO sessions VALUES (?,?,?,?,?,?,?,?,?,?,?)", row)
                    conn.execute("UPDATE sessions SET " + key + "=?", (value,))
                bad = runner.attempt(argv, root / key, root, os.environ.copy(), session_db=db)
                self.assertEqual(bad["status"], "blocked", key)
                self.assertIsNone(bad["scores"])
                self.assertFalse((root / key / "answer.txt").exists())
                self.assertTrue((root / key / "stdout.jsonl").exists())

    def test_main_stops_on_actual_child_failure_with_truthful_counts(self):
        import json
        import tempfile
        from unittest.mock import patch
        runner = load_runner()
        scratch = Path.home() / "AppData/Local/hermes/cache/scratch"
        with tempfile.TemporaryDirectory(prefix="eval-main-fail-", dir=scratch) as tmp:
            dest = Path(tmp) / "run"
            with patch.object(runner, "preflight", return_value=(sys.executable, {"session_db": str(Path(tmp) / "missing.db")})), \
                    patch.object(runner, "command", return_value=[sys.executable, "-c", "import sys; print('real child failure'); sys.exit(7)"]) as command:
                code = runner.main(["--arms", "control", "--scenarios", "local_solution,partial_fit", "--out", str(dest)])
            self.assertEqual(code, 2)
            self.assertEqual(command.call_count, 1, "stop immediately, never try next scenario")
            manifest = json.loads((dest / "manifest.json").read_text())
            self.assertEqual(manifest["status"], "blocked")
            self.assertEqual(manifest["attempted_processes"], 1)
            self.assertEqual(manifest["blocked_records"], 1)
            self.assertEqual(manifest["completed_records"], 0)
            self.assertEqual(manifest["pending_plans"], 1)
            record = manifest["records"][0]
            self.assertEqual(record["returncode"], 7)
            self.assertIsNone(record["scores"])
            self.assertEqual(json.loads((dest / record["transcript"] / "metadata.json").read_text()), record)

    def test_main_refuses_changed_prompt_before_launch(self):
        import json
        import tempfile
        from unittest.mock import patch
        runner = load_runner()
        scratch = Path.home() / "AppData/Local/hermes/cache/scratch"
        with tempfile.TemporaryDirectory(prefix="eval-tamper-", dir=scratch) as tmp:
            dest = Path(tmp) / "run"
            def tampering_preflight(*args):
                (dest / "prompts/control/local_solution-r1.txt").write_bytes(b"CHANGED AFTER PREPARATION")
                return sys.executable, {"session_db": str(Path(tmp) / "missing.db")}
            with patch.object(runner, "preflight", side_effect=tampering_preflight), \
                    patch.object(runner, "attempt", side_effect=AssertionError("must not launch changed prompt")) as attempt:
                code = runner.main(["--arms", "control", "--scenarios", "local_solution", "--out", str(dest)])
            self.assertEqual(code, 2)
            attempt.assert_not_called()
            manifest = json.loads((dest / "manifest.json").read_text())
            self.assertEqual(manifest["status"], "blocked")
            self.assertEqual(manifest["attempted_processes"], 0)
            self.assertIn("prompt", manifest["error"].lower())

    def test_main_preserves_attempt_when_prompt_disappears_during_child(self):
        import json
        import tempfile
        from unittest.mock import patch
        runner = load_runner()
        scratch = Path.home() / "AppData/Local/hermes/cache/scratch"
        with tempfile.TemporaryDirectory(prefix="eval-deleted-prompt-", dir=scratch) as tmp:
            dest = Path(tmp) / "run"
            query = dest / "prompts/control/local_solution-r1.txt"
            child = [sys.executable, "-c", "from pathlib import Path; import sys; Path(" + repr(str(query)) + ").unlink(); sys.exit(7)"]
            with patch.object(runner, "preflight", return_value=(sys.executable, {"session_db": str(Path(tmp) / "missing.db")})), \
                    patch.object(runner, "command", return_value=child):
                code = runner.main(["--arms", "control", "--scenarios", "local_solution", "--out", str(dest)])
            self.assertEqual(code, 2)
            manifest = json.loads((dest / "manifest.json").read_text())
            self.assertEqual(manifest["attempted_processes"], 1, "the real launch must not disappear from accounting")
            self.assertEqual(manifest["records"][0]["returncode"], 7)
            self.assertEqual(manifest["records"][0]["status"], "blocked")

    def test_prepare_snapshot_failure_preserves_blocked_manifest_without_calls(self):
        import json
        import subprocess
        import tempfile
        scratch = Path.home() / "AppData/Local/hermes/cache/scratch"
        with tempfile.TemporaryDirectory(prefix="eval-blocked-", dir=scratch) as tmp:
            dest = Path(tmp) / "blocked"
            child = subprocess.run([sys.executable, str(RUNNER), "--prepare", "--out", str(dest),
                                    "--baseline-ref", "not-an-existing-ref", "--scenarios", "local_solution"],
                                   capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(child.returncode, 2, child.stderr)
            self.assertTrue((dest / "manifest.json").exists(), "preparation failures must be recorded")
            manifest = json.loads((dest / "manifest.json").read_text())
            self.assertEqual(manifest["status"], "blocked")
            self.assertEqual(manifest["records"], [])
            self.assertEqual(manifest["attempted_processes"], 0)
            self.assertEqual(manifest["pending_plans"], 2)
            self.assertFalse((dest / "preflight.json").exists())

    def test_prepare_preserves_exact_utf8_prompt_bytes_with_crlf_skill_content(self):
        import json
        import tempfile
        from unittest.mock import patch
        runner = load_runner()
        scratch = Path.home() / "AppData/Local/hermes/cache/scratch"
        scratch.mkdir(parents=True, exist_ok=True)
        scenario = json.loads((ROOT / "evals/scenarios.json").read_text(encoding="utf-8"))[0]
        guidance = {"ref": "fixture", "sha256": "fixture", "files": {
            "skills/demo/SKILL.md": "---\r\nname: demo\r\n---\r\n\r\nExact body.\r\n"}}
        with tempfile.TemporaryDirectory(prefix="eval-prompt-bytes-", dir=scratch) as tmp:
            dest = Path(tmp) / "prepared"
            with patch.object(runner, "snapshot", return_value=guidance):
                code = runner.main(["--prepare", "--arms", "updated", "--updated-ref", "working-tree",
                                    "--scenarios", scenario["id"], "--out", str(dest)])
            self.assertEqual(code, 0)
            query = dest / "prompts/updated" / (scenario["id"] + "-r1.txt")
            self.assertEqual(query.read_bytes(), runner.prompt(scenario, guidance).encode("utf-8"),
                             "Text-mode newline translation must not add CRs or blank lines to supplied skills")
            self.assertIn(guidance["files"]["skills/demo/SKILL.md"].encode("utf-8"), query.read_bytes())

    def test_prepare_cli_preserves_prompts_and_unscored_status_without_inference(self):
        import json
        import subprocess
        import sys
        import tempfile
        scratch = Path.home() / "AppData/Local/hermes/cache/scratch"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="eval-prepare-", dir=scratch) as tmp:
            dest = Path(tmp) / "prepared"
            argv = [sys.executable, str(RUNNER), "--prepare", "--out", str(dest),
                    "--scenarios", "local_solution", "--arms", "baseline,control"]
            child = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(child.returncode, 0, child.stderr)
            manifest = json.loads((dest / "manifest.json").read_text())
            self.assertEqual(manifest["status"], "prepared-not-run")
            self.assertEqual(manifest["planned_calls"], 2)
            self.assertEqual(manifest["records"], [])
            baseline = (dest / "prompts/baseline/local_solution-r1.txt").read_text(encoding="utf-8")
            control = (dest / "prompts/control/local_solution-r1.txt").read_text(encoding="utf-8")
            self.assertIn("Stop dispatching once", baseline)
            self.assertNotIn("Stop dispatching once", control)
            self.assertIn("Controlled local inventory", control)
            self.assertFalse((dest / "preflight.json").exists())
            import hashlib
            self.assertEqual(manifest["completed_records"], 0)
            self.assertEqual(manifest["blocked_records"], 0)
            self.assertEqual(manifest["pending_plans"], 2)
            for filename in ["run.py", "preflight.py", "RUBRIC.md", "scenarios.json"]:
                saved = dest / "provenance" / filename
                self.assertEqual(saved.read_bytes(), (ROOT / "evals" / filename).read_bytes())
                self.assertEqual(manifest["provenance_sha256"][filename], hashlib.sha256(saved.read_bytes()).hexdigest())
            refused = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8")
            self.assertNotEqual(refused.returncode, 0, "must not overwrite prior evidence")


if __name__ == "__main__":
    unittest.main()
