# Prior art, per stage

The check this suite exists to enforce, applied to itself. Every stage was searched before it was written. Most were searched badly, or late, or both, and that is recorded here rather than quietly fixed.

Update this file in the same commit that adds or changes a stage. A skill about searching for existing work that does not track its own is the exact failure it warns against.

Last full pass: 2026-09-30

---

## `using-lookup`

**Occupied, and the convention is borrowed on purpose.** Superpowers uses `using-*` for a dispatch-only bootstrap. That is the pattern this stage follows.

- `superpowers:using-superpowers` — the closest structural match
- Any harness that gates skills behind a bootstrap

**Verdict:** keep. The name follows an existing convention rather than inventing one.

---

## `finding-existing-work`

**The most crowded stage.** It is first because that is where the value is, and the crowding is a reason to be good rather than a reason to leave.

- [`search-first`](https://github.com/affaan-m/everything-claude-code) (affaan-m) — five-phase workflow, decision matrix for scoring candidates. Coding-focused: npm, PyPI, MCP, GitHub.
- [`openclaw-skill-hunter`](https://github.com/mturac/skill-hunter) — "search before build" for OpenClaw. Closest in motivation, narrowest in scope.
- [`dont-reinvent-wheel`](https://github.com/Morrison-Lab/ai-config/blob/main/shared/principles/dont-reinvent-wheel.md) (Morrison-Lab) — a long, well-developed internal principle doc. Project-internal rather than general.

**Verdict:** keep. All three are software-only and none cover the brief-format or budget-level parts. The domain-agnostic angle is the differentiator.

---

## `evaluating-existing-work`

**Thinnest prior art of the six, and the most defensible one.**

The build-vs-buy literature is large and aimed at enterprise buyers:

- [Bizz — build vs buy AI agent stack](https://www.bizz.ai/blog/build-buy-ai-agent-stack-differentiation-control-tco) — four outcomes including adopt-with-ownership. TCO framing.
- [Agentplace — build vs buy vs borrow](https://agentplace.io/blog/build-vs-buy-vs-borrow-strategic-framework-for-agent-platform-decisions) — systematic framework, agent-platform decisions.
- [Windward](https://www.windwardstudios.com/blog/build-buy-framework-development) — the general software version of the same question.

All of them are written for someone with a procurement spreadsheet. None addresses bias in a partial match, the cost of being wrong, or what to do when the thing you found is 80% right and the 20% is what you care about.

**Verdict:** keep. This is where the suite is most clearly not a duplicate.

---

## `licensing-and-payback`

**Was the weakest link, and nobody knew until 2026-09-30, when the check finally ran.** Recorded here because the miss is the lesson.

What exists:

- [ORT](https://github.com/oss-review-toolkit/ort) and the [AboutCode](https://aboutcode.org) toolkit — the real compliance infrastructure. Apache-2.0. Do not hand-audit a dependency tree.
- [`license-checker`](https://github.com/policiescans/license-checker) for npm, wired into CI
- AI Compliance Notice Generator, melodic-software's `license-compliance`, `dependency-auditor` in [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) (26k stars), Anthropic's Open Source License Review — several skills already doing NOTICE generation, SBOM, and CI gates
- [Finite State on OSS compliance](https://finitestate.io/blog/open-source-license-compliance) — the best prose treatment of license families and obligations

What none of them cover: how to give back while keeping your own project closed, and the fact that doing so is legitimate rather than a compromise.

**Verdict:** rewired. The skill no longer explains compliance mechanics from scratch. It points at ORT, AboutCode, `license-checker`, and the notice generators, and keeps only the payback half, the commercial framing, and read-the-license-first.

---

## `contributing-back`

**Partial prior art, previously unattributed.**

- The first-contribution path is well trodden: `good first issue` and `help wanted` labels, [up-for-grabs.net](https://up-for-grabs.net), First Timers Only, CodeTriage
- [`publish-skills`](https://github.com/jindalAnuj/publish-skills) and GitHub's [`gh skill`](https://github.blog/changelog/2026-04-15-manage-agent-skills-with-github-cli) cover skill publishing across 40+ harnesses
- [Postiz](https://postiz.com) — 30+ channels, self-hosted, MCP server, explicit Hermes support. Publishing and scheduling, done properly by someone else.

**Verdict:** rewired to name all of the above. Kept the per-channel effort table, the minimum-viable-share framing, and the payback ranking, none of which have an equivalent.

---

## `domain-playbooks`

**Thin. The gap is real.**

- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) and [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) both carry domain-specific skills across engineering, compliance, research, and marketing
- Nothing found covers **non-software** domains as playbooks: games, study paths, infrastructure, creative work

**Verdict:** keep. The non-software angle is the point of the stage.

---

## What the miss taught

The suite checked prior art once, for the whole thing, before it was six separate things. Then it split without re-checking, and the stage with the most competition in it was the one nobody looked at.

That is the failure this skill exists to prevent, happening inside the skill.

The rule that came out of it now lives in `using-lookup`: when work is split, merged, or restructured, every new piece gets its own check rather than inheriting the parent's.
