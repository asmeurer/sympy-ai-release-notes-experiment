# Issues and pull requests referenced by this pull request

## Issue #21616: Adding oo to SetExpr of Interval gives nested FiniteSet

- Opened by @smichr, state: closed

```python
>>> SetExpr(Interval(2, oo)) + oo
SetExpr(FiniteSet(FiniteSet(oo)))
```
I think that should be `SetExpr(FiniteSet(oo))`
