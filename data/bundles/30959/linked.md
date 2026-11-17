# Issues and pull requests referenced by this pull request

## Issue #19324: Symbol.copy() raises weird TypeError

- Opened by @eric-wieser, state: closed

From https://gitter.im/sympy/sympy?at=5ebd78a149cc4a3b62e7a69f (ping @asmeurer):

```python
In [155]: s = Symbol('s')

In [156]: s.copy()
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-156-6e1d2ee6d3ad> in <module>
----> 1 s.copy()

c:\users\wiese\repos\ga\sympy\sympy\core\basic.py in copy(self)
    115
    116     def copy(self):
--> 117         return self.func(*self.args)
    118
    119     def __reduce_ex__(self, proto):

TypeError: __new__() missing 1 required positional argument: 'name'
```

This should probably either:
* Actually make a copy (perhaps by setting `self.func = functools.partial(Symbol, name=self.name)`
* Return `self`
* Raise a clearer error message
