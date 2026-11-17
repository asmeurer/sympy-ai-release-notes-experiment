# Issues and pull requests referenced by this pull request

## Issue #14716: integrate

- Opened by @vloddos, state: closed

Can't count the integral from log(x+5)*cos(pi*x).
Code:

from sympy import pi,sin,cos,log,S
x=S('x')
(log(x+5)*cos(pi*x)).integrate((x,0.5,1))

## Pull request #1234: Fix test failure in beginner/precision.py example

- Opened by @flacjacket, state: closed, merged 2012-04-14

Title says it all.

## Pull request #25544: ask: handle real linear inequalities

- Opened by @TiloRC, state: closed, merged 2023-09-29

Here are some examples of what this PR enables ask to do:

```python
x, y, z = symbols("x y z", real=True)
ask(x + y > 2, (x < 0) & (y < 0)) # returns False instead of None
ask(x > z, (x > y) & (y > z))     # returns True instead of None
```

Unfortunately, I didn't have time to figure out how to handle infinite values, non-rational values, or complex variables. In the future, it might make sense to remove the `lra_satask` function and integrate the code from this pull request into `satask` once these cases are handled. Then again, one advantage of keeping it separate might be speed.

Currently, variables need to be specified to be real when they are created using the old assumptions. In other words, queries like `ask(x > 0, (x > 1) & Q.real(x))` don't currently work.

Also, if a disallowed predicate such as Q.even is part of a query, that disables inequality handling. This could be changed fairly easily. However, I wanted to avoid slowing down queries that weren't primarily about inequalities.

#### logic/algorithms/lra_theory.py

Contains the LRASolver object which is designed to work in conjunction with a SAT solver to determine if a boolean formula involving inequalities is satisfiable or not. 

#### sympy/assumptions/lra_satask.py

A function that's called in `ask` when `satask` returns None. It does some preprocessing so that all predicates are either Q.gt, Q.lt, Q.ge, Q.le or Q.eq and then makes some calls to `satisfiable` with `use_lra_solver` set to True. The `use_lra_solver` parameter tells satisfiable to use an LRASolver object in conjunction with the dpll2 algorithm.

## Pull request #30558: integrals: fix the floor terms added to atan(tan) and atan(cot) antiderivatives

- Opened by @asmeurer, state: closed, merged 2026-10-16

Integral.doit() adds floor terms to antiderivatives containing
`atan(c*tan(a) + d)` or `atan(c*cot(a) + d)` to cancel the jumps of the atan
at the poles of tan(a) and cot(a). The term that was added was wrong in
several cases, each of which introduced a discontinuity into the
antiderivative and gave wrong definite integrals:

- The term for cot had the wrong sign, which doubled the jump instead of
  canceling it. integrate(diff(atan(2*cot(x)), x), (x, -1, 1)) was
  positive for a negative integrand.

- A coefficient c depending on the integration variable was accepted
  even if its sign changes, giving a term like
  `sign(x)*pi*floor((x - pi/2)/pi)`, which jumps where c changes sign.
  `integrate(diff(atan(x*tan(x)), x), (x, -1, 1))` gave `-2*pi` instead of `0`.
  Such a coefficient is now only accepted if its sign is the same for all
  real values, as in `atan(exp(x)*tan(x))`.

- tan and cot not depending on the integration variable were corrected
  too, so that `integrate(atan(tan(y)), x)` was not `x*atan(tan(y))`.

- With several tan or cot in the argument, each one was corrected
  separately, which corrects a pole that they have in common more than
  once, as at x = pi/2 for atan(tan(x) + tan(3*x)). Now those with the
  same poles are corrected by a single term, and two with different
  periods that have some poles in common get an additional floor term
  for the common poles, where the jump of the atan is given by the sign
  of the sum of the two poles. `atan(tan(x) + tan(3*x))` needs
  `pi*floor((3*x - pi/2)/pi)` only. The argument must also be jointly
  linear in the tan and cot.

An atan for which the floor terms cannot be determined (a coefficient
that changes sign or is not real, poles in common among more than two tan or cot, or
poles that cannot be compared) is left uncorrected. Definite integrals
over its poles are then wrong, as they are for other discontinuous
antiderivatives, since Integral.doit() does not check for those.

The pass is moved to its own function, _add_atan_floor_terms().

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

#### Other comments

#### AI Generation Disclosure

All code generated with Claude Fable 5.1.

## Pull request #30311: [GSoC] manualintegrate: full migration to new archiecture

- Opened by @salastro, state: closed, merged 2026-09-03

#### References to other Issues or PRs

* Builds on top of #30191.
* Reimplements and replaces #30065.
* Reimplements and replaces #30079.
* Reimplements and replaces #30001.
* Fixes #30223.
* Fixes #30087.
* Fixes #30014.
* Fixes #30064.
* Fixes #30070.
* Fixes #30071.
* Fixes #29999.

#### Brief description of what is fixed or changed

This PR was initially meant to be a simple edit of the original generator-based branch. However, it quickly grew to be a monolithic PR collecting all of my other stale implementations and fixes. Details regarding each are available in the original PRs.

#### Other comments

#### AI Generation Disclosure

Claude Code (Sonnet 5) was heavily used to port previous implementations to the new architecture, in debugging emergent issues along the way, and in implementing minor fixes.
