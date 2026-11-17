# Issues and pull requests referenced by this pull request

## Issue #31133: `atoms()` broken for And/Or with `evaluate=False`

- Opened by @dweindl, state: closed

Hi, I encountered a problem with And/Or with `evaluate=False` in sympy-1.15.0rc2. 

With sympy-1.14.0, *expected*:

```python
from sympy import *

x, y = symbols("x y")
e = And(x > 1, y > 2, evaluate=False)
print(e.args)              # (x > 1, y > 2)
print(e.atoms(Symbol))     # {y, x}
```

With sympy-1.15.0rc2, *unexpected*:

```python
from sympy import *

x, y = symbols("x y)
e = And(x > 1, y > 2, evaluate=False)
print(e.args)              # (x > 1, y > 2)
print(e.atoms(Symbol))     # set()
``` 

The problem seems to be that in `LatticeOp.__new__` `obj._argset = frozenset(args)` uses the `args` generator that was exhausted on the previous line:  

https://github.com/sympy/sympy/blob/43239d67766e39b50d0a160be525be975c832e1e/sympy/core/operations.py#L529-L536

Introduced in https://github.com/sympy/sympy/pull/28062

(Found with AI-assistance)
