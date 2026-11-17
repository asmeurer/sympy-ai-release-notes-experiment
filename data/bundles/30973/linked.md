# Issues and pull requests referenced by this pull request

## Issue #30970: array_derive with OneArray and ArrayTensorProduct fails

- Opened by @ThePauliPrinciple, state: closed

Currently, for a `OneArray` O, derived by an `ArraySymbol` X, sympy yields a `ZeroArray` Z with `Z.shape == X.shape` rather than `Z.shape == O.shape + X.shape`.

The derivative handling of `ArrayTensorProduct` expects `O.shape + X.shape` and thus generates an incorrect permutation:

```python
>>> from sympy.tensor.array.expressions import ArraySymbol, array_derive, OneArray, ArrayTensorProduct
>>> X = ArraySymbol("X", (1,1))
>>> O = OneArray(1)
>>> Z = array_derive(O, X)
>>> print(f'{O.shape=}')
>>> print(f'{X.shape=}')
>>> print(f'{Z.shape=}')
>>> array_derive(ArrayTensorProduct(O, X), X)
O.shape=(1,)
X.shape=(1, 1)
Z.shape=(1, 1)
---------------------------------------------------------------------------

ValueError                                Traceback (most recent call last)

[/tmp/ipykernel_21787/2624025206.py](https://localhost:8080/#) in <cell line: 0>()
      6 print(f'{X.shape=}')
      7 print(f'{Z.shape=}')
----> 8 array_derive(ArrayTensorProduct(O, X), X)

3 frames

[/usr/lib/python3.13/functools.py](https://localhost:8080/#) in wrapper(*args, **kw)
    932             raise TypeError(f'{funcname} requires at least '
    933                             '1 positional argument')
--> 934         return dispatch(args[0].__class__)(*args, **kw)
    935 
    936     funcname = getattr(func, '__name__', 'singledispatch function')

[/usr/local/lib/python3.13/dist-packages/sympy/tensor/array/expressions/arrayexpr_derivatives.py](https://localhost:8080/#) in _(expr, x)
     60                list(range(tot3, tot4))
     61         print(perm)
---> 62         addend = _permute_dims(addend, _af_invert(perm))
     63         addend_list.append(addend)
     64     if len(addend_list) == 1:

[/usr/local/lib/python3.13/dist-packages/sympy/tensor/array/expressions/array_expressions.py](https://localhost:8080/#) in _permute_dims(expr, permutation, **kwargs)
   1959 
   1960 def _permute_dims(expr, permutation, **kwargs):
-> 1961     return PermuteDims(expr, permutation, canonicalize=True, **kwargs)
   1962 
   1963 

[/usr/local/lib/python3.13/dist-packages/sympy/tensor/array/expressions/array_expressions.py](https://localhost:8080/#) in __new__(cls, expr, permutation, index_order_old, index_order_new, **kwargs)
    461         permutation_size = permutation.size
    462         if permutation_size != expr_rank:
--> 463             raise ValueError("Permutation size must be the length of the shape of expr")
    464 
    465         canonicalize = kwargs.pop("canonicalize", False)

ValueError: Permutation size must be the length of the shape of expr
```
