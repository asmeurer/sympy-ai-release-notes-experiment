# Issues and pull requests referenced by this pull request

## Issue #18411: Matrix slicing inconsistency with python

- Opened by @sylee957, state: closed

```python3
>>> from sympy import *

>>> A = MatrixSymbol('A', 4, 4)
>>> A[5:0:-1, 5:0:-1].as_explicit()
Matrix([
[A[5, 5], A[5, 4], A[5, 3], A[5, 2], A[5, 1]],
[A[4, 5], A[4, 4], A[4, 3], A[4, 2], A[4, 1]],
[A[3, 5], A[3, 4], A[3, 3], A[3, 2], A[3, 1]],
[A[2, 5], A[2, 4], A[2, 3], A[2, 2], A[2, 1]],
[A[1, 5], A[1, 4], A[1, 3], A[1, 2], A[1, 1]]])

>>> A.as_explicit()[5:0:-1, 5:0:-1]
Matrix([
[A[3, 3], A[3, 2], A[3, 1]],
[A[2, 3], A[2, 2], A[2, 1]],
[A[1, 3], A[1, 2], A[1, 1]]])

>>> A = list(range(5))
>>> A[5:0:-1]
[4, 3, 2, 1]

>>> A = Array([0, 1, 2, 3, 4])
>>> A[5:0:-1]
[4, 3, 2, 1]
```

I've made this discovery while working on #18298
And it looks like there are some flaws to the designs of matrix slicing for negative step.

~I wonder if this can be treated as a bug fix, or a backward incompatible suggestion like #15464 
But it looks like nobody had tested out slicing with negative step.~

## Issue #30999: Complete symbolic formula for matrix and array slicing

- Opened by @sylee957, state: closed

```python3
def sympify_slice(n, value):
    n = sp.sympify(n)
    if isinstance(value, slice):
        value = (value.start, value.stop, value.step)
    if len(value) == 2:
        value = (*value, None)
    if len(value) != 3:
        raise TypeError("a slice tuple needs start, stop, and step")
    start = None if value[0] is None else sp.sympify(value[0])
    stop = None if value[1] is None else sp.sympify(value[1])
    step = sp.S.One if value[2] is None else sp.sympify(value[2])
    if step.is_zero is True:
        raise ValueError("slice step cannot be zero")

    def delta(value):
        return (sp.sign(value)**2 - sp.sign(value)) / 2

    p = delta(step)
    if start is None:
        start = p*(n - 1)
    else:
        start = start + n*delta(start)
        start = sp.Max(-p, sp.Min(n - p, start))
    if stop is None:
        stop = (1 - p)*n - p
    else:
        stop = stop + n*delta(stop)
        stop = sp.Max(-p, sp.Min(n - p, stop))
    start = start - n*delta(start)
    stop = stop - n*delta(stop)
    return sp.Tuple(start, stop, step)

class MatrixSlice(MatrixExpr):
    def __new__(cls, parent, rowslice, colslice):
        parent = sp.sympify(parent)
        if not isinstance(parent, MatrixExpr):
            raise TypeError("parent must be a matrix")
        rowslice = sympify_slice(parent.rows, rowslice)
        colslice = sympify_slice(parent.cols, colslice)
        return sp.Basic.__new__(cls, parent, rowslice, colslice)

    parent = property(lambda self: self.args[0])
    rowslice = property(lambda self: self.args[1])
    colslice = property(lambda self: self.args[2])

    @property
    def shape(self):
        row_start, row_stop, row_step = self.rowslice
        col_start, col_stop, col_step = self.colslice
        row_start = row_start + self.parent.rows*(sp.sign(row_start)**2 - sp.sign(row_start))/2
        row_stop = row_stop + self.parent.rows*(sp.sign(row_stop)**2 - sp.sign(row_stop))/2
        col_start = col_start + self.parent.cols*(sp.sign(col_start)**2 - sp.sign(col_start))/2
        col_stop = col_stop + self.parent.cols*(sp.sign(col_stop)**2 - sp.sign(col_stop))/2
        rows = sp.Max(0, sp.ceiling((row_stop - row_start)/row_step))
        cols = sp.Max(0, sp.ceiling((col_stop - col_start)/col_step))
        return rows, cols

    def _entry(self, i, j, **kwargs):
        row_start, _, row_step = self.rowslice
        col_start, _, col_step = self.colslice
        row_start = row_start + self.parent.rows*(sp.sign(row_start)**2 - sp.sign(row_start))/2
        col_start = col_start + self.parent.cols*(sp.sign(col_start)**2 - sp.sign(col_start))/2
        return self.parent._entry(
            row_start + i*row_step,
            col_start + j*col_step,
            **kwargs,
        )
```

While reviewing the PR https://github.com/sympy/sympy/pull/30984 I've been working on if there is possibility to model complete formula for matrix/array slicing and I arrived this.
Although https://github.com/sympy/sympy/pull/30984 was merged before I review, it fixed the issue only partially
I think that there are still plenty of issues with matrix slicing like:

- Slicing for negative index `M[-10:-1:]`
- Slicing beyond the bound of matrix `M[0:100]`

that gives plenty of issues with inconsistency/errors between sympy and numpy, or python array slicing semantics

```python
def _f():
    return sp.MatrixSlice(sp.MatrixSymbol("X", n, 4), slice(-6, None), slice(None)).subs(n, 5)

def _g():
    return MatrixSlice(sp.MatrixSymbol("X", n, 4), slice(-6, None), slice(None)).subs(n, 5)

def _h():
    return np.empty((5, 4))[-6:, :]

print("sp.MatrixSlice shape:", _f().shape)
print("custom MatrixSlice shape:", _g().shape)
print("NumPy shape:", _h().shape)
print("sp.MatrixSlice entries:", _f().as_explicit())
print("custom MatrixSlice entries:", _g().as_explicit())
# sp.MatrixSlice shape: (1, 4)
# custom MatrixSlice shape: (5, 4)
# NumPy shape: (5, 4)
```
```python
def _f():
    return sp.MatrixSlice(A, slice(a, None, 2), slice(None))

def _g():
    return MatrixSlice(A, slice(a, None, 2), slice(None))

def _h():
    return np.empty((5, 4))[-4::2, :]

print("sp.MatrixSlice shape then subs:", sp.Tuple(*_f().shape).subs(a, -4))
print("custom MatrixSlice shape then subs:", sp.Tuple(*_g().shape).subs(a, -4))
print("sp.MatrixSlice subs then shape:", _f().subs(a, -4).shape)
print("custom MatrixSlice subs then shape:", _g().subs(a, -4).shape)
print("NumPy shape:", _h().shape)
# sp.MatrixSlice shape then subs: (5, 4)
# custom MatrixSlice shape then subs: (2, 4)
# sp.MatrixSlice subs then shape: (2, 4)
# custom MatrixSlice subs then shape: (2, 4)
# NumPy shape: (2, 4)
```

```python
def _f():
    return sp.MatrixSlice(A, slice(None, None, s), slice(None)).subs(s, -1)

def _g():
    return MatrixSlice(A, slice(None, None, s), slice(None)).subs(s, -1)

def _h():
    return np.empty((5, 4))[::-1, :]

try:
    print("sp.MatrixSlice shape:", _f().shape)
    print("sp.MatrixSlice entries:", _f().as_explicit())
except IndexError as _error:
    print("sp.MatrixSlice:", repr(_error))
print("custom MatrixSlice shape:", _g().shape)
print("NumPy shape:", _h().shape)
print("custom MatrixSlice entries:", _g().as_explicit())
# sp.MatrixSlice: IndexError()
# custom MatrixSlice shape: (5, 4)
# NumPy shape: (5, 4)
```

Although `MatrixSlice` originally seems like designed to reject like negative/out of bound slicing to avoid such complication with IndexError
it does not with symbolic expressions
for example, `MatrixSlice(A, (m, n), (1, 2))`
and there are plenty of issues such errors are raises spuriously after substitution/xreplace.

ChatGPT had found a formula for which is verified with Lean4 in my repository
https://github.com/sylee957/sympy-proofs/blob/5e2c7286bcfe6d282349f333fb175660f596eeff/SympyProofs/PythonSlice/Canonical.lean#L143-L177

Although it is complicated if you pass symbols with right assumption (like positive) or pass some numeric arguments the formula can simplify itself a bit by evaluatio

## Pull request #30984: fix(matrices): use ceiling instead of floor in MatrixSlice.shape

- Opened by @ish1416, state: closed, merged 2026-11-08

#### References to other Issues or PRs

Fixes item E1-3 from #30900.

#### Brief description of what is fixed or changed

`MatrixSlice.shape` was using `floor` when calculating dimensions for slices with step > 1:
```python
rows = rows if self.rowslice[2] == 1 else floor(rows/self.rowslice[2])
```

For a slice with step `s`, the number of elements is `ceiling(length / s)`. Using `floor` caused the last row or column to be dropped whenever the length was not evenly divisible by the step:
- For a 5x5 matrix with step 2 (indices 0, 2, 4), the shape was computed as `(2, 2)` instead of `(3, 3)`.
- Calling `.as_explicit()` silently dropped the 4th row and column.

This PR changes `floor` to `ceiling` in `MatrixSlice.shape` and adds regression tests verifying concrete odd and even matrix slices against standard `Matrix` slicing.

#### Other comments

All tests in `sympy/matrices/expressions/tests/` pass locally.

#### AI Generation Disclosure

Prepared and verified with an AI coding assistant (Antigravity). Tested against SymPy's explicit matrix evaluation and local test suite.
