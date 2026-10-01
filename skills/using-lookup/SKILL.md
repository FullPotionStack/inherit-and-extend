---
name: using-lookup
description: Use at the moment code is about to be written, a tool chosen, a file created, or an approach settled — before implementation starts, to check whether a maintained solution already exists and should be reused instead of rebuilt.
---

# Using Lookup

**Role: dispatch only.** This skill never searches, evaluates, or writes. It decides which stage of the pipeline applies and hands off.

## When to Use

This is a **self-check, not a keyword match.** Fire it at the moment you are about to do any of these:

- Write implementation code
- Pick a library, package, or tool
- Create a file, script, or config
- Settle on an approach and start executing it
- Debug something from scratch when a known fix might exist

You do **not** need the user to have announced an intent to build. Most of the time they haven't. The trigger is your own next action.

Typical moments this fires, none of which involve the user saying "I'm building something":

- About to hand-roll a parser, client, or retry loop
- About to pick a library and start wiring it up
- About to write a config file from scratch
- Answering a bug by patching rather than by finding the known fix

**Skip when:**

- The task is purely mechanical (formatting, renaming, running a command)
- The user says "just do it" or "skip the research"
- The user explicitly wants to build from scratch to learn it
- A previous stage in this conversation already ran

**Never skip because it seems obvious.**

"I already know how to build this" is the most common reason this stage gets dropped, and the worst one to trust. Knowing how to do something is not the same as knowing that a maintained, better, already-shipped version exists. That gap is where the cost hides: a hand-rolled PDF parser when `pypdf` exists, a scraper when a scraping API does it in two minutes, a from-scratch state machine when a library has already debugged the edge cases.

The situations that feel most confident to skip are the ones with the most existing solutions. Difficulty of implementation and how much already exists are not correlated — the boring problems are usually the solved ones.

If a research check still seems like a waste of a minute, the cheapest possible check is justified. Level 0 exists exactly for this: 2-3 searches, one-line answer, move on. You are not choosing between researching deeply and skipping. You are choosing between a minute of verification and a possible afternoon of debugging someone else's solved bug.

## Re-check when the shape of the work changes

A check you did once does not cover work that has since been restructured. This is the failure mode that produced this suite: prior art was checked for the whole, then the whole was split into six parts, and none of the six were checked. The most crowded part was the one nobody looked at.

Re-run the check when:

- The work gets split, merged, or restructured. **Every new piece needs its own check, not the parent's.**
- A stage is added or removed.
- You are about to build something at a scale, domain, or in a language you did not check at that scale before.
- Time has passed. Prior art moves, and things that were new become standard.

This applies to the suite itself. Each stage below carries its own prior-art check, and the honest summary lives in `PRIOR-ART.md` at the repo root. If you extend the suite, extend that file in the same commit. A skill that preaches searching for existing work and does not search for existing work is worse than one that never existed, because people trust it.

## Dispatch table

| Situation | Load next |
|---|---|
| User presents an idea; nothing found yet | `finding-existing-work` |
| Candidates found; deciding adopt vs build | `evaluating-existing-work` |
| A license, reuse, or dependency came up | `licensing-and-payback` |
| User built something and it might help others | `contributing-back` |
| Search needs domain-specific sources | `domain-playbooks` |

Stages chain: `finding-existing-work` → `evaluating-existing-work` → (`licensing-and-payback`) → (`contributing-back`).

**Load only the stage the current situation needs.** Pulling a later stage before its trigger wastes context and encourages acting on assumptions.

## Rules

- Dispatch on the user's words, not on what seems useful. If they asked "does X exist?", that's a lookup, not a build plan.
- If two stages apply, run them in order. Don't skip `evaluating-existing-work` because the first candidate looks good — that's exactly the assumption that stage exists to check.
- Stop dispatching once the pipeline reaches a decision. Hand the decision back to the user; don't continue into implementation.

## Suite

`inherit-and-extend` — find what exists, evaluate it, respect the license, and pass improvements forward.
