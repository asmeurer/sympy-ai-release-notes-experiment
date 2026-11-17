# Pull request #30966: fix(matrices): transpose inner derivative in Transpose._eval_derivative

- Author: @ish1416
- Merged: 2026-11-06T19:08:49Z into `master`
- Labels: (none)
- Size: +47 / -1 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes item E1-4 / E4-1 from #30900.

#### Brief description of what is fixed or changed

`Transpose._eval_derivative(x)` previously returned `self.arg._eval_derivative(x)` directly without applying the transpose operation to the inner derivative. This led to two mathematical inconsistencies:

1. Differentiating `Transpose(x * A)` where `A` has shape `(2, 3)` with respect to scalar `x` returned `A` with shape `(2, 3)` instead of `A.T` with shape `(3, 2)`, violating matrix shape preservation under scalar differentiation.
2. Differentiating `Transpose(C)` with respect to a matrix element `C[i, j]` returned `MatrixUnit(n, m, i, j)` instead of `MatrixUnit(m, n, j, i)`.

This PR updates `Transpose._eval_derivative` to return `d.T` when the inner derivative `d` is not `None`.

Comprehensive tests have been added to `test_transpose.py` covering scalar differentiation, matrix element differentiation, linear combinations with trigonometric functions, and explicit matrix comparison.

#### Other comments

All 287 matrix expression tests in `sympy/matrices/expressions/tests/` pass.

#### AI Generation Disclosure

None.

## Commits

- a237204ae5 (ish1416): fix(matrices): transpose inner derivative in Transpose._eval_derivative
      Differentiating a matrix transpose expression Transpose(expr) with respect
      to a scalar x previously called expr._eval_derivative(x) directly without
      transposing the result. This dropped the transpose operation, returning a
      matrix with flipped dimensions (e.g. (2, 3) instead of (3, 2)) when
      differentiating Transpose(x * A), and returning MatrixUnit(n, m, i, j)
      instead of MatrixUnit(m, n, j, i) when differentiating Transpose(C) with
      respect to element C[i, j].
      Transposing the inner derivative result preserves shape invariants and
      matches the explicit matrix derivative.
- 17d1af038f (Ishita Singh): author: add Ishita Singh to .mailmap
- 9b22635328 (Ishita Singh): tests: remove extra trailing newline in test_transpose.py

## Conversation

### @ish1416 commented

Thank you @sylee957 for reviewing and merging this fix! I appreciate the quick turnaround.


## Reviews

(no reviews)
