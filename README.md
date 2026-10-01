# inherit-and-extend

Ask an agent for a PDF parser and it will write one, every time. Most of the time a maintained library already does that job better, and the agent has no reason to go looking.

This suite makes it look first, then hand you a decision.

It does not install anything and it does not start writing code. You get a verdict and some links, and you decide what happens next.

MIT. Works with anything that reads `SKILL.md`, which includes Claude Code, Cursor, Codex, Gemini CLI and Hermes Agent. They all follow the same [Agent Skills](https://agentskills.io) format.

---

## Why it exists

Ask for a scraper, get a scraper. Ask for a parser, get a parser. Generating is the easy move, so that is the move agents make. The cost shows up later: hand-rolled code that needs maintaining, bugs other people already hit and fixed, and a week of debugging something that shipped in 2019.

## When it kicks in

On what the agent is about to do, not on what you said. You do not have to announce an intention to build anything. It fires right before code gets written, a library gets picked, or a config file gets created.

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

Each skill loads when its situation comes up, not before. Most runs touch two. A run that hits a licensing question might touch three.

## Sample output

Every run answers in this shape. Around 150 to 200 words, and the table is the whole thing:

| Question | Answer |
|---|---|
| Does something exist already? | yes, partial, or no |
| Who has done it? | two to four options, one line each |
| What has nobody done? | the gap, in one line |
| So what do I do? | adopt it, extend it, or build it, and why in a clause |

If the brief is not enough, ask and you get the full breakdown. The suite will not hand you both at once, because that is tokens spent on something you did not ask for.

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

There is also a CLI that detects your agents for you:

```bash
npx skills add FullPotionStack/inherit-and-extend
```

Take all six. `using-lookup` is the one that starts things off and the rest get reached through it.

## What's in the box

| Skill | Job |
|---|---|
| `using-lookup` | Fires as implementation starts, then hands off. Never researches on its own. |
| `finding-existing-work` | Search depth, where to look, the output format above |
| `evaluating-existing-work` | Whether to adopt or build, and what a partial match is really telling you |
| `licensing-and-payback` | What each license requires, plus nine ways to give back that keep your source closed |
| `contributing-back` | Seven places to post something, and how little effort each one takes |
| `domain-playbooks` | Where people in each field actually talk |

## Choices worth explaining

The brief is the default output and the full write-up waits until you ask for it. This suite learned that one by breaking it, which is worth saying plainly given that it now argues for the behavior it got wrong.

Search depth is set by how many tokens you want to spend, not by how hard the problem looks. Three levels, pick one, stop thinking about it. Difficulty and how much already exists turn out to be unrelated, and that is the argument for checking either way.

Paying back does not mean open-sourcing your project. Using MIT code in a commercial product while keeping your own source private is what most of the industry does. The skill covers what the license actually obligates you to, plus ways to give back that do not touch your IP.

It works outside software. Most "search before building" skills assume code. Picking a game engine, a study path or a Terraform module is the same decision, so the playbooks cover all of them.

## Similar things

- [`search-first`](https://github.com/affaan-m/everything-claude-code) for Claude Code. Coding only, though it has a scoring matrix worth borrowing.
- [`openclaw-skill-hunter`](https://github.com/mturac/skill-hunter) does this for OpenClaw.
- [Morrison-Lab's `dont-reinvent-wheel`](https://github.com/Morrison-Lab/ai-config/blob/main/shared/principles/dont-reinvent-wheel.md) is a good internal doc if you have an internal.

This one goes further on the licensing and contribution side, and it is not tied to code.

## Contributing

PRs welcome. If you write a playbook, stick to where people post rather than tutorials. Sources stay useful for years, tutorials go stale.

MIT, see [LICENSE](LICENSE).
