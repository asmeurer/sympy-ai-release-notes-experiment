# Pull request #31078: 🤖 Document convergence limits for summation results

- Author: @shreeeeee-rgb
- Merged: 2026-11-13T19:55:18Z into `master`
- Labels: (none)
- Size: +37 / -1 in 2 files (full diff in `diff.patch`)

## Description

🤖 Documentation-only follow-up to #14230 and #31067.

#### References to other Issues or PRs

Related to #14230 and #31067.

#### Brief description of what is fixed or changed

Clarifies that `Piecewise` guards attached to summation results indicate when the routine supplies a formula; they are not general convergence tests and may not describe the full convergence domain. Adds doctests for a symbolic geometric series and a matrix series whose entries include a divergent series.

#### Other comments

Documentation-only follow-up; no behavior changes.

#### AI Generation Disclosure

OpenAI Codex (GPT-6) generated the docstring note and doctest examples in `sympy/concrete/summations.py`.

## Commits

- 18faec7994 (shreeeeee-rgb): docs: clarify infinite sum convergence limitations
      AI-generated documentation and doctest examples by OpenAI Codex (GPT-6).
- 786424a3b0 (shreeeeee-rgb): Add contributor alias to mailmap
      AI disclosure: OpenAI Codex (GPT-6) generated this .mailmap entry.

## Conversation

(no comments)

## Reviews

(no reviews)
