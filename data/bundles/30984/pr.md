# Pull request #30984: fix(matrices): use ceiling instead of floor in MatrixSlice.shape

- Author: @ish1416
- Merged: 2026-11-08T04:08:15Z into `master`
- Labels: (none)
- Size: +32 / -7 in 4 files (full diff in `diff.patch`)

## Description

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

## Commits

- 4c3b62d5c7 (Ishita Singh): fix(matrices): use ceiling instead of floor in MatrixSlice.shape
- fc509ea93c (Ishita Singh): tests: update expected slice shape in codegen julia and octave tests
- 5f58526f7a (Christopher Smith): Apply suggestion from @smichr

## Conversation

### @smichr commented

Maybe a test where start is not 0 would be good

X = MatrixSymbol('X', 7, 7)
assert X[1:6:2, :].shape == (3, 7)
assert X[2:7:3, :].shape == (2, 7)

### @ish1416 commented

Added in commit cd1be54! Tested both non-zero start cases:
- `X[1:6:2, :].shape == (3, 7)`
- `X[2:7:3, :].shape == (2, 7)`

along with explicit `Matrix` comparisons for exact element verification. Thank you for the suggestion @smichr!


## Reviews

### @smichr reviewed: COMMENTED



### @smichr commented on `sympy/matrices/expressions/tests/test_slice.py`

```suggestion
    assert X7[::3, ::3].subs(X7, M7).as_explicit() == M7[::3, ::3]
    assert X7[1:6:2, :].shape == (3, 7)
    assert X7[2:7:3, :].shape == (2, 7)

```
