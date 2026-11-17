# Issues and pull requests referenced by this pull request

## Issue #21618: function(SetExpr(...)) could be handled better

- Opened by @smichr, state: closed

from #14251, when SetExpr is the argument of a function it is handled less gracefully than when the argument is AccumBounds:
```python
>>> cos(AccumBounds(-1, 2))
AccumBounds(cos(2), 1)
>>> cos(SetExpr(Interval(-1, 2)))
SetExpr(ImageSet(Lambda(x, cos(x)), Interval(-1, 2)))
>>> var('a b', real=True)
>>> sin(AccumBounds(a, b))
TypeError: input failed to evaluate
>>> sin(SetExpr(Interval(a, b)))
SetExpr(ImageSet(Lambda(x, sin(x)), Interval(a, b)))
```

## Issue #29675: `imageset` on `tan(x)`  takes  long time

- Opened by @JosephMehdiyev, state: closed

This will try to evaluate for a long time (possibly infinite)
```Python
x = Symbol("x", real=True)
imageset(x,tan(x),  S.Reals)
```
seems like `imageset` tries to calculate every singularity individually?
`imageset(x,tan(x), Interval(-100,100))` lists every singularity individually. Am I using `imageset` wrong?
Similar thing happens with `cot(x)`. I would expect a proper answer from this, but at least there should be some safehandling to avoid infinite calculations like this

There is a `TODO` comment on `sympy/sets/handlers/functions.py` about this

## Pull request #29682: Fix ImageSet hanging on infinite singularities

- Opened by @SarvaarthN, state: closed

Fix infinite loop in ImageSet._set_function when singularities are infinite

#### References to other Issues or PRs
Fixes #29675

#### Brief description of what is fixed or changed
If singularities() returns an infinite or non-FiniteSet result, then return None early instead of trying to iterate over it.

#### Other comments

#### AI Generation Disclosure
