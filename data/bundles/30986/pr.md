# Pull request #30986: fix regression in `monotonic_sign`

- Author: @smichr
- Merged: 2026-11-09T14:41:50Z into `master`
- Labels: (none)
- Size: +258 / -158 in 5 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Closes #30976  
Alternative to #30978  
Corrects an overgeneralization introduced in #30882

#### Brief description of what is fixed or changed

The general derivative-based sign inference introduced in #30882 has been replaced with explicit monotonicity checks for `exp`, `log`, and `sqrt` functions with univariate affine arguments, subject to appropriate domain restrictions. This preserves useful improvements in sign inference without the unsound generalization.

For anyone reviewing, it would be sufficient to look at the 2nd commit to see what has essentially changed. The first commit is concerned with moving `linear_coeffs` from solveset to exprtools.

The proposed fix in #30978 requires a variable-dependent denominator to have a known strict sign. However, this is insufficient because a denominator can be strictly positive at every integer while the expression has a discontinuity between consecutive integers.

For example:

```python
n = Dummy(integer=True, nonnegative=True)
t = 2*n - 1
f = Mul(t, Pow(t, -2, evaluate=False), evaluate=False)

assert f.as_numer_denom()[1].is_extended_positive is True
assert f.diff(n).is_negative is True

assert f.subs(n, 0) == -1
assert f.subs(n, 1) == 1
```

Although the denominator is positive and the derivative is negative at every allowed integer, the expression changes sign between `n = 0` and `n = 1` because of a pole at `n = 1/2`.

The same problem can arise without a variable-dependent denominator:

```python
g = n - 2*sign(n - S.Half)

assert g.diff(n).is_positive is True
assert g.subs(n, 0) == 2
assert g.subs(n, 1) == -1
```

Here the derivative is positive at integer values, but the expression decreases across a discontinuity.

Thus, derivative signs evaluated under integer assumptions do not establish monotonicity over the real interval between consecutive integers.

#### Other comments

`linear_coeffs` is used to recognize affine arguments without polynomial conversion or expansion. Since extracting linear coefficients is a general expression-analysis operation rather than a solver-specific task, `linear_coeffs` and `NonlinearError` have been moved to `exprtools`. The original import path in `solveset` is retained for backward compatibility.

#### AI Generation Disclosure

Collaborated with ChatGPT to review the changes introduced in #30882, identify the unsound derivative-based inference, develop a more conservative implementation, and add regression tests.

## Commits

- d8bd7a6ff9 (Christopher Smith): move linear_coeffs to exprtools
- 00f100ca16 (Christopher Smith): core: restrict nonpolynomial sign inference to safe monotonic families

## Conversation

(no comments)

## Reviews

### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @smichr commented on `sympy/core/tests/test_exprtools.py`

deleted tests are moved to the added functions below

### @smichr commented on `sympy/core/tests/test_exprtools.py`

This is just relocated here from its original location in `test_solveset` and a test that the import from solveset.py still works along with the error that used to be located there (NonlinearError).

### @smichr commented on `sympy/core/exprtools.py`

These are only relocated here from `solveset.py`. No other modifications were made.

### @oscarbenjamin commented on `sympy/core/exprtools.py`

Why were they moved?
