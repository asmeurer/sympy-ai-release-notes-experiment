# Pull request #31141: sets: Fixed a bug where `Ordinal` can produce non-canonical output.

- Author: @MajesticSlacks
- Merged: 2026-11-17T11:31:37Z into `master`
- Labels: sets
- Size: +5 / -1 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs
See https://github.com/sympy/sympy/issues/31086#issuecomment-6891811101

#### Brief description of what is fixed or changed
Before `Ordinal` could accept values in non-canonical ordering.
```
>>> from sympy.sets.ordinals import *
>>> Ordinal(OmegaPower(0,3), OmegaPower(0,2))
3 + 2
>>> Ordinal(OmegaPower(0,3), OmegaPower(0,2)) + 1
3 + 3
```
Now it raises `ValueError`.

#### Other comments
In the longer term, it may be better to for the `Ordinal` constructor to do the canonicalization itself.

#### AI Generation Disclosure
NO AI USE

## Commits

- 1b69a9345a (Benjamin Dolata): enforce canonical ordering on `Ordinal`

## Conversation

### @oscarbenjamin commented

Looks good.


## Reviews

(no reviews)
