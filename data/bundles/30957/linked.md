# Issues and pull requests referenced by this pull request

## Issue #17123: Combinatoric group with zero elements

- Opened by @drybalka, state: closed

This is a boundary case, but important for other modules nonetheless. Define 
```
g1 = get_symmetric_group_sgs(0)
g2 = ([], Permutation(1))
g3 = get_symmetric_group_sgs(2)
``` 
Currently, `g1 = ([], [])`. However, if it then used in the direct product an error is raised:
```
>>> bsgs_direct_product(*g1,*g3)
IndexError: list index out of range
```
On the other hand `g2` in the direct product behaves exactly as expected:
```
>>> bsgs_direct_product(*g2,*g3) == g3
True
```
Which of `g1` and `g2` is the true (or simply better candidate for) zero group bsgs?
