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

## Pull request #30965: 🤖 Add type annotations to Piecewise and piecewise_fold

- Opened by @hunterhogan, state: open

🤖 *This description was drafted by an AI agent (Claude Code); Hunter Hogan 👋 revised it.*

#### References to other Issues or PRs

* #30919 
* #30945
* Related typing PRs: #30946 (`solveset`): I had hoped typing this would shed a little light on `solveset`. It might help a little.

#### Brief description of what is fixed or changed

Adds type annotations to `Piecewise`, `ExprCondPair`, and `piecewise_fold` in `sympy/functions/elementary/piecewise.py`. ~One behavior change: an Exception in `piecewise_fold` was made more specific.~

Every change has a specific need:

- `Piecewise.__new__` overloads for the Boolean branch.
- ~`Piecewise.__new__` `# type: ignore` similar to `Mul`, `Add`, and `AppliedUndef`.~
- `evaluate: bool | None = True` in the overloads matches the `Add` and `Mul` stubs (Microsoft).
- ~`newargs: list[ExprCondPair]`, `new_args: list[tuple[Basic, Boolean]]`: typed lists help the type checkers.~
- `Piecewise.args -> tuple[ExprCondPair, ...]` under `TYPE_CHECKING`: eliminates some type-checker errors, such as `for e, c in pw.args` ("Basic" is not iterable).
- `ExprCondPair.args -> tuple[Basic, Boolean]`, `expr -> Basic`, `cond -> Boolean`: `ExprCondPair.__new__` guarantees a Boolean condition: before, `cond` was inferred as `Basic` (e.g. `cond = pair.cond` in `Piecewise.__new__`).
- `ExprCondPair.__iter__ -> Iterator[Basic]`: unpacking a pair was untyped.
- `Undefined: NaN`: `S.NaN` is resolved dynamically, so its type was unknown.
- `piecewise_fold` overloads: `Expr -> Expr`; `Boolean -> Boolean | Piecewise` (a Boolean can fold into a `Piecewise`); `Basic -> Basic`; non-`Basic` input is returned unchanged (`T -> T`).
- `for pair in expr.args: e, c = pair.expr, pair.cond` and `p.expr`/`p.cond` in the nested comprehension: unpacking goes through `__iter__`, which can only give `Basic`; `.cond` gives the `Boolean` that `And` requires.
- `exprs, conds = zip(*ec)`: `e` and `c` already hold a `Basic` and a `Boolean` in the `Piecewise` branch; `zip` gives tuples, and mypy rejects re-binding the names to a different type.
- `isinstance(rv, Piecewise)` in the `evaluate=None` shortcut: `Piecewise(...)` may return a non-`Piecewise`, which has no `.cond`; that path previously raised `AttributeError`.
- `ExprCondPair` branch (behavior change): `piecewise_fold(ExprCondPair(...))` with a `Piecewise` inside always raised `TypeError: cannot unpack non-iterable ...`, because the loop treated the pair's `(expr, cond)` as a sequence of pairs. It now raises a `TypeError` that names the `ExprCondPair`; a test is added to `test_piecewise_fold`.

#### Other comments

`mypy sympy`, `ruff check sympy`, `bin/test quality`, and the piecewise tests and doctests pass locally; the integrals, sets, logic, solveset, and continuous-RV tests also pass.

#### AI Generation Disclosure

Generated with Claude Code (Claude Opus 5.5), reworked for three hours by Hunter Hogan, over-cleaned by Claude, Hunter lectured Claude, Claude corrected Hunter on a few points, Claude tidied up, and Hunter reviewed all changes. AI-generated-ish: the annotations and code changes in `sympy/functions/elementary/piecewise.py`, the added `raises` line in `sympy/functions/elementary/tests/test_piecewise.py`, and this description.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
💪 Generated with [hard work](@hunterhogan)
