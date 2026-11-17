# Issues and pull requests referenced by this pull request

## Issue #27439: error in scalar multiplication of vectors

- Opened by @unybhgfd, state: closed

There is an endless loop when doing scalar multiplication of vectors
```
import sympy
from sympy.vector import Vector
print(1*Vector(*sympy.symbols('a b c')))
```
numpy:           2.2.1 
python:          3.11.11 
mpmath:          1.3.0
The following is the error message:
```
D:\ANACONDA\anaconda3\envs\brilliant_models\python.exe D:\pythonProject\pythonProject\brilliant_models\ray_caster\__main__.py 
Traceback (most recent call last):
  File "D:\pythonProject\pythonProject\brilliant_models\ray_caster\__main__.py", line 3, in <module>
    print(1*Vector(*sympy.symbols('a b c')))
          ~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\decorators.py", line 65, in __sympifyit_wrapper
    return func(a, b)
           ^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\decorators.py", line 106, in binary_op_wrapper
    return func(self, other)
           ^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\vector\basisdependent.py", line 51, in __rmul__
    return self._mul_func(other, self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\vector\vector.py", line 433, in __new__
    obj = BasisDependentMul.__new__(cls, *args, **options)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\vector\basisdependent.py", line 264, in __new__
    measure_number *= arg
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\numbers.py", line 1904, in __mul__
    return Rational.__mul__(self, other)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\decorators.py", line 65, in __sympifyit_wrapper
    return func(a, b)
           ^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\numbers.py", line 1468, in __mul__
    return Number.__mul__(self, other)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\decorators.py", line 65, in __sympifyit_wrapper
    return func(a, b)
           ^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\numbers.py", line 485, in __mul__
    return AtomicExpr.__mul__(self, other)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\decorators.py", line 236, in _func
    return func(self, other)
           ^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\decorators.py", line 105, in binary_op_wrapper
    return f(self)
           ^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\decorators.py", line 65, in __sympifyit_wrapper
    return func(a, b)
           ^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\decorators.py", line 106, in binary_op_wrapper
    return func(self, other)
           ^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\vector\basisdependent.py", line 51, in __rmul__
    return self._mul_func(other, self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\vector\vector.py", line 433, in __new__
    obj = BasisDependentMul.__new__(cls, *args, **options)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\vector\basisdependent.py", line 264, in __new__
    measure_number *= arg

  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\numbers.py", line 1904, in __mul__
    return Rational.__mul__(self, other)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\decorators.py", line 65, in __sympifyit_wrapper
    return func(a, b)
           ^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\numbers.py", line 1468, in __mul__
    return Number.__mul__(self, other)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\decorators.py", line 65, in __sympifyit_wrapper
    return func(a, b)
           ^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\numbers.py", line 485, in __mul__
    return AtomicExpr.__mul__(self, other)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\decorators.py", line 236, in _func
    return func(self, other)
           ^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\decorators.py", line 105, in binary_op_wrapper
    return f(self)
           ^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\decorators.py", line 65, in __sympifyit_wrapper
    return func(a, b)
           ^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\core\decorators.py", line 106, in binary_op_wrapper
    return func(self, other)
           ^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\vector\basisdependent.py", line 51, in __rmul__
    return self._mul_func(other, self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\vector\vector.py", line 433, in __new__
    obj = BasisDependentMul.__new__(cls, *args, **options)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\ANACONDA\anaconda3\envs\brilliant_models\Lib\site-packages\sympy\vector\basisdependent.py", line 264, in __new__

## Pull request #27488: Fix infinite recursion error when vectors are defined incorrectly

- Opened by @RushabhMehta2005, state: closed

#### References to other Issues or PRs  
Fixes #27439  

#### Brief description of what is fixed or changed  
This PR addresses a bug where incorrectly defining a `Vector` caused an infinite recursion error.  
The correct way to define a vector is documented in the [[SymPy documentation](https://docs.sympy.org/latest/modules/vector/basics.html#coordinate-systems-and-vectors)](https://docs.sympy.org/latest/modules/vector/basics.html#coordinate-systems-and-vectors), as highlighted by @oscarbenjamin in [[this comment](https://github.com/sympy/sympy/issues/27439#issuecomment-2571602853)](https://github.com/sympy/sympy/issues/27439#issuecomment-2571602853).  

A regression test has been added to ensure this issue does not reoccur.  

#### Other comments  
Feedback and constructive criticism are highly appreciated! I am currently learning about SymPy and its codebase by tackling issues I can contribute to.
