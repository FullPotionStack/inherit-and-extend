"""Lean, subscription-only vignette runner. Model behavior is scored by humans."""
from pathlib import Path
import json
import hashlib
import subprocess
import time
from datetime import datetime, timezone


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_manifest(path, manifest):
    records = manifest["records"]
    manifest.update({"attempted_processes": len(records),
                     "completed_records": sum(r["status"] == "completed-unscored" for r in records),
                     "blocked_records": sum(r["status"] == "blocked" for r in records),
                     "pending_plans": manifest["planned_calls"] - len(records)})
    save_json(path, manifest)


def session_provenance(database, session_id):
    """Read only whitelisted fields; never export credentials or whole model_config."""
    import sqlite3
    from contextlib import closing
    if not isinstance(session_id, str) or not session_id:
        raise Blocked("Missing session id for subscription provenance")
    try:
        with closing(sqlite3.connect(Path(database).resolve().as_uri() + "?mode=ro", uri=True)) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT id, source, model, parent_session_id, tool_call_count, api_call_count, "
                "billing_provider, billing_base_url, billing_mode, cost_status, "
                "json_extract(model_config, '$.reasoning_config.effort') AS reasoning_effort "
                "FROM sessions WHERE id=?", (session_id,)).fetchone()
    except (sqlite3.Error, OSError, TypeError) as exc:
        raise Blocked("Cannot read subscription session provenance") from exc
    if row is None:
        raise Blocked("Session provenance record missing")
    data = dict(row)
    required = {"id": session_id, "source": "tool", "model": MODEL, "parent_session_id": None,
                "tool_call_count": 0, "api_call_count": 1, "billing_provider": PROVIDER,
                "billing_base_url": "https://chatgpt.com/backend-api/codex",
                "billing_mode": "subscription_included", "cost_status": "included", "reasoning_effort": REASONING}
    for key, expected in required.items():
        if type(data.get(key)) is not type(expected) or data.get(key) != expected:
            raise Blocked("Unverified subscription session provenance: " + key)
    return data


def attempt(argv, destination, cwd, env, timeout=210, session_db=None):
    destination.mkdir(parents=True, exist_ok=False)
    record = {"argv": argv, "started_at": datetime.now(timezone.utc).isoformat(),
              "evidence_kind": "controlled-vignette", "status": "blocked", "scores": None}
    start = time.monotonic()
    with (destination / "stdout.jsonl").open("wb") as out, (destination / "stderr.txt").open("wb") as err:
        try:
            child = subprocess.run(argv, cwd=cwd, env=env, stdout=out, stderr=err, timeout=timeout)
            record["returncode"] = child.returncode
        except subprocess.TimeoutExpired:
            record["returncode"] = None
            record["error"] = f"Hermes timeout after {timeout}s; partial output preserved"
        except OSError as exc:
            record["returncode"] = None
            record["error"] = f"Could not launch Hermes: {exc}"
    record["elapsed_seconds"] = round(time.monotonic() - start, 3)
    if "error" not in record:
        try:
            result = parse_stream((destination / "stdout.jsonl").read_text(encoding="utf-8", errors="replace"),
                                  (destination / "stderr.txt").read_text(encoding="utf-8", errors="replace"),
                                  record["returncode"])
            if session_db is not None:
                record["session_provenance"] = session_provenance(session_db, result.get("session_id"))
        except Blocked as exc:
            record["error"] = str(exc)
        else:
            record.update({"status": "completed-unscored", "tokens": result.get("tokens", {}),
                           "session_id": result.get("session_id"), "answer_words": len(result["text"].split()),
                           "tool_calls": 0, "protocol_duration_ms": result.get("duration_ms")})
            (destination / "answer.txt").write_text(result["text"], encoding="utf-8")
    save_json(destination / "metadata.json", record)
    return record


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if result.returncode:
        raise Blocked(result.stderr.decode("utf-8", errors="replace").strip() or "git failed")
    return result.stdout.decode("utf-8")


def snapshot(repo, ref):
    def selected(path):
        parts = Path(path).parts
        return (len(parts) == 3 and parts[0] == "skills" and parts[2] == "SKILL.md"
                or len(parts) >= 4 and parts[0] == "skills" and parts[2] == "references"
                and parts[-1].endswith(".md"))

    if ref == "none":
        files, resolved = {}, "none"
    elif ref == "working-tree":
        def read_working_tree():
            captured = {}
            for path in sorted((repo / "skills").rglob("*.md")):
                if not selected(path.relative_to(repo)):
                    continue
                if path.is_symlink() or not path.resolve().is_relative_to(repo.resolve()):
                    raise Blocked("Snapshot must not read symlinks or outside-repository files")
                captured[path.relative_to(repo).as_posix()] = path.read_bytes().decode("utf-8")
            return captured
        head = git(repo, "rev-parse", "HEAD").strip()
        files = read_working_tree()
        if read_working_tree() != files or git(repo, "rev-parse", "HEAD").strip() != head:
            raise Blocked("Working-tree changed during snapshot; wait for all writers to finish")
        resolved = "working-tree@" + head
    else:
        resolved = git(repo, "rev-parse", "--verify", ref + "^{commit}").strip()
        paths = git(repo, "ls-tree", "-r", "--name-only", resolved, "--", "skills").splitlines()
        files = {path: git(repo, "show", resolved + ":" + path) for path in paths if selected(path)}
    if ref != "none" and not any(path.endswith("/SKILL.md") for path in files):
        raise Blocked("No skills in selected snapshot")
    canonical = json.dumps(files, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return {"ref": resolved, "sha256": hashlib.sha256(canonical).hexdigest(), "files": files,
            "file_sha256": {path: hashlib.sha256(text.encode("utf-8")).hexdigest()
                            for path, text in files.items()}}


def prompt(scenario, guidance):
    parts = ["This is a controlled decision vignette, not live research. All listed observations "
             "are synthetic fixtures supplied by the evaluator, NOT observations you obtained with tools. "
             "No tools are available. Do not claim to have searched, installed, changed files, or tested anything. "
             "Respond as the assistant at the next turn using the supplied state. "
             "Do not mention grading or this evaluator in your answer."]
    if guidance["files"]:
        parts.append("Apply the following reference skill suite where relevant (all skill bodies are provided, "
                     "so loading a named stage means consulting its body here):")
        parts.extend("<skill path=" + json.dumps(path) + ">\n" + text + "\n</skill>"
                     for path, text in guidance["files"].items())
    parts.extend(["<task>\n" + scenario["task"] + "\n</task>",
                  "<controlled-fixtures>\n" + scenario["fixtures"] + "\n</controlled-fixtures>"])
    return "\n\n".join(parts) + "\n"


class Blocked(RuntimeError):
    """A runtime failure, not a scored model decision."""


def parse_stream(stdout, stderr, returncode):
    if returncode != 0:
        raise Blocked(f"Hermes process exited {returncode}")
    if "fallback" in stderr.lower():
        raise Blocked("Fallback diagnostic observed; routing not trusted")
    try:
        events = [json.loads(line) for line in stdout.splitlines() if line.strip()]
    except (ValueError, TypeError) as exc:
        raise Blocked("Non-JSON stdout; inspect preserved raw transcript") from exc
    if any(not isinstance(event, dict) for event in events):
        raise Blocked("Invalid event object")
    inits = [event for event in events if event.get("type") == "system" and event.get("subtype") == "init"]
    results = [event for event in events if event.get("type") == "result"]
    if len(inits) != 1 or inits[0].get("model") != MODEL:
        raise Blocked("Missing/ambiguous init or model pin mismatch")
    if any(event.get("type") not in ("system", "text", "result") for event in events):
        raise Blocked("Tool/error/unknown event in a no-tools vignette")
    if any(event.get("type") == "system" and event.get("subtype") != "init" for event in events):
        raise Blocked("Unexpected system event; routing not trusted")
    if len(results) != 1 or events[0] is not inits[0] or events[-1] is not results[0]:
        raise Blocked("Exactly one terminal result after init required")
    result = results[0]
    for event in events:
        if event.get("error") or event.get("tool_calls") or event.get("tool_call_count"):
            raise Blocked("Error or tool activity in protocol")
        if "provider" in event and event["provider"] != PROVIDER:
            raise Blocked("Provider pin mismatch")
        if "model" in event and event["model"] != MODEL:
            raise Blocked("Model pin mismatch")
        if event.get("type") == "text" and not isinstance(event.get("text"), str):
            raise Blocked("Invalid text event")
    if inits[0].get("session_id") != result.get("session_id"):
        raise Blocked("Init/result session mismatch")
    if (type(result.get("exit_code")) is not int or result["exit_code"] != 0
            or not isinstance(result.get("text"), str) or not result["text"].strip()):
        raise Blocked("Unsuccessful/empty/invalid terminal result")
    tokens = result.get("tokens", {})
    if not isinstance(tokens, dict) or any(type(value) is not int or value < 0 for value in tokens.values()):
        raise Blocked("Invalid token accounting")
    return result

PROVIDER = "openai-codex"
MODEL = "gpt-6.1-sol"
REASONING = "high"


def command(executable, query_path):
    return [str(executable), "chat", "--provider", PROVIDER, "--model", MODEL,
            "--reasoning", REASONING, "--safe-mode", "--ignore-user-config",
            "--ignore-rules", "--toolsets", "bot_room", "--query-file", str(query_path),
            "--oneshot", "--format", "stream-json", "--max-turns", "2",
            "--run-budget", "180", "--source", "tool"]


def validate_preflight(data):
    required = {"provider": PROVIDER, "api_mode": "codex_responses", "host": "chatgpt.com",
                "source": "device_code", "valid_toolset": True, "tool_count": 0,
                "fallback_count": 0, "cli_fallback_count": 0,
                "model": MODEL, "scheme": "https", "path": "/backend-api/codex",
                "safe_mode": True, "ignore_user_config": True, "ignore_rules": True}
    if not isinstance(data, dict):
        raise Blocked("Invalid preflight object")
    if not isinstance(data.get("session_db"), str) or not data["session_db"].strip():
        raise Blocked("Missing session database for subscription provenance")
    for key, expected in required.items():
        if type(data.get(key)) is not type(expected) or data.get(key) != expected:
            raise Blocked(f"Unsafe/unverified preflight {key}: expected {expected!r}, got {data.get(key)!r}")


def preflight(executable, destination, env):
    import shutil
    resolved = Path(shutil.which(executable) or executable).resolve()
    # This evaluator targets the verified local Windows git installation.
    interpreter = resolved.parent / "python.exe"
    source = resolved.parent.parent.parent
    if not interpreter.is_file() or not (source / "cli.py").is_file():
        raise Blocked("Cannot locate Hermes interpreter/source for read-only preflight")
    argv = [str(interpreter), str(Path(__file__).with_name("preflight.py")), str(source)]
    child = subprocess.run(argv, cwd=source, env=env, capture_output=True, timeout=60)
    (destination / "preflight.stdout.txt").write_bytes(child.stdout)
    (destination / "preflight.stderr.txt").write_bytes(child.stderr)
    if child.returncode:
        raise Blocked("Hermes preflight failed; see preflight.stderr.txt")
    lines = child.stdout.decode("utf-8", errors="replace").splitlines()
    marker = "EVAL_PREFLIGHT_JSON="
    records = [json.loads(line[len(marker):]) for line in lines if line.startswith(marker)]
    if len(records) != 1:
        raise Blocked("Missing/ambiguous routing preflight record")
    data = records[0]
    validate_preflight(data)
    version = subprocess.run([str(resolved), "--version"], env=env, capture_output=True, timeout=30)
    (destination / "hermes-version.txt").write_bytes(version.stdout + version.stderr)
    if version.returncode:
        raise Blocked("Cannot record Hermes version")
    save_json(destination / "preflight.json", data)
    return str(resolved), data


def main(argv=None):
    import argparse
    import os
    import tempfile
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arms", default="baseline,control", help="baseline,control,updated (comma separated)")
    parser.add_argument("--baseline-ref", default="c94a9f6")
    parser.add_argument("--updated-ref", help="Completed immutable revision preferred, or explicit working-tree")
    parser.add_argument("--scenarios", default="local_solution,partial_fit,search_unavailable,authorized_implementation")
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--out", type=Path, required=True, help="New immutable output directory")
    parser.add_argument("--prepare", action="store_true", help="Snapshot/prompt only; no inference or preflight")
    parser.add_argument("--hermes", default="hermes", help="Hermes executable (routing remains pinned)")
    args = parser.parse_args(argv)
    if args.repetitions < 1:
        parser.error("repetitions must be positive")
    root = Path(__file__).resolve().parents[1]
    scenario_path = Path(__file__).with_name("scenarios.json")
    all_scenarios = json.loads(scenario_path.read_text(encoding="utf-8"))
    by_id = {scenario["id"]: scenario for scenario in all_scenarios}
    ids = list(by_id) if args.scenarios == "all" else args.scenarios.split(",")
    arms = args.arms.split(",")
    if len(set(arms)) != len(arms) or len(set(ids)) != len(ids):
        parser.error("duplicate arm/scenario")
    if any(arm not in ("baseline", "control", "updated") for arm in arms):
        parser.error("unknown arm")
    if any(scenario_id not in by_id for scenario_id in ids):
        parser.error("unknown scenario")
    if "updated" in arms and not args.updated_ref:
        parser.error("updated arm requires --updated-ref; do not snapshot unfinished skills")
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=False)
    manifest = {"status": "prepared-not-run", "provider": PROVIDER, "model": MODEL, "reasoning": REASONING,
                "evidence_kind": "controlled-vignette", "live_research": False,
                "planned_calls": len(arms) * len(ids) * args.repetitions, "records": [],
                "created_at": datetime.now(timezone.utc).isoformat(), "arms": arms,
                "scenarios": ids, "repetitions": args.repetitions,
                "scenario_sha256": hashlib.sha256(scenario_path.read_bytes()).hexdigest(),
                "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "repo_status_at_start": git(root, "status", "--short")}
    provenance = args.out / "provenance"
    provenance.mkdir()
    manifest["provenance_sha256"] = {}
    for filename in ["run.py", "preflight.py", "RUBRIC.md", "scenarios.json"]:
        data = Path(__file__).with_name(filename).read_bytes()
        (provenance / filename).write_bytes(data)
        manifest["provenance_sha256"][filename] = hashlib.sha256(data).hexdigest()
    save_json(args.out / "scenarios.json", all_scenarios)
    refs = {"baseline": args.baseline_ref, "control": "none", "updated": args.updated_ref}
    plans = []
    manifest["prompt_sha256"] = {}
    save_manifest(args.out / "manifest.json", manifest)
    try:
        for arm in arms:
            guidance = snapshot(root, refs[arm])
            save_json(args.out / (arm + "-snapshot.json"), guidance)
            for scenario_id in ids:
                for rep in range(1, args.repetitions + 1):
                    relative = Path(arm) / (scenario_id + f"-r{rep}")
                    query = args.out / "prompts" / relative.with_suffix(".txt")
                    query.parent.mkdir(parents=True, exist_ok=True)
                    query.write_bytes(prompt(by_id[scenario_id], guidance).encode("utf-8"))
                    manifest["prompt_sha256"][query.relative_to(args.out).as_posix()] = hashlib.sha256(query.read_bytes()).hexdigest()
                    plans.append((arm, scenario_id, rep, query, relative))
    except (Blocked, OSError, ValueError) as exc:
        manifest.update({"status": "blocked", "error": str(exc), "failure_phase": "preparation"})
        save_manifest(args.out / "manifest.json", manifest)
        print(f"BLOCKED: {exc}; evidence preserved at {args.out}", flush=True)
        return 2
    save_manifest(args.out / "manifest.json", manifest)
    if args.prepare:
        print(f"Prepared {len(plans)} prompts, zero inference calls: {args.out}")
        return 0
    env = os.environ.copy()
    for key in list(env):
        if key.startswith(("HERMES_KANBAN_", "HERMES_EPHEMERAL_")):
            env.pop(key)
    env.update({"HERMES_SAFE_MODE": "1", "HERMES_IGNORE_USER_CONFIG": "1", "HERMES_IGNORE_RULES": "1",
                "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
    scratch = Path.home() / "AppData/Local/hermes/cache/scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    env["TMPDIR"] = env["TEMP"] = env["TMP"] = str(scratch)
    try:
        executable, route = preflight(args.hermes, args.out, env)
        manifest["routing_preflight"] = route
        manifest["status"] = "running"
        save_manifest(args.out / "manifest.json", manifest)
        # Every query is a new process/session; no resume/history/shared conversation.
        with tempfile.TemporaryDirectory(prefix="inherit-eval-", dir=scratch) as cwd:
            for arm, scenario_id, rep, query, relative in plans:
                prompt_path = query.relative_to(args.out).as_posix()
                expected_hash = manifest["prompt_sha256"][prompt_path]
                if hashlib.sha256(query.read_bytes()).hexdigest() != expected_hash:
                    raise Blocked("Prompt changed after preparation; refusing inference")
                prompt_words = len(query.read_text(encoding="utf-8").split())
                record = attempt(command(executable, query), args.out / "transcripts" / relative, cwd, env,
                                 session_db=route["session_db"])
                try:
                    prompt_unchanged = hashlib.sha256(query.read_bytes()).hexdigest() == expected_hash
                except OSError:
                    prompt_unchanged = False
                if not prompt_unchanged:
                    integrity_error = "Prompt changed or disappeared during execution"
                    record.update({"status": "blocked", "prompt_integrity_error": integrity_error,
                                   "error": "; ".join(filter(None, [record.get("error"), integrity_error]))})
                record.update({"arm": arm, "scenario": scenario_id, "repetition": rep,
                               "transcript": (Path("transcripts") / relative).as_posix(),
                               "prompt": prompt_path, "prompt_sha256": expected_hash,
                               "prompt_words": prompt_words})
                manifest["records"].append(record)
                save_json(args.out / record["transcript"] / "metadata.json", record)
                save_manifest(args.out / "manifest.json", manifest)
                print(f"{arm}/{scenario_id}/r{rep}: {record['status']}", flush=True)
                if record["status"] == "blocked":
                    raise Blocked(record["error"])
    except (Blocked, subprocess.TimeoutExpired, OSError, ValueError) as exc:
        manifest.update({"status": "blocked", "error": str(exc)})
        save_manifest(args.out / "manifest.json", manifest)
        print(f"BLOCKED: {exc}; evidence preserved at {args.out}", flush=True)
        return 2
    manifest["status"] = "completed-unscored"
    save_manifest(args.out / "manifest.json", manifest)
    print(f"Completed {len(manifest['records'])} calls; human scoring required: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
