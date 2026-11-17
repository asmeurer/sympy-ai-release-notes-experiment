# Pull request #31075: printing: pass torch_code settings to TorchPrinter

- Author: @raman118
- Merged: 2026-11-13T20:45:48Z into `master`
- Labels: (none)
- Size: +21 / -3 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Addresses the `CmathPrinter` float-recursion finding in [#30844](https://github.com/sympy/sympy/issues/30844). The other findings in that issue are outside this change.

#### Brief description of what is fixed or changed

Removed `CmathPrinter._print_Float` so the cmath printer inherits Python’s existing float-printing behavior.

The override called `self._print()` on the same `Float`, causing infinite recursion. It also attempted to wrap the result in `cmath.mpf`, which does not exist. Consequently, `lambdify` could not generate cmath functions containing floating-point constants.

For example:

```python
from sympy import lambdify, symbols

x = symbols('x')
f = lambdify(x, x + 2.5, 'cmath')
```

Previously, constructing `f` raised `RecursionError`. With this change:

```python
>>> f(1)
3.5
>>> f(1j)
(2.5+1j)
```

Added regression coverage for printing positive and negative floats, evaluating generated functions with real and complex inputs, and taking a complex square root of an expression containing a floating-point constant.

#### Other comments

Validation:

- Both regression tests failed with `RecursionError` before the fix.
- Python printer and lambdify tests: 167 passed, 23 skipped.
- Python printer doctests: 2 passed.
- Code-quality tests: 6 passed, 1 deselected.
- Ruff across `sympy`, diff checks, and the post-commit mailmap check passed.

The existing `.mailmap` already maps both Doremon aliases to the canonical contributor identity, so no author-mapping changes were needed.

GitHub CI results were not available when these local checks were recorded.

#### AI Generation Disclosure

I did the analysis and chose the fix; OpenAI Codex wrote the code in `sympy/printing/pycode.py`, `sympy/printing/tests/test_pycode.py`, and `sympy/utilities/tests/test_lambdify.py` under my direction. I reviewed and tested everything before pushing.

## Commits

- 03c027512b (raman118): printing: pass torch_code settings to TorchPrinter
      OpenAI Codex generated this change.
- 58b1641f33 (raman118): printing: preserve torch_code assignment targets
      OpenAI Codex generated this change in response to review.

## Conversation

### @raman118 commented

@smichr Thanks for catching this. I missed that `assign_to` belongs to `doprint`, not the printer settings.

The fix is pushed in 58b1641f33, with tests for scalar and matrix assignments and for using `assign_to` alongside printer settings. All 43 relevant tests pass locally, along with the quality and Ruff checks.

You're also right about the description it describes the cmath fix and still needs replacing.


## Reviews

(no reviews)
