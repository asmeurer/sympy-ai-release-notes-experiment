# Pull request #30971: SetExpr maintenance

- Author: @smichr
- Merged: 2026-11-08T03:15:16Z into `master`
- Labels: sets
- Size: +116 / -8 in 5 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

This fixes several issues with consistency related to SetExpr operations (add, multiply) when working with scalars and infinite values.

The biggest change might be that intervals containing 0 when multiplied by and infinite value will generate a nan entry in the set.

#### Other comments

#### AI Generation Disclosure

ChatGPT collaboration.

## Commits

- 07aa234616 (Christopher Smith): handle scalar results in set operations
- 6becb1d7db (Christopher Smith): handle SetExpr(Interval)*oo
- 0428b779dc (Christopher Smith): sympify set in SetExpr to FiniteSet
- 6adfb83b60 (Christopher Smith): check SetExpr({..nan})*Number handling
- 020489d34b (Christopher Smith): Handle interval multiplication by infinity pointwise
- f17396c5c9 (Christopher Smith): test ImageSet collapsing to infinite singleton

## Conversation

### @oscarbenjamin commented

It looks like SetExpr tests are failing in CI now:
https://github.com/sympy/sympy/pull/30985


## Reviews

### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin commented on `sympy/sets/tests/test_setexpr.py`

This test fails intermittently because `-oo` and nan do not have a consistent sort order.
