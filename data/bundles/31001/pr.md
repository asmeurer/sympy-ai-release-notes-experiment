# Pull request #31001: cse: use list(args) for comparison

- Author: @smichr
- Merged: 2026-11-09T04:54:01Z into `master`
- Labels: (none)
- Size: +4 / -1 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

Issue found while investigating [report](https://groups.google.com/g/sympy/c/FJt8rP8XTDM) on mailing list where apparently `cse` was capturing a symbol as a replacement pattern. This can be reproduced by introducing an UnevaluatedExpr which rebuilds to a symbol; the root cause for doing the rebuild (which was intended *not* to happen) was a test involving a tuple and list container which compared as unequal (and thus permitted the rebuild).

#### Other comments

#### AI Generation Disclosure

Author noted issue and ChatGPT located the issue and suggested the correction and test which were added.

## Commits

- 5271d62a92 (Christopher Smith): cse: use list(args) for comparison

## Conversation

### @moorepants commented

Here is the behavior in the latest release 1.14.0 (for reference):

```
In [8]: import sympy as sm

In [9]: x = sm.symbols('x')

In [10]: p = sm.Pow(x, 1, evaluate=False)

In [11]: p
Out[11]: x**1

In [12]: sm.cse([p, p])
Out[12]: ([(x0, x)], [x0, x0])
```


## Reviews

(no reviews)
