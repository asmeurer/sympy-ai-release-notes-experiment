# Pull request #31025: 🤖 Annotate fraction, numer, and denom

- Author: @hunterhogan
- Merged: 2026-11-13T14:45:57Z into `master`
- Labels: typing
- Size: +12 / -9 in 2 files (full diff in `diff.patch`)

## Description

🤖 *This description was drafted by an AI agent (Claude Code).*

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

Type annotations in `sympy/simplify/radsimp.py`:

- `fraction(expr: Expr, exact: bool = False) -> tuple[Expr, Expr]`
- `numer` and `denom`: same parameters, `-> Expr`
- In `fraction`, `term.is_Rational` becomes `isinstance(term, Rational)` so type checkers accept `term.p` and `term.q`. Only `Rational` sets `is_Rational = True`, so behavior is unchanged.

#### Other comments

`mypy sympy`, `ruff check sympy`, `bin/test quality`, `radsimp.py` doctests, and the radsimp/simplify tests pass locally.

#### AI Generation Disclosure

Claude Code (Claude Opus 5.5) wrote all changes in this PR and this description. Hunter Hogan reviewed them.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Commits

- 762e0ba467 (Hunter Hogan): Annotate fraction, numer, and denom
      fraction takes an Expr and returns a pair of Expr. Testing
      isinstance(term, Rational) instead of term.is_Rational lets type
      checkers see .p and .q; only Rational sets is_Rational.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- a43eef58d9 (Hunter Hogan): Accept unsympified input in fraction, numer, and denom
      fraction sympifies its argument, so Expr | complex matches the convention
      for parameters that have not been sympified yet.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- fdff1f4d95 (Hunter Hogan): Declare fraction's numer and denom lists as Expr | int
      Rational.p and Rational.q are int. Once @cacheit was typed, mypy inferred
      list[Expr] for the lists and rejected appending them.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- 32a80b0127 (Hunter Hogan): Narrow numer to Mul in LatexPrinter._print_Mul
      fraction now returns Expr, so numer.args is tuple[Basic, ...]; with the
      Integer.__mul__ overloads from #29422, a*x no longer type checks.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

## Conversation

### @oscarbenjamin commented

Looks good.


## Reviews

### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin commented on `sympy/simplify/radsimp.py`

I think the parameter annotation should be `Expr | complex`. At least for now this is what we use for parameters that have not been sympified yet.
