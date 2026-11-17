# Issues and pull requests referenced by this pull request

## Issue #30925: avoid Basic ops during evalf

- Opened by @smichr, state: open

#30874 identified an issue in evalf (fixed in #30924) and an audit reveals the following items that could also use attention:

- [x] Fix recursion in `get_abs` under `evaluate(False)`. #30950

  ```python
  from sympy import Abs, I
  from sympy.core.parameters import evaluate

  with evaluate(False):
      Abs(1 + I, evaluate=False).evalf()
  ```

- [ ] Fix recursion in `evalf_log` for complex arguments under `evaluate(False)`.

  ```python
  from sympy import I, log
  from sympy.core.parameters import evaluate

  with evaluate(False):
      log(1 + I, evaluate=False).evalf()
  ```

- [ ] Fix recursion in `evalf_mul` when multiplying complex infinities under `evaluate(False)`.

  ```python
  from sympy import Mul, zoo
  from sympy.core.parameters import evaluate

  with evaluate(False):
      Mul(zoo, zoo, evaluate=False).evalf()
  ```

- [ ] Preserve the sign of finite factors when multiplying by infinity.

  ```python
  from sympy import Mul, oo

  assert Mul(-1, oo, evaluate=False).evalf() == -oo
  ```

- [ ] Preserve the sign of finite factors when multiplying by negative infinity.

  ```python
  from sympy import Mul, oo

  assert Mul(-1, -oo, evaluate=False).evalf() == oo
  ```

- [ ] Fix recursion in `evalf_log` for logarithms with a base under `evaluate(False)`.

  ```python
  from sympy import log
  from sympy.core.parameters import evaluate

  with evaluate(False):
      log(2, 3, evaluate=False).evalf(20)
  ```

- [ ] Fix `evalf_prod` handling of integer bounds under `evaluate(False)`.

  ```python
  from sympy import Product, symbols
  from sympy.core.parameters import evaluate

  n = symbols('n', integer=True)
  p = Product(n, (n, 1, 4))

  with evaluate(False):
      assert p.evalf() == 24
  ```
