# inherit-and-extend

Agent skills that make an agent check whether something already exists before it builds it.

Ask for a PDF parser and a naive agent writes one. This suite makes it search first, then hand you a decision: **adopt what's out there, extend it, or build your own.**

It never installs anything and never starts implementing. The output is a verdict and a link. What you do with it is yours.

MIT licensed. Works with any harness that reads `SKILL.md` — Claude Code, Cursor, Codex, Gemini CLI, Hermes Agent, and others following the [Agent Skills](https://agentskills.io) standard.

---

## The problem

Agents are biased toward action. Ask for a scraper and you get a scraper. Ask for a parser and you get a parser. The default is *generate*, not *evaluate* — so wheels get reinvented, maintenance debt accrues, and the same bug gets debugged by everyone separately.

This suite inserts a check before implementation, and a contribution path after it.

## When it fires

**On the agent's action, not on your announcement.** You don't have to say "I'm building something." It triggers at the moment code is about to be written, a library is about to be chosen, or a config is about to be created — the point where a two-minute search can save an afternoon.

## The pipeline

```
using-lookup              fires as implementation is about to start
     │
     ▼
finding-existing-work     search depth, sources, output format
     │
     ▼
evaluating-existing-work  adopt / extend / compose / build
     │
     ├──► licensing-and-payback   when a license or reuse question comes up
     │
     └──► contributing-back       once something is built worth sharing
     
domain-playbooks          loaded on demand, any stage
```

Each skill loads only when its situation occurs. A typical run touches two; a licensing question might touch three. Nothing loads speculatively.

## What you get

Not an essay — a verdict:

```
## Brief
[2-3 lines: what exists, the gap, should you proceed?]

| | |
|---|---|
| **Exists?** | yes / partial / no |
| **Who does it** | 2-4 players, one line each |
| **The gap** | one line — what nobody has done |
| **Verdict** | adopt / extend / build, and why in one clause |
```

Ask for the full breakdown if you want it. You aren't paying for research you didn't ask for.

## Install

```bash
git clone https://github.com/FullPotionStack/inherit-and-extend.git
```

Copy the folders you want into your skills directory:

| Harness | Path |
|---|---|
| Claude Code | `~/.claude/skills/` or `.claude/skills/` |
| Hermes Agent | `~/.hermes/skills/` |
| Cursor | `.cursor/skills/` |
| Codex / Gemini CLI | `~/.agents/skills/` |

Or use the Agent Skills CLI, which detects your agents automatically:

```bash
npx skills add FullPotionStack/inherit-and-extend
```

Install all six. `using-lookup` is the entry point; the rest are reached through it.

## The skills

| Skill | Does |
|---|---|
| `using-lookup` | Fires as implementation starts, then dispatches. Never researches itself. |
| `finding-existing-work` | Search depth levels, where to look, the Brief output format |
| `evaluating-existing-work` | Adopt vs build, bias in partial solutions, cost of being wrong |
| `licensing-and-payback` | License types, obligations, attribution, nine payback methods |
| `contributing-back` | Seven channels, minimum viable share, low-friction rules |
| `domain-playbooks` | Where practitioners post, per domain |

## Design decisions

**The Brief is the default output.** Verdict first, a four-row table, 150-200 words. The full breakdown exists but is opt-in. Producing both in one turn wastes tokens the user didn't ask to spend — a lesson this suite learned by violating it.

**Search depth is set by budget, not complexity.** Levels 0/1/2 exist because token cost is the thing users actually reason about. Pick one and stay there.

**Payback is not open-sourcing your project.** Using MIT code in a commercial product and keeping your own source closed is legitimate and normal. The suite explains what each license actually obligates you to, and gives nine payback options that don't touch your IP.

**The suite is domain-agnostic.** Most "search before building" skills assume software. The approach is identical whether you're choosing a game engine, a study path, or a Terraform module, so the playbooks cover all of them equally.

## Related work

- [`search-first`](https://github.com/affaan-m/everything-claude-code) — Claude Code skill, coding-specific, strong decision matrix
- [`openclaw-skill-hunter`](https://github.com/mturac/skill-hunter) — "search before build" for OpenClaw
- [Morrison-Lab's `dont-reinvent-wheel`](https://github.com/Morrison-Lab/ai-config/blob/main/shared/principles/dont-reinvent-wheel.md) — a well-developed internal principle doc

This suite differs by being domain-agnostic, budget-aware, and covering the contribution and licensing side that the others don't.

## Contributing

Issues and PRs welcome. If you add a domain playbook, keep it to *where people actually post* — sources, not tutorials. That's the part that goes stale, and sources are what stays useful.

MIT. See [LICENSE](LICENSE).
