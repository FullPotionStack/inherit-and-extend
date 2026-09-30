---
name: domain-playbooks
description: Use when a search needs domain-specific sources beyond the general list — software, games, infrastructure, study and learning, or creative work — to find where practitioners in that field actually post what they've built and what broke.
---

# Domain Playbooks

Where people in each domain actually talk. Load from `finding-existing-work` when the generic source list isn't enough.

## Software and apps

- **Look in:** GitHub (repos *and* issues), npm/PyPI, AlternativeTo, Product Hunt
- **Read:** issue trackers for pain points — the most useful signal, and the least searched
- **Check:** is there an open-source project worth forking or extending?
- **Learn from:** production post-mortems, architecture write-ups

## Games

- **Look in:** gamedev forums (itch.io, r/gamedev), GitHub gamedev repos, GDC talks and postmortems, Game Jolt
- **Read:** what engines others used for this genre, and what they wish they'd known
- **Check:** common patterns for the specific mechanic you're implementing
- **Learn from:** postmortems of shipped games, especially the small successful ones

## Infrastructure and setup

- **Look in:** Terraform Registry and Ansible Galaxy for modules, GitHub for docker-compose and CI configs
- **Read:** official docs, then community tutorials
- **Search for:** "how I set up X" — these reliably contain the pitfalls the docs omit
- **Check:** whether someone solved your exact stack combination, not just adjacent ones

## Study and learning

- **Look in:** course syllabi, learning-path repos, community recommendations (Reddit, forums, Discord)
- **Read:** how different people sequenced the same material, and why
- **Check:** whether the path you're proposing differs from the consensus — and whether that's a strength or a mistake
- **Note:** for a language, the *community* is the curriculum. For a framework, official docs beat tutorials.

## Creative work

- **Look in:** similar projects, the technique's lineage, community showcases
- **Read:** how others solved the same structural problem
- **Guard:** understand the landscape without letting it flatten your intent. Prior art is a reference, not a spec.

## Cross-domain

The reason this suite is domain-agnostic: the *shape* of the problem is often identical across fields. "What's the established approach, what failed, what's the trade-off" applies to a database engine and a novel structure the same way.

If your domain isn't listed, apply the general list in `finding-existing-work` and add what you learn — the next person needs it.
