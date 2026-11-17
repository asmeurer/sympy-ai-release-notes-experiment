# Issues and pull requests referenced by this pull request

## Issue #14230: Sums of matrices

- Opened by @ghost, state: open

```
>>> A = diag(I/2, -I/3)
>>> Sum(n*A**n, (n, 0, oo)).doit()
⎡    ⅈ                 ⎤
⎢──────────      0     ⎥
⎢         2            ⎥
⎢  ⎛    ⅈ⎞             ⎥
⎢2⋅⎜1 - ─⎟             ⎥
⎢  ⎝    2⎠             ⎥
⎢                      ⎥
⎢               -ⅈ     ⎥
⎢    0       ──────────⎥
⎢                     2⎥
⎢              ⎛    ⅈ⎞ ⎥
⎢            3⋅⎜1 + ─⎟ ⎥
⎣              ⎝    3⎠ ⎦
```
I think the terms should be rewritten, in the form
```
>>> expand(radsimp(I/(2*(1 - I/2)**2)))
8    6⋅ⅈ
- ── + ───
  25    25
```

```
>>> A = diag(a, b)
>>> Sum(A**n, (n, 0, oo)).doit()
⎡⎧   1                                         ⎤
⎢⎪ ──────   for │a│ < 1                        ⎥
⎢⎪ -a + 1                                      ⎥
⎢⎪                                             ⎥
⎢⎪  ∞                                          ⎥
⎢⎪ ___                                         ⎥
⎢⎨ ╲                               0           ⎥
⎢⎪  ╲    n                                     ⎥
⎢⎪  ╱   a    otherwise                         ⎥
⎢⎪ ╱                                           ⎥
⎢⎪ ‾‾‾                                         ⎥
⎢⎪n = 0                                        ⎥
⎢⎩                                             ⎥
⎢                                              ⎥
⎢                        ⎧   1                 ⎥
⎢                        ⎪ ──────   for │b│ < 1⎥
⎢                        ⎪ -b + 1              ⎥
⎢                        ⎪                     ⎥
⎢                        ⎪  ∞                  ⎥
⎢                        ⎪ ___                 ⎥
⎢          0             ⎨ ╲                   ⎥
⎢                        ⎪  ╲    n             ⎥
⎢                        ⎪  ╱   b    otherwise ⎥
⎢                        ⎪ ╱                   ⎥
⎢                        ⎪ ‾‾‾                 ⎥
⎢                        ⎪n = 0                ⎥
⎣                        ⎩                     ⎦
```
I think the answer should be of the form
```
⎡  1           ⎤
⎢──────    0   ⎥
⎢-a + 1        ⎥                          if |a| < 1 and |b| < 1
⎢              ⎥
⎢          1   ⎥
⎢  0     ──────⎥
⎣        -b + 1⎦

  The sum does not exist otherwise
```

```
>>> A = diag(1/sqrt(2), pi/4)
>>> Sum(A**n, (n, 0, oo)).doit()
⎡   1             ⎤
⎢────────     0   ⎥
⎢  √2             ⎥
⎢- ── + 1         ⎥
⎢  2              ⎥
⎢                 ⎥
⎢             1   ⎥
⎢   0      ───────⎥
⎢            π    ⎥
⎢          - ─ + 1⎥
⎣            4    ⎦
```

I think `1/(-sqrt(2)/2 + 1)` should be radsimped

## Pull request #31067: Fix infinite sums of explicit matrices

- Opened by @shreeeeee-rgb, state: closed

#### References to other Issues or PRs

Fixes #14230

#### Brief description of what is fixed or changed

Infinite sums of explicit matrices are summed entry by entry. When an entry is a series whose convergence depends on a symbol, such as a geometric series, that entry evaluates to a Piecewise with its own convergence condition. The result was a matrix whose entries each carried a different condition. That doesn't represent the matrix series correctly, because a matrix series converges only when all of its entries converge.

This PR changes Sum.doit() in sympy/concrete/summations.py for explicit matrix summands with a single infinite upper limit:

- After the expanded sum is evaluated, the result goes through a new helper, _eval_matrix_sum_after_expansion.
- The helper collects the convergence condition from each entry's Piecewise and checks that the fallback branch is the original unevaluated Sum of that entry.
- If any entry still contains a Sum, is infinite, or has an unexpected Piecewise structure, the original unevaluated Sum is returned. This avoids returning a partly evaluated matrix.
- Numeric entries are simplified with expand(radsimp(...)).
- **hints are now passed through to expanded.doit(...).

The helper returns its input unchanged for anything outside this case (multiple limits, finite limits, non-matrix summands).

#### Other comments

Tests for the new behavior are included in the second changed file.

#### AI Generation Disclosure

Parts of this change were written with the help of an AI tool (OpenAI Codex). I reviewed, tested and understand all of the code. AI-generated lines: sympy/concrete/summations.py:29, 254-255, 1713-1755; sympy/concrete/tests/test_sums_products.py:1559-1577.
