# Issues and pull requests referenced by this pull request

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
