# Pull request #30963: Respect binary precision in codegen numerical evaluation

- Author: @raman118
- Merged: 2026-11-09T19:27:12Z into `master`
- Labels: (none)
- Size: +55 / -11 in 6 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #22326.

#### Brief description of what is fixed or changed

The numerical evaluation hooks for `log2`, `logaddexp`, `logaddexp2`, `cosm1`, and `powm1` passed binary precision to `evalf`, which interprets it as decimal digits. A 53-bit request consequently produced a 179-bit result. Use public `evalf(prec_to_dps(prec))` to convert binary precision to decimal digits while preserving adaptive precision during cancellation.

#### Other comments

The precision regressions failed before the fix. All 20 tests in the three affected test files passed, including checks at 53 and 113 bits, symbolic evaluation, and cancellation-sensitive `cosm1` and `powm1` cases at 15, 30, and 50 decimal digits. Code-quality tests (6 passed), Ruff, and the pre-push author check passed.

#### AI Generation Disclosure

OpenAI Codex (GPT-6 Astra) generated all changes in `sympy/codegen/cfunctions.py`, `sympy/codegen/numpy_nodes.py`, `sympy/codegen/scipy_nodes.py`, and their corresponding test files.

## Commits

- 8d4ca2687f (raman118): Respect binary precision in codegen numerical evaluation
      Forward precision through the binary _evalf helper for log2, logaddexp, logaddexp2, cosm1, and powm1.
      AI-generated changes by OpenAI Codex (GPT-6 Astra).
- 8ab445a07a (raman118): Use public evalf with converted decimal precision
      Preserve adaptive precision during cancellation and cover small cosm1 and powm1 results at 15, 30, and 50 digits.
      AI-generated changes by OpenAI Codex.

## Conversation

### @smichr commented

Using evalf with dps/prec conversion,  not underscore version, is the way to ensure accurate results.

### @raman118 commented

Thanks for pointing this out Christopher. I’ll use the public evalf() method with the appropriate conversion from binary precision to decimal digits. I’ll also update the tests to check numerical accuracy, including cancellation-sensitive cases, rather than relying on _prec alone.

### @raman118 commented

> Using evalf with dps/prec conversion, not underscore version, is the way to ensure accurate results.

Done

### @smichr commented

The extra (accidental) precision allowed these routines to be more accurate; they can probably be improved now that they are receiving the correct precision, but that is an internal problem, not a problem for the caller.


## Reviews

(no reviews)
