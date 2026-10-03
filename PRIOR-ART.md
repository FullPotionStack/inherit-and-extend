# Prior art and evidence limits

## Scope and date

Primary-source verification: **2026-10-02**. This pass inspected the sources below, the six local skill bodies, and the prior positioning in baseline `c94a9f6`. It is **not exhaustive**: it revisits named citations and adds contribution and cross-domain precedents, rather than searching every skill registry or all build-versus-buy literature. Private community discussions and paid catalogs were not inspected. No competing workflow was executed.

The earlier file recorded a "Last full pass: 2026-09-30" and described checks happening late or inadequately. Those are historical statements from that file, not evidence that every stage was searched before authorship. Its query logs and source snapshots were not available in this checkout. Current pages cannot reconstruct what their authors published or what this suite inspected on that date.

## Verified primary sources

The summaries describe retrieved content, not search snippets. GitHub file revisions below were resolved through its commits API and read at the identified commit. Live articles without archived snapshots establish present overlap only.

| Source | Evidence inspected | Overlap and limits |
|---|---|---|
| [Superpowers `using-superpowers`](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/using-superpowers/SKILL.md) | File revision `5bf4e780`, committed 2026-09-19 | A `using-*` entry skill requires relevant skill loading. Structural precedent, not evidence of reliable automatic triggers. It has a subagent exception. |
| [ECC `search-first`](https://github.com/affaan-m/everything-claude-code/blob/0765f7a2ca2bd5df214d3aa7ba7e7ac19db8b189/skills/search-first/SKILL.md) | File revision `0765f7a2`, committed 2026-09-27 | Tool Availability Preflight, local repository checks, Quick Mode, Full Mode, candidate scoring, adopt/extend/compose/build, and implementation. This revision predates the earlier recorded pass, but does not show which revision that pass read. |
| [Morrison-Lab `dont-reinvent-wheel`](https://github.com/Morrison-Lab/ai-config/blob/0c1708dcc88af384c4d01f71a9a26a4511b5dd27/shared/principles/dont-reinvent-wheel.md) | File revision `0c1708dc`, committed 2026-10-01 | Own repositories first, external sources, weak evidence from empty searches, partial-match extension, license/attribution gate, upstream contribution, and custom-work exceptions. Its organization-specific examples do not make the principles organization-specific. This revision postdates the earlier pass. |
| [Bizz: build or buy AI agents](https://www.bizz.ai/blog/build-buy-ai-agent-stack-differentiation-control-tco) | Live article, sections on decomposition, differentiation, due diligence, lock-in, and total cost | Explicitly warns that vendor packaging can become the architecture. It discusses narrow custom behavior inside adopted systems, failure consequence, validation, maintenance, and exit cost. No publication/version history was established here. |
| [Agentplace: build, buy, or borrow](https://agentplace.io/blog/build-vs-buy-vs-borrow-strategic-framework-for-agent-platform-decisions) | Live article's options, weighted decision dimensions, and hidden-cost sections; access succeeded on this recheck | Describes customization, maintenance, integration, organizational readiness, and exit costs. Its numeric cost, success-rate, and efficacy estimates were not verified; no publication/version history was established here. |
| [Windward: build vs. buy framework](https://www.windwardstudios.com/blog/build-buy-framework-development) | Live article's numbered tendencies and framework description | Discusses developer/business bias, ill-fitting purchases, missing evidence, fit to the real problem, ongoing support, and long-term impact. The linked white paper was not inspected, so no claim about its full worksheet is made. |
| [ORT README](https://github.com/oss-review-toolkit/ort#introduction) and [AboutCode](https://aboutcode.org/) | Upstream README and project site | Dependency analysis, license detection/policy, attribution reports and SBOM tooling. A family of tools is not one license or a legal opinion. Tool execution was not tested. |
| [Open Source Guides: how to contribute](https://opensource.guide/how-to-contribute/) | Guide's non-code contributions, project orientation, suitability checklist, and submission guidance | Small contributions, documentation, teaching, examples, community questions, and checking maintainer expectations are established advice. It also discusses non-software projects. |
| [`publish-skills`](https://github.com/jindalAnuj/publish-skills#what-does-it-do), [GitHub `gh skill`](https://github.blog/changelog/2026-04-15-manage-agent-skills-with-github-cli/), [Postiz](https://postiz.com/) | Upstream README, publisher changelog, and product site | Skill publishing via pull requests, distribution/provenance, and publishing/scheduling tools already exist. These are advertised/documented capabilities, not independently tested integrations. |
| [MIT OCW syllabus](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/pages/syllabus/), [OpenStax preface](https://openstax.org/books/introductory-statistics-2e/pages/preface), [Poe's essay](https://www.eapoe.org/works/essays/philcomp.htm), [Saunders's essay](https://www.theguardian.com/books/2017/mar/04/what-writers-really-do-when-they-write) | Institution/publisher material and authored craft essays | Study sequences, prerequisites, deliberate composition, and learning through revision predate this suite. They inform the illustrative examples, not a claim that the suite improves learning or writing. |

## Positioning by stage

### `using-lookup`

Retain a dispatch-only entry point. Credit Superpowers for the `using-*` convention and skill-loading pattern. This suite scopes a check to the decision under review and rechecks when relevant constraints or components change. That is a design rule, not a new discovery or an enforcement mechanism.

### `finding-existing-work`

Retain as a search stage with explicit boundaries. ECC already has quick/full modes, local checks, tool availability reporting, structured comparison, and the four outcomes. Morrison-Lab already covers internal and external work, synonyms, and bounded interpretation of empty results. Separate research effort from output length here as a presentation choice; do not claim that brief answers or effort modes are unique.

### `evaluating-existing-work`

Retain as a constraint-based decision aid, with substantial overlap. The previous description discounted enterprise frameworks and claimed missing treatment of partial fit, bias, and mistake cost. The inspected Bizz and Windward articles address these concerns directly. Bizz's layer-by-layer custom/adopted boundaries are especially relevant when the missing behavior matters more than the generic features that fit.

We have not established that these live articles had identical wording on 2026-09-30. The correction is to current positioning: their present content cannot support a claim that this stage occupies an otherwise empty niche. Small validation probes and exit planning should be credited as common evaluation practice, not proprietary techniques.

### `licensing-and-payback`

Retain the handoff to license texts and existing compliance tools. ORT and AboutCode cover much of the tooling problem; Morrison-Lab and Open Source Guides overlap with attribution and contribution advice. Optional bug reports, documentation, examples, or sponsorship do not require publishing an entire private project. No uniqueness claim is established for combining that advice with a license check. Legal obligations and voluntary contributions remain separate.

### `contributing-back`

Retain optional suggestions appropriate to the completed work and user permission. Small useful contributions, sharing examples, asking maintainers first, and publishing through existing tools all have precedent. Channel/effort tables are editorial conveniences, not measured rankings or an unprecedented framework. This stage does not require the user to share their work.

### `domain-playbooks`

Retain domain-specific references as a way to find and compare precedent. A course, craft essay, game postmortem, or infrastructure module needs different fit criteria; a package-maintenance checklist alone is insufficient. The worked [study](docs/examples/study-path.md) and [creative](docs/examples/creative-work.md) examples demonstrate the proposed comparison shape, not a validated cross-domain method. Broad domain-skill catalogs are leads, not proof that an exact format is absent elsewhere.

## Unverified and incomplete citations

- `openclaw-skill-hunter`: the earlier file linked [mturac/skill-hunter](https://github.com/mturac/skill-hunter). The repository, `main/README.md`, `main/SKILL.md`, and GitHub repository API returned 404. This does not establish whether the project was deleted, renamed, made private, or never available at those paths. Its claimed scope is unverified and excluded from the comparison.
- [Agentplace build/buy/borrow article](https://agentplace.io/blog/build-vs-buy-vs-borrow-strategic-framework-for-agent-platform-decisions): extraction and browser access failed in the earlier repair attempt. A 2026-10-02 recheck retrieved the article, now included above. The earlier access failure was not evidence of absent content; its quantitative estimates and historical wording remain unverified.
- The earlier licensing list named AI Compliance Notice Generator, melodic-software's `license-compliance`, `dependency-auditor`, and Anthropic's Open Source License Review without exact verified artifacts. These remain unverified leads, not evidence of features, popularity, license, or comparative coverage. The earlier star counts and "best" ranking were removed.
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) and [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) were earlier catalog leads. Their complete contents were not audited in this pass. Neither a catalog mention nor failure to find a match proves that no non-software playbook exists.

## What is supported

The suite is a packaging and adaptation of overlapping practices: local-first lookup, constraint-based comparison, reuse/license checks, optional contribution, and domain references. Retaining six files is an organizational decision. Novelty, superiority, reliable invocation, and reduced research overhead are not established by this source review.

When changing a stage, record the actual sources and revisions inspected, search boundaries, inaccessible material, and remaining uncertainty. Scope a negative finding to that inspection. Preserve historical notes as historical notes rather than silently treating today's sources as yesterday's evidence.
