# Issues and pull requests referenced by this pull request

## Pull request #30942: 🤖 Add type overloads for solve

- Opened by @hunterhogan, state: closed

🤖 This PR description was drafted by an AI agent (Claude Code) and revised by the human author.

#### References to other Issues or PRs

None.

#### Brief description of what is fixed or changed

Adds `@overload` signatures to `solve` so type checkers can infer its return type in the common cases:

- one expression/equation and exactly one symbol: `list[Expr]`
- `dict=True`: `list[dict[Expr, Expr]]`
- `set=True`: `tuple[list[Expr], set[tuple[Expr, ...]]]`
- everything else: `Any`

No runtime change. This follows the pattern used for `symbols()` in `sympy/core/symbol.py`.

#### Other comments

Known imprecision: `solve(Eq(x, True), x)` returns a boolean, but type checkers cannot distinguish it from an ordinary `Equality`, so it matches the `list[Expr]` overload.

#### AI Generation Disclosure

Claude Code (Claude Opus 5.5) generated most changes in `sympy/solvers/solvers.py` (the `TYPE_CHECKING` imports and the `solve` overloads) and this PR description. The human author revised the code.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Pull request #30946: Annotate `solvers.solveset`

- Opened by @hunterhogan, state: open

🤖 This PR description was drafted by an AI agent (Claude Code).

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

Annotates `solveset`, `solveset_real`, and `solveset_complex` so type checkers infer `Set` as the return type.

- `f: Basic | complex` and `symbol: Basic | None`, because both are passed through `sympify`, and internal callers (`sympy/calculus/singularities.py`) pass `Basic` and `Boolean` values.
- `domain: Set`, return `-> Set`.

After annotating the symbols in the signature, it was necessary to create new symbols in the function body if they object type changed, such as `f` to `expr`. The public API is unchanged. No behavior change.

#### Other comments

`mypy sympy`, `ruff`, `bin/test quality`, `sympy/solvers/tests/test_solveset.py`, `sympy/calculus` tests, and the `solveset.py` doctests pass.

#### AI Generation Disclosure

Claude Code (Claude Opus 5.5) generated code changes and drafted this PR description at my direction. Hunter "The Human" Hogan reviewed everything.
