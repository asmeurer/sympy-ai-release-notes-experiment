# Pull request #31090: raise TypeError for non-Number Expr initial guess in nsolve

- Author: @zorgonk
- Merged: 2026-11-15T19:03:48Z into `master`
- Labels: (none)
- Size: +19 / -0 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs
Closes #31039 

#### Brief description of what is fixed or changed
`nsolve` now raises a `TypeError` that the initial guess should be a Number or Python number when an unevaluated SymPy `Expr` (like `pi` or `E`) is passed as an initial guess instead of crashing with `TypeError: cannot create mpf from pi`

- Validates elements of `x0` to reject instances of `Expr` that are not `Number`
- Iterates through all values of `x0` when iterable to make sure every guess gets checked -in case of multivariate systems or other 1D  bracketed stuff

#### Other comments

- Allowed `S.ImaginaryUnit` (`I`), since `mpmath` handles it natively and existing tests rely on it.
- Added regression tests in `sympy/solvers/tests/test_numeric.py`.

#### AI Generation Disclosure

Constantly used Gemini 4 (Hydrogen) to assist with the style of writing the code

## Commits

- af3025ddb9 (Anandhu Sathyan): raise TypeError for non-Number Expr initial guess in nsolve
- 3409094aad (Anandhu Sathyan): Update sympy/solvers/solvers.py
      Co-authored-by: Christopher Smith <smichr@gmail.com>
- 05b6b4f76f (Anandhu Sathyan): Update sympy/solvers/tests/test_numeric.py
      Co-authored-by: Christopher Smith <smichr@gmail.com>
- 7b54c2a760 (Anandhu Sathyan): Update sympy/solvers/solvers.py
      Co-authored-by: Christopher Smith <smichr@gmail.com>

## Conversation

### @zorgonk commented

Thank you so much for reviewing the code and making those changes, @smichr. That was a silly oversight on my part.


## Reviews

### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr commented on `sympy/solvers/solvers.py`

```suggestion
from sympy.core.evalf import pure_complex
from sympy.core.numbers import Float, Rational, _illegal
```

### @smichr commented on `sympy/solvers/tests/test_numeric.py`

```suggestion
    assert abs(nsolve(sin(x), x, pi.n(2)) - pi) < 1e-15
    assert nsolve(x - 1 + I, x, 1 - I/2) == 1.0 - 1.0*I
    assert nsolve(x - 1 + I, x, '42') == 1.0 - 1.0*I
    assert nsolve(x - 1 + I, x, 42) == 1.0 - 1.0*I
```

### @smichr commented on `sympy/solvers/solvers.py`

```suggestion
    for i in (x0 if isinstance(x0, list) else [x0]):
        if isinstance(i, Expr) and pure_complex(i, or_real=True) is None:
            raise TypeError(
                "You must evaluate numeric initial guesses; "
                "e.g. use pi.n() instead of pi"
            )
```
