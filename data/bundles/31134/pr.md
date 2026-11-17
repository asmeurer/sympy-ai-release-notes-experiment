# Pull request #31134: Handle uncertain endpoint membership when simplifying interval unions

- Author: @raman118
- Merged: 2026-11-17T01:33:54Z into `master`
- Labels: (none)
- Size: +12 / -2 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

See [#31017](https://github.com/sympy/sympy/issues/31017), item C4.

#### Brief description of what is fixed or changed

Fixed a `TypeError` when combining an open interval with a finite set containing a known endpoint and a symbolic element.

For example:

```python
Union(Interval.open(-1, 1), FiniteSet(x, 1))
```

Previously, this raised `TypeError: did not evaluate to a bool: Eq(x, -1)`. It now returns the union of `Interval.Lopen(-1, 1)` and `{x}`, closing the known right endpoint while retaining the symbolic element.

The interval-union handler already checks whether each endpoint is definitely contained in the other set. The fix reuses those checks instead of repeating them with Python membership operators, which raise when membership is undecidable.

Added regression coverage for both endpoint directions and substitutions at the endpoints, inside and outside the interval, at a complex value, and at either infinity.

#### Other comments

Validation:

- The new regression test failed before the fix and passed afterward.
- Set-module and calculus-utility tests: 250 passed, 2 deselected, 9 xfailed.
- Set doctests: 41 passed.
- Code-quality tests: 6 passed, 1 deselected.
- Ruff across `sympy`, final diff checks, and the post-commit `python bin/mailmap_check.py` passed.

This addresses C4 only; the remaining findings in the umbrella issue are outside this change.

#### AI Generation Disclosure

OpenAI Codex generated the changes in `sympy/sets/handlers/union.py` and `sympy/sets/tests/test_sets.py`.

## Commits

- 440e6a0496 (raman118): Handle uncertain endpoint membership when simplifying interval unions
      OpenAI Codex generated this change.

## Conversation

### @smichr commented

Looks good, thanks.


## Reviews

(no reviews)
