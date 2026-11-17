# Issues and pull requests referenced by this pull request

## Issue #31083: trigsimp with method='groebner' or 'combined' raises PolificationFailed for y + sin(x)**2 + cos(x)**2

- Opened by @csp256, state: closed

`trigsimp` with `method='groebner'` or `method='combined'` raises `PolificationFailed` when the expression has a term that does not involve the trigonometric functions and whose coefficient is a number.

### Reproducer

```python
>>> from sympy import trigsimp, sin, cos, tan
>>> from sympy.abc import x, y
>>> trigsimp(y + sin(x)**2 + cos(x)**2, method='groebner')
Traceback (most recent call last):
...
sympy.polys.polyerrors.PolificationFailed: Cannot construct polynomials from 1, 1
>>> trigsimp(y + sin(x)**2 + cos(x)**2, method='combined')
Traceback (most recent call last):
...
sympy.polys.polyerrors.PolificationFailed: Cannot construct polynomials from 1, 1
```

The expected result is `y + 1`. The same happens for `2*y + 3 + sin(x)**2 + cos(x)**2` and `y + tan(x)*cos(x)`. When every term involves the other symbol, it works: `trigsimp(y*sin(x)**2 + y*cos(x)**2, method='groebner')` gives `y`.

### How this was found

Simplifying Riemann tensor components of the Kerr metric (rational functions of `sin(theta)`, `cos(theta)`, `r`, `M` and `a`) with the different `trigsimp` methods: `method='combined'` failed with this error on one of them, and the reproducer above is the smallest expression that shows the same failure.

### Cause

In `trigsimp_groebner`, when the expression has generators that are not involved in the trigonometric ideal (`freegens`), the numerator is split into one coefficient per monomial in those generators, and for each coefficient the generators it involves are found with

```python
ourgens = set(parallel_poly_from_expr([coeff, denom])[1].gens)
```

(`sympy/simplify/trigsimp.py`, line 384 on master). If `coeff` and `denom` are both numbers (here, the coefficient of `y` is `1` and the denominator is `1`), there is nothing to build polynomials from and `parallel_poly_from_expr` raises `PolificationFailed`. The same function already catches this exception for its first `parallel_poly_from_expr` call (line 361) but not here.

### Proposed fix

A number coefficient involves no generators, so treat it that way:

```python
try:
    ourgens = set(parallel_poly_from_expr([coeff, denom])[1].gens)
except PolificationFailed:
    ourgens = set()
```

With this change the reproducer gives `y + 1` for both methods, `2*y + 3 + sin(x)**2 + cos(x)**2` gives `2*y + 4`, `y + tan(x)*cos(x)` gives `y + sin(x)`, and `sympy/simplify/tests/test_trigsimp.py` passes (28 passed, 1 xfailed).

### Versions

Reproduced with SymPy 1.14.0 and master `2864aaefe1` (1.15.0.dev), Python 3.14.0, macOS arm64, ground types `python`.

---

*Investigation and write-up assisted by an AI model (Claude), reproduced, checked and reviewed by me.*
