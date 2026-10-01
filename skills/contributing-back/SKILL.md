---
name: contributing-back
description: Use when the user has built, learned, or shipped something others could benefit from, or asked about publishing, open-sourcing, sharing, or where to post something — including when they want it to be easy rather than a whole project.
---

# Contributing Back

Make sharing cheap. That's the whole job.

**Optional. Never pressure.** A suggestion, not a requirement. Contribution must not delay shipping.

## Straight talk

- You used their public work. Paying that forward is fair, not heroic.
- Your mistakes are someone else's shortcut.
- Good solutions get rediscovered. Making yours findable saves time.
- The goal is not to be a hero. It's to stop the next person losing an afternoon.

## Pick the lowest-friction channel that fits

| Channel | Fits | Effort |
|---|---|---|
| **GitHub repo or gist** | Code, configs, scripts, skills | Low — push, share link |
| **Skill publishing CLI** | Agent skills for 40+ harnesses — `npx publish-skills publish`, or GitHub's `gh skill` | Low — one command, PR-based |
| **Stack Overflow answer** | A specific problem you solved | Low — answer an existing question |
| **Twitter/X, LinkedIn** | Short summary + link | Low — a few sentences |
| **Reddit / specialist forum** | A specific community that needs this | Low-Medium |
| **Dev.to / Hashnode / Medium** | "How I did X", lessons learned | Medium |
| **Docs PR to a project you use** | Confusing documentation | Low — no code shared, pure value |
| **Personal blog** | Ongoing documentation | Medium-High — ongoing cost |
| **Upstream contribution** | A real bug or gap you found | Medium-High — PR process |

Publishing a skill publicly does **not** require your product's code to be public. Those are separate decisions with separate licenses. See `licensing-and-payback`.

## Minimum viable share

Polish is optional. These four things make a useful post:

1. **What problem** you were solving
2. **What you tried** — including what didn't work (usually the most valuable part)
3. **What worked**, or what you'd do differently
4. **Links** to what helped you (credit where due)

## Keep it light

- Don't wait for perfect. A rough share beats a planned one that never ships.
- A screenshot and a paragraph is often enough.
- "Here's what I tried, here's what worked, here's what I'd do differently" is a complete contribution.
- Small finding → forum post or SO answer. Not a blog.
- Ship first, share after.

## Contributing to a project you depend on

If the goal is helping a project you use rather than announcing your own work, the prior art is well trodden and worth naming:

| Looking for | Go to |
|---|---|
| Beginner-friendly issues | GitHub search with `label:"good first issue"`, or `label:"help wanted"` |
| Curated first-PR lists | [up-for-grabs.net](https://up-for-grabs.net), First Timers Only, CodeTriage |
| Docs gaps | Usually the fastest first PR, and almost always welcome |

Naming these beats improvising a search strategy.

## Distributing across many channels at once

Posting the same thing to LinkedIn, X, Dev.to and Reddit by hand is the tedious part people give up on. If the user wants one input to become several channel-tailored posts, tools already exist and are worth checking before writing anything:

- **[Postiz](https://postiz.com)** — open source, self-hosted, 30+ channels, ships an MCP server, explicitly supports Hermes Agent. Handles publishing and scheduling.
- Anything that drafts per-channel copy from one input, which is the layer above Postiz rather than a competitor to it.

Drafts get reviewed by a human before they go out. Never auto-post.

## Don't

- Force it. Pick your battles; not everything is worth posting.
- Share anything proprietary, private, or under someone else's NDA.
- Elaborate documentation for a small finding.
- Tell the user "just push to GitHub" without checking whether a publishing CLI already does it for them — the Agent Skills standard (`agentskills.io`) has tooling for exactly this, and it works across 40+ harnesses.

## Hand off

- Unsure whether you may share at all, to `licensing-and-payback`
- Nothing built yet, back to `finding-existing-work`
