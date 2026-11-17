# Issues and pull requests referenced by this pull request

## Issue #31030: Interval(a, b).measure is wrong if b < a

- Opened by @asmeurer, state: closed

```
>>> Interval(a, b).measure
-a + b
```

This is wrong if `b < a`, because the interval would be empty. The more correct expression would be `Piecewise((b - a, b >= a), (0, True))`.
