# inherit-and-extend

A skill suite for AI coding agents. Find what already exists, evaluate it honestly, respect the license, and pass improvements forward.

MIT licensed. Works with any harness that reads `SKILL.md` — Claude Code, Cursor, Codex, Gemini CLI, Hermes Agent, and others following the [Agent Skills](https://agentskills.io) standard.

---

## The problem

Agents are biased toward action. Ask for a scraper and you get a scraper. Ask for a parser and you get a parser. The default is *generate*, not *evaluate* — so wheels get reinvented, maintenance debt accrues, and the same bug gets debugged by everyone separately.

This suite inserts a decision point before implementation, and a contribution path after it.

## The pipeline

```
using-lookup              dispatch only, does no work itself
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

Start with `using-lookup` — it's the bootstrap. The rest are reached through it.

## The skills

| Skill | Does | Loaded when |
|---|---|---|
| `using-lookup` | Dispatches to the right stage. Never researches. | Always consulted when the user presents an idea |
| `finding-existing-work` | Search depth levels, where to look, the Brief output format | Before any implementation |
| `evaluating-existing-work` | Adopt vs build, bias in partial solutions, cost of being wrong | Once candidates exist |
| `licensing-and-payback` | License types, obligations, attribution, 9 payback methods | When reuse or a dependency comes up |
| `contributing-back` | 7 channels, minimum viable share, low-friction rules | After something is built |
| `domain-playbooks` | Where practitioners post, per domain | When generic sources aren't enough |

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
