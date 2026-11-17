# Issues and pull requests referenced by this pull request

## Issue #30976: Regression: sign inference makes Abs and sqrt return negative values for integer expressions

- Opened by @vatsalyd, state: closed

### Description

Core sign inference incorrectly treats a sign-changing rational expression as always negative. This silently makes `Abs` and `sqrt` return negative values and causes incorrect `sign`, inequality, and `Piecewise` evaluation.

### Reproducer

```python
from sympy import Abs, Rational, Symbol, sign, sqrt

n = Symbol('n', integer=True, nonnegative=True)
f = 1/(2*n - 1) - Rational(1, 2)

print(Abs(f).subs(n, 1))
print(sqrt(f**2).subs(n, 1))
print(sign(f).subs(n, 1))
print(Abs(f.subs(n, 1)))

```

Actual output on current master:

```text
-1/2
-1/2
-1
1/2
```

Expected output:

```text
1/2
1/2
1
1/2
```

At `n = 1`, `f` is exactly `1/2`. The denominator `2*n - 1` is never zero for integer `n`, so all allowed inputs are valid. Evaluating the same absolute value before or after substitution gives opposite signs.

Also, `f.is_negative` and `f < 0` incorrectly evaluate to `True`. Consequently, `Piecewise((1, f < 0), (2, True)).subs(n, 1)` returns `1` instead of `2`, and `simplify(Abs(f) + f)` returns `0` instead of retaining the dependence on `n`.

### Regression and cause

The regression begins with commit `ccf7f5732b145de0da03db190d1f957aaefb8f9a` (#30882). The reproducer was executed against separate, unmodified source snapshots immediately before and after that commit. The parent revision `8d955e7ef24b0322e4ae5e168c2b64a881c15f14` gives the expected output.

The new non-polynomial branch of `_monotonic_sign` uses the negative derivative `-2/(2*n - 1)**2` and the value at `n = 0` to infer a uniformly negative sign. However, the continuous extension has a pole at `n = 1/2`; derivative sign does not establish monotonicity across it. Indeed, `f(0) = -3/2`, while `f(1) = 1/2`.

### Environment and validation

- Upstream master `c508f90ea0b0c33169eb11ca2e1705ca2233e996`; SymPy `1.15.0.dev3298+gc508f90ea0.uninstalled`.
- CPython `3.14.8`, Windows, Python integer ground types.
- Locally reproduced in five fresh processes with different hash seeds.
- Also reproduced for `1/(k*n - 1) - Rational(1, k)` with `k = 4, 6, 8`.
- All 14 existing tests in `sympy/core/tests/test_exprtools.py` pass using SymPy's built-in test runner.

### AI Generation Disclosure

OpenAI Codex (GPT-6) helped draft this report. The error was reproduced locally on the checkout above and verified against the before-and-after revisions described in this report.

## Pull request #30978: core: require strictly signed denominators for _monotonic_sign derivative check

- Opened by @knowprasad, state: closed

#### References to other Issues or PRs

Fixes #30976

#### Brief description of what is fixed or changed

In `sympy.core.exprtools._monotonic_sign`, derivative-based endpoint analysis is used to determine if a univariate expression is strictly positive or negative based on the sign of `self.diff(x)` and the boundary evaluation `self.subs(x, x0)`.

For expressions where the denominator contains the free symbol `x`, the derivative of the continuous function does not imply monotonicity across the variable's domain if the denominator changes sign on the real axis. Even when `x` is declared with `integer=True` (where `(2*n - 1).is_extended_nonzero` evaluates to `True`), the continuous extension has a pole at $n = 1/2$ and $2n - 1$ changes sign between $n = 0$ ($-1$) and $n = 1$ ($+1$).

This caused `1/(2*n - 1) - Rational(1, 2)` to be incorrectly inferred as negative for `n = Symbol('n', integer=True, nonnegative=True)`, which caused `Abs(f)` and `sqrt(f**2)` to evaluate to negative values upon substitution (e.g., `Abs(f).subs(n, 1)` returning `-1/2`).

This change:
1. In `_monotonic_sign`, requires that when the denominator contains `x`, it must be strictly positive or strictly negative (`den.is_extended_positive is True or den.is_extended_negative is True`) before applying continuous derivative endpoint analysis.
2. If the denominator is not strictly signed, derivative-based sign inference is bypassed and deferred to the numerator/denominator sign analysis.
3. Adds regression tests in `sympy/core/tests/test_exprtools.py` and `sympy/core/tests/test_assumptions.py`.

#### Other comments

Unit tests added and verified with pytest.

#### AI Generation Disclosure

Antigravity AI was used to assist with locating the denominator sign handling in `sympy/core/exprtools.py` and writing regression tests in `sympy/core/tests/test_exprtools.py` and `sympy/core/tests/test_assumptions.py`.

## Pull request #30882: better inference with monotonic expressions and additive non-Rational numbers

- Opened by @smichr, state: closed, merged 2026-10-29

#### References to other Issues or PRs

fixes #9154

#### Brief description of what is fixed or changed

The extended sign assumption for Add (is_extended_positive, etc...) did not use end-point analysis on anything but expressions with a Rational additive constant. Now, expressions with additive constants comprised of extended_real numbers are analyzed so `pi - Dummy(integer=True,positive=True) < 3` is recognized as True.

`_monotonic_sign` now analyzes monotonic univariate functions, not only polynomials. This allows endpoint-based sign inference for expressions when the variable range and derivative sign are known (as for `exp(x)` and `log(x)`).

#### Other comments

#### AI Generation Disclosure

This is a collaboration with ChatGPT.
