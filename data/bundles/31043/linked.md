# Issues and pull requests referenced by this pull request

## Pull request #31016: 🤖 Fix wrong solveset results for modular powers with a non-coprime base

- Opened by @adityaanikam, state: closed, merged 2026-11-11

#### References to other Issues or PRs
Fixes #30996

#### Brief description of what is fixed or changed
`solveset` gave wrong answers for `Mod(b**x, m) = r` when `b` shares a factor with `m`, for example `Mod(2**x, 42)`. `_invert_modular` assumed the powers of `b` are periodic from the start, which is false in that case. Following the review, it now returns the expression unevaluated unless the modulus, rhs and base are integers and the base and rhs are coprime to the modulus. It also returns early when the term is not a `Mod`, which covers `Mod(2*2**x - 1, 42)` (it raised `TypeError`).

#### Other comments
`Mod(12**x, 21) - 18` is now unevaluated, so I changed that existing test to expect a `ConditionSet`. The issue's cases are added to `test_solve_modular`.

#### AI Generation Disclosure
I used Claude Code (Claude Sonnet 5.5) to help find the cause and to write the change and tests. I reviewed it and ran the tests myself.
