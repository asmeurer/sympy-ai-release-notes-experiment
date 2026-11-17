# Pull request #31074: 🤖 Annotate doit

- Author: @hunterhogan
- Merged: 2026-11-13T21:21:40Z into `master`
- Labels: core, typing
- Size: +11 / -2 in 3 files (full diff in `diff.patch`)

## Description

🤖 *This description was drafted by an AI agent (Claude Code).*

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

Type annotations for `doit`:

- `Basic.doit`
- `Atom.doit`
- `TYPE_CHECKING` `Expr.doit`.
- `TYPE_CHECKING` `TensAdd.doit`.

#### Other comments

#### AI Generation Disclosure

Claude Code (Claude Opus 5.5)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Commits

- 8f19d15043 (Hunter Hogan): Annotate doit
      Basic.doit returns Basic, Atom.doit returns Self, and Expr declares
      doit -> Expr. TensAdd declares Expr args so TensAdd.doit type checks.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

## Conversation

(no comments)

## Reviews

(no reviews)
