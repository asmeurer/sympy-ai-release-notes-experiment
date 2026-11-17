# Issues and pull requests referenced by this pull request

## Issue #30913: Limit should define bound_symbols

- Opened by @smichr, state: closed

```python
>>> Limit(x + y, y, 1).bound_symbols
Traceback (most recent call last):
  File "<python-input-6>", line 1, in <module>
    Limit(x + y, y, 1).bound_symbols
AttributeError: 'Limit' object has no attribute 'bound_symbols'
```
It behaves like it knows what the bound symbols are, however:
```python
def test_limit_bound_symbols():
    L = Limit(x + y, x, 0)
    assert L.bound_symbols == (x,)
    assert L.free_symbols == {y}

    L = Limit(x + y, x, z)
    assert L.bound_symbols == (x,)
    assert L.free_symbols == {y, z}
```

Maybe just add the following for its property:

```python
@property
def bound_symbols(self):
    return (self.args[1],)
```

## Pull request #1234: Fix test failure in beginner/precision.py example

- Opened by @flacjacket, state: closed, merged 2012-04-14

Title says it all.
