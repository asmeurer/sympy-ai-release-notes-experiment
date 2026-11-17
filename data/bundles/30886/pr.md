# Pull request #30886: solvers: avoid IndexError in _solve_system when symbols is empty

- Author: @aarav570
- Merged: 2026-11-05T18:44:29Z into `master`
- Labels: (none)
- Size: +28 / -1 in 4 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #26504

#### Brief description of what is fixed or changed

When `_solve_system` is called on a system with no symbols to solve for (i.e. `symbols` is empty `()`), `g.as_poly(*symbols)` auto-detects generators from any non-algebraic terms (such as `(log(2), log(3))`). Because the linear system matrix was created with `len(symbols) + 1 == 1` column, assigning coefficients to `matrix[i, j]` for subsequent generators raised `IndexError: Index out of range: a[1]`.

This caused `integrate(2**(2+3*x)*3**(5+7*x), x)` to fail in `heurisch_wrapper` when inspecting the poles of the candidate denominator `3*log(2) + 7*log(3)`.

This change adds an early check in `_solve_system` when `symbols` is empty:
- If all equations evaluate to zero, it returns the consistent trivial solution `[{}]`.
- If any equation is a non-zero constant, it returns `[]` directly.

Regression tests have been added to `test_solvers.py` and `test_heurisch.py`.

#### Other comments

#### AI Generation Disclosure

Assisted by Google Antigravity / Gemini coding assistant to diagnose the IndexError in `_solve_system` and draft the empty symbols check in `sympy/solvers/solvers.py`. Verified and tested locally using pytest.

## Commits

- fc1091e133 (Aarav): solvers: avoid IndexError in _solve_system when symbols is empty
      # Conflicts:
      #	sympy/solvers/tests/test_solvers.py
- 12020a50f1 (Aarav): mailmap: add Aarav Malde
- ea26e2641e (Aarav): mailmap: add aliases for aarav570 and aarav.malde@iitgn.ac.in
- 7b4109f982 (aarav570): Update sympy/solvers/solvers.py
      Co-authored-by: Christopher Smith <smichr@gmail.com>
- 9292bada23 (Aarav): solvers: use checksol instead of equals(0) for empty symbols check
- ab3df223d1 (Christopher Smith): remove redundant .mailmap entry

## Conversation

### @knowprasad commented

I tested this locally against `sympy/solvers/solvers.py`. The early exit in `_solve_system` directly handles the problem reported in #26504.

When `symbols` is empty, calling `g.as_poly(*symbols)` fell back to auto-detected generators for transcendental terms like `log(2)` and `log(3)`. Because the linear system matrix only had 1 column allocated (`len(symbols) + 1`), writing coefficients for those generators raised an `IndexError`.

Evaluating `checksol(u, u, e)` correctly separates true zeros like `log(2) + log(3) - log(6)` from non-zero constants, returning `True, [{}]` for consistent systems and `True, []` for inconsistent systems. Tested the regression cases in `test_solvers.py` and `test_heurisch.py`, and the integration of `2**(2+3*x)*3**(5+7*x)` resolves cleanly.

One minor point in `.mailmap`:
The entry `Aarav Malde <aarav458@gmail.com> <aarav458@gmail.com>` maps the primary address to itself and can be removed.

Overall, this is a clean, targeted fix that stops the solver crash without touching unrelated solver paths.

### @aarav570 commented

@smichr @knowprasad 
A merge conflict was resolved .
Could you approve the updated PR?

### @knowprasad commented

I tested the rebased branch locally against latest main. The merge conflict resolution in `test_solvers.py` is clean and all solver tests pass without regressions. LGTM.

### @smichr commented

Thanks. I corrected mailmap and set to merge.


## Reviews

### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @aarav570 reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @aarav570 reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr commented on `sympy/solvers/solvers.py`

```suggestion
    if the system was linear or if no symbols were provided, else False; ``solution``
```

### @smichr commented on `sympy/solvers/solvers.py`

Why return [{}] for a consistent zero-variable system when _solve_system normally removes empty solution dictionaries? Could we use return True, [] here, or is there a caller that requires distinguishing the two cases? Why is `equals(0)` needed instead of a cheaper zero check using `checksol(x, x, e)`?

### @aarav570 commented on `sympy/solvers/solvers.py`

1. `_solve_system` itself requires distinguishing the two cases when splitting equations into connected components(`flags.pop('_split', True)` at line 1816). If we used True, [] for consistent subsytems then any valid system containing a consistent constant/parameter equation would receive `subsols = [[{x: 1}], []]`, causing `product(*subsols)` to return [] , falsely claiming that no solution exists.
2. Yeah, using equals(0) is redundant and incurs a lot of overhead. I'll update the check to 
    ```python
    if not symbols:
        u = Dummy()
        if all(e.is_zero or checksol(u, u, e) for e in exprs):
            return True, [{}]
        return True, []
    ```

### @oscarbenjamin commented on `sympy/solvers/solvers.py`

If there are no equations then `[{}]` is the correct result. I opened an issue somewhere about this. This is incorrect:
```python
In [25]: solve([])
Out[25]: []
```

### @aarav570 commented on `sympy/solvers/solvers.py`

Yess , for zero variables, the domain consists of the empty maping `{}` ,making `[{}]` the mathematically consistent result. `[]` would treat the system as inconsistent.
Please let me know if there are any further adjustments needed for this PR!

### @smichr commented on `.mailmap`

```suggestion
```
