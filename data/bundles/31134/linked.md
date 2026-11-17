# Issues and pull requests referenced by this pull request

## Issue #31017: Solvers, integrals, assumptions, polys, series: 30 verified defects found while building a downstream package (wrong results, exceptions, two regressions)

- Opened by @Upabjojr, state: open

> **AI disclosure.** This issue text and the underlying checks were produced by an AI agent (Claude Code, model Claude Fable 5.2) at the request of the account owner. The defects were met while building a downstream package on SymPy 1.14.0 (list kept in Upabjojr/sympy-extras#25); each one was then re-run by a separate, skeptical pass on master `1eb7878357` (2026-11-09) and on 1.14.0, the expected values were re-derived independently (quadrature, substitution into the equation), and sympy/sympy was searched for existing reports. Items of the original list that turned out to be fixed, already reported, or not defects are left out (see the end). Searches may have missed a duplicate.

One umbrella issue so the items can be triaged together; any of them can be split out. Every snippet starts from `from sympy import *` and states its symbols; outputs are from master. Unless marked *regression*, 1.14.0 behaves the same.

## 1. Wrong results

**W1. `rsolve` returns `0` for first-order hypergeometric recurrences, ignoring the initial condition**
```python
>>> n = Symbol('n', integer=True); y = Function('y')
>>> rsolve((n + 1)**2*y(n + 1) - y(n), y(n), {y(0): 1})        # 1/factorial(n)**2
0
>>> rsolve(y(n + 1) - (n + 1)*(n + 2)*y(n), y(n), {y(0): 1})   # factorial(n)*factorial(n + 1)
0
>>> rsolve((n + 1)*y(n + 1) - y(n), y(n), {y(0): 1})
1/factorial(n)
```
Cause: `rsolve_hyper` (`solvers/recurr.py:592-602`) takes `roots(p, n).keys()`, dropping multiplicities, and tries only single linear factors as `A`, `B`; Petkovšek's algorithm needs all monic divisors. Related: #27902 (also `0`, for higher order, attributed to a different cause).

**W2. `dsolve(..., hint='2nd_power_series_ordinary')` returns a wrong series with a leaked internal function `r(3)`**
```python
>>> x = Symbol('x'); f = Function('f')
>>> eq = (x**2 + 1)*f(x).diff(x, 2) + x*f(x).diff(x) + (x**3 + 2)*f(x)
>>> dsolve(eq, f(x), hint='2nd_power_series_ordinary')
Eq(f(x), -11*x**5*r(3)/20 + C2*(-x**5/20 - x**2 + 1) + C1*x*(1 - x**5/30) + O(x**6))
```
Substituting a polynomial ansatz gives `C2*(1 - x**2 + x**4/2 - x**5/20) + C1*(x - x**3/2 + 11*x**5/40) + O(x**6)`: the `x**4/2` and `-x**3/2` terms are missing. For `f'' + f'/(x + 2) + q*f` with `q = (3*x**3 + 16*x**2 + 28*x + 17)/((x + 1)**2*(x + 2)**2)` the default `dsolve` returns `Eq(f(x), O(1))`, and the explicit hint with `n=4` gives an `x**2` coefficient of `-497/64` instead of `-17/8`. Location: `ode_2nd_power_series_ordinary` in `solvers/ode/ode.py`. Closed #22525 showed the same `r(...)` symptom for Floats.

**W3. `dsolve` returns `y = C1*x` for a homogeneous first-order equation**
```python
>>> x = Symbol('x'); y = Function('y')
>>> eq = y(x).diff(x) - (2*x**3*y(x) - y(x)**4)/(x**4 - 2*x*y(x)**3)
>>> sol = dsolve(eq, y(x)); sol
Eq(y(x), C1*x)
>>> checkodesol(eq, sol, y(x))
(False, C1**4 + C1)
```
The general solution is `x**3 + y**3 = C*x*y`; `C1*x` is a solution only for `C1 = 0, -1`. The `factorable` and both `1st_homogeneous_coeff` hints return it.

**W4. `integrate(y**x, (x, 0, 2))` returns `2` for every `y <= 0`**
```python
>>> x, y = symbols('x y')
>>> r = integrate(y**x, (x, 0, 2)); r
Piecewise((y**2/log(y) - 1/log(y), (y > 0) & Ne(y, 1)), (2, True))
>>> r.subs(y, -2), N(((y**2 - 1)/log(y)).subs(y, -2))     # quadrature agrees with the second
(2, 0.200911111726264 - 0.910601514838311*I)
```
The antiderivative carries `Ne(log(y), 0)`; `Piecewise._handle_irel` (`functions/elementary/piecewise.py`) solves this x-independent condition over the reals and narrows it to `(y > 0) & Ne(y, 1)`, so the value at `y = 1` is used for all other `y`.

**W5. Definite integrals evaluated across a branch cut or a jump of the antiderivative**
```python
>>> z = Symbol('z')
>>> integrate(log(z)/z**2, (z, -I, -1))               # quadrature: 1 + pi/2 + I - I*pi
1 + pi/2 + I + I*pi
>>> N(integrate(csc(z), (z, 1 - I, 1 + I)))           # quadrature: +1.89879495*I
0.e-21 - 1.24279769984425*I
>>> integrate(acoth(z), (z, 0, 1)), N(acoth(S.Half))  # with SymPy's own acoth: log(2) - I*pi/2
(log(2) + I*pi/2, 0.549306144334055 - 1.5707963267949*I)
>>> integrate((z**(I/2))**I, (z, 0, 1)), integrate(log(z**I)**2, (z, 0, 1))   # quadrature: 1.91373, -1.45594
(2, -2)
```
The first three are off by `2*I*pi`, `I*pi`, `I*pi`. In the last two the antiderivatives (`2*z*(z**(I/2))**I`; `log(z**I)` replaced by `I*log(z)`) are valid only piecewise in `z`, with jumps at `z = exp(-(2*k + 1)*2*pi)` resp. for `z < exp(-pi)`.

**W6. `expint(2, x).series(x)` has a spurious `-I*pi*x`**
```python
>>> x = Symbol('x')
>>> s = expint(2, x).series(x, 0, 3); s
1 + x*(log(x) - 1 + EulerGamma - I*pi) - x**2/2 + O(x**3)
>>> s.removeO().subs(x, S(1)/10).n(), expint(2, S(1)/10).n()
(0.722463057190749 - 0.314159265358979*I, 0.722545022194021)
```
Cause: `Ei._eval_rewrite_as_Si` (`functions/special/error_functions.py:1232`) subtracts `I*pi` when `z.is_negative`; inside `series` the argument is `xp*exp_polar(I*pi)` with a positive dummy, which `is_negative`, although `Chi` of it has already produced the `I*pi`. `expint(3, x)` is affected in the `x**2` coefficient, and `Ei(xp*exp_polar(I*pi)).rewrite(Si)` loses `I*pi` for positive `xp`.

**W7. `limit(log(n**a + n**b)/log(n), n, oo)` returns `b`**
```python
>>> n, a, b = symbols('n a b', positive=True)
>>> L = limit(log(n**a + n**b)/log(n), n, oo); L
b
>>> L.subs({a: 3, b: 2}), limit(log(n**3 + n**2)/log(n), n, oo)
(2, 3)
```
Expected `Max(a, b)` or the `NotImplementedError: Result depends on the sign of sign(a - b)` that `limit((n**a + n**b)/n**b, n, oo)` raises. Same family as #22893, #8241.

**W8. `solveset` over the reals returns a point where the equation does not hold**
```python
>>> x = Symbol('x'); eq = log(x) + log(x - 1) - log(2)
>>> solveset(eq, x, S.Reals), eq.subs(x, -1)
({-1, 2}, 2*I*pi)
```
Same family as #16648 (`sqrt`).

**W9. `nonlinsolve` leaves an unknown free and `solve_poly_system`/`solve` return `[]` for a system with ten solutions**
```python
>>> x, y = symbols('x y
