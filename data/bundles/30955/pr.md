# Pull request #30955: Fix FpSubgroup conversion to finitely presented groups

- Author: @raman118
- Merged: 2026-11-05T19:14:40Z into `master`
- Labels: (none)
- Size: +23 / -1 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #24811.

#### Brief description of what is fixed or changed

`FpSubgroup.to_FpGroup()` omitted the required generators argument when calling `FpGroup.subgroup()`, raising `TypeError`. It now passes the generators along with the optional cached coset table, so conversion works before or after calling `order()`.

#### Other comments

The regression failed before the fix. Tests cover fresh and cached conversion, a proper subgroup, the trivial subgroup, and the whole group. Validation: `test_fp_groups.py` (8 passed, 1 slow test deselected), code-quality tests (6 passed), Ruff, and `bin/mailmap_check.py` passed.

#### AI Generation Disclosure

OpenAI Codex (GPT-6 Astra) generated all changes in `sympy/combinatorics/fp_groups.py`, `sympy/combinatorics/tests/test_fp_groups.py`, and `.mailmap`. This PR description was also written by the AI agent at the account owner's request.

## Commits

- 7f382ecd3b (raman118): Pass subgroup generators when converting FpSubgroup
      Allow conversion with or without a cached coset table and cover trivial, whole, and proper subgroups.
      AI-generated code and tests by OpenAI Codex (GPT-6 Astra).

## Conversation

### @smichr commented

Looks like it is following function signature. Straightforward fix. Thanks.


## Reviews

(no reviews)
