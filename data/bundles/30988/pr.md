# Pull request #30988: restricting critical-point searches to the domain of interest

- Author: @smichr
- Merged: 2026-11-10T06:52:01Z into `master`
- Labels: (none)
- Size: +81 / -32 in 5 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

- Partially fixes #21618 by evaluating `sin` and `cos` on `SetExpr` intervals with concrete endpoints.
- Incorporates the approach proposed in #29682, with an improvement to preserve handling of `EmptySet`; closes #29682
- Partially fixes #29675 by preventing enumeration of infinitely many singularities. The efficiency of processing large finite sets of singularities remains unresolved.

#### Brief description of what is fixed or changed

Improves evaluation of the image of a function over an interval:

- Restricts critical-point solving to the given interval, allowing functions such as `sin` and `cos` to be evaluated when they have infinitely many critical points globally but finitely many within the interval.
- Corrects endpoint openness by determining whether an extremal value is attained within the domain.
- Allows `sin` and `cos` applied to a `SetExpr` interval to return an evaluated interval when possible.
- Checks whether the set of singularities is finite before attempting enumeration. Infinite or unresolved sets are left unevaluated, while `EmptySet` and finite singularity sets continue to be handled normally.

#### Other comments

The singularity-handling change is based on the approach proposed by @SarvaarthN in #29682.

A possible future improvement is to handle equally spaced singularities symbolically, avoiding enumeration even when there are many finitely many points.

#### AI Generation Disclosure

Collaboration with ChatGPT who wrote this OP after a minimal description.

## Commits

- 94e79b2603 (Christopher Smith): Restrict imageset critical-point solving to the interval
- e053b2a0c4 (Christopher Smith): Respect endpoint inclusion in interval imagesets
- 0cc1b76bbe (Christopher Smith): Evaluate sine and cosine of SetExpr intervals
- 7dc5efef4b (Christopher Smith): Avoid enumerating infinite imageset singularities
      Adapt the guard proposed by Sarvaarth Narang in sympy/sympy#29682,
      while preserving evaluation for EmptySet singularities.
      See sympy/sympy#29675.

## Conversation

(no comments)

## Reviews

(no reviews)
