# Pull request #31042: retune how Mod handles Floats in args

- Author: @smichr
- Merged: 2026-11-15T20:13:24Z into `master`
- Labels: (none)
- Size: +162 / -52 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

fixes #31031 

#### Brief description of what is fixed or changed

I have iteratively re-evaluated with ChatGPT what is happening in the Mod.eval method. The original issue identified undesirable redistribution of Floats. Investigating that exposed other issues (and opportunities) as well. The current state has improved expression fidelity and leaves handling with Floats to the user, refusing to make transformations that might apply if the Floats were Rationals since that is a decision for the caller. A quintessential example is `Mod(6*x, 0.2*x)`, which formerly simplified to zero even though direct floating-point evaluation can produce a nonzero remainder.
```python
>>> Mod(6*x, 0.2*x)
0  <---- now unchanged as Mod(6*x, 0.2*x)
>>> Mod(6*x, 0.2*x, evaluate=False).subs(x,1)
0.200000000000000
```
*Die ganzen Zahlen hat der liebe Gott gemacht, alles andere ist Menschenwerk.*
(God made the integers; all else is the work of man. -Leopold Kronecker)

This is the summary of changes (written by ChatGPT):

### Summary of `fmod` changes relative to SymPy master

- Prevent unsafe Float simplification in `Mod`. Symbolic expressions containing Floats are no longer automatically rearranged, reduced, or rescaled when doing so could change numerical results after substitution.
- Preserve numerical evaluation. Fully numerical expressions, including those containing Floats, can still evaluate normally. For example, `Mod(5.0*sqrt(2), sqrt(5))` simplifies to `5.0*sqrt(2) - 3*sqrt(5)`.
- Restrict common-factor extraction. GCD extraction and coefficient normalization are performed only when the operands contain no Floats. This avoids rounding differences from otherwise valid algebraic transformations.
- Improve exact modular normalization. Integer-valued symbolic terms with Integer or Rational coefficients can be reduced modulo an exact Rational modulus, even when the entire dividend is not integer-valued. For example, [with `i` integer-valued and `x` vanilla]:
```python
Mod(3*i + x, 2)      # -> Mod(i + x, 2)
Mod(4*i/3 + x, S(1)/5)  # -> Mod(2*i/15 + x, 1/5)
```
- Preserve negative-modulus conventions. Coefficients are reduced using the signed modulus, maintaining correct behavior for negative divisors.
- Add regression tests demonstrating Float rounding differences, protection of nested `Mod` expressions, exact Rational normalization, and the importance of integer assumptions.
- Update C printer tests to reflect the preservation of symbolic Float expressions without introducing synthetic `1.0` coefficients.

Overall: `Mod` now performs more useful canonicalization for exact arithmetic while avoiding transformations that could alter floating-point results.

#### Other comments

#### AI Generation Disclosure

ChatGPT collaboration.

## Commits

- a62bc44d56 (Christopher Smith): Keep Float operands inside Mod during symbolic evaluation
- 5fabd45920 (Christopher Smith): Preserve Float operands while extracting exact factors from Mod
- 78d9fb8ccb (Christopher Smith): Extract exact integer factors from Float moduli for canonical Mod terms
- 546971b80a (Christopher Smith): Allow exact Mod reductions around nested Floats and update C printer expectations
- 7523e90d8c (Christopher Smith): Avoid common-factor extraction from symbolic Float Mod arguments
- edc9851c0e (Christopher Smith): Make Float remainder regression checks robust to final-bit rounding
- f9bf30175b (Christopher Smith): more restricted Mod with Float
- d8c5099500 (Christopher Smith): add integer Mod tests
- 5dc4a4a150 (Christopher Smith): Simplify Mod Float guards and consolidate redundant regression tests

## Conversation

### @Naveen447-a11y commented

I reviewed the changes in `sympy/core/mod.py`, `sympy/core/tests/test_arit.py`, and `sympy/printing/tests/test_c.py`.

The Float guards appear consistent with the goal of avoiding potentially unsafe symbolic rearrangements involving floating-point expressions. I also checked the integer-term simplification tests and the large-integer substitution regression case.

I ran the targeted arithmetic and C printer tests locally, and they passed.

I haven't identified a concrete correctness issue in the reviewed changes. Thank you for the implementation and regression tests.


## Reviews

(no reviews)
