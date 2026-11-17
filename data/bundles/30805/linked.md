# Issues and pull requests referenced by this pull request

## Pull request #1234: Fix test failure in beginner/precision.py example

- Opened by @flacjacket, state: closed, merged 2012-04-14

Title says it all.

## Issue #2521: PurePoly error

- Opened by @taylansengul, state: open

Why is there a difference between these two cases?
The following code works

```
In [3]: a,x = symbols('a x')

In [4]: p = PurePoly(x ** 2 - 4 * a, x, domain='ZZ(a)')
```

but this does not:

```
In [2]: beta, x = symbols('beta x')

In [3]: p = PurePoly(x ** 2 - 4 * beta, x, domain='ZZ(beta)')
```
