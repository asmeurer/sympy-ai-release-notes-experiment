# Pull request #31027: 🤖 Declare the set singletons on SingletonRegistry

- Author: @hunterhogan
- Merged: 2026-11-13T17:17:56Z into `master`
- Labels: (none)
- Size: +29 / -7 in 2 files (full diff in `diff.patch`)

## Description

🤖 *This description was drafted by an AI agent (Claude Code).*

#### References to other Issues or PRs

`S.EmptySet` is left out until #30946 merges: `singularities()` is annotated `-> set[Symbol]` but returns `S.EmptySet`, and #30946 changes that annotation to `Set`.

#### Brief description of what is fixed or changed

Adds `Rationals`, `Naturals`, `Naturals0`, `Integers`, `Reals`, `Complexes`, and `UniversalSet` to `SingletonRegistry`.

`StochasticProcess.index_set` and the `state_space` parameter are annotated as `Set`, since subclasses use `S.Naturals0`.

#### Other comments

#### AI Generation Disclosure

Claude Code (Claude Opus 5.5) 

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Commits

- 0a6650f8c4 (Hunter Hogan): Declare the set singletons on SingletonRegistry
      S.Integers, S.Reals, and the other set singletons were Unknown to type
      checkers. StochasticProcess.index_set and state_space are annotated as Set
      so subclasses may use other sets. S.EmptySet is left for later because
      singularities() declares set[Symbol] while returning S.EmptySet.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- 8e782c1611 (Hunter Hogan): Remove incomplete typing

## Conversation

(no comments)

## Reviews

(no reviews)
