# Issues and pull requests referenced by this pull request

## Issue #18788: Incorrect parenthesizing of fractions

- Opened by @kom-bu, state: closed

One of the test cases of test_str.py is as follows:
```
assert str(Mul(-2, x, Pow(Mul(y,y,evaluate=False), -1, evaluate=False),
                                                evaluate=False)) == '-2*x/(y*y)'
```
The current master branch passes this test. However, it fails to behave correctly in the following case.
```
>>> x, y = symbols('x y')
>>> expr = Mul(2, Pow(x*y, -1, evaluate=False), evaluate=False)
>>> str(expr)
'2/((x*y))'
```
In the former case the expression was printed correctly just because the precedence of the whole expression was reduced by the following rule in printing/precedence.py:
```
63 def precedence_Mul(item):
64     if _coeff_isneg(item):
65         return PRECEDENCE["Add"]
66     return PRECEDENCE["Mul"]
```
This rule may be revised for #17737. So this bug should be fixed in advance, or the correction of #17737 will fail in the automatic test.
