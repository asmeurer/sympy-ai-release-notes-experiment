# Pull request #31016: 🤖 Fix wrong solveset results for modular powers with a non-coprime base

- Author: @adityaanikam
- Merged: 2026-11-11T08:01:14Z into `master`
- Labels: solvers.solveset
- Size: +19 / -4 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs
Fixes #30996

#### Brief description of what is fixed or changed
`solveset` gave wrong answers for `Mod(b**x, m) = r` when `b` shares a factor with `m`, for example `Mod(2**x, 42)`. `_invert_modular` assumed the powers of `b` are periodic from the start, which is false in that case. Following the review, it now returns the expression unevaluated unless the modulus, rhs and base are integers and the base and rhs are coprime to the modulus. It also returns early when the term is not a `Mod`, which covers `Mod(2*2**x - 1, 42)` (it raised `TypeError`).

#### Other comments
`Mod(12**x, 21) - 18` is now unevaluated, so I changed that existing test to expect a `ConditionSet`. The issue's cases are added to `test_solve_modular`.

#### AI Generation Disclosure
I used Claude Code (Claude Sonnet 5.5) to help find the cause and to write the change and tests. I reviewed it and ran the tests myself.

## Commits

- 44fd6a6f73 (adityaanikam): Fix modular solveset for powers whose base shares a factor with the modulus
      Fixes #30996
      Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
- 51112d016c (adityaanikam): Limit the modular power solver to integer bases and integer exponents
      Add .mailmap entry
      Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
- 776c03d687 (adityaanikam): Leave modular powers with a non-coprime base unevaluated
      Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
- 3d2b407bda (Christopher Smith): update doctest for restricted solving

## Conversation

### @smichr commented

The .mailmap file needs to be updated because there are commits with
unrecognised author/email metadata.

        For instructions on updating the .mailmap file see:
https://docs.sympy.org/dev/contributing/new-contributors-guide/workflow-process.html#mailmap-instructions

### @smichr commented

Consider the following as identified by ChatGPT:

```python
x = symbols('x')

expr = Mod(4**(x/2), 12) - 2
assert expr.subs(x, 1) == 0

solveset(expr, x, S.Integers)
# PR: EmptySet

expr = Mod((S.Half)**x, 4) - 2
assert expr.subs(x, -1) == 0

solveset(expr, x, S.Integers)
# PR: EmptySet

expr = Mod(4**(x/2), 8)
assert expr.subs(x, 3) == 0

solveset(expr, x, S.Integers)
# PR: Intersection(ImageSet(Lambda(n, 2*n + 4),
#                           S.Naturals0), S.Integers)
```

Restrict the new number-theoretic logic to cases where:
- The base is an integer.
- The exponent is guaranteed to be an integer for integer values of the solving symbol.
Cases outside those conditions should retain the existing fallback behavior until they can be handled correctly.

### @adityaanikam commented

Thanks both. Following oscarbenjamin's suggestion I replaced the change with the smaller one: _invert_modular now leaves the expression unevaluated unless the base and rhs are coprime to the modulus, so the cases from the issue and from smichr's comment fall back to the ConditionSet instead of giving wrong sets. I also fixed the .mailmap entry. Mod(12**x, 21) - 18 is now unevaluated too, so I changed that existing test to expect it.

### @henryksobon300-code commented

I opened #31048 to follow up on one of the cases that returns a `ConditionSet`. In that example, the only integer solution is `x = -1`.


## Reviews

### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin commented on `sympy/solvers/solveset.py`

I think it is a mistake to overcomplicate things by trying to make solveset's ill-conceived handling of Mod more complete.

A more minimal fix is better:
```diff
diff --git a/sympy/solvers/solveset.py b/sympy/solvers/solveset.py
index ff0395aaad..6108066894 100644
--- a/sympy/solvers/solveset.py
+++ b/sympy/solvers/solveset.py
@@ -1538,6 +1538,8 @@ def _invert_modular(modterm, rhs, n, symbol):
     (x**2 + x + 1, ImageSet(Lambda(_n, 3*_n + 1), Naturals0))
 
     """
+    if not isinstance(modterm, Mod):
+        return modterm, rhs
     a, m = modterm.args
 
     if rhs.is_integer is False:
@@ -1575,7 +1577,9 @@ def _invert_modular(modterm, rhs, n, symbol):
         if expo.has(symbol) and not base.has(symbol):
             # remainder -> solution independent of n of equation.
             # m, rhs are made coprime by dividing number_gcd(m, rhs)
-            if not m.is_Integer and rhs.is_Integer and a.base.is_Integer:
+            if not (m.is_Integer and rhs.is_Integer and base.is_Integer):
+                return modterm, rhs
+            if number_gcd(m.p, base.p) != 1 or number_gcd(m.p, rhs.p) != 1:
                 return modterm, rhs
 
             mdiv = m.p // number_gcd(m.p, rhs.p)
```
