# Issues and pull requests referenced by this pull request

## Issue #31069: `pow(i, 2, 5)` and `Integer(Fraction)` rejected by type checkers

- Opened by @hunterhogan, state: closed

(after the cacheit patch #31045 and after the Integer update #29422)

### `Integer.__pow__`
https://github.com/sympy/sympy/blob/e4797f44f5fe4af0566514227eb371131aaf8e48/sympy/core/numbers.py#L2056-L2061

### `Integer.__new__`
https://github.com/sympy/sympy/blob/e4797f44f5fe4af0566514227eb371131aaf8e48/sympy/core/numbers.py#L1834-L1835

```python
from fractions import Fraction
from sympy import Integer

i = Integer(3)

reveal_type(pow(i, 2, 5))
# Integer(4)

reveal_type(Integer(Fraction(7, 2)))
# Integer(3)
```

## But mypy 2.4.1 has errors, Py 3.10

```
error: Cannot infer value of type parameter "_M_contra" of "pow"  [misc]
note: Revealed type is "Any"
note: Revealed type is "sympy.core.numbers.Integer"
error: Argument 1 to "Integer" has incompatible type "Fraction"; expected "str | bytes | bytearray | SupportsInt | SupportsIndex"  [arg-type]
```

## pyright, too, Py 3.10

```
error: No overloads for "pow" match the provided arguments (reportCallIssue)
error: Argument of type "Literal[5]" cannot be assigned to parameter "mod" of type "None" in function "pow"
information: Type of "pow(i, 2, 5)" is "Unknown"
error: Argument of type "Fraction" cannot be assigned to parameter "i" of type "str | bytes | bytearray | SupportsInt | SupportsIndex" in function "__new__"
```

<details><summary>Explanation</summary>
<p>

> - `pow()`: typeshed's three-argument `pow` matches against the first `__pow__` overload, whose `mod` is `None`. Moving the `mod: Integer | int` overload first gives `Integer` in both checkers; `i ** 2`, `i ** 0` and `i ** S.Half` keep their types.
> - `Integer(Fraction)`: `Fraction.__int__` exists only from Python 3.11; on 3.10 `int(Fraction(7, 2))` works through `__trunc__`. `__new__` calls `int(i)`, so the parameter type is `_typeshed.ConvertibleToInt` (`str | Buffer | SupportsInt | SupportsIndex | SupportsTrunc`). That also removes the `SupportsIndex, SupportsInt` imports.

> With both changes: `mypy sympy` passes, pyright gives `Integer` for both lines on 3.10 and 3.14, and `test_numbers.py` and `test_power.py` pass.

</p>
</details> 

<details><summary>Potential fix</summary>
<p>

```diff
diff --git a/sympy/core/numbers.py b/sympy/core/numbers.py
index a28874f87b..c71b99f97f 100644
--- a/sympy/core/numbers.py
+++ b/sympy/core/numbers.py
@@ -1,6 +1,6 @@
 from __future__ import annotations
 
-from typing import overload, Literal, TYPE_CHECKING, SupportsIndex, SupportsInt
+from typing import overload, Literal, TYPE_CHECKING
 
 import numbers
 import decimal
@@ -72,6 +72,7 @@
 
 if TYPE_CHECKING:
     from typing import TypeAlias
+    from _typeshed import ConvertibleToInt
     from sympy.logic.boolalg import Boolean
     _NonNegativeInteger: TypeAlias = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
 
@@ -1832,7 +1833,7 @@ def _mpmath_(self, prec: int, rnd: str) -> _mpf:
         return _make_mpf(self._as_mpf_val(prec))
 
     @cacheit
-    def __new__(cls, i: str | bytes | bytearray | SupportsInt | SupportsIndex) -> Integer:
+    def __new__(cls, i: ConvertibleToInt) -> Integer:
         if isinstance(i, str):
             i = i.replace(' ', '')
         # whereas we cannot, in general, make a Rational from an
@@ -2053,12 +2054,12 @@ def __rmod__(self, other: Expr | complex) -> Expr:
             return Rational.__rmod__(self, other)
         return Rational.__rmod__(self, other)
 
+    @overload
+    def __pow__(self, other: Integer | int, mod: Integer | int) -> Integer: ...
     @overload
     def __pow__(self, other: _NonNegativeInteger, mod: None = None) -> Integer: ...
     @overload
     def __pow__(self, other: Expr | complex, mod: None = None) -> Expr: ...
-    @overload
-    def __pow__(self, other: Integer | int, mod: Integer | int) -> Integer: ...
 
     def __pow__(self, other: Expr | complex, mod: Integer | int | None = None) -> Expr:
         if mod is not None:
```

</p>
</details> 

I'm skeptical of the typeshed import. It just adds `SupportsTrunc`, which is a typeshed protocol.

```python
class SupportsTrunc(Protocol):
    def __trunc__(self) -> int: ...
```
