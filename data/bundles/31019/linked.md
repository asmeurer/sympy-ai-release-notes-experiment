# Issues and pull requests referenced by this pull request

## Issue #10697: subs is too slow for large mappings

- Opened by @asmeurer, state: open

If you have a large mapping, subs iterates over each term in the mapping, even if `simultaneous=True`. Contrast this with `xreplace`, which does the substitution all at once.

```
In [18]: a = (x + 1)**2 + 1

In [19]: mapping = {Symbol('x%d' % i): i for i in range(10000)}

In [20]: %timeit a.subs(mapping)
1 loop, best of 3: 4.93 s per loop

In [21]: %timeit a.subs(mapping, simultaneous=True)
1 loop, best of 3: 8.04 s per loop

In [22]: %timeit a.xreplace(mapping)
100000 loops, best of 3: 11.5 µs per loop
```

`subs` should only traverse an expression once when `simultaneous=True` (side note: I agree with the `XXX` comment in the code, simultaneous=True should be the default for dictionaries, maybe even the default always, but that's another issue). Even when simultaneous=False, it may be faster to recursively apply subs recursively to the mapping (in reverse), remove duplicates, and then apply the mapping all at once to the expression. We'd have to test it, but I suspect it would be faster, since in the common case the expression will be large and the terms in the mapping will be small.

## Issue #22240: subs is slow

- Opened by @nguyenthanhvuh, state: open

Hi, it seems that the `.subs` function is quite slow. When I have a long expression `e` (can contain nonlinear terms like `x**2, y*x*z`), calling `e.subs(some_dict)` takes some noticeable time (two sec's or so). In fact `subs` is often slower than solving  large equations. Is there something obvious that I miss ?  My main goal is to just substitute variables in the expression with concrete values,   e.g.,  `x*y.subs({x:3}) = 3*y`
