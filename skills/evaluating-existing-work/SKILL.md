---
name: evaluating-existing-work
description: Use when prior art, tools, skills, or libraries have been found and the decision is whether to adopt, extend, fork, or build your own — especially when the match is partial, the license needs checking, or the agent is under pressure to just pick one.
---

# Evaluating Existing Work

The decision is adopt / extend / compose / build. This skill exists because the wrong pick here costs more than a slow pick.

## The core tension

Adopting existing work is faster — and it imports someone else's assumptions, priorities, and blind spots. When something is 80% right, the missing 20% is often the part you care about.

## Analysis lenses

**Against the user's idea**

- **Similarities** — what it shares with what's wanted
- **Differences** — what's unique about the user's approach
- **Gaps** — what it does *not* address
- **Improvements** — whether the user's idea fixes known limitations

**Health of the existing work**

- Mature or experimental?
- Actively maintained, or stable-and-done (both fine, differently)?
- Community size, responsiveness to issues?
- Known limitations worth flagging?
- License compatible? → hand to `licensing-and-payback` before deciding.

**Lessons, not just facts**

- Build vs use: adopt, extend, or build?
- Pitfalls others hit — bugs, design mistakes, maintenance burden
- Patterns that worked
- Context: why did it work for them, and does that context apply here?

## Adopt when

- It solves the core problem; gaps are edge cases you can work around
- The license fits
- Maintained (or stable and mature)
- The author's priorities match yours
- You can read how it works and debug it

## Build your own when

- Its assumptions conflict with your needs
- The gap is the part you actually care about
- Unmaintained, undocumented, or opaque
- License incompatible
- Adapting costs more than rebuilding

Both "always reuse" and "always custom" are positions to argue against. This is a trade-off, not a virtue.

## Partial solutions

Common case — something close but not exact.

1. **Why is it partial?** Deliberate scope? Same boundary you hit? Incomplete?
2. **Is the gap fillable?** Hook, config, small wrapper? Partial solution plus glue is often the answer.
3. **Mind the bias.** Every solution encodes its author's priorities. What did they optimize for? What did they trade off? Does that match your need?
4. **Test early.** Don't assume it works because it worked for someone else. On first mismatch: adapt, extend, or replace.

## How to be reasonably sure

No solution is certain — you're making an informed bet. Aim for an informed one.

- **Read the source**, not just the README. Twenty minutes reading saves hours of debugging.
- **Check the issue tracker.** Open blockers? Does the maintainer respond? Dead issues are a risk signal.
- **Spike it.** Validate on a small slice before committing the whole project.
- **Have an exit plan.** Isolate it behind your own interface so you can swap it out.
- **Price being wrong.** If the cost of being wrong is low, adopt freely. If high, validate harder.

## Output

Same shape as the Brief: verdict first, table, full breakdown only on request. Lead with adopt / extend / build and the reason in one clause.

## Hand off

- License question blocks the decision → `licensing-and-payback`
- Decision made and something novel may result → `contributing-back` after it's built
