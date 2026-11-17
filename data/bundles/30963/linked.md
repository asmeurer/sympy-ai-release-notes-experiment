# Issues and pull requests referenced by this pull request

## Issue #22326: Incorrect call of evalf from _eval_evalf in codegen

- Opened by @oscargus, state: closed

`evalf` has a first argument of correct number of decimal digits, `_eval_evalf` instead has number of binary digits. Parts of this is solved in #22325 but there are some cases in `codegen` that was not straightforward for me to solve keeping the `*arg, *kwargs` approach. @bjodah 

https://github.com/sympy/sympy/blob/cb8a2971d67154f8ea7c0ac9f69181bcceea8eae/sympy/codegen/cfunctions.py#L272-L273

https://github.com/sympy/sympy/blob/cb8a2971d67154f8ea7c0ac9f69181bcceea8eae/sympy/codegen/numpy_nodes.py#L59-L60

https://github.com/sympy/sympy/blob/cb8a2971d67154f8ea7c0ac9f69181bcceea8eae/sympy/codegen/numpy_nodes.py#L101-L102
