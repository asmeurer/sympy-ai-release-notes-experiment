# Pull request #31037: Fix interval measure for reversed/symbolic bounds using Max(0, end - start)

- Author: @Hirata-Origami
- Merged: 2026-11-11T16:01:57Z into `master`
- Labels: (none)
- Size: +63 / -3 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs
Fixes #31030. Also addresses the maintainer's request to compare `Max` versus `Piecewise` (see the maintainer's comment here: https://github.com/sympy/sympy/issues/31030#issuecomment-6780930328).

#### Brief description of what is fixed or changed
- **The problem:** `Interval(a, b).measure` previously returned `b - a`, which evaluates to a negative value when `b < a`.
- **The change:** It now returns `Max(0, end - start)`.
- **Comparison & reasoning:** While both `Max` and `Piecewise` variants fix the bug equally and pass identical downstream checks, `Max` is chosen because it is a plain function rather than a conditional with bound variables. This makes it safer to embed in other expressions and avoids noisy relational conditions (such as `b >= -oo` on infinite intervals).
- **The tests:** `test_measure` was updated to reflect the new behavior, and a new test `test_Interval_measure_reversed_symbolic_endpoints` was added.

#### Other comments
- Both variants break the exact same single test (`test_measure`), which previously encoded the buggy behavior.
- `Max` yields significantly cleaner output expressions.
- Extensively tested: ran the test suites for `sympy/sets`, `calculus`, `solveset`, `inequalities`, and `stats`, along with all sets doctests.

#### AI Generation Disclosure
An AI assistant helped compare the `Max` vs. `Piecewise` variants, drafted the one-line code change, and drafted the corresponding test cases across `sympy/sets`. I reviewed the changes thoroughly, verified them, and ran the test suite locally.

## Commits

- 5af7d06687 (Hirata-Origami): Interval.measure: use Max(0, end - start)
- ef81fa632c (Hirata-Origami): author: add Hirata-Origami to .mailmap
      Co-Authored-By: Claude <noreply@anthropic.com>
- 8962fb7c05 (Hirata-Origami): sets: test Interval.measure with sign assumptions, infinite endpoints and empty intervals

## Conversation

(no comments)

## Reviews

### @smichr reviewed: COMMENTED



### @Hirata-Origami reviewed: COMMENTED



### @smichr commented on `sympy/sets/tests/test_sets.py`

We should probably test negative and nonpositive, too. And finite=False assumptions -- will it work for (-oo,oo), (0,oo)?

Does an interval with 0 measure also report EmptySet?

### @Hirata-Origami commented on `sympy/sets/tests/test_sets.py`

Thanks, added tests in 8962fb7 (`test_Interval_measure_assumptions`, `test_Interval_zero_measure_not_always_empty`):

- **negative / nonpositive:** `Interval(n, 0).measure == -n`, `Interval(n, p).measure == p - n`, `Interval(nonpos, 0).measure == -nonpos`, and `Interval(0, nonpos).measure == 0` (`Max` collapses using the sign assumptions). `Interval(0, n)` with `n` negative is already `EmptySet`.
- **infinite endpoints:** `(-oo, oo)`, `(0, oo)`, `(-oo, 0)`, `(-oo, a)`, `(a, oo)` all give `oo`, and a symbol with `extended_positive=True, finite=False` gives itself.
- **zero measure vs `EmptySet`:** not equivalent. Provably empty intervals (`Interval(3, 1)`, `Interval.open(a, a)`, `Interval(0, n)`) are `EmptySet` with measure 0, but a single point (`Interval(1, 1)`, `Interval(a, a)`) is a `FiniteSet` with measure 0. For undetermined cases such as `Interval(a, b)` or `Interval(0, nonpos)`, `is_empty` is `None`, so nothing claims `EmptySet`.

One thing I found while checking `finite=False`: for a symbol like `Symbol('f', extended_real=True, finite=False)` (infinite but sign unknown), `f <= 0` evaluates to `True` on master, so `Max(0, f)` returns `0` and `Interval(0, f).measure` becomes `0` with this change (it was `f` before). That comes from the relational evaluation / assumptions for such symbols, not from `_measure`, so I left it out of the tests here. Happy to open a separate issue if you think it's worth tracking.
