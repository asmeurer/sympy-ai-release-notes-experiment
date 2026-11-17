# Issues and pull requests referenced by this pull request

## Issue #18349: Derivative.expr must be parenthesized when printed

- Opened by @mcpl-sympy, state: closed

Here is an example:
```python
from sympy import Derivative, Function
from sympy.abc import x
f = Function('f')
g = Function('g', commutative=False)
### These two result are printed identically
Derivative(f(x), x) * g(x)
Derivative(f(x)*g(x), x)
```

Thus, I suggest that ``Derivative.expr`` be parenthesized with ``PRECEDENCE['Mul']`` when printed.
