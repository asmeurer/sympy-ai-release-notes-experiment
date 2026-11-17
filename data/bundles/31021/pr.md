# Pull request #31021: feat(matrices): implement Conjugate(MatrixExpr) for matrix complex conjugation (fixes #16498, fixes #30900)

- Author: @ish1416
- Merged: 2026-11-12T08:34:27Z into `master`
- Labels: (none)
- Size: +245 / -12 in 16 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs
Fixes #16498
#30900 (regression from #30983)

#### Brief description of what is fixed or changed
As suggested by @sylee957, this PR implements `Conjugate(MatrixExpr)` as a first-class matrix expression in `sympy.matrices.expressions.conjugate`:

1. **`class Conjugate(MatrixExpr)`**:
   - Represents the elementwise complex conjugate $\overline{A}$ of a matrix expression.
   - Symmetrically completes the Klein four-group with `Transpose` and `Adjoint`:
     - $\overline{A}^T = A^\dagger$
     - $\overline{A}^\dagger = A^T$
     - $(A^\dagger)^T = \overline{A}$
     - $\overline{\overline{A}} = A$
   - Implements `refine()` handler for `Q.real_elements(A)`.
2. **Dispatch in scalar `conjugate.eval`**:
   - When `conjugate(arg)` receives an unevaluated matrix expression, it dispatches to `Conjugate(arg)` instead of scalar `conjugate`.
   - This cleanly eliminates `AttributeError: 'conjugate' object has no attribute 'shape'` on unevaluated matrix powers like `(C**-2).adjoint()` or `(C**I).adjoint()` without needing unproven nonsingularity assumptions in `MatPow`.
3. **Dispatch across expressions**:
   - Implemented `_eval_conjugate` on `MatrixExpr`, `MatMul`, `MatAdd`, and `BlockMatrix`.
4. **Printers**:
   - Pretty: $\overline{A}$ (overline bar).
   - LaTeX: `\overline{A}`.
   - Str: `Conjugate(A)`.

#### Other comments
Added comprehensive test suite in `sympy/matrices/expressions/tests/test_conjugate.py` covering shapes, Klein four-group duality, explicit matrices, refine, pretty/latex printing, and issue #16498 / #30900 regression tests.

#### AI Generation Disclosure
I used an AI assistant (Antigravity) to help explore the architectural design and draft the patch. I have personally verified the math and tests myself and understand the code.

## Commits

- e5470cb9bc (Ishita Singh): feat(matrices): implement Conjugate matrix expression for complex matrix conjugate
      - Add Conjugate class in sympy.matrices.expressions.conjugate inheriting from MatrixExpr
      - Dispatch MatrixExpr in sympy.functions.elementary.complexes.conjugate.eval to Conjugate
      - Implement _eval_conjugate across MatrixExpr, MatMul, MatAdd, and BlockMatrix
      - Support pretty, LaTeX (\overline{A}), and str printing for Conjugate
      - Add complete Klein four-group symmetry tests and fix Issue #16498
- 3e65388585 (Ishita Singh): test(matrices): add shape and multiplication test for negative power adjoint
- b1113fe485 (Ishita Singh): style: remove unused imports in test_conjugate
- c029d5429e (Ishita Singh): refactor(matrices): use idiomatic is_Matrix checks in Conjugate
- b08e3e96de (Ishita Singh): refactor(matrices): rely on MatrixExpr._eval_conjugate fallback and simplify Conjugate.doit
- 5ad08e22ac (Ishita Singh): refactor(matrices): remove redundant _eval_derivative in Conjugate
- b8ef06d5f9 (Ishita Singh): test: add test_args entry and fix doctest for Conjugate
- 88a4b98554 (Ishita Singh): style: remove trailing extra newline in conjugate files
- afefa04871 (Ishita Singh): Merge remote-tracking branch 'upstream/master' into fix-matpow-negative-power-adjoint

## Conversation

### @sylee957 commented

> However, all integer powers $k \in \mathbb{Z}$ (positive, zero, or negative) satisfy:
$(A^k)^\dagger = (A^\dagger)^k$ and $\overline{A^k} = (\overline{A})^k$.

This only holds for nonsingular matrix. So strictly it should be restricted to positive integers
we can give ambient assumption that arbitrary expression that is passed to `Inverse` or `MatPow`are just nonsingular
but that may not be true because we definitely have in new assumption system about singular matrix
we have to be careful about employing assumptions correctly in places like `refine`

https://docs.sympy.org/latest/modules/assumptions/predicates.html#sympy.assumptions.predicates.matrices.SingularPredicate

Can you investigate if things can be fixed in alternative way, like defining `Conjugate` and using it instead of scalar `conjugate` and then it does not give attribute error?

https://github.com/sympy/sympy/issues/16498

### @ish1416 commented

You are completely right @sylee957 — for negative powers, $(A^k)^\dagger = (A^\dagger)^k$ strictly requires $A$ to be nonsingular/invertible, so unconditionally distributing over negative exponents is mathematically unsound and can clash with `SingularPredicate` / `Q.singular` assumptions in `refine`.

I investigated defining `Conjugate` as you suggested (#16498), and it cleanly addresses the root cause:

1. **Why the crash happens:** Currently, when an unevaluated matrix conjugate cannot be simplified (for example `(C**-2).adjoint()` or even `(C**I).adjoint()` on master), SymPy falls back to scalar `sympy.functions.elementary.complexes.conjugate`. Because that scalar function does not inherit from `MatrixExpr`, accessing `.shape` raises `AttributeError: 'conjugate' object has no attribute 'shape'`, and `MatMul` raises `NotImplementedError`.
2. **With `Conjugate(MatrixExpr)`:**
   - Symmetrically completes the Klein four-group with `Transpose` and `Adjoint`:
     - `Conjugate(A).transpose() -> Adjoint(A)`
     - `Conjugate(A).adjoint() -> Transpose(A)`
     - `Conjugate(A).conjugate() -> A`
   - Keeps `MatPow._eval_adjoint` and `_eval_conjugate` safely restricted to positive/nonnegative integers, avoiding any ambient nonsingularity assumptions.
   - For negative or generic powers, `(C**k).adjoint()` safely evaluates to `Conjugate(C.T**k)`, which preserves `.shape`, entry indexing, and matrix multiplication.

Would you prefer me to implement `Conjugate(MatrixExpr)` in this PR to resolve both #16498 and this regression cleanly?

### @sylee957 commented

Sure can you repurpose this PR to implement `Conjugate(MatrixExpr)` instead?

### @ish1416 commented

Done, I've repurposed this PR to implement `Conjugate(MatrixExpr)`:

- Added `Conjugate` in `sympy.matrices.expressions.conjugate` with Klein four-group duality (`.transpose() -> Adjoint`, `.adjoint() -> Transpose`, `.conjugate() -> self.arg`).
- Added dispatch in scalar `conjugate.eval` for `arg.is_Matrix`, resolving #16498 and keeping `(C**-2).adjoint()` and `(C**I).adjoint()` as valid matrix expressions without needing ambient nonsingularity in `MatPow`.
- Implemented `_eval_conjugate` on `MatMul`, `MatAdd`, and `BlockMatrix`.
- Added pretty ($\overline{A}$) and LaTeX (`\overline{A}`) printers along with full test coverage.

### @sylee957 commented

Can you ask AI to do runtime/dynamic inspection (with debugger MCP/CLI) that it can get rid of `getattr` or `hasattr` used?

### @ish1416 commented

Updated! Cleaned up all dynamic `getattr`/`hasattr` checks in favor of standard SymPy idioms:
- Used `arg.is_Matrix` directly in `complexes.py` and `conjugate.py` (matching `Inverse`/`Trace`/`Adjoint`)
- `Conjugate.doit` now delegates directly via `conjugate()` matching `Adjoint.doit`
- Direct shape assertion in `test_matpow.py`

### @sylee957 commented

Can you merge master to resolve issues in CI?

### @ish1416 commented

Merged upstream master!

### @oscarbenjamin commented

It isn't necessary to merge master. It gets merged each time CI is run.

### @ish1416 commented

Ah got it, thanks for letting me know!


## Reviews

### @sylee957 reviewed: COMMENTED



### @sylee957 reviewed: COMMENTED



### @sylee957 reviewed: COMMENTED



### @ish1416 reviewed: COMMENTED



### @ish1416 reviewed: COMMENTED



### @ish1416 reviewed: COMMENTED



### @sylee957 commented on `sympy/functions/elementary/complexes.py`

Can you ask if it is feasible to solve this alternatively by defining _eval_conjugate base fallback to MatrixExpr?

### @sylee957 commented on `sympy/matrices/expressions/conjugate.py`

Can we get rid of isinstance(arg, Basic) if it is always Basic with dynamic runtime inspection with debugger?

### @sylee957 commented on `sympy/matrices/expressions/conjugate.py`

Can you ask if this override is necessary?

### @ish1416 commented on `sympy/functions/elementary/complexes.py`

Yes, exactly! Defining `_eval_conjugate` on `MatrixExpr` returning `Conjugate(self)` works cleanly as the base fallback, and subclasses like `MatPow` fall back to `super()._eval_conjugate()`. Reverted `complexes.py` completely so scalar logic stays untouched.

### @ish1416 commented on `sympy/matrices/expressions/conjugate.py`

Done, since `mat` is always sympified into `Basic` in `__new__`, `arg` is guaranteed to be `Basic`, so `isinstance(arg, Basic)` has been removed.

### @ish1416 commented on `sympy/matrices/expressions/conjugate.py`

Not necessary at all — inheriting `MatrixExpr._eval_derivative` directly handles zero-matrix evaluation for independent variables and keeps dependent cases unevaluated (matching `Adjoint`). Removed it.
