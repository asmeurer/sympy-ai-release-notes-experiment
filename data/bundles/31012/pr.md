# Pull request #31012: fix: keep the function argument in elementwise derivative rules

- Author: @rynwang
- Merged: 2026-11-09T20:03:24Z into `master`
- Labels: (none)
- Size: +34 / -3 in 5 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes item 2 of #30902

#### Brief description of what is fixed or changed

`ElementwiseApplyFunction._get_function_fdiff` (and the array-expression counterpart) replaces the derivative of an elementwise function by its *function class* whenever the derivative is a `Function`. That is only valid when the derivative is `f(d)` itself: for `exp(d + 1)` the argument is dropped and the result becomes `exp(d)`.

For example, on `master`:

```python
X = MatrixSymbol('X', 2, 2)
X.applyfunc(lambda z: exp(z + 1)).diff(X).as_explicit()[0, 0, 0, 0]  # exp(X[0, 0])
```

while the correct value is `exp(X[0, 0] + 1)`. The same happens for `sin(d + 1)`, `exp(2*d)`, and the `ArrayElementwiseApplyFunc` version.

The fix keeps the bare function class only when `fdiff.args == (d,)`; otherwise it wraps the derivative in a `Lambda`, so the argument is preserved. Common cases such as `sin(d)` / `exp(d)` keep their previous representation and behaviour.

#### Other comments

Two regression tests were added, one for `ElementwiseApplyFunction` and one for `ArrayElementwiseApplyFunc`. Both fail on `master` and pass with this change.

- `sympy/matrices/expressions/tests` + `sympy/tensor/array/expressions/tests`: 408 passed, 6 xfailed.
- Derivatives checked numerically against explicit elementwise differentiation for `exp(z+1)`, `sin(z+1)`, `exp(2z)` and `z**2 + 1`.

AI disclosure: this change was prepared with AI assistance (DeepSeek Harness coding agent) and reviewed by the account owner.

#### AI Generation Disclosure

AI tool: DeepSeek Harness coding agent (deepseek-flash). It generated the changes in
`sympy/matrices/expressions/applyfunc.py`, `sympy/tensor/array/expressions/array_expressions.py`,
`sympy/matrices/expressions/tests/test_applyfunc.py` and
`sympy/tensor/array/expressions/tests/test_arrayexpr_derivatives.py`.
The account owner reviewed the changes and the test results before submission.

## Commits

- e2e0612fe9 (Ryn Wang): fix: keep the function argument in elementwise derivative rules
- fb7275819a (Ryn Wang): chore: register author in .mailmap
- fbeeaec3ca (Ryn Wang): chore: keep .mailmap sorted

## Conversation

### @smichr commented

kudos for nice use of issue number without closing it :-)

Thanks for your work on this. Looks good.


## Reviews

### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin commented on `.mailmap`

@smichr can you check this before merging:
https://github.com/sympy/sympy/blob/530b96df17237dbdb81fb08aa734e82b18122873/.mailmap#L146-L148
