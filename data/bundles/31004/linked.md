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

## Issue #30902: Review of the matrix/array derivative algorithm: 35 verified defects (follow-up to #30900)

- Opened by @Upabjojr, state: open

*This issue was written by an AI agent (Claude Code, model Claude Fable 5.1) at the request of the account owner, as a follow-up to #30900 focused on the matrix/array derivative algorithm. Every item was found by a reviewer run and then independently re-run on master 6134f599e1 (Python 3.12). Three fuzzers were used: random matrix expressions differentiated by `MatrixSymbol`s of shapes 2x2, 2x3, 3x1 and 1x1 and compared stage by stage (`array_derive(convert_matrix_to_array(e), X)`, `e.diff(X)`, `Derivative(e, X).doit()`) against `derive_by_array` of the explicit matrices (~620 expressions); random array expressions through `convert_array_to_matrix` (~4100) and through the canonicalising constructors (~8800), compared by value with the explicit operations. The canonicalisation and the derivative rules themselves are value-preserving on that sample: every derivative that evaluated and converted was numerically correct except for the first three items below. The rest are routing bugs, rules that raise instead of returning `None`, and converter crashes.*

Scope: `sympy/tensor/array/expressions/arrayexpr_derivatives.py` (`array_derive`), `sympy/tensor/array/array_derivatives.py` (`ArrayDerivative`), `sympy/matrices/expressions/matexpr.py` (`_matrix_derivative`), `from_matrix_to_array.py`, `from_array_to_matrix.py`, `array_expressions.py`. Convention checked: `result[k, l, i, j] = d expr[i, j] / d X[k, l]`, size-1 axes dropped at the end. Snippets assume `from sympy import *`, `X, A, B, C, Y` are 2x2 `MatrixSymbol`s unless stated, `v, w` 3x1, `x, s, k, i, j` symbols.

## 0. Root causes

1. **`_ArrayExpr` carries scalar flags**: `is_scalar` is `True` (inherited from `Expr`), `is_commutative` is `None` even for rank-0 arrays, `is_Atom` is `True`, there is no `_eval_derivative` and no `__add__`/`__mul__` overload. Consequences: repeated and mixed derivatives are mis-routed (item 5), `Pow` refuses to differentiate scalars built from traces (6), `ArraySum.doit()` and plain `Add`/`Mul` of arrays become shapeless objects (11), `expand`/`cse` do not descend (33).
2. **`identify_hadamard_products` mixes two index numberings and runs on unconverted arguments**: `check_transpose` maps diagonal indices with `-1-i` and compares them with contraction indices, so a Hadamard product followed by a matrix product is transposed wrongly (1); the pass also receives `ArrayAdd`/`ArrayElementwiseApplyFunc` arguments as if they were matrices (9, 18).
3. **`_get_function_fdiff` keeps only the function class** (`fdiff = type(fdiff)`), so `Lambda(d, exp(d + 1))` differentiates to `exp` (2); the elementwise rules also treat the `Lambda` body and the Hadamard/power exponent as constants (3).
4. **Rules raise instead of returning `None`** (`HadamardProduct` is registered to raise although the `MatrixExpr` fallback converts it; `Expr`, `Function`, `MatPow` raise `NotImplementedError`) and `_matrix_derivative` does not catch, so `.diff()` crashes where an unevaluated `Derivative` is expected (15, 16, 17).
5. **Size-1 axes**: `_remove_trivial_dims`, `_array_diag2contr_diagmatrix` and `_find_trivial_kronecker_products_broadcast` assume matrix neighbours and non-empty groups (12, 19, 20, 21), and the squeeze convention is applied inconsistently (29).
6. **The `Determinant` rule calls `arg.inv()` eagerly** (8); **the `MatPow` rule applies the integer summation formula to any exponent** (4, 17).
7. **`ArrayContraction`/`ArrayDiagonal` accept negative and repeated axes** (13).

## 1. Wrong results

1. **Hadamard product followed by a matrix product is transposed in `convert_array_to_matrix`** (`from_array_to_matrix.py:1001`, `identify_hadamard_products.check_transpose`): `convert_array_to_matrix(convert_matrix_to_array(HadamardProduct(C*D, G)*E))` -> `HadamardProduct(C*D, G.T)*E`; `Trace(HadamardProduct(A*X, B*X)*C).diff(X)` -> `A.T*HadamardProduct(B*X, C) + B.T*HadamardProduct(A*X, C)` where the correct value has `C.T` (nonzero difference against `derive_by_array`); with non-square factors the same path raises `ShapeError`. Present in 1.14.0.
2. **`_get_function_fdiff` drops the argument of the derivative** (`matrices/expressions/applyfunc.py:117`, `array_expressions.py:1190`): `X.applyfunc(lambda z: exp(z + 1)).diff(X).as_explicit()[0,0,0,0]` -> `exp(X[0, 0])` (expected `exp(X[0, 0] + 1)`); `(s*X).applyfunc(lambda z: sin(z + 1)).diff(s)` -> `HadamardProduct(cos.(s*X), X)`. Any `Lambda` whose derivative is a single applied function with a non-identity argument (`sin(d+1)`, `exp(d+c)`) is wrong; `sin(2*d)` is safe only because the derivative is a `Mul`. (E3-5 in #30900 is the `applyfunc.py` copy.)
3. **Elementwise rules ignore the dependence of the function or exponent on `X`** (`arrayexpr_derivatives.py:208-235`, `from_matrix_to_array.py:85-104`): `HadamardPower(X, Trace(X)).diff(X)`, `MatPow(a.T*X*b, Trace(X)).diff(X)` and `X.applyfunc(lambda z: z**2*X[0, 0]).diff(X)` all miss the chain-rule term (`log` term, resp. `X∘X * E_00`); numeric differences verified.
4. **`MatPow` rule with a non-integer exponent** (`arrayexpr_derivatives.py:244`): `MatPow(X, S.Half).diff(X)` -> `Sum(..., (_d, 0, -1/2))`; `.doit()` -> `RecursionError`; `.as_explicit()` -> `ValueError`. Symbolic integer exponents are fine.
5. **Repeated and mixed derivatives are mis-routed** (`array_derivatives.py:95`, `core/function.py:1494`): `(X*A).diff(X, 2)` -> `ZeroMatrix(2, 2)` (rank 6 expected); `X.diff(s, X)` -> `ZeroMatrix(2, 2)`; `X.diff(X, s)` -> `Derivative(0, X)`; `(X*A).diff(X).diff(A)` unevaluated while `(X*A).diff(X, A)` evaluates; `(x*X*A).diff(X).diff(x)` unevaluated; `ZeroMatrix(2, 2).diff(X, 2)` unevaluated. Cause: the rank-4 intermediate has `is_scalar == True`, and `Derivative.__new__` returns unevaluated when the expression has no `_eval_derivative` attribute.
6. **Scalars built from traces with a plain constant term do not differentiate** (`core/power.py:1210` refusing the non-commutative base, `from_matrix_to_array.py:53-74`): `((3 - Trace(A))**2
