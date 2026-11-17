# Issues and pull requests referenced by this pull request

## Issue #30900: Review of the matrices module: 179 verified defects, mostly in matrices.expressions

- Opened by @Upabjojr, state: open

*This issue was written by an AI agent (Claude Code, model Claude Fable 5.1) at the request of the account owner, who asked for a thorough review of the matrices module with focus on `sympy/matrices/expressions`. Every item below was found by a reviewer run and then independently re-run on master 6134f599e1 (Python 3.12); the outputs quoted are from those runs. Nothing here has been fixed yet; the point is to have one place to pick fixes from and to link duplicates.*

Scope: `sympy/matrices/expressions` (sections E1-E4), explicit matrices (M1 data layer, M2 decompositions/inverse/solvers/determinant, M3 eigen/reductions/subspaces/normal forms), a random-expression fuzzer (F), a re-run of all closed `matrices`/`matrices.expressions` issues to find ones closed without a fix, and a re-run of the open `matrices.expressions` issues to find ones already fixed. Common setup for snippets: `from sympy import *`, `x, y` plain symbols, `n, m` integer symbols, `i, j` integer symbols, `A, B, C, ...` are `MatrixSymbol`s with the shapes stated. Where an "Expected" is not given, it is the result of the explicit computation (`as_explicit()` / `Matrix`).

## 0. Cross-cutting root causes

1. **Negative indices are accepted but never normalised** in `MatrixExpr.__getitem__` (`valid_index` allows `i >= -rows`), so every structured `_entry` gets a raw negative index: E1-2, E3-11.
2. **`is_square is None` treated as `False`** for symbolic shapes: `BlockDiagMatrix` det/inverse (E3-4), `Q.square` and every `if not expr.is_square: return False` handler (E1-8, E4-9).
3. **`refine` confuses the elementwise conjugate with the adjoint**: `MatrixExpr.conjugate()` is `Adjoint(Transpose(X))`, but the unitary rules in `refine_Inverse`/`refine_MatMul` compare with it (E1-5, E2-3, E4-3); the orthogonal rule returns an identity of the inner dimension (E2-4); `refine(det(A), Q.orthogonal(A))` gives `1` (E4-2).
4. **`Transpose._eval_derivative` drops the transpose** (E1-4 / E4-1).
5. **`MatAdd`/`MatMul` are `Add`/`Mul` subclasses**, so core helpers build scalar+matrix or `Mul._from_args` trees the matrix constructors reject: `collect`, `factor`, `factor_terms`, `subs(simultaneous=True)`, `evalf` (RecursionError), `integrate`, `signsimp` inside `simplify` (E1-13, E2-5, E2-10, E2-12, E4-23, F-1). Umbrella: #6220.
6. **`_entry(i, j, **kwargs)` protocol not uniform**: `Transpose`/`MatMul` inject keywords that `CompanionMatrix._entry` rejects (E1-15, E3-12); `Transpose._entry` forces `expand=False` (E1-23).
7. **Eigenvalues equal only after simplification are treated as distinct**: lost multiplicities, singular `P` from `jordan_form`, wrong `is_diagonalizable` (M3-1, M3-2); the Float path never checks eigenvector independence (M3-5).
8. **Numeric ordering via `default_sort_key`** in `singular_values` and `diagonalize(sort=True)` (M3-3, M3-9).
9. **Sparse paths diverge from dense**: `applyfunc` skips zeros (M1-7), Cholesky/LDL skip zero diagonals (M2-1), least squares uses `.T` instead of `.H` (M2-5), triangular solves return `zoo` (M2-18), construction (M1-24), `solve` semantics (M2-21).
10. **Singular systems give `nan`/`zoo` instead of raising**: M1-3, M2-15, M2-16, M2-17, M2-19, E1-7.
11. **Assumption handlers answer True/False where only None is justified** (E4-4 to E4-13, E4-15).
12. **`Matrix.norm()` default regressed** from Frobenius to the spectral norm in e8f31a253f (typing annotations, unreleased; 1.14.0 is fine): M1-1, with more `norm` edge cases in M1-4/5/6/30.

## 1. Matrix expressions

<details><summary><b>E1. matexpr / _shape / slice / transpose / adjoint / inverse / matpow (29)</b></summary>

Wrong results
- **E1-1** `(C**2)**S.Half` -> `C`; `(C**n)**(1/n)` -> `C`; `(C**x)**y` -> `C**(x*y)`. `MatPow.doit` merges nested powers for any outer exponent; with `P = Matrix([[0,1,0],[1,0,0],[0,0,1]])` the explicit `(P**2)**S.Half` is `eye(3)`, the symbolic chain gives `P`. (`matpow.py:66`)
- **E1-2** Negative indices wrong: `Identity(3)[-1, 2]` -> `0` (explicit `1`); `Xs[2:5, 3:6][-1, -1]` -> `Xs[1, 2]` (should be `Xs[4, 5]`); `W[-1, 0].diff(W[1, 0])` -> `0`; `(A*B)[-1, 0] != (A*B).as_explicit()[-1, 0]`; `FunctionMatrix(3,3,Lambda((i,j),i+j))[-1,0]` -> `-1`. (`matexpr.py:294-335`)
- **E1-3** `MatrixSlice.shape` uses `floor`: `X5[::2, ::2].shape` -> `(2, 2)` for a 5x5 symbol (explicit `(3, 3)`), the last row/column is dropped in `as_explicit()`; `test_slice.py:40` asserts the `floor` formula. (`slice.py:72-77`)
- **E1-4** `Transpose(x*A).diff(x)` -> `A` (shape `(2,3)`, should be `A.T`); `(C.T).diff(C[0, 1])` -> `MatrixUnit(3, 3, 0, 1)` (should be `(1, 0)`). (`transpose.py:71`)
- **E1-5** `refine(W.I, Q.unitary(W))` -> `Adjoint(W.T)` = elementwise conjugate; for `U = Matrix([[0, I], [1, 0]])` (unitary) this gives `[[0, -I], [1, 0]]` while `U.inv()` is `[[0, 1], [-I, 0]]`. (`inverse.py:98`)
- **E1-6** `Adjoint(MatPow(W1, I)).doit()` -> `Adjoint(W1)**I`: the exponent is not conjugated (1x1 check: `2**I` vs explicit `2**(-I)`). (`matpow.py:93-99`)
- **E1-7** `MatMul(0, C).inverse()` -> `zoo*C**(-1)` while `Inverse(MatMul(0, C)).doit()` raises. (`matmul.py:214`)
- **E1-8** `ask(Q.square(X))` -> `False` for `X` n x m (should be None). (`assumptions/handlers/matrices.py:37`)
- **E1-9** `MatrixSymbol('Z', 0, 3).as_explicit().shape` -> `(0, 0)`; `.equals(zeros(0, 3))` -> `False`. (`matexpr.py:369`)

Crashes
- **E1-10** `MatPow(C, n)[0, 0]` and `MatPow(C, S.Half)[0, 0]` for a 3x3 symbol do not return (symbolic Jordan form in `_entry`); any `as_explicit()`/`equals()` on such an expression hangs. (`matpow.py:44-57`)
- **E1-11** `X[a:b, :][1:2, :]` -> `TypeError: cannot determine truth value of Relational` (`slice_of_slice`, `if stop > stop1`). (`slice.py:97`)
- **E1-12** `MatrixSlice(Matrix(3, 3, range(9)), (0, 2), (0, 2))[1, 1]` -> `AttributeError: 'MutableDenseMatrix' object has no attribute '_entry'` (parent not sympified). (`slice.py:57`)
- **E1-13** `collect(x*C + x*D, x)` and `factor_terms(2*C + 4*D)` -> `TypeError: Mix of Matrix
