# Pull request #30993: fix(core): consistent ordering for nan vs -oo

- Author: @oscarbenjamin
- Merged: 2026-11-08T15:49:05Z into `master`
- Labels: core.numbers
- Size: +10 / -1 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes intermitten test failures after gh-30971.

#### Brief description of what is fixed or changed

Add nan.sort_key to distinguish from -oo sort key. Previously both had the same sort key meaning that ordered does not give a deterministic order of {nan, -oo}.

#### Other comments

#### AI Generation Disclosure

Used codex.

## Commits

- 0a05c5fa19 (Oscar Benjamin): fix(core): consistent ordering for nan vs -oo
      Previously both had the same sort key meaning that ordered does not
      give a deterministic order of {nan, -oo}.

## Conversation

(no comments)

## Reviews

(no reviews)
