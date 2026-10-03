---
name: using-lookup
description: Use before writing code, choosing a tool, creating a non-mechanical file, or settling an approach, and when asked whether a solution exists.
---

# Using Lookup

Dispatch only: choose the needed stage; it does the research or evaluation.

Trigger on the next action, not keywords in the user's wording. The user's request determines authorization: checking existence is not permission to build.

## Reuse and invalidation

Reuse a recorded check only for the same decision with unchanged constraints and adequate evidence. A completed stage elsewhere in the conversation is not coverage.

**Invalidation takes precedence over reuse.** Re-check affected decisions when scope is split, merged, or restructured; requirements, domain, platform, language, scale, license constraints, budget, or freshness change; evidence is stale; or the user requests another check. A parent's check does not cover a new component automatically.

Mechanical work needs no lookup. Respect explicit no-search/offline limits and learning-from-scratch requests; unsearched alternatives remain unknown. "Just do it" is not automatically a search ban. Confidence is not evidence.

## Dispatch

| Current decision state | Load by skill name |
|---|---|
| No adequately checked candidates | `finding-existing-work` |
| Candidates need fit/trade-off judgment | `evaluating-existing-work` |
| License or reuse obligations need checking | `licensing-and-payback` |
| Domain-specific sources needed | `domain-playbooks` |
| Finished work worth sharing | `contributing-back` |

Load only applicable stages. Discovery starts locally before public search; evaluation follows when selection is needed. Keep one compact decision record across stages, not separate briefs. Skill names resolve through the harness's skill loader, not repository paths.

## Return control

- **Lookup-only request:** return the answer with inspected sources, limits, and unknowns; do not implement.
- **Implementation request:** return the decision to the authorized workflow and continue its approved work. Lookup completion is not task completion. This suite grants no new permission to install, execute third-party code, publish, or expand scope. Resolve blocking uncertainty before a consequential action.
