# Pull request #31013: fix: use the generic array fallback for HadamardProduct derivatives

- Author: @rynwang
- Merged: 2026-11-09T22:50:41Z into `master`
- Labels: (none)
- Size: +23 / -7 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes item 15 of #30902

#### Brief description of what is fixed or changed

`arrayexpr_derivatives.py` registers a handler for `HadamardProduct` that unconditionally raises `NotImplementedError`. Because `singledispatch` picks the most specific class, this registration shadows the generic `MatrixExpr` handler, which would have converted the expression with `convert_matrix_to_array` and recursed. As a result, `.diff()` fails for expressions such as:

```python
Determinant(HadamardProduct(X, A)).diff(X)
Inverse(HadamardProduct(X, Y)).diff(X)
HadamardProduct(X, X).applyfunc(sin).diff(X)
DiagMatrix(HadamardProduct(v, w)).diff(v)
DiagonalMatrix(HadamardProduct(X, Y)).diff(X)
MatPow(HadamardProduct(X, Y), -1).diff(X)
```

All of these raise `NotImplementedError` on `master`. Removing the registration lets the generic fallback handle them; the existing `cg == expr` guard in that fallback still prevents infinite recursion.

#### Other comments

- Added `test_hadamard_product_derivative`, which compares the derivative of `det(X∘Y)` and `(X∘Y)**-1` against `derive_by_array` on explicit matrices. It fails on `master` and passes with this change.
- `sympy/matrices/expressions/tests` + `sympy/tensor/array/expressions/tests`: 409 passed, 6 xfailed.
- This does not address item 22 of the same issue (products of two `HadamardProduct`s), which needs a separate fix in `convert_matrix_to_array`.

AI disclosure: this change was prepared with AI assistance (DeepSeek Harness coding agent) and reviewed by the account owner.

#### AI Generation Disclosure

AI tool: DeepSeek Harness coding agent (deepseek-flash). It generated the changes in
`sympy/tensor/array/expressions/arrayexpr_derivatives.py` and
`sympy/matrices/expressions/tests/test_derivatives.py`.
The account owner reviewed the changes and the test results before submission.

## Commits

- f28b6da3c8 (Ryn Wang): fix: use the generic array fallback for HadamardProduct derivatives
- 6bb32a68cd (Ryn Wang): chore: register author in .mailmap and drop unused import
- b3ec6b5d2a (Ryn Wang): chore: keep .mailmap sorted

## Conversation

(no comments)

## Reviews

(no reviews)
