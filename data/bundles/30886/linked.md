# Issues and pull requests referenced by this pull request

## Issue #26504: IndexError: Index out of range:   calling integrate in sympy 1.12

- Opened by @nasser1, state: open

I do not know if this is known or reported before. Feel free to close if so.

I see some exceptions TypeError: Invalid NaN comparison. Here is just one example 

```
from sympy import *
x=symbols('x')
integrand="2**(2+3*x)*3**(5+7*x)"
integrate( sympify(integrand), x)

```
gives

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.11/site-packages/sympy/integrals/integrals.py", line 1567, in integrate
    return integral.doit(**doit_flags)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/site-packages/sympy/integrals/integrals.py", line 612, in doit
    antideriv = self._eval_integral(
                ^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/site-packages/sympy/integrals/integrals.py", line 1084, in _eval_integral
    h = heurisch_wrapper(g, x, hints=[])
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/site-packages/sympy/integrals/heurisch.py", line 158, in heurisch_wrapper
    slns += solve([d], dict=True, exclude=(x,))
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/site-packages/sympy/solvers/solvers.py", line 1147, in solve
    linear, solution = _solve_system(f, symbols, **flags)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/site-packages/sympy/solvers/solvers.py", line 1815, in _solve_system
    matrix[i, j] = coeff
    ~~~~~~^^^^^^
  File "/usr/lib/python3.11/site-packages/sympy/matrices/repmatrix.py", line 400, in __setitem__
    rv = self._setitem(key, value)
         ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/site-packages/sympy/matrices/matrices.py", line 1157, in _setitem
    i, j = key = self.key2ij(key)
                 ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/site-packages/sympy/matrices/matrices.py", line 1810, in key2ij
    return [a2idx(i, n) if not isinstance(i, slice) else i
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/site-packages/sympy/matrices/matrices.py", line 1810, in <listcomp>
    return [a2idx(i, n) if not isinstance(i, slice) else i
            ^^^^^^^^^^^
  File "/usr/lib/python3.11/site-packages/sympy/matrices/common.py", line 3189, in a2idx
    raise IndexError("Index out of range: a[%s]" % (j,))
IndexError: Index out of range: a[1]
>>> 

```

Version info

```
>>> import sympy
>>> sympy.__version__
'1.12'

>python --version
Python 3.11.8
>

```

For reference the result should be

```
Integrate[2^(2+3*x)*3^(5+7*x),x]

   (2^(2+3 x) 3^(5+7 x))/Log[17496]

```
