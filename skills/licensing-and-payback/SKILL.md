---
name: licensing-and-payback
description: Use when a license, reuse question, or dependency comes up. Check permissions and obligations against the intended use; separate compliance from optional ways to give back.
---

# Licensing and payback

Identify what the license requires before suggesting voluntary contributions.
This is license-risk triage, not legal advice or a compliance certification.

## Establish the facts

1. Record the component, source URL, revision, and exact license and version.
   Read the shipped license text, file headers, exceptions, and any dual-license
   choices; repository metadata alone is not enough. Distinguish version-only
   grants from "or any later version" permissions and record the chosen license
   where the grant offers a choice.
2. Record the intended private use, distribution of source or binaries, network
   interaction, and integration method. Copying code, linking a library, running
   a separate process, and bundling independent programs are different facts.
3. Identify modifications, recipients, notices, source-delivery requirements,
   patents, and compatibility questions for that use. Commercial use alone does
   not determine whether disclosure obligations apply.

If permission is missing or the scope is uncertain, say what is unknown and
pause the affected reuse or release decision. Ask the rights holder for missing
permission or clarification; escalate material interpretation or compatibility
questions to qualified legal counsel. Do not declare an entire product safe or
incompatible from a license family label.

## Inventory with tools, then review

Use [ORT](https://github.com/oss-review-toolkit/ort),
[AboutCode](https://aboutcode.org), or an ecosystem scanner such as
[`license-checker`](https://github.com/policiescans/license-checker) for an npm
inventory. Syft or CycloneDX tooling can produce an SBOM.

Scanners provide inventory and evidence, not legal judgments. Review unresolved
or conflicting results, vendored code, assets, generated output, and transitive
dependencies against the actual release contents. Notice generators can assemble
known obligations; neither a generated file nor a clean CI result proves compliance.

## License-risk triage

These are review prompts for the named versions, not exhaustive requirements.
For other versions, exceptions, or custom terms, read those terms instead.

| License | Review for the intended use |
|---|---|
| MIT | Keep the copyright and permission notice in copies or substantial portions. Preserve the full shipped license; a repo link alone does not replace it. |
| Apache-2.0 | On redistribution, supply the license, mark changed files, and retain applicable source notices. If upstream includes a NOTICE file, preserve the applicable attribution notices as section 4(d) allows; do not assume every Apache work has one. Review the patent grant and termination terms. |
| LGPL-3.0 | Library and combined-work rules differ from MPL. On conveying a combined work, review library source, notices, copies of both the GPLv3 and LGPLv3 license texts, the permitted relinking or suitable shared-library mechanism, reverse engineering for debugging library modifications, and installation information where required (section 4; section 3 separately addresses library header material). Physical separation alone is not compliance. |
| MPL-2.0 | File-level copyleft: distribution of covered files, including modifications, preserves MPL terms and notices. Executable distribution requires making the covered source available and informing recipients; a larger work may use other terms for separate files (sections 3.1–3.4). This is not LGPL's relinking rule. |
| GPL-3.0 | Private modification and use do not require public posting. When you convey covered works, review notices, licensing scope, Corresponding Source, and any installation information. An aggregate of independent works differs from a combined covered work (sections 2, 4–6); unrelated code does not automatically inherit GPL. |
| AGPL-3.0 | In addition to conveyance rules, section 13 requires a modified version supporting remote network interaction to prominently offer its Corresponding Source to all users interacting with it remotely. Review this even without distributing copies; GPL has no equivalent general network-interaction trigger. |

BSD and ISC terms vary; preserve the applicable notices and check the exact
variant. CC licenses have version-specific attribution, share-alike, and
noncommercial conditions and are not interchangeable software licenses. Public
domain or CC0 claims still need provenance and review of rights outside their
scope. An absent LICENSE file is not a grant of permission: check other notices
and agreements before assuming reuse is authorized.

Primary texts: [MIT](https://opensource.org/license/mit),
[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0),
[LGPL-3.0](https://www.gnu.org/licenses/lgpl-3.0.html) (includes GPLv3 terms),
[MPL-2.0](https://www.mozilla.org/en-US/MPL/2.0/),
[GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html), and
[AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.html).
The [GNU FAQ on private modifications](https://www.gnu.org/licenses/gpl-faq.html#GPLRequireSourcePostedPublic)
and [Mozilla FAQ](https://www.mozilla.org/en-US/MPL/2.0/FAQ/) explain common cases;
FAQs supplement, rather than replace, license texts.

## Compliance and acknowledgment are different

A credit line is not license compliance. A "Uses Library (License)" line with a
repository link can be a useful acknowledgment, but it does not replace required
copyright and license text, applicable NOTICE content, modification notices,
source delivery, or other obligations. Preserve supplied attribution accurately;
do not invent authors or replace copyright holders with inferred names.

For this skill's own distribution, keep [LICENSE](LICENSE) and
[PROVENANCE.md](PROVENANCE.md) with the folder. The license covers this material,
not the external tools it mentions.

## Optional ways to give back

Once obligations are understood, offer contribution only if the user wants it.
Donations, a sanitized bug report, a docs correction, or a permitted standalone
helper can help without publishing an unrelated product. Declining, postponing,
or keeping a finding private is a valid choice; do not pressure immediate posting.

Before sharing even documentation or an isolated helper, check ownership,
employer/client approval, contribution terms (including any CLA or DCO), copied
material, credentials, private data, and NDA restrictions. No contribution format
is automatically free of license or IP implications. Do not publish anything
without the user's approval of the exact material and destination.

## Report and hand off

Return the component/version, intended use, primary-text evidence, required
release artifacts, and unresolved questions. Separate established obligations
from assumptions and voluntary suggestions. Keep release approval with the owner
and their compliance process.

- If the user wants to share permitted material, load `contributing-back`.
- If constraints affect candidate selection, load `evaluating-existing-work`
  with the constraint stated. If either skill is unavailable, report that and
  continue with the relevant checks here rather than pretending a handoff ran.
