# Naming decision

The owner selected `look-before-build` for this repository. The six installed skill names stay the same: changing the repository name does not rename skill identifiers.

| Option | What it communicates without a README | Tradeoff |
|---|---|---|
| `look-before-build` | Inspect existing approaches before committing to new work | Clear order and an easy phrase to say. It underplays extension and optional contribution; “build” can sound software-specific. |
| `find-build-share` | A sequence from discovery to making something and sharing it | Includes giving back, but can imply that building and public sharing are required. Adoption, private work, and choosing not to publish are valid outcomes here. |
| `beyond-scratch` | Work need not start from nothing | Broad enough for study and creative work. It says less about the actual decision process and can be confused with the Scratch programming language. |

The former name `inherit-and-extend` emphasized continuation and adaptation, but sounded like a programming inheritance pattern and understated the initial search. No candidate names every part of the workflow equally well. Sharing findings is optional, regardless of the name.

## Collision check and limits

Earlier GitHub searching reported no exact repository-name match for these three candidates. A read-only recheck on **2026-10-02** used GitHub's repository search API with `<candidate> in:name`, requested up to 100 results, and compared returned repository names case-insensitively with the exact candidate:

| Candidate | Reported search results inspected | Exact repository-name matches |
|---|---|---|
| `look-before-build` | 0 | 0 |
| `find-build-share` | 2 | 0 |
| `beyond-scratch` | 15 | 0 |

The API reported no incomplete results in these responses. Near matches still exist, and an empty exact-match list is only a finding from those public GitHub queries. It is **not trademark clearance**, proof of global uniqueness, or a reservation. Private/unindexed repositories, domains, package registries, brands, and trademark databases were not checked. This was a bounded collision check, not a legal clearance.
