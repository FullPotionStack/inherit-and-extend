---
name: licensing-and-payback
description: Use when a license, reuse question, or dependency has come up — the user wants to know what they owe for using open source, whether they can use something commercially, what attribution is required, or how to give back without open-sourcing their own project.
---

# Licensing and payback

Two questions people usually answer by guessing: what am I allowed to do, and what do I owe.

This skill does the second one properly. For the first, it tells you which tool to use instead of re-explaining it badly.

## Use a tool for the audit. Do not eyeball it.

License compliance has real tooling. It is mature, it is free, and it reads manifests you would have to read by hand. Checking manually means missing a transitive dependency, which is the whole failure mode.

| Need | Use |
|---|---|
| Audit a full dependency tree, generate a report | [ORT](https://github.com/oss-review-toolkit/ort) (Apache-2.0), or [AboutCode](https://aboutcode.org)'s toolkit |
| npm projects | `license-checker`, wired into CI |
| Generate NOTICE / THIRD-PARTY-NOTICES | An existing notice generator skill, or AboutCode's ABOUT files |
| Produce an SBOM for a release | Syft, CycloneDX, or your platform's own tool |
| One-off question about a single license | Read it. This skill covers the families below. |

Do not hand-audit a dependency tree. That is what the tools are for, and they are better at it.

**If a license blocks a build decision, stop and say so before continuing.** A GPL dependency inside a closed-source product is a decision the user has to make, not one to discover at release.

## The license families

Enough to classify a license at a glance. For the specific terms, read the actual license.

| License | Commercial use | What you owe |
|---|---|---|
| **Permissive** (MIT, BSD, ISC) | Yes | Keep the copyright notice and license text. Nothing else. |
| **Permissive + patent** (Apache-2.0) | Yes | The above, plus the NOTICE file and a note on changes you made. Explicit patent grant. |
| **Weak copyleft** (LGPL, MPL-2.0) | Yes, if you keep the licensed part separate | Disclose changes to the licensed files. Your own code can stay closed. |
| **Strong copyleft** (GPL, AGPL) | Yes, but your project inherits the license | **Stop and ask.** This can force you to open-source. |
| **Public domain / CC0** | Yes | Nothing |
| **Creative Commons** (CC-BY, CC-BY-SA, CC-BY-NC) | Varies, CC-BY-NC bars commercial use | Attribution nearly always required. Check the specific CC variant. |
| **No license file** | No | Assume all rights reserved. Reading is fine, reuse is not. |

**No license file is the most common trap.** It is not public domain and it is not permission. Plenty of repos have none, and that is a legal fact rather than an oversight you can lean on.

Apache-2.0 differs from MIT mainly in the explicit patent grant. If you are licensing your own project and care about patent exposure, that is the reason to pick it.

## Attributing

- **The license requires it** — non-negotiable, include the license text and the copyright notice
- **It is a significant dependency** — an acknowledgments page or a "Built with" section, good practice even when not required
- **Someone helped you** — a shout-out, which is manners rather than law

Minimum correct form: "Uses [Library] ([License]) by [Author]." Link the repo.

## Paying back without open-sourcing your project

The recurring question: I used open source in a commercial product, I do not want to release my code, now what.

**You do not owe your source code.** Not for MIT, not for Apache, not for BSD. Building on other people's permissive work and selling something is how most of the commercial software industry operates. The obligation is whatever the license says, and the form of payback is yours to choose.

| You can | Why it helps |
|---|---|
| Give credit | Often required, and it sends them traffic |
| Report bugs | Free QA for the maintainer, and it helps everyone who comes after you |
| File feature requests | Naming a gap is already a contribution |
| Donate (GitHub Sponsors, Open Collective, Ko-fi) | Money is the most universally useful contribution, and $5 a month to a project you depend on is real |
| Write a case study | Social proof drives users, contributors, and funding |
| Answer their questions | You learned it, so pass it on in their issues, forum, or Discord |
| Submit a docs PR | Often the weakest part of a project, and it carries zero license implications |
| Publish your experience | "How I used X to build Y" helps others evaluate it and gives the tool attention, at no cost to your IP |
| Open-source an isolated helper | If you built something standalone, releasing that is a clean contribution with no risk to your product |

**What you do not owe:** your project's source, unless strong copyleft actually requires it. Free labor on someone's roadmap. Anything the license does not say.

## Anti-patterns

| Mistake | Reality |
|---|---|
| Hand-auditing a dependency tree | Use ORT or `license-checker`. You will miss transitive deps. |
| "No license means free" | It means no permission. Learn, do not copy. |
| Skipping the copyleft check | GPL in a closed product can force you to open-source. Ask before building on it. |
| "MIT means I owe nothing" | Attribution is usually required, and payback is still worth doing. |
| "I must open-source everything I build" | False, and it keeps people from sharing at all. |
| Romanticizing contribution | Useful rather than noble. Do it because it helps. |
| "I will contribute later" | The finding dies. A quick forum post now beats a blog post you never write. |

## Hand off

- Something worth sharing got built, to `contributing-back`
- A license blocks the decision, back to `evaluating-existing-work` with the constraint stated
