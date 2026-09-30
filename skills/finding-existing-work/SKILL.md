---
name: finding-existing-work
description: Use when a user presents an idea, solution, or build goal and the priority is discovering what already exists for it — searching prior art, tools, libraries, tutorials, and prior attempts before any implementation happens.
---

# Finding Existing Work

Find what already exists, understand it, and hand the user a decision. Do not implement anything here.

## Search depth

Pick a level and stay there. The user chooses by budget, not complexity.

| Level | Fits | Cost | Output |
|---|---|---|---|
| **0** Minimal | Tight token budget, "just check real quick" | 2-3 searches, ~50-100 tokens | Exists or not, 1-2 pointers |
| **1** Standard *(default)* | Most situations | 3-5 searches, ~200-400 tokens | Synthesized findings with links |
| **2** Deep | Tokens are cheap, high stakes, novel territory | 5-10+ searches, reads key sources, ~500-1500+ tokens | Landscape, trade-offs, failure modes |

Override phrases: "quick check" → 0, "go deep" → 2, "standard" → 1. Ambiguous → 1.

## Where to look

1. **GitHub** — repos, and issues as much as repos. Issues reveal the pain.
2. **Web** — tutorials, blog posts, forum threads (Reddit, Stack Overflow, HN, specialist forums)
3. **Package registries** — npm, PyPI, RubyGems, Cargo
4. **Docs** — official documentation for the tools in play
5. **Papers** — for research-adjacent ideas
6. **Community** — Discords, Slacks, subreddits for the domain

Load `domain-playbooks` when the domain isn't software-generic.

## What to look for

Finding a link isn't research. Understand it:

- **What exists** — approaches, implementations, products
- **How they did it** — architecture, decisions, trade-offs
- **Whether it worked** — adoption, maintenance, known issues
- **What failed** — dead ends, bug threads, frustrated write-ups
- **The landscape** — many options, or unexplored territory?

## Output: the Brief

Default output. A full breakdown is opt-in. Producing both wastes tokens the user didn't ask to spend.

```
## Brief
[2-3 lines: what exists, the gap, should you proceed?]

| | |
|---|---|
| **Exists?** | yes / partial / no |
| **Who does it** | 2-4 players, one line each |
| **The gap** | one line — what nobody has done |
| **Verdict** | adopt / extend / build, and why in one clause |

Full breakdown available on request.
```

Target 150-200 words. If it doesn't fit a table, it doesn't belong in the Brief.

**Rules:** one or the other, never both in the same turn. Lead with the verdict. "Nothing exists" stated in one line is a complete answer. The user's attention is the scarce resource, not your context window.

## Anti-patterns

| Mistake | Reality |
|---|---|
| Searching but not analyzing | A link is not research. Understand and judge relevance. |
| One source only | GitHub alone misses forums, tutorials, papers. |
| Only exact matches | Related work teaches you. A Rust habit tracker teaches architecture even if you use Python. |
| Ignoring failures | What didn't work is as valuable as what did. |
| "Nothing exists" from a shallow search | Empty results are weak evidence. Try synonyms — you may not know what it's called. |
| Research as procrastination | Research informs building; it doesn't replace it. Set a boundary, move on. |
| Over-searching | Level 0 or 1 covers most ideas. Match effort to stakes. |

## Hand off

- Candidates found → `evaluating-existing-work`
- Licenses or reuse came up → `licensing-and-payback`
- Novel idea worth sharing later → `contributing-back` (after it's built)
