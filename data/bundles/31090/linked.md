# Issues and pull requests referenced by this pull request

## Issue #31039: `nsolve(sin(x), x, pi)`

- Opened by @11350613, state: closed

sympy commit hash: de06b948bd78245559aa355081c1b85feec67f03 (current master)

---

```python
In [1]: nsolve(sin(x), x, pi)
TypeError                                 Traceback (most recent call last)
Cell In[1], line 1
----> 1 nsolve(sin(x), x, pi)

File ~/sympy-dev/sympy/sympy/external/mpmath.py:223, in conserve_mpmath_dps.<locals>.func_wrapper(*args, **kwargs)
221 dps = mpmath.mp.dps
222 try:
--> 223     return func(*args, **kwargs)
224 finally:
225     mpmath.mp.dps = dps

File ~/sympy-dev/sympy/sympy/solvers/solvers.py:3135, in nsolve(dict, *args, **kwargs)
3129 # the function is much better behaved if there is no denominator
3130 # but sending the numerator is left to the user since sometimes
3131 # the function is better behaved when the denominator is present
3132 # e.g., issue 11768
3134 f = lambdify(fargs, f, modules)
-> 3135 x = sympify(findroot(f, x0, **kwargs))
3136 if as_dict:
3137     return [{fargs: x}]

File ~/sympy-dev/sympy/venv/lib/python3.12/site-packages/mpmath/calculus/optimization.py:923, in findroot(ctx, f, x0, solver, tol, verbose, verify, **kwargs)
921     x0 = [ctx.convert(x) for x in x0]
922 else:
--> 923     x0 = [ctx.convert(x0)]
925 if isinstance(solver, str):
926     try:

File ~/sympy-dev/sympy/venv/lib/python3.12/site-packages/mpmath/ctx_mp_python.py:866, in PythonMPContext.convert(ctx, x, strings)
864 if type(x).module == 'decimal':
865     return ctx.make_mpf(from_Decimal(x, prec, rounding))
--> 866 return ctx._convert_fallback(x, strings)

File ~/sympy-dev/sympy/venv/lib/python3.12/site-packages/mpmath/ctx_mp.py:605, in MPContext._convert_fallback(ctx, x, strings)
603     else:
604         raise ValueError("can only create mpf from zero-width interval")
--> 605 raise TypeError("cannot create mpf from " + repr(x))

TypeError: cannot create mpf from pi
```

---

~Expected result = 3.14159265358979~

Update: see https://github.com/sympy/sympy/issues/31039#issuecomment-6862665609
