# Issues and pull requests referenced by this pull request

## Issue #24593: Latex printer - weird output with Idx objects

- Opened by @Davide-sd, state: closed

On Jupyter notebook I get this:

```python
from sympy import *
init_printing(use_latex=True)
j = Idx("j", 5)
j
```

![image](https://user-images.githubusercontent.com/9921777/214582697-6171103c-f07c-4983-99e6-5a496cb99790.png)

```python
print(latex(j))
# {j}_{0\mathrel{..}\nobreak 4}
```
