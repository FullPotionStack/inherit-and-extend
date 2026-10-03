# look-before-build

Before settling on an approach, find out what already exists and whether it fits. These six agent skills guide that check for software, study plans, and creative work. They help you decide whether to adopt, adapt, combine, or build, with evidence and unresolved questions attached to the decision.

They are instructions for an agent, not a hook that intercepts tool calls. Discovery and invocation depend on the harness, model, and session instructions. The suite does not guarantee that a check will run, that reuse will win, or that it will save time or tokens.

For example, if you ask for a CSV parser, the agent should inspect the project's existing code and Python's `csv` module before writing one. If a candidate fits, it can reuse it. If it only partly fits, it can identify the gap and test whether extending it is safer than starting over. This is an illustration of the intended decision, not a claim that every agent will follow it.

## Install

Install all six. The stages reference one another; installing only the entry skill leaves those handoffs unavailable. Make the suite available, then load only the stage and references needed for a decision. Copy each complete skill directory, including `references/`, `LICENSE`, and `PROVENANCE.md`, rather than just `SKILL.md`.

### Skills CLI: explicit agent and scope

With Node.js/npm available, inspect the offered skills first. `npx` may download and execute the CLI; `--list` lists skills without installing them. Review the repository and CLI before trusting their instructions:

```bash
npx skills add FullPotionStack/look-before-build --list
```

Use this command only when none of the six names is already installed in the selected scope, including canonical `.agents/skills/` copies or agent-specific folders. The CLI can replace existing skills; `--copy` is not a no-overwrite flag. Cancel if its summary lists an overwrite. If you cannot establish that the destinations are unused, use the guarded manual route instead.

This command selects all six for Claude Code in **project scope**, relative to your current project directory:

```bash
npx skills add FullPotionStack/look-before-build --agent claude-code --copy --skill \
  using-lookup \
  finding-existing-work \
  evaluating-existing-work \
  licensing-and-payback \
  contributing-back \
  domain-playbooks
```

Add `--global` for user scope across projects. Replace `claude-code` with your intended agent identifier, such as `codex`, `cursor`, or `gemini-cli`; check the [CLI's current agent list](https://github.com/vercel-labs/skills#supported-agents). Review its destination summary before confirming. Avoid `--all` if you only want one harness: it selects all skills **and all agents**. On PowerShell, enter the command on one line; Bash's `\` continuation is not PowerShell syntax.

CLI flags were checked against the [upstream README](https://github.com/vercel-labs/skills#options) and overwrite behavior against its [installer source](https://github.com/vercel-labs/skills/blob/main/src/installer.ts) on 2026-10-02. Real installation and cross-harness behavior were not tested. CLI destinations can differ from a harness's current documented discovery paths (notably Codex user scope). Check its summary against the table below; prefer manual copying when they differ. For Hermes, use the profile-aware instructions below instead of assuming the CLI resolves your profile.

### Manual installation

```bash
git clone https://github.com/FullPotionStack/look-before-build.git
cd look-before-build
```

Copy the six directories inside `skills/` into the destination's `skills/` directory. Do not create an extra `skills/skills/` layer. If any name is already discoverable, stop and compare the existing copy; these instructions do not authorize replacing or merging it. Inspect names in category folders, linked directories, and other discovery locations too, not just six top-level paths. Review the checked-out revision before copying.

| Harness | Project scope | User or profile scope | Primary documentation |
|---|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | [Skills](https://code.claude.com/docs/en/skills) |
| Codex | `.agents/skills/` | `~/.agents/skills/` | [Skills](https://developers.openai.com/codex/skills/) |
| Cursor | `.cursor/skills/` or `.agents/skills/` | `~/.cursor/skills/` or `~/.agents/skills/` | [Skills](https://cursor.com/docs/context/skills) |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | `~/.gemini/skills/` or `~/.agents/skills/` | [Skills](https://geminicli.com/docs/cli/skills/) |
| Hermes Agent | Check project trust and discovery rules in your version | `<resolved profile home>/skills/` | [Skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills), [profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) |

These are documented discovery locations, not a compatibility certification. Check your installed version's rules for precedence, consent, and session refresh.

### Hermes: resolve the profile home first

Run `hermes profile` to identify the active profile, then `hermes profile show default` (or `hermes profile show <name>`) to read its actual path. In an agent session, `HERMES_HOME` normally carries the resolved profile home. In an external shell it may be unset or refer to another profile; match it to the displayed path before copying. `HOME` and the working directory are not substitutes.

Common layouts, with custom homes taking precedence:

- Linux/macOS/WSL default: `~/.hermes/skills/`; named profiles: `~/.hermes/profiles/<name>/skills/`.
- Native Windows installer default: `%LOCALAPPDATA%\hermes\skills\`; named profiles: `%LOCALAPPDATA%\hermes\profiles\<name>\skills\`.
- Append `skills/` **once** to the resolved profile home. If `HERMES_HOME` already points to a named profile, do not append another `profiles/<name>`.

The [native Windows guide](https://hermes-agent.nousresearch.com/docs/user-guide/windows-native) documents a different home from WSL. Verify your installation instead of copying into both.

Bash/Git Bash, from the checkout root, after verifying `HERMES_HOME` matches the intended profile:

```bash
# If unset, stop and set HERMES_HOME to the path shown by Hermes.
test -n "$HERMES_HOME" || { printf '%s\n' 'Resolve HERMES_HOME first'; exit 1; }
test -d "$HERMES_HOME" || { printf '%s\n' 'Profile home does not exist'; exit 1; }
set -- using-lookup finding-existing-work evaluating-existing-work licensing-and-payback contributing-back domain-playbooks
# Validate the six complete sources before creating anything in the profile.
for name in "$@"; do
  for required in SKILL.md LICENSE PROVENANCE.md; do
    test -f "skills/$name/$required" || { printf 'Missing source: skills/%s/%s\n' "$name" "$required"; exit 1; }
  done
done
# Check every destination, including category folders, before copying any skill.
for name in "$@"; do
  test ! -e "$HERMES_HOME/skills/$name" && test ! -L "$HERMES_HOME/skills/$name" || { printf 'Already exists: %s\n' "$name"; exit 1; }
  if test -d "$HERMES_HOME/skills"; then
    matches=$(find "$HERMES_HOME/skills" -name "$name" -print) || exit 1
    test -z "$matches" || { printf 'Already exists: %s\n' "$matches"; exit 1; }
  fi
done
mkdir -p "$HERMES_HOME/skills" || exit 1
for name in "$@"; do
  cp -R "skills/$name" "$HERMES_HOME/skills/" || exit 1
done
```

PowerShell alternative, also from the checkout root with the resolved `HERMES_HOME` set:

```powershell
if (-not $env:HERMES_HOME -or -not (Test-Path -LiteralPath $env:HERMES_HOME -PathType Container)) {
    throw 'Resolve HERMES_HOME from hermes profile show first'
}
$destination = Join-Path $env:HERMES_HOME 'skills'
$names = @('using-lookup', 'finding-existing-work', 'evaluating-existing-work',
    'licensing-and-payback', 'contributing-back', 'domain-playbooks')
$sources = @()
foreach ($name in $names) {
    $path = Join-Path './skills' $name
    foreach ($required in @('SKILL.md', 'LICENSE', 'PROVENANCE.md')) {
        if (-not (Test-Path -LiteralPath (Join-Path $path $required) -PathType Leaf)) {
            throw "Missing source: $path/$required"
        }
    }
    $sources += Get-Item -LiteralPath $path -ErrorAction Stop
}
foreach ($source in $sources) {
    if (Test-Path -LiteralPath (Join-Path $destination $source.Name)) {
        throw "Already exists: $($source.Name); reconcile before copying"
    }
    if (Test-Path -LiteralPath $destination -PathType Container) {
        $matches = @(Get-ChildItem -LiteralPath $destination -Recurse -Force -ErrorAction Stop |
            Where-Object { $_.Name -eq $source.Name })
        if ($matches.Count -gt 0) {
            throw "Already exists: $($matches.FullName -join ', '); reconcile before copying"
        }
    }
}
New-Item -ItemType Directory -Path $destination -Force -ErrorAction Stop | Out-Null
foreach ($source in $sources) {
    Copy-Item -LiteralPath $source.FullName -Destination $destination -Recurse -ErrorAction Stop
}
```

The copy recipes were exercised only against disposable fake profile homes, in Bash/Git Bash and Windows PowerShell. They check required metadata and refuse top-level or categorized name collisions before copying; they are not atomic installers. Inspect the discovered skill catalog and linked locations first, avoid concurrent installation, and check any partial copy if an I/O error interrupts the operation.

Start a new session in the intended profile and confirm all six names are discoverable. Explicitly load `using-lookup` for a small task and check its returned sources and scope. Discovery alone is not proof of automatic invocation or a correct decision.

## How to use it

For an existence question, request a lookup. For a build request, let the agent check fit and return to the **original request**. Research stages do not themselves install dependencies or implement results; they hand back to the caller, which continues authorized implementation or asks when a decision changes scope or needs approval.

1. `using-lookup` dispatches at a decision boundary. A completed check covers its recorded scope, not every later file or new component.
2. `finding-existing-work` checks local work, installed skills, declared dependencies, and existing decisions first, then uses available external sources when needed. It records unavailable or skipped search channels.
3. `evaluating-existing-work` compares candidates against constraints, including partial-fit assumptions, validation needs, maintenance, and exit cost.
4. `licensing-and-payback` checks reuse obligations and points to compliance tools when appropriate. Contribution suggestions are separate from legal obligations.
5. `contributing-back` offers optional ways to share useful results after work exists. Publishing requires the user's authorization.
6. `domain-playbooks` supplies domain-specific sources and comparison criteria on demand.

Research effort and output length are separate choices: deeper source inspection can still end in a short answer. Start with the smallest check that can resolve the decision; expand when evidence is weak or a mistake would matter. There is no measured optimal search count or universal token-saving claim here.

## What a decision contains

The default is a short verdict with relevant evidence. This is an output contract, not a recorded run:

| Field | Content |
|---|---|
| Decision | Adopt / extend / compose / build, for the stated task or component |
| Candidates | Relevant inspected options and primary-source links |
| Fit and gap | Constraints met, missed, or left unverified |
| Search scope | Local paths and external sources checked, date, and unavailable channels |
| Next step | Validation needed and handback to the original request |

Use "not found in the inspected sources" when a bounded search finds no fit, rather than claiming nobody has done it. Ask for a detailed comparison if needed. Tests or an implementation request may require longer deliverables than a research brief.

## Worked examples and limits

- [Study path](docs/examples/study-path.md): compare an algebra-based statistics text with a calculus-based course, then compose a limited plan informed by learning research.
- [Creative work](docs/examples/creative-work.md): compare ending-first planning with discovery through revision for an original short story, without adopting another author's plot or voice.

Both are illustrative decisions based on retrieved sources, not recorded model trials. The proposed study and writing processes have not been executed and do not establish cross-domain efficacy. Offline documentation checks catch broken local links, missing sections, and inconsistent guidance; they do not establish reliable triggers, decision quality, or performance.

In local, controlled evaluations, eight baseline/control pilot responses and one updated response on each of 14 zero-tool scenarios were reviewed by a nonblind model judge. No critical failure was observed; one research-only answer had unnecessary report overhead. All four matched scenarios were at the rubric ceiling in all arms, so **no measured improvement is demonstrated**. The ten other scenarios have no baseline/control comparison. These are not end-to-end runs or replicated efficacy evidence. The updated prompts also contained a Windows newline-formatting artifact, fixed in the local evaluator after the run without replacing its evidence. The [protocol and runnable evaluator](evals/RUNNING.md) are included; raw transcripts and session-specific reviews are not published.

The owner selected `look-before-build` after [comparing names and checking bounded GitHub collisions](docs/naming-options.md).

## Related work and contributions

[`search-first`](https://github.com/affaan-m/everything-claude-code/blob/main/skills/search-first/SKILL.md) already covers quick/full modes, local checks, tool availability, and adopt/extend/compose/build. [Morrison-Lab's reuse principle](https://github.com/Morrison-Lab/ai-config/blob/main/shared/principles/dont-reinvent-wheel.md) covers internal and external work, license checks, upstream contribution, and reasons to build custom. Build-versus-buy literature also addresses bias, poor fit, lifecycle cost, and exit risk.

This repository packages related guidance into six linked skills with domain references. That describes its organization, not novelty or superiority. [PRIOR-ART.md](PRIOR-ART.md) records inspected sources, overlaps, historical limits, and unverified citations.

For a new playbook, include primary sources, constraints, rejected alternatives, transferable lessons, and evidence limits. Keep detailed examples in references or docs instead of enlarging every runtime prompt.

MIT; see [LICENSE](LICENSE). Each skill's license and provenance travel with its complete directory. External works retain their own terms; the repository license does not relicense them.
