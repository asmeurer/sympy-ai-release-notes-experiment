# Pull request #31011: matrices: fix trace evaluation for KroneckerProduct with rectangular …

- Author: @vyassoham
- Merged: 2026-11-12T14:40:11Z into `master`
- Labels: (none)
- Size: +50 / -0 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

See #30900 (defect E2-7 in the matrices module review).

#### Brief description of what is fixed or changed

This PR prevents an uncaught `NonSquareMatrixError` crash in `KroneckerProduct._eval_trace` when rectangular factors form an overall square Kronecker product:

1. **Bug and Root Cause:**
   `KroneckerProduct._eval_trace` previously called `trace(a)` unconditionally on every factor:
   ```python
   def _eval_trace(self):
       from .trace import trace
       return Mul(*[trace(a) for a in self.args])
   ```
   When factors $A_1, \dots, A_k$ are rectangular, but their overall Kronecker product is square (for example, $C \in \mathbb{R}^{2 \times 3}$ and $D \in \mathbb{R}^{3 \times 2}$, so $C \otimes D \in \mathbb{R}^{6 \times 6}$), calling `trace(C)` directly raised `NonSquareMatrixError: Trace only defined on square matrices`. Consequently, `Trace(C \otimes D)` and `trace(C \otimes D)` crashed even though the overall matrix expression is square and has a mathematically well-defined trace.

2. **Mathematical Rationale & Fix:**
   When every individual factor is square, the standard Kronecker-product trace identity applies:
   $$\operatorname{Tr}\left(\bigotimes_{k} A_k\right) = \prod_{k} \operatorname{Tr}(A_k)$$
   For rectangular factors, individual traces are undefined, so this factor-wise simplification cannot be used. The overall Kronecker product may nevertheless be square and have a well-defined trace.
   
   The fix checks `if not all(a.is_square for a in self.args): return None`. This matches the architectural pattern in `_eval_determinant` (line 154 of `sympy/matrices/expressions/kronecker.py`). When any factor is rectangular or of indeterminate squareness, `_eval_trace` returns `None`. `Trace(kp)` remains cleanly unevaluated as a symbolic expression without raising an exception.
   
   Expanding the product explicitly via `.as_explicit()` or coordinate representation correctly computes the exact numerical trace (verified against numerical matrix trace of 205). If the overall Kronecker product is known to be non-square, `Trace.__new__` continues to raise `NonSquareMatrixError`.

#### Other comments

- Changes are strictly isolated to `kronecker.py` and its test suite `test_kronecker.py`.
- Regression tests were added covering:
  - Square factors continuing to evaluate to $\prod \operatorname{Tr}(A_k)$.
  - Rectangular factors with square product ($2 \times 3 \otimes 3 \times 2$) remaining unevaluated `Trace(kp)`.
  - Numerical consistency verified with explicit numerical matrices.
  - Commutativity/order variation ($3 \times 2 \otimes 2 \times 3$).
  - Multi-factor products with mixed rectangular and square arguments ($2 \times 2 \otimes 2 \times 3 \otimes 3 \times 2$).
  - Multi-factor all-square products.
  - Non-square Kronecker products ($2 \times 3 \otimes 2 \times 2 \to 4 \times 6$) raising `NonSquareMatrixError`.
  - Indeterminate symbolic dimensions leaving `Trace` unevaluated.

#### AI Generation Disclosure

An AI coding assistant (Google DeepMind Antigravity) was used for exploratory analysis of the defect traceback in #30900 and drafting initial test cases. All code changes in `kronecker.py`, mathematical arguments, and test executions were manually inspected and validated against the local SymPy test suite.

## Commits

- 8cbb127113 (vyassoham): matrices: fix trace evaluation for KroneckerProduct with rectangular factors
- a6f3b632ff (vyassoham): authors: add Soham Vyas to .mailmap

## Conversation

(no comments)

## Reviews

(no reviews)
