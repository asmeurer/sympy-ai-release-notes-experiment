# Pull request #30954: Reject direct construction of Vector

- Author: @raman118
- Merged: 2026-11-05T17:03:41Z into `master`
- Labels: (none)
- Size: +14 / -0 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #27439. Follows the constructor-level approach requested in #27488.

#### Brief description of what is fixed or changed

`Vector(a, b, c)` currently creates an invalid object that raises `RecursionError` during scalar multiplication. Direct `Vector(...)` construction now raises `TypeError` with guidance to use `CoordSys3D` basis vectors. Subclass construction remains supported.

#### Other comments

Regression failed before the fix. Validation: vector suite (121 passed, 2 xfailed), vector argument tests (7 passed), code-quality tests (6 passed), Ruff, and `bin/mailmap_check.py` passed.

#### AI Generation Disclosure

OpenAI Codex (GPT-6 Astra) generated all changes in `sympy/vector/vector.py`, `sympy/vector/tests/test_vector.py`, and `.mailmap`. This PR description was also written by the AI agent at the account owner's request.

## Commits

- 3425eff34b (raman118): Reject direct construction of abstract Vector class
      Raise TypeError at construction instead of allowing invalid Vector objects that recurse during scalar multiplication. Preserve subclass construction.
      AI-generated code and tests by OpenAI Codex (GPT-6 Astra).

## Conversation

### @smichr commented

Looks good, thanks.


## Reviews

(no reviews)
