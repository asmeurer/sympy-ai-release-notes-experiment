# Issues and pull requests referenced by this pull request

## Issue #23912: Modulo parenthesization

- Opened by @bjodah, state: closed

First off, I'm not sure if there's a universally agreed upon definition of what the modulo operator should return for complex numbers, python's built in operator raises a `TypeError`.

Regardless of that, the parenthesization currently looks dubious and should perhaps be fixed?
```python
>>> Mod(3+2j,4+5j)
(3.0 + 2.0⋅ⅈ) mod 4.0 + 5.0⋅ⅈ
```
