# Pull request #31087: Fix Subs symbol handling for derivatives with composite arguments

- Author: @Cypher-Monarch
- Merged: 2026-11-15T06:54:00Z into `master`
- Labels: (none)
- Size: +63 / -5 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #29714

#### Brief description of what is fixed or changed

Differentiating an undefined function with multiple composite arguments could introduce unintended symbols into `free_symbols`.

For example:

```python
x, y = symbols('x y')
f = Function('f')
result = f(x + y, x*y).diff(y).diff(x)
```

Previously, the result could contain an unintended symbol such as `_x + y` instead of only the expected `x` and `y`.

The issue was traced to collision detection in `Subs.__new__()` and structural identity handling in `Subs._hashable_content()`.

Two changes were made:

- `Subs.__new__()`: Updated the collision check to handle free symbols that are not among the substitution variables, while reusing the existing `s_pts` mapping.
- `Subs._hashable_content()`: Added the number of substitution variables and sorted substitution points to distinguish `Subs` objects after canonicalization.

A dedicated regression test, `test_Subs_composite_arguments_derivative`, was added to `sympy/core/tests/test_functions.py`. It checks the original reproducer and additional cases involving different differentiation orders, powers and constants, repeated composite arguments, overlapping free symbols, nested expressions, and repeated differentiation.

#### Other comments

`./bin/test test_function`: 145 passed, 1 xfailed.

`./bin/test`: 13366 passed, 749 skipped, 261 deselected, 328 xfailed, 1 xpassed.

The original issue was reproduced on the unmodified branch and verified as fixed after the changes.

#### AI Generation Disclosure

An AI coding assistant was used during the investigation to help triangulate the source of the issue and suggest possible approaches to fixing it.

The AI assistant's involvement was limited to investigation and proposing potential solutions. The implementation and regression tests were developed independently.

## Commits

- 9a2fb5de43 (Cypher-Monarch): tests: add regression test for Subs with composite arguments
- 17d2570474 (Cypher-Monarch): fix(core): correct Subs symbol handling and hashing
- c540bd08be (Cypher-Monarch): test(core): expand Subs derivative regression coverage
- 07b94eb898 (Cypher-Monarch): fix(functions): fix inconsistent indentation in _hashable_content
- e72b2dad88 (Cypher-Monarch): perf: remove redundant frozenset return in _hashable_content
- 187acb9fb1 (Cypher-Monarch): chore(mailmap): add Cypher-Monarch to mailmap
- 6fc6b67da9 (Cypher-Monarch): chore: fix code formatting with ruff
- 7084315eb0 (Cypher-Monarch): tests: add coverage for doit collision case

## Conversation

### @smichr commented

Welcome to SymPy! This is in.


## Reviews

### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr commented on `sympy/core/function.py`

I am not sure this change is necessary. The hash collision was allowing an already hashed Subs to replace the correct one and once that is corrected as you have done below, you should not see the extraneous symbol. This test formerly contained such a symbol and now it doesn't:
```python
>>> f=Function('f')
>>> Subs(Derivative(f(z, x*y), z), z, x + y).diff(x)
y*Subs(Derivative(f(z, _xi_2), _xi_2, z), (_xi_2, z), (x*y, x + y)) + Subs(Derivative(f(z, x*y), (z, 2)), z, x + y)
>>> _.atoms()
{1, y, 2, z, x, _xi_2}
```

### @smichr commented on `sympy/core/tests/test_function.py`

All these tests pass with only the change to hashing.

### @smichr commented on `sympy/core/tests/test_function.py`

Ahh....but if you add this I suspect it will pass for your full PR
```python
>>> x = Symbol('x')
... u = Symbol('_0')
...
... a = Subs(x + u, x, 0)
... b = Subs(2*x, x, 0)
...
>>> a,b
(Subs(_0 + x, x, 0), Subs(2*x, x, 0))
>>> a==b
True  <--- I suspect you will get False (as it should be) since a.doit() != b.doit()
```

### @smichr commented on `sympy/core/tests/test_function.py`

```suggestion
    assert Subs(x + Symbol('_0'), x, 0) != Subs(2*x, x, 0)
    assert Subs(f(x), x, 0) == Subs(f(y), y, 0)
```
