# Issues and pull requests referenced by this pull request

## Pull request #30990: 🤖 Annotate Basic.xreplace

- Opened by @hunterhogan, state: closed, merged 2026-11-13

🤖 *This description was drafted by an AI agent (Claude Code) and revised by Hunter Hogan.*

#### References to other Issues or PRs

Related typing PRs: #30946 (`solveset`), #30965 (`piecewise_fold`).

#### Brief description of what is fixed or changed

- Annotates `Basic.xreplace` and adds type-checking-only overloads for some subclasses. 
- `Atom.xreplace` replaced by `Atom._xreplace`
- Change `rule` parameter dictionary keys to TypeVars.

#### Other comments

<details><summary>Other</summary>
- `TensExpr.xreplace` needs `# type: ignore[override]`: mypy rejects a leading overload that `Expr.xreplace` lacks.
- Known gap: a `Symbol` statically typed as `Boolean` matches `Boolean`'s `Expr`-to-`Expr` overload, so `p.xreplace({p: sin(x)})` is typed `Boolean`.
</details>

#### AI Generation Disclosure

Generated with Claude Code (Claude Opus 5.5), Hunter Hogan, and Predator Energy Drink.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
