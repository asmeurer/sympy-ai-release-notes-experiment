# Pull request #30973: tensor: support array_derive for OneArray

- Author: @Roshanraj2580
- Merged: 2026-11-09T23:20:45Z into `master`
- Labels: tensor
- Size: +31 / -3 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #30970

#### Brief description of what is fixed or changed

`array_derive` lacked a registration for `OneArray`, causing it to fall back to the generic `Expr` handler which only returned `ZeroArray(*x.shape)` without preserving the shape of the expression being differentiated. In `ArrayTensorProduct._array_derive`, this shape mismatch resulted in `PermuteDims` raising `ValueError: Permutation size must be the length of the shape of expr`.

This PR:
- Registers `OneArray` in `array_derive` returning `ZeroArray(*(get_shape(x) + expr.shape))` consistent with `ZeroArray`.
- Updates the `Expr` fallback in `array_derive` to return `ZeroArray(*(get_shape(x) + get_shape(expr)))`.
- Adds regression tests for `OneArray` differentiation and `ArrayTensorProduct` in `test_arrayexpr_derivatives.py`.
- Adds `Roshanraj2580` to `.mailmap`.

#### Other comments

None

#### AI Generation Disclosure

NO AI USE

## Commits

- 16bf0cb113 (Roshanraj2580): tensor: support array_derive for OneArray
- e697a9e016 (Roshanraj2580): authors: add Roshanraj2580 to .mailmap

## Conversation

### @Roshanraj2580 commented

Thanks for pointing that out! A shell escaping issue had clipped the backticks into a control character. Fixed now, and the bot output looks clean.

### @ThePauliPrinciple commented

Thanks for the quick work!

This looks good to me. It fixes the issue I had. The order of the indices are correct.

Perhaps it is also related to https://github.com/sympy/sympy/issues/30902

### @Roshanraj2580 commented

Thanks for testing and confirming! Yeah, #30902 covers several related routing issues and rank assumptions across `array_derive` and the converters. Will check if some of the simpler zero-array / rank-handling cases there can be addressed cleanly in a follow-up.


## Reviews

(no reviews)
