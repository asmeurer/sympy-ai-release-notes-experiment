# Issues and pull requests referenced by this pull request

## Issue #24811: `FpSubgroup.to_FpGroup()` depends on a possibly missing `self.C`?

- Opened by @James-G-Hill, state: closed

In the following line we can see that the method `to_FpGroup()` may return `self.parent.subgroup(C=self.C)`:

https://github.com/sympy/sympy/blob/75691e5cbdb3dfda4c8164a217bac6a6434404f6/sympy/combinatorics/fp_groups.py#L704

However, on `init` the internal variable `self.C` is set to `None`:

https://github.com/sympy/sympy/blob/75691e5cbdb3dfda4c8164a217bac6a6434404f6/sympy/combinatorics/fp_groups.py#L564

How should `self.C` be set? It seems to be set by the `order` method only.

I may be wrong on this and perhaps misunderstand some mathematical principle.
