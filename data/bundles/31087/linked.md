# Issues and pull requests referenced by this pull request

## Issue #29714: Derivative of function with composite arguments creates non-Dummy symbols with expression names

- Opened by @yeguarr, state: closed

## Issue

When differentiating a function with multiple arguments that are compositions of the base symbols (e.g., `f(x+y, x*y)`), SymPy introduces symbols whose names are the string reps of those compositions, such as `Symbol('_x + y')`, instead of proper `Dummy` symbols. These symbols are not `Dummy` and therefore are not treated as internal temporaries; they leak into `free_symbols` and break any subsequent evaluation / `lambdify` attempt.

## Steps to Reproduce

```python
import sympy as sp

x, y = sp.symbols('x y')
f = sp.Function('f')

expr = f(x + y, x*y)
dexpr = expr.diff(y).diff(x)

print(dexpr)
print(sp.srepr(dexpr))
```

## Expected Behavior

Only `Dummy` variables (e.g., `Dummy('xi_1')`) should appear in the `Subs` and `Derivative` nodes. The expression’s free symbols should be just `{x, y}`.

## Actual Output

The printed expression contains symbols like `_x + y`. The internal representation (`srepr`) shows:
```
...
Symbol('_x + y')
...
```
and `free_symbols` returns `{y, _x + y, x}` (or similar). These symbols are ordinary `Symbol` objects, not `Dummy`, and lack substitution.

## Python Version

- SymPy version: 1.14.0
- Python version: 3.14.4

## Additional Context

This behaviour was discovered while trying to create a custom `lambdify` for Julia’s `SymPyPythonCall` package, but the bug is reproducible in pure SymPy. Workaround involves manually replacing these symbols by the corresponding expressions, but the root cause should be fixed.
