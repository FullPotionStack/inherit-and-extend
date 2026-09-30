---
name: licensing-and-payback
description: Use when a license, reuse question, or dependency has come up — the user wants to know what they owe for using open source, whether they can use something commercially, what attribution is required, or how to give back without open-sourcing their own project.
---

# Licensing and Payback

Two questions that most people answer by guessing: *what am I allowed to do* and *what do I owe*.

## The license is the contract

**No license file means "all rights reserved."** Not public domain. Not free to reuse. Many GitHub repos have no license, and that is a legal fact, not an oversight you can rely on.

| License | What it allows | What you owe |
|---|---|---|
| **Permissive** (MIT, Apache, BSD, ISC) | Use however, including commercially | Keep the copyright notice and license text (NOTICE file or about box). That's it. |
| **Copyleft** (GPL, AGPL) | Use, but derivative works inherit the license | Your project may have to be open-sourced. **Check before building on these.** |
| **Weak copyleft** (LGPL, MPL) | Use in proprietary projects, typically if you keep the licensed part separate | Keep changes to the licensed part under the same license. Often fine commercially. |
| **Public domain / CC0** | Anything | Nothing |
| **Creative Commons** (CC-BY, CC-BY-SA, CC-BY-NC) | Varies — CC-BY-NC bars commercial use, CC-BY-SA is copyleft for creative work | Follow the specific CC terms. Attribution nearly always required. |
| **No license / proprietary** | Reading only, unless stated otherwise | Don't reuse code or assets. Learn from it. |

Apache-2.0 adds an explicit patent grant over MIT. If you're choosing a license for your own project and patent exposure matters, that's the difference.

## Attributing

- **License requires it** — non-negotiable. Include the license text and copyright notice.
- **Significant dependency** — a "Built with" section or acknowledgments page. Good practice even when not required.
- **Someone helped** — a shout-out is manners, not law.

Minimal correct form: *"Uses [Library] ([License]) by [Author]."* Link the repo. Done.

## Paying back without open-sourcing your project

The recurring question: *I used open source in a commercial product. I don't want to release my code. Now what?*

**You don't owe your source code.** Not for MIT, not for Apache, not for BSD. You built on other people's permissive work and sold something — that's how most of the commercial software industry functions. The obligation is the license's, and the form of payback is yours to choose.

| You can | Why it helps |
|---|---|
| Give credit | Often required, always appreciated, sends them discovery traffic |
| Report bugs | Free QA for the maintainer; helps everyone after you |
| File feature requests | You found a gap. Naming it is already a contribution. |
| Donate (GitHub Sponsors, Open Collective, Ko-fi) | Money is the most universally useful contribution. $5-10/month to a project you depend on is real. |
| Write a case study | Social proof drives users, contributors, and funding |
| Answer their questions | You learned it — pass it on in their issues, forum, or Discord |
| Submit a docs PR | Often the weakest part of a project. Zero license implications. |
| Publish your *experience* | "How I used X to build Y" — helps others evaluate it, helps the tool get attention, costs you no IP |
| Open-source an isolated helper | If you built something standalone, releasing that is a clean contribution with no risk to your product |

**What you don't owe:** your project's source (unless strong copyleft actually requires it), free labor on the maintainer's roadmap, or anything the license doesn't say.

## Anti-patterns

| Mistake | Reality |
|---|---|
| "No license means free" | It means no permission. Learn, don't copy. |
| Skipping copyleft checks | GPL in a commercial product can force you to open-source. Check first. |
| "I used MIT, so I owe nothing at all" | Attribution is usually required, and payback is still worth doing. |
| "I must open-source everything I build" | False, and it keeps people from sharing at all. |
| Romanticizing contribution | Useful, not noble. Do it because it helps, not for credit. |
| "I'll contribute later" forever | The finding dies. A quick forum post now beats a planned blog post that never happens. |

## Hand off

- Something worth sharing got built → `contributing-back`
- License blocks the adopt/build decision → return to `evaluating-existing-work` with the constraint
