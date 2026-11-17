# Pull request #31003: cse function postprocess

- Author: @smichr
- Merged: 2026-11-12T01:33:11Z into `master`
- Labels: (none)
- Size: +147 / -6 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Inspired by discussion in [report](https://groups.google.com/g/sympy/c/FJt8rP8XTDM) on mailing list. Objects like Derivative, Integral, etc... that have variables targeting variables in the expression of the object can benefit from having cse symbols replaced with functions whose arguments match the free symbols of the pattern they represent. This would allow doit to be applied to the cse result without having such objects collapse because they appear to be independent of the variables (when the cse symbol is used).

#### Brief description of what is fixed or changed

```python
>>> cse(exp(a)+Derivative(x + exp(a), x), postprocess=cse_to_functions)
([(x0(a), exp(a))], [x0(a) + Derivative(x + x0(a), x)])
>>> cse(x*exp(a)+Derivative(x + x*exp(a), x), postprocess=cse_to_functions)
([(x0(a, x), x*exp(a))], [x0(a, x) + Derivative(x + x0(a, x), x)])
>>> _[1][0].doit()
x0(a, x) + Derivative(x0(a, x), x) + 1
```

#### Other comments

#### AI Generation Disclosure

This is a collaboration with ChatGPT.

## Commits

- f86ba5b94f (Christopher Smith): cse: add function-valued replacement postprocessor
- 94aefbc15b (Christopher Smith): test function postprocessor and dependency-aware replacement
- 76f53913f6 (Christopher Smith): Preserve differentiation variables in CSE function arguments
      Include freely occurring differentiation variables in variable_count order,
      updating them through earlier replacements. Test ArraySymbol derivatives
      and argument ordering with repeated differentiation variables.
      Generated with OpenAI Codex (GPT-6).
- 19f71c8b5c (Christopher Smith): Limit CSE function arguments to matching differentiation variables
      Treat other symbols as parameters and use zero-argument functions when
      no differentiation variables match. Test parameter exclusion and name
      collisions for zero-argument functions.
      Generated with OpenAI Codex (GPT-6).
- dab6049a04 (Christopher Smith): cse: do not extract symbol-like expressions
      Treat is_symbol objects consistently in CSE and preserve ArrayElement
      as the differentiation variable in function-valued CSE output.

## Conversation

### @ThePauliPrinciple commented

I tried this with an `Indexed` object and got the following:
```python
from sympy import cse, Derivative, Function, symbols
from sympy.simplify.cse_main import cse_to_functions
from sympy.abc import i
from sympy.tensor.array.expressions import ArraySymbol

X = ArraySymbol('X', (3,))
#x = symbols('x')
x = X[i]
f = Function('f')
cse(f(x)**2 + Derivative(f(x), x), postprocess=cse_to_functions)
```
```
([(x0(X, i), X[i]), (x1(X, i), f(x0(X, i)))],
 [x1(X, i)**2 + Derivative(x1(X, i), x0(X, i))])
```
I expected `x0(X[i])` rather than `x0(X, i)`.

### @smichr commented

@ThePauliPrinciple We need a better way to recognize free_symbol-like objects.

### @moorepants commented

This looks like a nice addition. It would be helpful if you need to take the derivative of the simplified expressions, e.g.:

```
In [1]: %paste
    >>> from sympy import cse, Derivative, Function, symbols
    >>> from sympy.simplify.cse_main import cse_to_functions
    >>> x = symbols('x')
    >>> f = Function('f')
    >>> cse(f(x)**2 + Derivative(f(x), x), postprocess=cse_to_functions)

## -- End pasted text --
Out[2]: ([(x0(x), f(x))], [x0(x)**2 + Derivative(x0(x), x)])

In [3]: _[1][0].diff(x)
Out[3]: 2*x0(x)*Derivative(x0(x), x) + Derivative(x0(x), (x, 2))

In [4]: expr = f(x)**2 + Derivative(f(x), x)

In [5]: cse(expr.diff(x))
Out[5]: ([(x0, f(x))], [2*x0*Derivative(x0, x) + Derivative(x0, (x, 2))])
```


## Reviews

### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @ThePauliPrinciple reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @ThePauliPrinciple reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr commented on `sympy/simplify/tests/test_cse.py`

notice that F0(x) not F0(x, y) and F1() not F1(y, z) -- we don't pollute function args with symbols that are constant wrt differentiation.

### @smichr commented on `sympy/simplify/tests/test_cse.py`

Although F1 doesn't hurt, it's not really necessary, is it? But full Derivatives can be differentiation variables, too, and I think I would prefer to see those pulled out, so I am not sure where to draw the line.

### @ThePauliPrinciple commented on `sympy/simplify/tests/test_cse.py`

You are right, it depends entirely on context. Maybe there can be some argument to `cse_to_functions`? In a way, I consider `X[i]` to be an "atom" eventhough in sympy it structurally is not. Maybe there is some way to define a list of "non-atom" differentiation variables?

I don't think `x0() = X[i]` is helpful here to me, since `d x1(x0()) dX[i] = 0 ` because `x0()` does not depend on `X[i]`.

Maybe it's just for the user to substitute their "non-atom" differentiation variables with `Symbol`s,  then running `cse_to_functions` and finally substituting them back.

### @smichr commented on `sympy/simplify/tests/test_cse.py`

I will modify cse to ignore anything for which is_symbol is true -- see #30917

### @smichr commented on `sympy/simplify/tests/test_cse.py`

OK, now line 358 shows the non-extracted "symbol" still acting as the Derivative variable.

### @ThePauliPrinciple commented on `sympy/simplify/tests/test_cse.py`

That seems reasonable.

Not really within the scope of this PR, but something to also consider

```python
from sympy import cse
from sympy.simplify.cse_main import cse_to_functions
from sympy.tensor.array.expressions import ArraySymbol

X = ArraySymbol('X', (3,))
A = ArraySymbol('A', (3,))
cse(X*(X+A)+ X+A, postprocess=cse_to_functions)
```
Since `X.is_symbol == False` this runs into the same issue.
Regardless, I don't think there is anything in `sympy` that is a symbol that maps a number of shaped symbols to an arbitrary shape.

### @smichr commented on `sympy/simplify/tests/test_cse.py`

It can be modified if there is a use case.
