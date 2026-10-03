# Running the evaluator

Internal operator notes: reproduce controlled decision vignettes and preserve the evidence for manual review. Nothing here installs the skills or changes Hermes configuration.

## What it does

`run.py` is Python stdlib only. It snapshots the original suite with `git show`, writes exact prompts, starts one fresh Hermes process per answer, and saves untouched stdout JSONL/stderr plus extracted answer and run metadata. All observations embedded in `scenarios.json` are controlled synthetic fixtures, not research results. The runner does no automatic behavioral scoring; use `RUBRIC.md`.

Only `openai-codex/gpt-6.1-sol`, high reasoning, is supported. Routing is checked before inference: exact startup model (no alias/endpoint override), OAuth `device_code`, HTTPS `chatgpt.com/backend-api/codex`, `codex_responses`, no fallback in either CLI or shared config, and zero tools for the `bot_room` selection. Guards check both values and JSON types. `--safe-mode --ignore-user-config --ignore-rules` excludes profile config, preloaded skills, memory, project rules, plugins, and MCP. Inherited kanban/ephemeral prompt variables are removed. The normal Hermes base prompt and shared OAuth credential storage remain; this is a no-suite-guidance control, not a bare model API call.

After each successful protocol result, the runner reads only whitelisted fields from the matching Hermes session record using SQLite `mode=ro`. Completion additionally requires the pinned model/provider, high reasoning, subscription-included billing at the expected endpoint, a fresh parentless session, one reported API call and zero tools. Missing or inconsistent session provenance blocks the run; it is not treated as free inference or a behavioral failure. This is a framework-record audit, not independent packet capture or invoice verification.

The preflight currently targets the verified Windows git-installed Hermes layout (`venv/Scripts/hermes.exe` with adjacent `python.exe` and source above the venv). A changed installation/auth source fails closed; inspect the actual route before updating support. No credentials are printed. Do not substitute `--toolsets ''`: source inspection showed that an empty value restores platform defaults rather than disabling tools.

## Commands (Windows Git Bash, repo root)

```bash
cd look-before-build

# Mechanical tests; no model inference.
python3 -B -m unittest discover -s tests -p test_eval_runner.py -v

# Default small pilot: four scenarios, baseline then control, one fresh call each.
# Output directory must not already exist. Use a new run name for every invocation.
python3 -B evals/run.py --arms baseline,control \
  --baseline-ref c94a9f6 \
  --out evals/runs/baseline-control-next

# Prepare prompts/snapshots without preflight or inference.
python3 -B evals/run.py --prepare --arms baseline,control \
  --scenarios all --out evals/runs/all-scenarios-prepared-next

# AFTER all sibling edits are finished: updated arm on the same pilot.
# Explicit working-tree snapshot is saved and hashed; no automatic rolling reads.
python3 -B evals/run.py --arms updated --updated-ref working-tree \
  --scenarios local_solution,partial_fit,search_unavailable,authorized_implementation \
  --out evals/runs/updated-smoke-next
```

Prefer replacing `working-tree` with a completed immutable git revision, if one is available. Do not commit just to run this evaluator when commits have not been authorized. Do not run the updated arm on half-written files. A new run cannot overwrite an earlier evidence directory.

For a narrower follow-up, supply comma-separated IDs with `--scenarios`. `--repetitions` is explicit and defaults to one. `--scenarios all` is a coverage expansion, not the default. Confirm the subscription budget before expanding to replication (at least five fresh calls per variant for wording claims); a single pilot cannot establish variance or improvement. Reverse arm order in a separate run to probe order effects.

## Artifacts

Each output directory contains:

- `manifest.json`: exact provider/model/reasoning, hashes, scenario IDs, status and per-call metrics. `planned_calls` is intent, not executed coverage. `attempted_processes`, `completed_records`, `blocked_records` and `pending_plans` are separate counts; attempts include launch failures and cannot alone establish inference cost. A completed run stays `completed-unscored` until an external reviewer creates scoring records.
- `baseline-snapshot.json`, `control-snapshot.json`, or `updated-snapshot.json`: exact supplied skill bodies **and Markdown under each skill's `references/`**, source ref, per-file hashes and canonical content hash. Working-tree capture compares two reads and HEAD to reject detected concurrent edits; it is not an atomic filesystem lock, so finish writers first.
- `provenance/{run.py,preflight.py,RUBRIC.md,scenarios.json}`: exact source bytes used to prepare the run, with hashes in the manifest. The pretty-printed scenario copy is not substituted for original source bytes.
- `scenarios.json`: versioned copy of the task/fixtures/rubrics; rubric fields are **not** placed in model prompts.
- `prompts/<arm>/<scenario>-rN.txt`: exact UTF-8 query files passed without shell interpolation.
- `transcripts/<arm>/<scenario>-rN/{stdout.jsonl,stderr.txt,answer.txt,metadata.json}`: actual process output and protocol status. `answer.txt` exists only for a successful checked result.
- `preflight.json`, `preflight.stdout.txt`, `preflight.stderr.txt`, `hermes-version.txt`: routing/tool guard and installed version provenance.

Prompts go into the query file, never an interpolated shell command. Subprocesses use argument lists and a scratch working directory under `AppData/Local/hermes/cache/scratch`, with no resume or conversation history. Their normal Hermes session records may still be saved by the CLI; this evaluator does not delete or modify those records.

A preparation/runtime/auth/protocol/provenance failure stops the run immediately with exit status 2 and a blocker in the manifest. Raw partial output is retained. The stream guard accepts only init, text deltas and one final successful result, rejects errors/tools/unknown events, checks session consistency and rejects any emitted provider/model mismatch. Prompts are hashed before inference and checked before/after each process; changed or missing prompts block attribution, including after an attempted launch. If late integrity checking blocks an otherwise parsed answer, the extracted answer remains evidence, **not** a scorable successful record. Do not count a blocker as a behavioral failure, synthesize a replacement answer, or switch to another provider/model. Missing token counts are missing accounting, not zero cost.

## Coverage and limits

The 14-scenario catalog covers local reuse, popular partial mismatch, unavailable versus empty search, a new unrelated task, learning exemption, sanitized public query, study/creative precedents, authorized continuation versus research-only boundary, license distribution differences, and quick/deep answer shapes. Catalog coverage is not executed coverage; the default pilot exercises only the four named scenarios.

This evaluator cannot verify real outbound search queries, real dependency fitness, actual edits, or code execution by the model. Those require a separately authorized end-to-end sandbox. Any manual execution of code from a vignette is a check of the proposed artifact, not proof that the model used tools or completed the original project task.

## Preserved pilot and final updated review

`runs/baseline-control-smoke-1` has eight real completed records: four baseline and four control, one repetition each. The original evidence is unchanged. Derived audit and scoring live separately under `reviews/baseline-control-smoke-1-review-1/`:

- `audit.json` and `source-integrity.json`: checked prompt/snapshot/protocol consistency, raw evidence hashes, and matching read-only session routing/billing records. Each original session reports `openai-codex/gpt-6.1-sol`, high reasoning, `subscription_included`, one API call and zero tools; historical preflight reports zero fallbacks and no fallback diagnostics were observed.
- `scores.json`: manual **model-judged, nonblind** rubric review, not an independent human score or automatic behavior pass. All eight answers received 2 on each of the four dimensions, with quotes/rationales and no observed critical failure. This is a ceiling pilot, not evidence that either suite improves behavior.
- `artifact-checks/`: reviewer-extracted `parse_labels` snippets and actual passing regression-test output for both arms. This does not mean the model edited or tested the repo.

The original run records hashes/revision but did not archive its runner/preflight source bytes. New runs archive those bytes. Routing/billing evidence is framework-reported, not independent wire capture or subscription invoice audit. No additional model inference was needed for this review.

`runs/updated-all-final-1` now contains exactly one updated repetition for all 14 scenarios: 14 completed, zero blocked or pending. No baseline/control call was repeated. The working-tree suite was frozen before snapshot capture; `updated-snapshot.json` preserves all six bodies and four domain references. Framework session checks confirm 14 distinct parentless sessions, each `openai-codex/gpt-6.1-sol`, high reasoning, subscription-included at the expected endpoint, one reported API call and zero tools; preflight reports zero fallbacks.

The local derived final review, `scores.json`, `audit.json`, and `matched-comparison.json` preserve absolute source paths, hashes, quote evidence, and mechanical results. Raw transcripts and session-specific reviews are deliberately not distributed in this repository; this summary cannot substitute for independent reproduction. Scores are **nonblind model-judged**, not independent human or automatic behavior passes. No critical failure was observed. Thirteen answers received 2 on all four dimensions; `research_only` received overhead 1 for repeated reporting. All four matched scenarios retain baseline/control/updated rubric ceiling, so **no measured improvement is demonstrated**. Ten updated-only scenarios have no comparator.

A final provenance check exposed Windows text-mode newline translation in the archived runner: existing CRLF skill lines became CRCRLF in query files, creating extra blank lines on read. Exact query bytes and hashes remain preserved, and their non-whitespace content matches the saved suite/task/fixtures. `run.py` now writes prompt UTF-8 bytes directly; a failing-then-passing preparation regression verifies exact bytes. This correction happened **after** the 14-call run; its provenance archives the old runner, and the fixed runner has not been inference-tested. No evidence directory was rewritten and no extra inference was launched.

The apparent `checking ***` prose in tool output was tool-output redaction, not a damaged source file: byte-level review confirms the original object is `existence` and no literal triple asterisk is present. A temporary wording change was reverted before the immutable snapshot. The focused regression catches a deliberately damaged scratch copy.

All 14 catalog scenarios have updated-arm vignette output, but real outbound privacy, live discovery/fitness/license work, actual edits/model execution, automatic invocation, on-demand prompt loading, and repeated-trial variance/order effects remain unverified. The evaluator deliberately injects the entire suite and references, so these trials do not measure compact on-demand runtime; matched updated prompt words were 18,802 versus baseline 17,074 and control 606. Answer words were 469, 387, and 337 respectively. These descriptive single-run counts do not establish efficiency or latency effects. Replication or end-to-end runs require fresh explicit authorization; do not rerun completed directories or replace valid evidence.
