# Pull request #31077: fix(matrices): refine unitary matrices to Adjoint and simplify products

- Author: @ish1416
- Merged: 2026-11-15T13:06:20Z into `master`
- Labels: (none)
- Size: +36 / -13 in 6 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Follow-up to #31021.
Addresses items E1-5, E2-3, E2-4, and E4-3 from #30900.

#### Brief description of what is fixed or changed

In #31021, we properly separated `Conjugate` (elementwise matrix complex conjugation) from `Adjoint` (conjugate transpose). This PR updates the `refine` and assumption handlers to use `Adjoint` for unitary matrices:

1. **`refine_Inverse` (E1-5)**:
   For a unitary matrix $U$, the definition of unitary is $U^{-1} = U^\dagger = \text{Adjoint}(U)$. Previously, `refine_Inverse` returned `expr.arg.conjugate()` (elementwise conjugate), which is incorrect for complex unitary matrices. Now returns `expr.arg.adjoint()`.

2. **`refine_MatMul` (E2-3 & E2-4)**:
   - Checked `arg == last.conjugate()` instead of `last.adjoint()`. Now simplifies $(U U^\dagger)$ and $(U^\dagger U)$ to `Identity` when $U$ is assumed unitary.
   - Fixed dimension for rectangular orthogonal matrix products (E2-4): $An \cdot An^T$ for shape $(n, m)$ now correctly yields `Identity(n)` (`Identity(last.shape[0])`) instead of `Identity(m)` (`Identity(arg.shape[0])`).

3. **Matrix Assumption Handlers (E4-3)**:
   Registered `Adjoint` and `Conjugate` in `UnitaryPredicate`, `InvertiblePredicate`, `FullRankPredicate`, and `DiagonalPredicate` in `sympy/assumptions/handlers/matrices.py`.

#### Other comments

All 307 tests in `sympy/matrices/expressions/tests/`, 22 tests in `sympy/assumptions/tests/test_matrices.py`, and all doctests in `inverse.py` and `matmul.py` pass with zero regressions.

#### AI Generation Disclosure

I used an AI assistant to explore test cases. I reviewed the change, ran the tests and doctests locally, and I can explain the code and the reasoning behind it.

## Commits

- e55b95f285 (Ishita Singh): fix(matrices): refine unitary matrices to Adjoint and simplify products
      Refining Inverse of a unitary matrix previously returned its elementwise
      Conjugate instead of Adjoint (Hermitian conjugate transpose). Likewise,
      refine_MatMul checked for Conjugate rather than Adjoint and used an inner
      dimension instead of the outer row dimension for rectangular orthogonal
      products.
      In addition, register Adjoint and Conjugate for UnitaryPredicate,
      InvertiblePredicate, FullRankPredicate, and DiagonalPredicate in matrix
      assumption handlers.
      Addresses items E1-5, E2-3, E2-4, and E4-3 from #30900.
- 660c0255db (Ishita Singh): refactor(matrices): express orthogonal and unitary assumptions disjunction via | in refine_MatMul

## Conversation

### @sylee957 commented

Can you ask AI if it is possible to express `ask(Q.orthogonal(arg), ...) or ask(Q.orthogonal(last), ...))` into `ask(Q.orthogonal(arg) | Q.orthogonal(last), ...)` and similar?

### @ish1416 commented

Yes, tested it out and `ask(Q.orthogonal(arg) | Q.orthogonal(last), assumptions)` works nicely in a single query! Updated both the orthogonal and unitary checks to use `|` and pushed the commit.


## Reviews

(no reviews)
