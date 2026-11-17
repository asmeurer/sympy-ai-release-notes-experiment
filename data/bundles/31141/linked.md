# Issues and pull requests referenced by this pull request

## Issue #31086: Should finite `Ordinal`s evaluate as equal to `int`s and `Integer`s?

- Opened by @MajesticSlacks, state: open

This has come up a few times now, most recently in https://github.com/sympy/sympy/pull/29733#discussion_r3178471780.
```
>>> from sympy import *
>>> from sympy.sets.ordinals import *
>>> S.Zero == ord0
False
>>> 0 == ord0
True
>>> S.Zero == 0
True
>>> sin(ord0)
AttributeError: 'OrdinalZero' object has no attribute 'as_coefficient'
>>> sin(0)
0
>>> sin(S.Zero)
0
>>> 
```
In the sense of SymPy, it seems to me that finite ordinals and `int`s could be considered unequal, in that they don't support the same operations.
