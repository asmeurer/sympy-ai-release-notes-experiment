# Pull request #30961: Fix nested sets in interval addition with infinity

- Author: @raman118
- Merged: 2026-11-06T06:52:26Z into `master`
- Labels: (none)
- Size: +11 / -2 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #21616.

#### Brief description of what is fixed or changed

`SetExpr(Interval(2, oo)) + oo` returned a nested singleton set instead of `{oo}`. Remove the extra set wrapper from the positive- and negative-infinity addition handlers. Tests cover bounded and unbounded intervals in both operand orders.

#### Other comments

The regression failed before the fix. All 16 `SetExpr` tests, code-quality tests (6 passed), Ruff, and `bin/mailmap_check.py` passed.

#### AI Generation Disclosure

OpenAI Codex (GPT-6 Astra) generated all changes in `sympy/sets/handlers/add.py` and `sympy/sets/tests/test_setexpr.py`.

## Commits

- 2f9bcec55d (raman118): Fix nested singleton sets in interval infinity addition
      Remove the extra set wrapper in both infinity addition handlers and cover bounded and unbounded intervals in both operand orders.
      AI-generated changes by OpenAI Codex (GPT-6 Astra).

## Conversation

### @smichr commented

This appears to follow the `Wrapper(Container(Value))` model, now.  Thanks for looking into this.


## Reviews

(no reviews)
