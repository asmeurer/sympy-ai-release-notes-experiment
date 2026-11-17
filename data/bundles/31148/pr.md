# Pull request #31148: printing: fix IndexError for empty NDimArray in LaTeX and pretty printers

- Author: @tusharcancodehere
- Merged: 2026-11-17T12:06:27Z into `master`
- Labels: (none)
- Size: +17 / -0 in 5 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Part of #30844.

#### Brief description of what is fixed or changed

`latex(Array([], (0, 2)))` and `pretty(Array([], (0, 2)))` crash with `IndexError: list index out of range`.

The bug is in `_print_NDimArray` -- it iterates over `itertools.product(*shape_ranges)` to visit every element. When any dimension is 0, the product yields nothing, so `level_str[0]` stays empty and the following `level_str[0][0]` access blows up.

Fix: return early before entering the loop when any dim in `expr.shape` is zero. LaTeX gets an empty matrix environment (consistent with how `Matrix([])` renders), pretty printer gets `[]`.

#### Other comments

Added tests for shapes `(0,)`, `(0, 2)`, and `(2, 0)` for all four array types.

#### AI Generation Disclosure

NO AI USE

## Commits

- da154bb111 (tushar): fix crash in latex/pretty when array has a zero dimension
      Array([], (0, 2)) blows up with IndexError because _print_NDimArray
      assumes the itertools.product loop runs at least once. short-circuit
      when any dim is 0.
- 516757a3fa (tushar): mailmap: add Tushar Verma and raman118

## Conversation

(no comments)

## Reviews

(no reviews)
