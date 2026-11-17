# Pull request #30952: Fix reshape validation for empty templates

- Author: @raman118
- Merged: 2026-11-05T19:29:15Z into `master`
- Labels: (none)
- Size: +50 / -19 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #30951

#### Brief description of what is fixed or changed

`reshape` now validates counts before division: negative counts and nonpositive total sizes raise `ValueError`. Nested zero-size groups are supported when the overall template has positive size; for example, `reshape([1, 2, 3, 4], ([0], 4))` returns `[([], 1, 2, 3, 4)]`.

The recursive grouping follows smichr's suggestion, passing and returning the sequence position explicitly instead of using `nonlocal`.

#### Other comments

The new regressions failed before the revision. All 49 iterable tests, repository quality checks, `ruff check sympy`, and `python bin/mailmap_check.py` passed. The commit author's email and aliases are included in `.mailmap`.

#### AI Generation Disclosure

OpenAI Codex (GPT-6.1 Sol) generated the original changes in `sympy/utilities/iterables.py` and `sympy/utilities/tests/test_iterables.py`. OpenAI Codex (GPT-6 Astra) generated the follow-up changes in those files based on smichr's suggestion, added the user-provided identity to `.mailmap`, and wrote this description at the account owner's request.

## Commits

- 930c1e6ce6 (raman118): utilities: validate reshape template size before division
      AI-assisted implementation and tests by OpenAI Codex using GPT-6.1 Sol; reviewed by GPT-6 Astra.
      Co-authored-by: OpenAI Codex <noreply@openai.com>
- 35dd836420 (Doremon): Add Doremon to .mailmap
      Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
- 2d7204a145 (raman118): author: map Doremon commit identity to raman118
      AI-assisted change by OpenAI Codex (GPT-6 Astra).
- 8c54de2c13 (raman118): Handle nested zero counts and reject negative reshape counts
      Adapt the recursive grouping approach suggested by smichr. Pass and return the sequence position explicitly to avoid nonlocal state, and validate the complete template once.
      AI-generated changes by OpenAI Codex (GPT-6 Astra).

## Conversation

### @smichr commented

Thanks for looking into this. What about

```diff
diff --git a/sympy/utilities/iterables.py b/sympy/utilities/iterables.py
index 45a2e86012..955d60afab 100644
--- a/sympy/utilities/iterables.py
+++ b/sympy/utilities/iterables.py
@@ -178,27 +178,26 @@ def reshape(seq, how):
     [[0, 1, [2, 3, 4], {5, 6}, (7, (8, 9, 10), 11)]]
 
     """
-    m = sum(flatten(how))
-    n, rem = divmod(len(seq), m)
-    if m < 0 or rem:
-        raise ValueError('template must sum to positive number '
-        'that divides the length of the sequence')
+    sizes = flatten(how)
+    m = sum(sizes)
+    if any(s < 0 for s in sizes) or m <= 0 or len(seq) % m:
+        raise ValueError('template must contain nonnegative counts '
+                         'with a positive sum that divides the sequence length')
+
     i = 0
-    container = type(how)
-    rv = [None]*n
-    for k in range(len(rv)):
-        _rv = []
-        for hi in how:
-            if isinstance(hi, int):
-                _rv.extend(seq[i: i + hi])
-                i += hi
+
+    def make_group(template):
+        nonlocal i
+        result = []
+        for item in template:
+            if isinstance(item, int):
+                result.extend(seq[i:i + item])
+                i += item
             else:
-                n = sum(flatten(hi))
-                hi_type = type(hi)
-                _rv.append(hi_type(reshape(seq[i: i + n], hi)[0]))
-                i += n
-        rv[k] = container(_rv)
-    return type(seq)(rv)
+                result.append(make_group(item))
+        return type(template)(result)
+
+    return type(seq)([make_group(how) for _ in range(len(seq) // m)])
 
 
 @overload
diff --git a/sympy/utilities/tests/test_iterables.py b/sympy/utilities/tests/test_iterables.py
index a9e42444f6..cb50706430 100644
--- a/sympy/utilities/tests/test_iterables.py
+++ b/sympy/utilities/tests/test_iterables.py
@@ -709,6 +709,19 @@ def test_reshape():
     raises(ValueError, lambda: reshape([0, 1], [-1]))
     raises(ValueError, lambda: reshape([0, 1], [3]))
 
+    seq = [1, 2, 3, 4]
+
+    assert reshape(seq, (0, 4)) == [(1, 2, 3, 4)]
+    assert reshape(seq, ([0], 4)) == [([], 1, 2, 3, 4)]
+    assert reshape(seq, ((0,), 4)) == [((), 1, 2, 3, 4)]
+    assert reshape(seq, ([0], (0,), 4)) == [
+        ([], (), 1, 2, 3, 4)]
+
+    assert reshape(seq, (2, [2])) == [(1, 2, [3, 4])]
+
+    for how in [(-1, 5), (2, -1, 3), (0, -1, 5)]:
+        raises(ValueError, lambda: reshape(seq, how))
+
 
 def test_uniq():
     assert list(uniq(p for p in partitions(4))) == \
```

### @Haeherfeder commented

i personally don't like the nonlocal, but will look at it when at home

### @raman118 commented

@Haeherfeder sure

### @smichr commented

Thanks, this is in.


## Reviews

(no reviews)
