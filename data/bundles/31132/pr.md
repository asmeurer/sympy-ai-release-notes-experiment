# Pull request #31132: algebras: fix Quaternion.from_rotation_matrix for 180-degree rotations

- Author: @hardikkaurani
- Merged: 2026-11-16T19:09:44Z into `master`
- Labels: algebras
- Size: +85 / -6 in 2 files (full diff in `diff.patch`)

## Description

﻿

#### References to other Issues or PRs
Fixes #31130

#### Brief description of what is fixed or changed
When converting a 3x3 rotation matrix corresponding to a 180-degree (pi radians) rotation around any 3D axis to a `Quaternion` via `Quaternion.from_rotation_matrix(M)`, `0 + 0*i + 0*j + 0*k` (zero quaternion, norm 0) was previously returned instead of a unit quaternion.

This occurred because for any 180-degree rotation, the matrix is symmetric (`M = 2*u*u^T - I = M^T`) with trace(M) = -1.
1. Because trace(M) = -1, the scalar part `a = sqrt(1 + trace(M)) / 2 = 0`.
2. Because M is symmetric, all antisymmetric off-diagonal differences vanish: `M[2, 1] - M[1, 2] = 0`, `M[0, 2] - M[2, 0] = 0`, and `M[1, 0] - M[0, 1] = 0`.
3. Multiplying b, c, d by `sign(...)` multiplied them by `sign(0) = 0`, zeroing out all vector components.

This update adopts the algebraic `leading_sign` recurrence suggested by @sylee957:
1. Uses `leading_sign` to determine relative component signs without premature conditional branching (`sign_b = leading_sign(ab)`, `sign_c = leading_sign(ac, bc)`, `sign_d = leading_sign(ad, bd, cd)`).
2. Eliminates substitution discrepancies between pre- and post-substituted symbolic rotation matrices (e.g. half-turns about `(cos(t), sin(t), 0)`).
3. Correctly handles both general and 180-degree rotations while remaining purely algebraic and compatible with SymPy's symbolic manipulation and assumptions.
4. Adds regression tests covering unit rotations (`Rx, Ry, Rz`), symbolic half-turn substitution consistency across multiple angles, and direct tests for `leading_sign`.

#### Other comments

#### AI Generation Disclosure
I used an AI assistant (Antigravity powered by Gemini 3.8 Flash (High)) to help investigate the root cause, verify the algebraic `leading_sign` formulation, and draft regression tests. I reviewed and verified the mathematical logic and test suite locally.

## Commits

- 181b216260 (Hardik Kaurani): algebras: fix Quaternion.from_rotation_matrix for 180-degree rotations
      Fixes #31130
      When converting a 180-degree rotation matrix (rotation by pi radians
      around any unit axis u) to a Quaternion via Quaternion.from_rotation_matrix,
      the matrix is symmetric (M = 2*u*u.T - I = M.T) and trace(M) = -1.
      Because trace(M) = -1, the scalar part a = 0.
      Because M is symmetric, all antisymmetric off-diagonal differences
      (M[j, k] - M[k, j]) vanish to 0. Multiplying b, c, d by sign(...)
      previously wiped out the vector components to 0, producing the zero
      quaternion (norm 0).
      This fix determines the signs of vector components from symmetric
      terms (4bc = M[0, 1] + M[1, 0], 4bd = M[0, 2] + M[2, 0], 4cd = M[1, 2] + M[2, 1])
      when a is zero, restoring exact unit quaternions for all 180-degree
      rotations and enabling exact matrix round-trips.
- faa0c11307 (Hardik Kaurani): algebras: use algebraic leading_sign recurrence in Quaternion.from_rotation_matrix
- e96b437cfb (Hardik Kaurani): quaternion: annotate leading_sign result as Expr for mypy

## Conversation

### @hardikkaurani commented

cc @sylee957 - Whenever you get some time, would appreciate a review on this Quaternion rotation matrix fix. Regression tests have been added for symmetric/180-degree rotations.

### @sylee957 commented

```python3
def leading_sign(*xs: Expr) -> Expr:
    """The sign of the first nonzero argument, and 1 if there is none."""
    result = S.One
    for x in reversed(xs):
        s = sign(x)
        # Keep the running value when x is zero, replace it by sign(x) otherwise.
        result = s + (1 - s**2) * result
    return result

def from_scaled_rotation_matrix(M: MatrixBase) -> Quaternion:
    """requires M = s*R with s >= 0 and R a rotation matrix."""
    scale = M.det() ** Rational(1, 3)

    # The absolute values of the four components, from 4a**2, 4b**2, 4c**2, 4d**2.
    abs_a = sqrt(scale + M[0, 0] + M[1, 1] + M[2, 2]) / 2
    abs_b = sqrt(scale + M[0, 0] - M[1, 1] - M[2, 2]) / 2
    abs_c = sqrt(scale - M[0, 0] + M[1, 1] - M[2, 2]) / 2
    abs_d = sqrt(scale - M[0, 0] - M[1, 1] + M[2, 2]) / 2

    # The six mixed products 4ab, 4ac, 4ad, 4bc, 4bd, 4cd.
    ab = M[2, 1] - M[1, 2]
    ac = M[0, 2] - M[2, 0]
    ad = M[1, 0] - M[0, 1]
    bc = M[0, 1] + M[1, 0]
    bd = M[0, 2] + M[2, 0]
    cd = M[1, 2] + M[2, 1]

    # The sign of each component relative to the first nonzero earlier one.
    sign_b = leading_sign(ab)
    sign_c = leading_sign(ac, bc)
    sign_d = leading_sign(ad, bd, cd)
    return Quaternion(abs_a, abs_b * sign_b, abs_c * sign_c, abs_d * sign_d)
```
Can you discuss with AI about replacing code with my suggested formula?
This is better because this does not premature branching, like the formula used in this PR
which gives obvious flaw with quaternions with symbolic parameters, substituted before and after

```python3
# A half turn about (cos t, sin t, 0), at t = pi/4.
_s = Symbol("t", real=True)
_m = Matrix([[cos(2 * _s), sin(2 * _s), 0], [sin(2 * _s), -cos(2 * _s), 0], [0, 0, -1]])
print(
    "#31132:",
    Quaternion.from_rotation_matrix(_m.subs(_s, pi / 4))
    - Quaternion.from_rotation_matrix(_m).subs(_s, pi / 4),
)
print(
    "new:   ",
    from_scaled_rotation_matrix(_m.subs(_s, pi / 4))
    - from_scaled_rotation_matrix(_m).subs(_s, pi / 4),
)
# 31132: 0 + sqrt(2)/2*i + sqrt(2)/2*j + 0*k
# new:    0 + 0*i + 0*j + 0*k
```

I have formally verified this formula with Lean4

https://github.com/sylee957/sympy-proofs/blob/ed9b9f4a2e3fd4530ae027b6df95d1026bb696f4/SympyProofs/Quaternion/FromRotationMatrix/ScaledSign.lean#L58-L79

Anyway I also explored further that, for matrices outside scaled SO(3) group, there is choice of normalization and sign that can give different formulas

for example, Cayley/Sheppard gave different formula, as noted in the comprehensive survey
https://digital.csic.es/bitstream/10261/202072/1/A%20Survey%20on%20the%20Computation_Sarabandi.pdf

I tried that but that gives more complicated symbolic expressions and I would not favor of that and it can be misleading to pick formulas optimized for numeric computation than symbolic computation.
For symbolic computation we generally want formulas optimized with fewest terms and easiest to simplify, and not formula based on pre determinism with numeric values, because that does not work very well with substitution

### @hardikkaurani commented

﻿Thanks @sylee957 for the detailed suggestion and the Lean4 formal proof!

We tested the proposed `leading_sign` recurrence against the symbolic half-turn counterexample:
```python
_s = Symbol("t", real=True)
_m = Matrix([[cos(2 * _s), sin(2 * _s), 0], [sin(2 * _s), -cos(2 * _s), 0], [0, 0, -1]])
```
While the previous branching implementation produced an evaluation discrepancy upon substitution (`0 + sqrt(2)/2*i + sqrt(2)/2*j + 0*k`), the algebraic `leading_sign` formula eliminates the premature branching completely and preserves exact substitution consistency (`q_sub_first == q_sym_sub`) across all angles.

We have updated the PR to:
1. Implement `leading_sign` and use it in `Quaternion.from_rotation_matrix` for relative sign selection.
2. Update the docstring example and test assertions to reflect the algebraic sign expression.
3. Add regression tests for `leading_sign`, 180-degree coordinate rotations, matrix round-trips, and symbolic half-turn substitution consistency across axes and angles.
4. Pass all doctests, unit tests, and code quality checks cleanly.


## Reviews

### @sylee957 reviewed: COMMENTED



### @hardikkaurani reviewed: COMMENTED



### @sylee957 commented on `sympy/algebras/quaternion.py`

If mypy gives error lets see if you can do type widening with `result: Expr = S.One` works

### @hardikkaurani commented on `sympy/algebras/quaternion.py`

Added explicit `result: Expr = S.One` type widening. `mypy sympy` now passes cleanly across all 1557 source files with zero issues.
