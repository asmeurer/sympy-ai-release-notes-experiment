# Pull request #31103: printing: share Mul factor staging and group printed reciprocals

- Author: @smichr
- Merged: 2026-11-14T20:34:59Z into `master`
- Labels: (none)
- Size: +148 / -114 in 5 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

close #31095 as alternative (with co-authorship)
fixes point 2 of #30844

#### Brief description of what is fixed or changed

Parentheses are missing on fractions in denominators of some printers, printing 1/1/y instead of 1/(1/y).

In addition, there is unnecessary duplication of code across the printers . Now all the printers use the same function to break a Mul into numerators and denominators.

#### Other comments

#### AI Generation Disclosure

I directed the work for ChatGPT which staged code and tests which I have reviewed.

## Commits

- 296b3d323a (Christopher Smith): printing: share Mul factor staging and preserve reciprocal grouping
      Stage numerator and denominator factors without re-evaluating nested
      reciprocal powers, so printers produce x/(1/y) rather than x/1/y.
      Share the staging logic across string and code printers, while retaining
      language-specific formatting and existing reciprocal optimizations.
      Add cross-printer regression cases and numeric tests for positive and
      negated expressions.
      Fixes the code-printer denominator issue in #30844; supersedes #31095.
      Co-authored-by: Viranshul Panchal <viranshulpanchal23@gmail.com>
- f9eaf0553a (Christopher Smith): delete extra last line

## Conversation

(no comments)

## Reviews

### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr commented on `sympy/printing/tests/test_mul_factor_staging.py`

```suggestion
from sympy.abc import x, y
```

### @smichr commented on `sympy/printing/tests/test_mul_factor_staging.py`

```suggestion
```

### @smichr commented on `sympy/printing/tests/test_mul_factor_staging.py`

```suggestion


```

### @smichr commented on `sympy/printing/tests/test_mul_factor_staging.py`

```suggestion
from sympy import Float, Mul, Pow, S
```

### @smichr commented on `sympy/printing/tests/test_mul_factor_staging.py`

```suggestion
```
