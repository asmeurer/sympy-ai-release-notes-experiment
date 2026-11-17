# Pull request #31010: matrices: fix trace evaluation and is_square for MatrixUnit

- Author: @vyassoham
- Merged: 2026-11-12T15:09:49Z into `master`
- Labels: (none)
- Size: +52 / -8 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

See #30900 (defect E3-6 in the matrices module review).

#### Brief description of what is fixed or changed

This PR resolves two related defects in `sympy.matrices.expressions.special.MatrixUnit`:

1. **Incorrect Trace Evaluation for $n \times n$ Matrix Units ($n > 1$):**
   In `MatrixUnit._eval_trace`, the method previously checked `if self.shape == (1, 1): return S.One` and unconditionally returned `S.Zero` for any square matrix unit of size $n > 1$. Consequently, evaluating the trace of any diagonal matrix unit larger than $1 \times 1$ erroneously produced 0:
   ```python
   >>> mu = MatrixUnit(3, 3, 1, 1)
   >>> Trace(mu).doit()
   0  # Incorrect: should be 1
   ```
   The trace of a matrix unit $E_{i,j} \in \mathbb{R}^{n \times n}$ is $\operatorname{Tr}(E_{i,j}) = \sum_{k=0}^{n-1} (E_{i,j})_{k,k} = \delta_{i,j}$ for $0 \le i < n$. The fix replaces the hardcoded conditional with `KroneckerDelta(self._i, self._j, (0, self.rows-1))` whenever `self.is_square` is True, correctly evaluating diagonal units (1), off-diagonal units (0), out-of-bounds indices (0), and symbolic indices/dimensions.

2. **Violation of the `MatrixExpr.is_square` Contract:**
   `MatrixUnit` previously defined a custom property `@property def is_square(self): return Eq(self.rows, self.cols)`. `Eq(...)` returns a SymPy boolean atom (`BooleanFalse` / `BooleanTrue`) or a relational expression, rather than a Python `bool` (`True`, `False`) or `None` as required by the `MatrixExpr.is_square` contract.
   
   Because `BooleanFalse` is not the Python primitive `False` singleton object, identity comparisons such as:
   ```python
   if mat.is_square is False:
       raise NonSquareMatrixError("Trace only defined on square matrices")
   ```
   evaluated to `False`. As a result, `Trace` failed to recognize non-square `MatrixUnit` instances (e.g. `MatrixUnit(3, 4, 1, 1)`), allowing non-square matrix units into `Trace` without raising `NonSquareMatrixError`.
   
   Removing this redundant override allows `MatrixUnit` to inherit `MatrixExpr.is_square`, properly returning Python primitive `bool` or `None`.

#### Other comments

- Changes are strictly isolated to `special.py` and its test file `test_special.py`.
- Regression tests were added covering:
  - All 9 elements of a $3 \times 3$ matrix unit verified against explicit matrix traces (`as_explicit()`).
  - Diagonal and off-diagonal units for $1 \times 1, 2 \times 2, 4 \times 4, 10 \times 10$.
  - Out-of-bounds index handling.
  - Linearity with `Trace(2 * E_11 + 3 * E_00).doit() == 5`.
  - Symbolic indices and dimensions returning `KroneckerDelta(i, j, (0, n - 1))`.
  - Verification that rectangular units raise `NonSquareMatrixError`.

#### AI Generation Disclosure

An AI coding assistant (Google DeepMind Antigravity) was used for exploratory analysis of issue #30900 and drafting initial test cases. All code changes in `special.py`, mathematical arguments, and test executions were manually inspected and validated against the local SymPy test suite.

## Commits

- ee5150f943 (vyassoham): matrices: fix trace evaluation and is_square for MatrixUnit
- 1c927c44c6 (vyassoham): authors: add Soham Vyas to .mailmap

## Conversation

### @sylee957 commented

It can be `KroneckerDelta(self.i, self.j)` than `KroneckerDelta(self.i, self.j, (0, self.rows-1))`
I'm not sure it's more useful than we just make out-of-bounds index undefined and simplify to `KroneckerDelta(self.i, self.j)`
Actually third argument is quite confusing and looks like naively implemented that it can break simplifcation `KroneckerDelta(n, n, (0, m))` should not be `1` because it need to check bound.
But I merged despite flaw because I want to get into comprehensive discussion later when this is exploited as bug.

### @vyassoham commented

Thank you @sylee957 for reviewing and merging!

I appreciate the insight regarding `KroneckerDelta`'s third argument and potential boundary simplification limitations. I'll keep an eye on this and would be happy to participate in any follow-up discussion whenever that refactor is explored.


## Reviews

(no reviews)
