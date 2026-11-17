# Pull request #31073: 🤖 Annotate Set.intersect, Set.__contains__, and Union.__new__

- Author: @hunterhogan
- Merged: 2026-11-13T17:22:40Z into `master`
- Labels: (none)
- Size: +6 / -6 in 1 files (full diff in `diff.patch`)

## Description

🤖 *This description was drafted by an AI agent (Claude Code).*

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

- `Set.intersect` and its alias `Set.intersection`.
- `Set.__contains__
- `Union.__new__.

#### Other comments

`Union.__new__.args` uses `tuple` in the body instead of `list` because it's the same type as the signature.

#### AI Generation Disclosure

Claude Code (Claude Opus 5.5)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Commits

- 6d2b0013c4 (Hunter Hogan): Annotate Set.intersect, Set.__contains__, and Union.__new__
      Union.__new__ builds args as tuples instead of lists so args keeps one
      type; simplify_union converts its input to a set either way.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

## Conversation

(no comments)

## Reviews

(no reviews)
