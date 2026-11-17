# Pull request #30947: 🤖 Annotate `MatrixBase.LUsolve` and `MatrixBase.__iter__`

- Author: @hunterhogan
- Merged: 2026-11-05T14:45:37Z into `master`
- Labels: (none)
- Size: +5 / -1 in 2 files (full diff in `diff.patch`)

## Description

🤖 This PR description was drafted by an AI agent (Claude Code).

#### References to other Issues or PRs

Related: #30942, #30946 (other annotation PRs).

#### Brief description of what is fixed or changed

- `MatrixBase.LUsolve(rhs: Tmat, iszerofunc: Callable[[Expr], bool | None] = _iszero) -> Tmat`. The return type follows `rhs`, not `self`, because `_LUsolve` returns `rhs.__class__(b)`.
- `MatrixBase.__iter__ -> Iterator[Expr]`, declared only under `TYPE_CHECKING`. Matrices are iterable at runtime through `__getitem__`/`IndexError`, but type checkers don't treat that as `Iterable`, so `tuple(M)` or `map(int, M)` fail type checking.

No runtime change.

#### Other comments

`mypy sympy`, `ruff`, `bin/test quality`, `bin/test sympy/matrices`, and `bin/doctest sympy/matrices` pass. Also adds a `.mailmap` entry for me.

#### AI Generation Disclosure

Claude Code (Claude Opus 5.5) generated the code changes in `sympy/matrices/matrixbase.py` and drafted this PR description at my direction. Hunter "The Human" Hogan reviewed everything.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Commits

- 7f79543621 (Hunter Hogan): typing: annotate MatrixBase.LUsolve
      The return type follows rhs because _LUsolve returns rhs.__class__(b).
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- 2d260d6636 (Hunter Hogan): typing: declare MatrixBase.__iter__ for type checkers
      Matrices iterate at runtime through __getitem__ and IndexError, which
      type checkers do not treat as Iterable. The declaration is under
      TYPE_CHECKING, so runtime behavior is unchanged.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- a4d119fa6c (Hunter Hogan): Add Hunter Hogan to .mailmap
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

## Conversation

(no comments)

## Reviews

(no reviews)
