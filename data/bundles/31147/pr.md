# Pull request #31147: assumptions: handle non-Float evalf results when inspecting precision

- Author: @pranjal9091
- Merged: 2026-11-17T18:25:43Z into `master`
- Labels: (none)
- Size: +42 / -40 in 4 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes item C6 of #31017

#### Brief description of what is fixed or changed

In assumption handlers (`_RealPredicate_number`, `_Imaginary_number`, `_PositivePredicate_number`, `_NegativePredicate_number`, and `NonZeroPredicate`), `evalf(2)` is called and its result checked with `._prec != 1`.

When testing expressions whose components cannot be purely split into real and imaginary parts symbolically (such as radical roots of quartic polynomials with complex Ferrari resolvents), `evalf(2)` on the symbolic component yields an `Add` (e.g. `Float + Float*I`). Because `Add` does not have a `_prec` attribute, accessing `._prec` directly raised `AttributeError: 'Add' object has no attribute '_prec'`.

Following feedback from @smichr, this PR implements the narrow crash-fix without broadening numerical inference policy:
- Replaces direct `._prec` access with `getattr(..., '_prec', 1) != 1` (defaulting to `1` when precision is absent or indeterminate, safely returning `None` instead of raising `AttributeError`).
- Consolidates duplicated positive and negative number logic into a single `_number_sign(expr, positive)` helper.
- Adds regression tests in `sympy/assumptions/tests/test_query.py` asserting that evaluating predicates on these radical roots cleanly returns `None` rather than raising an unhandled exception.

#### Other comments

All 158 tests in `sympy/assumptions/tests/` pass.

#### AI Generation Disclosure

I used an AI assistant to help investigate the issue and draft the initial patch. I reviewed, refined, and tested all changes locally.

## Commits

- 210417de32 (pranjal9091): assumptions: handle non-Float evalf results when inspecting precision
      In assumptions handlers for sets and order predicates (_RealPredicate_number,
      _Imaginary_number, _PositivePredicate_number, _NegativePredicate_number, and
      NonZeroPredicate), evalf(2) was called and its output checked with ._prec != 1.
      When evaluating complex radical roots (such as quartic Ferrari resolvents),
      as_real_imag() does not cleanly isolate real and imaginary parts symbolically,
      causing evalf(2) to return an Add (e.g. Float + Float*I). Since Add does not
      have a _prec attribute, this raised AttributeError.
      Check if the evaluated part has _prec, and fallback to evaluating the full
      expression via expr.evalf(2).as_real_imag() when as_real_imag() was unable
      to separate pure numeric parts symbolically.
      Fixes item C6 of #31017
- f67a963382 (pranjal9091): mailmap: add pranjal9091 and raman118
- 54018522b0 (pranjal9091): assumptions: simplify crash-fix for non-Float evalf precision checks

## Conversation

### @smichr commented

I worked on #30755 and the concerns of @sylee957 have left it uncommited. I feel like these changes are moving in the same direction and should be reconsidered (or considered carefully) before moving ahead. Here is the ChatGPT reaction after having worked on #30755 and looking at these changes:

----
I think there is an opportunity to simplify the code substantially, and your concern about what is being compared is justified.

The PR fixes a real problem: `evalf(2)` can return an `Add` rather than a `Float`, so accessing `._prec` directly raises `AttributeError`.

But the fix introduces two concerns:

1. **Repeated logic:** The positive and negative predicate handlers contain nearly identical fallback code, duplicated again within each handler.
2. **Comparison semantics:** The patch uses `getattr(x, '_prec', 0) != 1` as permission to compare `x` numerically. That doesn't establish that `x` is numeric or that the comparison is meaningful.

The second point is more important than the duplication. We should establish what kind of object we have before interpreting a numerical comparison.

## **Comparison with your PR #30755**

The relationship is quite direct.

|                     | Your #30755                                           | #31147                                                          |
| ------------------- | ----------------------------------------------------- | --------------------------------------------------------------- |
| Location            | Core `Expr` and `Add` assumptions                     | `Q` predicate handlers                                          |
| Numerical mechanism | `_n2()` using 2-bit, then 10-bit evaluation           | `evalf(2)` with fallback to whole-expression evaluation         |
| Intended purpose    | Resolve previously unknown realness and signs         | Prevent exceptions and resolve difficult numerical expressions  |
| Exposure            | Broad, often implicit through `.is_real`              | Narrower, through `ask(Q...)`                                   |
| Principal risk      | Incorrect assumptions propagating into simplification | Incorrect predicate answers propagating into logical deductions |

Your PR has more substantial safeguards, including checking for numerical components and retrying at greater precision. Nevertheless, we held it because numerical evaluation can change fundamental symbolic assumptions.

**#31147 is taking the same approach, but with fewer safeguards.**

### **A concrete counterexample**

There is a particularly revealing example already documented in issue #31017:

```
z = -sqrt(3) - sqrt(2) + sqrt(5 + 2*sqrt(6))q = sqrt(z) - 2
```

Here `z` is exactly zero, so `q` is exactly `-2`.

On my local SymPy 1.14 installation:

```
>>> z.equals(0)True>>> q.equals(-2)True>>> q.evalf(2)-2.0 + 5.8e-11*I
```

Now follow the new negative predicate code in #31147.

The symbolic imaginary component is zero, so it first evaluates the real component. That evaluation produces a complex `Add`, triggering the new fallback:

```
r, i = q.evalf(2).as_real_imag()
```

The resulting `i` is approximately `5.8e-11`, with `_prec = 10`. Consequently:

```
if getattr(i, '_prec', 0) != 1:    if i != 0:        return False
```

The handler returns **False for&#x20;**`Q.negative(q)`, although `q` is exactly `-2`.

This is a traced prediction from the PR code using the locally reproduced numerical values, not a test run against the PR branch. But it exposes the precise problem: `_prec` tells us about the stored Float's precision, not whether cancellation error has made a mathematically zero component appear nonzero.

This is exactly the concern that led us to be cautious about #30755.

## **Are the handlers comparing the right things?**

There are two additional semantic concerns.

| Predicate                  | What it checks                      | What it actually needs                           |
| -------------------------- | ----------------------------------- | ------------------------------------------------ |
| `Q.real`                   | Imaginary part is zero              | Correct                                          |
| `Q.imaginary`              | Real part is zero                   | Imaginary part must also be nonzero              |
| `Q.positive`, `Q.negative` | Imaginary part zero, then real sign | Correct structure, unreliable numerical evidence |
| `Q.nonzero`                | Either component is nonzero         | Must also establish realness                     |

The distinction matters because SymPy explicitly excludes zero from `Q.imaginary`, and `Q.nonzero` means *real and nonzero*, not merely complex and nonzero.

For example, consider `sqrt(z)` in the example above. It is exactly zero, but its two-digit evaluation produces a tiny imaginary number. Following #31147's `_Imaginary_number` fallback, the numerical real part is zero, so the handler returns `True`. That would incorrectly classify zero as imaginary.

This indicates an existing limitation of testing only the real component, which the PR's new fallback exposes to additional expressions.

## **A much smaller correction**

If the objective is to fix the exception without enlarging the numerical inference policy, the basic change is simply:

```
if getattr(i, '_prec', 1) != 1:    return not i
```

The default should be **1 rather than 0**: if there is no recognized numerical precision, we have insufficient information and should return `None`.

For positive and negative, the existing duplication could be removed with one private helper, preserving the original component-first strategy:

```
def _number_sign(expr, positive):    r, i = expr.as_real_imag()    if r is S.NaN or i is S.NaN:        return    if i:        i = i.evalf(2)        if getattr(i, '_prec', 1) == 1:            return        if i:            return False    r = r.evalf(2)    if getattr(r, '_prec', 1) != 1:        return r > 0 if positive else r < 0
```

The two handlers become:

```
def _PositivePredicate_number(expr, assumptions):    return _number_sign(expr, True)def _NegativePredicate_number(expr, assumptions):    return _number_sign(expr, False)
```

This is a **minimal crash-fix proposal**, not a solution to the pre-existing numerical-inference risks. In particular, it intentionally returns `None` for the difficult quartic cases rather than introducing whole-expression evaluation.

## **Where I would draw the line**

I would suggest separating #31147 into two questions:

1. Can we prevent an `AttributeError` when `evalf(2)` returns a non-Float? **Yes, with a very small change.**
2. Should we use additional numerical evaluation to classify previously unresolved expressions? **That deserves the same scrutiny as #30755.**

The second question is a change of assumptions policy, not merely a bug fix.

In fact, issue #31017 contains both the crashing quartic case (C6) and the numerical misclassification case (W10). Fixing one by broadening numerical inference risks aggravating the other.

My preference would be to accept the narrow exception fix, consolidate the sign handlers, and defer expanded numerical reasoning until we have settled the policy behind your #30755.

That keeps the optional complexity with the cases that need it, and avoids turning uncertainty into a mathematical assertion.&#x20;

### @pranjal9091 commented

Thank you @smichr for the thorough review and comparison with #30755!

You're right expanding numerical evaluation to classify difficult expressions introduces floating-point cancellation risks that can turn into false mathematical assertions. Keeping this PR strictly scoped to a narrow crash-fix is much safer and avoids conflating bug fixing with the broader assumptions policy questions being discussed in #30755.

I have updated the branch with the suggested changes:
1. Replaced direct `._prec` access with `getattr(..., '_prec', 1) != 1` in `order.py` and `sets.py` (defaulting to `1` so unestablished/missing precision cleanly yields `None` rather than an exception).
2. Consolidated `_PositivePredicate_number` and `_NegativePredicate_number` using the `_number_sign(expr, positive)` helper.
3. Removed the whole-expression `evalf(2).as_real_imag()` fallback entirely.
4. Updated the regression test in `test_query.py` to verify that `ask` queries on these quartic radical roots safely return `None` without raising `AttributeError`.

All 158 tests in `sympy/assumptions/tests/` pass cleanly.

### @smichr commented

This looks not worse that master. But W10 is still a real issue.


## Reviews

(no reviews)
