# Pull request #31024: 🤖 Annotate Mul.__neg__ and Mul.as_ordered_factors

- Author: @hunterhogan
- Merged: 2026-11-10T22:17:50Z into `master`
- Labels: (none)
- Size: +9 / -5 in 2 files (full diff in `diff.patch`)

## Description

🤖 *This description was drafted by an AI agent (Claude Code).*

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

Type annotations in `sympy/core/mul.py`:

- `Mul.__neg__ -> Expr` 
- `Mul.as_ordered_factors(order: str | Symbol | MonomKey | None = None) -> list[Expr]`
- `Mul._sorted_args -> tuple[Expr, ...]`, plus `is_Mul` and `_kind_dispatcher` attribute annotations.
- `.. py:class:: MonomKey` in `doc/src/modules/core.rst` so the documented signature resolves.

No runtime changes.

#### Other comments

ran some tests.

#### AI Generation Disclosure

Claude Code (Claude Opus 5.5) 

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Commits

- 3d6d61ffe1 (Hunter Hogan): Annotate Mul.__neg__ and Mul.as_ordered_factors
      Mul.__neg__ returns Expr: _from_args returns the lone factor when only
      one remains. The order parameter of as_ordered_factors reaches
      monomial_key through sort_key, so it takes monomial_key's order type.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

## Conversation

### @oscarbenjamin commented

Looks good.


## Reviews

### @oscarbenjamin reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED



### @oscarbenjamin commented on `sympy/core/mul.py`

Is this necessary?

### @hunterhogan commented on `sympy/core/mul.py`

No, it is 100% not necessary.

I annotate everything because it makes it much easier for me to annotate the package correctly. In VS Code, adding that annotation prevents inferred Ghost Annotations on later lines. Sympy has the mypy rule against redeclarations, so by adding the annotation at the first opportunity, 1) VS Code displays fewer inferred annotations, 2) mypy will prevent later redeclarations, and 3) the type checkers diagnose incompatible redeclarations.
