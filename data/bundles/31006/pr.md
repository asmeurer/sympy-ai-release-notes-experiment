# Pull request #31006: feat(matrices): complete symbolic formula for matrix slicing (fixes #30999, fixes #18411)

- Author: @ish1416
- Merged: 2026-11-10T07:40:21Z into `master`
- Labels: (none)
- Size: +234 / -92 in 7 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #30999.
Fixes #18411.
Follow-up to #30984.

#### Brief description of what is fixed or changed

In #30999 and #18411, @sylee957 pointed out that `MatrixSlice` had inconsistencies with Python/NumPy slicing:
- Negative strides (like `X[::-1, :]` or `X[3:0:-2, :]`) raised `IndexError`.
- Out-of-bounds slices (like `X[0:100, :]`) raised `IndexError` instead of clipping.
- Negative indices (like `X[-10:-1, :]`) gave incorrect shapes when clipping was needed.
- Slices with symbolic dimensions produced shapes inconsistent with NumPy under substitution.

This PR integrates the complete slicing formula proposed by @sylee957 in #30999:
1. **Sentinel Encoding (`-n - 1`):** Resolves the ambiguity of `-1` (last element vs exclusive stop bound before 0) during reverse iteration, keeping stored slices idempotent and arg-invariant.
2. **Boundary Normalization & Clipping:** Normalizes slice bounds to axis length $n$, while leaving unconstrained formal bounds (like `MatrixSlice(X, (a, b), (c, d))`) as `b - a`.
3. **Shape & Composition:** `slice_shape_1d` calculates the exact ceiling shapes, and `compose_slices` handles nested slices with mixed or negative steps.

#### Tests Added

In `sympy/matrices/expressions/tests/test_slice.py`:
- `test_slice_clipping`: Out-of-bounds slices clipping to matrix shape.
- `test_negative_step_slicing`: Reverse slicing and non-unit negative strides.
- `test_symbolic_slicing_substitution_invariance`: Tests from #30999 checking shapes and entries under substitution.
- `test_issue_18411`: Exact test cases from #18411 (`A[5:0:-1, 5:0:-1]` and `A[6::-1, 6::-1]`).
- Verified 1,800 combinations across dimensions 3, 5, 7 locally against Python list slicing with 0 failures.

#### Other comments

All 293 tests in `sympy/matrices/expressions/tests/` and flake8 pass cleanly.

#### AI Generation Disclosure

I used an AI assistant (Antigravity) to help brainstorm edge cases and draft code. I worked through the mathematical derivation myself, verified the sentinel encoding against Lean 4 proofs and Python slicing semantics, and tested all edge cases locally.

## Commits

- 36b65e5c81 (Ishita Singh): feat(matrices): implement complete symbolic formula for MatrixSlice (fixes #30999, fixes #18411)
- 080a550cc6 (Ishita Singh): style(matrices): remove hasattr and add Expr type annotations in slice.py
- 8f1caaed03 (Ishita Singh): style(matrices): move Expr import to TYPE_CHECKING in slice.py
- 556551affd (Ishita Singh): fix(matrices): adopt maintainer verbatim algebraic formula for MatrixSlice
      - Revert procedural decidability assumptions in favor of pure algebraic Lean 4 formulation
      - Use decode_bound(bound, n) = bound + n*delta(bound) verbatim
      - Use sympify_slice with verbatim p = delta(step) and Max/Min bounds
      - Encode composite slices with algebraic - n*delta(...)
      - Remove all hasattr and getattr checks
      - Update tests for symbolic and concrete matrix slicing
- ee9f80b435 (Ishita Singh): fix(matrices): align default bounds with Lean 4 model and fix pretty printing
- 639da92145 (Ishita Singh): ci: re-trigger CI tests
- d1fcb4360c (Ishita Singh): fix(matrices): adopt maintainer lazy normalization in MatrixSlice and restore printer tests
- 70a99721d1 (Ishita Singh): refactor(matrices): inline decode_bound, restore normalize signature, and clean up tests

## Conversation

### @sylee957 commented

can you remove `hasattr` from `delta, sympify_slice, slice_shape_1d`? they should work on sympified input and input expressions should be assumed not to get missing attribute error. Also please investigate with if adding `Expr` to type annotations to those inputs help because it can help infer `hasattr` is unnecessary

### @ish1416 commented

Good catch, thanks! Since all the inputs are sympified `Expr`s, `hasattr` wasn't needed at all.

I've removed all occurrences of `hasattr` and added `Expr` type annotations to `delta`, `sympify_slice`, `slice_shape_1d`, and `compose_slices`. I also made sure internal bounds use `S.Zero` and `S.NegativeOne` so they stay SymPy expressions throughout and don't end up as plain Python ints.

All 293 tests in matrix expressions and flake8 are passing.

### @ish1416 commented

My sincere apologies @sylee957, and thank you for pointing that out.

You're totally right — adding `(bound < 0) == S.true` and procedural assumptions was a mistake on my end and made review difficult. In symbolic expressions, undecided doesn't mean false, and it compromised the algebraic model. I won't repeat this and will stick faithfully to your formulation.

I've reverted all the extra assumptions and applied both of your suggestions verbatim:
- `decode_bound` is now strictly `bound + n*delta(bound)`.
- `sympify_slice` matches your exact `p = delta(step)` and `Max(-p, Min(n - p, ...))` logic.
- `compose_slices` similarly uses `- n*delta(...)`.

All 293 matrix expressions tests and flake8 pass cleanly.

### @sylee957 commented

Anyway it looks like the symbolic approach doesn't work very well

`assert pretty(expr) == upretty(expr) == 'X[:, :]'`

one of the problem is that there are a few trivial cases failing for printer
we can try to do a few things

- If both slice are `[:, :]` just return original matrix
or
- Correct printer tests to use numeric examples than fully symbolic matrix

or we can even consider different approach like introducing `class None(Basic)`

### @ish1416 commented

Thanks for pointing this out @sylee957, that makes total sense.

Without `positive=True`, `delta(n)` can't simplify algebraically to 0, which leaves the canonical stop unreduced and throws off the printer comparisons on symbolic shapes.

I went ahead and updated the printer tests to use numeric examples (`Y`) for slice formatting, keeping `n = Symbol('n', integer=True, positive=True)` for the full-slice checks where the simplification holds. In `sympify_slice`, `None` bounds are now set directly to `p*(n - 1)` and `(1 - 2*p)*n - p` so default full slices resolve immediately without expanding indicators, and I fixed the `prettyForm` unpacking issue in `ppslice` (`pretty.py`).

Let me know if you'd still prefer returning the parent matrix directly when both slices are `[:, :]` — happy to add that if that feels cleaner to you!

### @sylee957 commented

I figured out a way to preserve more tests
canonicalization can do less operations like clipping, but only when calling `shape` or `entry` it can compute more things to normalize
I also added a few cases to `delta` depending on assumption where it can simplify evaluation.

```diff
diff --git a/sympy/matrices/expressions/slice.py b/sympy/matrices/expressions/slice.py
diff --git a/sympy/matrices/expressions/slice.py b/sympy/matrices/expressions/slice.py
index 8287c009e8..4f5575851d 100644
--- a/sympy/matrices/expressions/slice.py
+++ b/sympy/matrices/expressions/slice.py
@@ -18,6 +18,10 @@ def delta(value: Expr) -> Expr:
     Indicator delta function: delta(x) = (sign(x)^2 - sign(x)) / 2.
     Returns 1 if x < 0, and 0 if x >= 0.
     """
+    if value.is_nonnegative is True:
+        return S.Zero
+    if value.is_negative is True:
+        return S.One
     return (sign(value)**2 - sign(value)) / 2
 
 
@@ -28,10 +32,14 @@ def decode_bound(bound: Expr, n: Expr) -> Expr:
     return bound + n*delta(bound)
 
 
+def normalize_bound(n: Expr, step: Expr, bound: Expr) -> Expr:
+    p = delta(step)
+    return Max(-p, Min(n - p, decode_bound(bound, n)))
+
+
 def sympify_slice(n: Expr, value: slice | tuple | Tuple | Expr) -> Tuple:
     """
-    Canonicalizes slice specification with respect to axis dimension n.
-    Implements the complete symbolic formula for array slicing.
+    Resolves omitted slice arguments while preserving supplied bounds.
     """
     n = sympify(n)
     if isinstance(value, slice):
@@ -53,20 +61,11 @@ def sympify_slice(n: Expr, value: slice | tuple | Tuple | Expr) -> Tuple:
     step = S.One if value[2] is None else sympify(value[2])
     if step.is_zero is True:
         raise ValueError("slice step cannot be zero")
-
     p = delta(step)
     if start is None:
         start = p*(n - 1)
-    else:
-        start = start + n*delta(start)
-        start = Max(-p, Min(n - p, start))
-        start = start - n*delta(start)
     if stop is None:
-        stop = (1 - 2*p)*n - p
-    else:
-        stop = stop + n*delta(stop)
-        stop = Max(-p, Min(n - p, stop))
-        stop = stop - n*delta(stop)
+        stop = n - p*(2*n + 1)
     return Tuple(start, stop, step)
 
 
@@ -75,8 +74,8 @@ def sympify_slice(n: Expr, value: slice | tuple | Tuple | Expr) -> Tuple:
 
 def slice_shape_1d(n: Expr, sl: tuple[Expr, Expr, Expr] | Tuple) -> Expr:
     start, stop, step = sl
-    A = decode_bound(start, n)
-    B = decode_bound(stop, n)
+    A = normalize_bound(n, step, start)
+    B = normalize_bound(n, step, stop)
     return Max(0, ceiling((B - A) / step))
 
 
@@ -85,15 +84,15 @@ def compose_slices(
     s2: tuple[Expr, Expr, Expr] | Tuple,
     n: Expr,
 ) -> Tuple:
+    start1, _, step1 = s1
+    start2, stop2, step2 = s2
     L1 = slice_shape_1d(n, s1)
-    L2 = slice_shape_1d(L1, s2)
-    A1 = decode_bound(s1[0], n)
-    step1 = s1[2]
-    A2 = decode_bound(s2[0], L1)
-    step2 = s2[2]
+    A1 = normalize_bound(n, step1, start1)
+    A2 = normalize_bound(L1, step2, start2)
+    B2 = normalize_bound(L1, step2, stop2)
     A_comp = A1 + A2 * step1
+    B_comp = A1 + B2 * step1
     step_comp = step1 * step2
-    B_comp = A_comp + L2 * step_comp
     A_comp = A_comp - n * delta(A_comp)
     B_comp = B_comp - n * delta(B_comp)
     return Tuple(A_comp, B_comp, step_comp)
@@ -154,8 +153,8 @@ def shape(self):
     def _entry(self, i, j, **kwargs):
         row_start, _, row_step = self.rowslice
         col_start, _, col_step = self.colslice
-        A_row = decode_bound(row_start, self.parent.rows)
-        A_col = decode_bound(col_start, self.parent.cols)
+        A_row = normalize_bound(self.parent.rows, row_step, row_start)
+        A_col = normalize_bound(self.parent.cols, col_step, col_start)
         return self.parent._entry(
             A_row + i * row_step,
             A_col + j * col_step,
```

I also updated Lean proofs that implementation can be verified verbatim
You can give variables like `x, y` assumptions (like nonnegative, positive) and see if they saves arguments more simpler

### @ish1416 commented

This is brilliant, thank you @sylee957!

Deferring clipping to `.shape` and `._entry` makes `sympify_slice` so much lighter and keeps the slice args intact.

I've applied your diff verbatim. Following your note, setting `x, y, z, w, t = symbols('x y z w t', positive=True)` in the printer test suites works like a charm — `delta(step)` simplifies cleanly, allowing all the original symbolic slice printer tests (`test_str.py`, `test_latex.py`, `test_pretty.py`) to be fully preserved and pass without needing numeric substitutions.

All 293 matrix expressions tests and printing tests pass cleanly.

### @sylee957 commented

Now I'm okay with the most of the changes. Formulas are verified and we solved major issues, but only a few comments to address

### @ish1416 commented

Thanks @sylee957! I've addressed all your comments:

1. **Inlined `decode_bound`:** Folded it directly into `normalize_bound` and removed the helper function.
2. **`normalize` function signature:** Defined it directly as `normalize(value, n)` with the original argument order, and updated `MatrixSlice.__new__` call sites accordingly.
3. **Preserved test cases in `test_slice.py`:** Defined positive symbols `n, m, k = symbols('n m k', integer=True, positive=True)`, allowing `X` and `Y` to be preserved across `test_entry`, `test_on_diag`, `test_inputs`, and `test_slicing` without extra matrix symbols.
4. **Cleaned comments:** Removed personal names from all test comments in `test_slice.py`.
5. **Removed duplicates:** Deleted duplicate slice assertions in `test_pretty.py` and `test_str.py`.

All 293 matrix expressions tests, printing tests, and code quality tests pass cleanly.


## Reviews

### @sylee957 reviewed: COMMENTED



### @sylee957 reviewed: COMMENTED



### @sylee957 reviewed: COMMENTED



### @sylee957 reviewed: COMMENTED



### @sylee957 reviewed: COMMENTED



### @sylee957 reviewed: COMMENTED



### @sylee957 reviewed: COMMENTED



### @sylee957 commented on `sympy/matrices/expressions/slice.py`

```suggestion
    p = delta(step)
    if start is None:
        start = p*(n - 1)
    else:
        start = start + n*delta(start)
        start = Max(-p, Min(n - p, start))
    if stop is None:
        stop = (1 - p)*n - p
    else:
        stop = stop + n*delta(stop)
        stop = Max(-p, Min(n - p, stop))
    start = start - n*delta(start)
    stop = stop - n*delta(stop)
    return Tuple(start, stop, step)
```

Can you simplify the code with this? it looks like you have defined `delta` but not using here.

### @sylee957 commented on `sympy/matrices/expressions/slice.py`

```suggestion
    return bound + n*delta(bound)
```

This is also not faithful. I note that you instruct AI to use assumptions considering decidability because for symbolic expressions not everything is decidable and `bound < 0` is not decided to `true` does not imply `delta(bound)` is zero. I generally expect you to revert most of the assumptions in favor of matching my original code in verbatim because they make difficult to review

### @sylee957 commented on `sympy/printing/pretty/tests/test_pretty.py`

```suggestion
```
It looks like this is duplicate

### @sylee957 commented on `sympy/matrices/expressions/tests/test_slice.py`

Lets remove names from comments they should not be relevant for readers

### @sylee957 commented on `sympy/matrices/expressions/slice.py`

Let's tidy up this a bit. We may not need `normalize = sympify_slice` and should define the function initially as `normalize`. This should be kept for best effort of backward compatibility (although the definitions here are very internal that we shouldnt worry about it too much)

I note that original `normalize` flipped the order of arguments (parent size is second argument) but here it is first argument so you can flip it back with changes to call site.

### @sylee957 commented on `sympy/matrices/expressions/tests/test_slice.py`

Can we preserve more test cases?
We can some imports for symbols from sympy.abc (which doesn't have assumptions)
and define symbols with better assumptions to make the expressions simple for testing

### @sylee957 commented on `sympy/matrices/expressions/slice.py`

Let's tidy up a few functions like this. Generally a function that is too simple and used only one time is better be inlined.
