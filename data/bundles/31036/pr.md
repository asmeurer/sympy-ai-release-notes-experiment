# Pull request #31036: add solve-ode.md to optional tests

- Author: @smichr
- Merged: 2026-11-11T02:06:14Z into `master`
- Labels: (none)
- Size: +6 / -5 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

A solve-ode.md has a dependency on numpy/scipy but was not included in the files to be run when those are available. It seems like we could use a script that would automatically add a file with a dependency to the appropriate whitelist(s).

#### Other comments

#### AI Generation Disclosure

ChatGPT created corrections based on my findings and directions.

## Commits

- e69eec2649 (Christopher Smith): Align solve-ode documentation with current expression ordering
- c78529ccc1 (Christopher Smith): Run solve-ode guide doctests in optional-dependency CI
- 9ff1e53ec3 (Christopher Smith): Renumber ODE constants in positive-first printed order
- 51c65b3335 (Christopher Smith): Test positive-first constant renumbering in ODE systems
- c3e671c99f (Christopher Smith): Update ODE guide for positive-first constant numbering
- 34008d3918 (Christopher Smith): Update ODE system examples for positive-first constant numbering
- f9b9e52311 (Christopher Smith): Revert sign-sensitive ODE constant renumbering
- 04050ded08 (Christopher Smith): Remove positive-term constant renumbering regression test
- 66f7bf57d2 (Christopher Smith): Restore ODE doctest expectations for unchanged constant renumbering
- c74501e39f (Christopher Smith): Apply batched suggestions from code review
      Co-authored-by: Christopher Smith <smichr@gmail.com>
- ccbc42dba3 (Christopher Smith): Update remaining solve-ode doctest expectations for current term order

## Conversation

### @smichr commented

The constant simplification can be adjusted after the doctests that are not being tests on CI (but will be after this commit) are passing. That way anyone running local tests will not see failures.


## Reviews

### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr commented on `sympy/solvers/ode/systems.py`

```suggestion
    [[Eq(f(x), C2*exp(x) - C1*exp(-x)), Eq(g(x), C1*exp(-x) + C2*exp(x))]]
```

### @smichr commented on `sympy/solvers/ode/systems.py`

```suggestion
    [[Eq(f(x), C2*exp(x) - C1*exp(-x)), Eq(g(x), C1*exp(-x) + C2*exp(x))]]
```
