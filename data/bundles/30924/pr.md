# Pull request #30924: Avoid symbolic multiplication in evalf_mul

- Author: @smichr
- Merged: 2026-11-05T20:13:08Z into `master`
- Labels: (none)
- Size: +118 / -13 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

closes #30874
alternative to close #30897

#### Brief description of what is fixed or changed

Improvements to the legacy `evalf_mul` code (that I worked on almost 15 years ago). The use of `Mul` inside the function has been removed. The purpose of using that `Mul` is retained by using a custom accumulator to multiply exactly the complex numbers with only Rational parts.

#### Other comments

* don't mix Float and Rational while accumulating the exact part
* flatten args so unevaluated Mul are allowed to have their exact portions accumulated (once you pass an expression to evalf it will do its best to give you the correct answer).
* tests were added that either fail in master (or fail if exact accumulation is not performed)

#### AI Generation Disclosure

This was a highly collaborative change made with ChatGPT.

## Commits

- 0d21430f09 (Christopher Smith): Avoid symbolic multiplication in evalf_mul
      Multiplying SymPy expressions inside evalf_mul
      can trigger infinite recursion when called in an
      evaluate(False) context. Replace the symbolic expansion
      of complex factors with a small exact accumulator that
      uses only integer arithmetic and math.gcd.
      Nested Mul arguments are now flattened, and exact
      rational complex factors are accumulated into a
      single coefficient before numerical evaluation.
      Factors containing Floats are handled separately
      to avoid premature rounding.
      This avoids recursive evaluation and changes to
      the global evaluation setting while preserving exact
      cancellation and improving numerical accuracy, as
      demonstrated by the added tests.

## Conversation

(no comments)

## Reviews

(no reviews)
