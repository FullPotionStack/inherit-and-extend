# Software and infrastructure

Load for packages, applications, deployment, or configuration choices.

## Start locally

Inspect the component being changed, declared dependencies and lockfiles, existing modules/tests, installed skills, runbooks, and recorded architecture decisions. Check whether a known upstream fix applies to the pinned version before writing a replacement.

## Sources

Use official docs and source for the exact version; package registries for metadata; issue trackers and release notes for blockers. GitHub repositories, AlternativeTo, and Product Hunt can identify candidates, but popularity and descriptions do not establish fit. For deployment, inspect [Terraform Registry](https://registry.terraform.io/) or [Ansible Galaxy](https://galaxy.ansible.com/) alongside provider docs and module source.

## Compare

Record required behavior, language/runtime, deployment model, data/privacy boundary, operational owner, license, migration cost, and what the dependency adds. For infrastructure, check provider/version compatibility, secret handling, state ownership, privileges, rollback and destroy behavior. A tutorial for a different operating system or cloud account is a lead, not an applicable recipe.

Read at least the relevant failure path or reported limitation when it can change the decision. A stale issue is not automatically a current blocker; a closed issue is not proof that your pinned version contains the fix. Consider extending existing work when its interfaces permit the missing behavior; build custom when the mismatch concerns the core requirement or adapting creates more burden.

## Validation and output

Recommend the smallest representative probe and state what it would test. Running a documented example is different from validating your real input, authentication, or production topology. Report actual commands/results only when executed; otherwise mark the probe pending. Hand the decision back to the original task with available evidence and unresolved risks.
