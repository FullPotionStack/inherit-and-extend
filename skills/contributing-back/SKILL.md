---
name: contributing-back
description: Use when the user wants to share something they built or learned. Offer a small contribution, check publication rights and privacy, and leave posting optional.
---

# Contributing back

Contribution is optional. Declining, postponing, or keeping a finding private
is a valid choice. Do not turn a suggestion into an obligation or delay the
user's work to make a voluntary post. License compliance is a separate question.

## Check before preparing a public share

- Confirm ownership and permission to publish, including employer/client
  approval, NDA restrictions, and rights in copied code, documentation, or assets.
- Remove credentials, private data, customer identifiers, internal URLs, and
  proprietary details from examples, screenshots, logs, and repository history.
  Prefer a synthetic example over a redacted production dump.
- Check the destination's contribution and licensing terms, including any CLA
  or DCO. A docs PR or isolated helper can still transfer rights or expose IP.
- If scope or permission is unclear, load `licensing-and-payback` and pause the
  affected publication decision. If that skill is unavailable, report it and
  check the exact terms or ask for qualified advice rather than assume permission.

Sharing a genuinely separate, permitted artifact need not mean publishing an
unrelated product. That does not settle the obligations for reused material or
guarantee a private product remains unaffected; review the actual license and
integration before making that claim.

## Pick one channel if the user wants to share

| Channel | Fits | Check first |
|---|---|---|
| Repository or gist | Code, scripts, skills, or reusable examples | License, notices, sensitive files and history |
| Project issue or discussion | A reproducible bug or small finding | Project template, existing reports, sanitized reproduction |
| Stack Overflow or specialist forum | An answer to a concrete question | Community rules, duplicates, relevance |
| Docs PR | A correction to documentation | Contribution terms and rights in the submitted text |
| Blog or social post | An explanation with permitted links or examples | Privacy, attribution, platform rules |
| Donation | Support without publishing an artifact | Official project funding link and the user's budget |

For a first upstream contribution, look for `good first issue` or `help wanted`
labels and read the project's contribution guide. Existing directories include
[Up For Grabs](https://up-for-grabs.net),
[First Timers Only](https://www.firsttimersonly.com/), and
[CodeTriage](https://www.codetriage.com/). Listing an issue does not mean the
maintainer wants an unsolicited PR; follow the project's process.

For skills, check the destination's current publishing documentation before
choosing a CLI. Verify the command, version, prerequisites, visibility, and what
it uploads. Do not run a publishing command as a discovery probe or promise
compatibility with an unverified list of harnesses.

## Draft the smallest useful share

A draft can state the problem, what was tried, what worked, and links to useful
sources. Add enough context to reproduce the finding without revealing private
material. A short permitted example is often enough; a public repository is not
required. Keep mandatory notices with copied material; a credit link alone is
not a replacement for license compliance.

Return the draft, proposed destination, and any unresolved rights or privacy
checks. Wait for the user's approval of the exact material and destination before
posting, opening a public issue or PR, uploading an artifact, or scheduling it.
Permission to draft is not permission to publish. If the user declines, stop.

## Multiple channels

Only explore publishing or scheduling tools if the user asks for this workflow.
[Postiz](https://postiz.com) is one candidate to evaluate, not a requirement or
an endorsement. Verify its current integrations and licensing before adopting
it; channel support and commands can change. Keep private content out of public
queues, and obtain approval for each destination and any scheduled publication.

## Distribution and hand off

Keep [LICENSE](LICENSE) and [PROVENANCE.md](PROVENANCE.md) with copies of this
skill folder; external projects mentioned here have their own licenses.

- If permission or obligations remain unclear, load `licensing-and-payback`.
- If nothing suitable has been built and the user wants options, load
  `finding-existing-work`. If a referenced skill is unavailable, report that
  and continue with the relevant checks above rather than invent a handoff.
