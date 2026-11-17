# Pull request #30918: avoid numerical evaluation when ordering expression terms

- Author: @smichr
- Merged: 2026-11-10T19:58:10Z into `master`
- Labels: (none)
- Size: +1534 / -1757 in 194 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

alternate to #30904, #30818
fixes #2834 
fixes #10800
fixes #19790
fixes #17609
fixes #23211 (construction is fast when using evaluate(False) context
fixes #16090
fixes #17911 (like 10800)

#### Brief description of what is fixed or changed

No longer apply `complex` to numerical coeffcients of terms in as_terms (see first commit for commentary).
Try to retain nice (and nicer) mathematical default printing through the printers (see second commit).

These are the two layers of change:
1. Expr.as_terms() / as_ordered_terms() -- establishes the underlying structural ordering while avoiding evalf
2. Printer._as_ordered_terms() -- makes presentation adjustments, including putting negative terms and explicit imaginary terms in the desired positions. This is shared by all printers, so we don't need three implementations of those adjustments.

Note: the printers still have separate code for interpreting signs and rendering terms. They therefore won't necessarily produce identical ordering behavior in every special printing path. For example, `multiline_latex()` calls `as_ordered_terms()` directly rather than going through the shared `_as_ordered_terms`.

#### Other comments

Numerical evaluation has been removed from the ordering of terms based on their complex coefficients. Instead, sort keys determine the ordering, and printers (when `order=None`) attempt to present terms in a mathematically pleasing way.

However, numerical evaluation can still be triggered indirectly by assumptions queries, including during expression construction. Using `evaluate(False)` avoids much of the evaluation normally performed during construction, allowing even very large expressions to be built quickly.

Unfortunately, *printing* such unevaluated expressions could still be extremely slow. The problem was traced to the following sequence:

```text
evaluate(False)
    ↓
Large unevaluated expression
    ↓
str(expr)
    ↓
as_terms()
    ↓
decompose_power()
    ↓
Reconstruct a power with evaluation enabled
    ↓
Assumptions inference
    ↓
evalf(2)
```

The reconstruction in `decompose_power()` could trigger expensive numerical inference on expressions that had deliberately been left unevaluated.

This commit replaces `decompose_power()` with `as_base_exp()` in `as_terms()`, treating powers with non-integer exponents as individual generators rather than reconstructing them.

As a result, a radical expression representing `cos(pi/257)`, containing approximately 46,730 nodes, can be constructed using `evaluate(False)` in about 2 ms and converted to a string in approximately 0.5 seconds.

Possible additions to `from sympy import this`: 
* inference is costly: don't use it when structure suffices
* the cost of curiosity should be borne by the consumer
* don't make everyone pay for what you need to know
* Inspect what is present. Don't compute what might be discovered.

#### AI Generation Disclosure

Extensive collaboration with ChatGPT.

## Commits

- aa98ebb0d6 (Christopher Smith): avoid evaluation during ordering
- 7f178caf46 (Christopher Smith): _as_ordered_terms changes in printer
- 52ff88e955 (Christopher Smith): fix test expectations
- 97df16ec55 (Christopher Smith): Restore abbreviated doctest output in sympy/physics/biomechanics/musculotendon.py
- 714b13033c (Christopher Smith): Restore abbreviated doctest output in sympy/core/function.py
- c922e69e89 (Christopher Smith): Restore abbreviated doctest output in sympy/solvers/ode/subscheck.py
- 08109c3916 (Christopher Smith): Refresh biomechanics.rst doctest expectations for printer ordering
- e148da7870 (Christopher Smith): Refresh biomechanical-model-example.rst doctest expectations for printer ordering
- 0c74ad2e3b (Christopher Smith): Keep full floating-point outputs in biomechanics doctests

## Conversation

### @oscarbenjamin commented

Where are the substantive changes in this PR? Which files have the actual code change?

> Possible additions to `from sympy import this` is:
> 
> * inference is costly: don't use it when structure suffices
> * the cost of curiosity should be borne by the consumer
> * don't make everyone pay for what you need to know

What is this? It sounds like some kind of repentance after self-flagellation...

### @smichr commented

@asmeurer , @oscarbenjamin please see the OP for summary and the first commit for commentary.

### @smichr commented

@asmeurer , this is the PR to check.

### @smichr commented

@asmeurer , the first two commits show changes to code and the ones following are the expectation changes. I have a summary of the types of changes in printing that you will see. I like the changes, especially since they resolve an open issue #16090. There's an overall better consistency and mathematically pleasing presentation. It would be great to get this committed before it becomes stale. Although tools help with the test alignment, it is still a fairly intensive process.

### @smichr commented

This is a desired direction. Any modifications to printing can be handled in follow-up.


## Reviews

### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr commented on `sympy/core/expr.py`

This is a printing preference and is not necessary for deterministic, non-evaluative ordering. The more impactful performance change is the smaller change in the next portion of code.

### @smichr commented on `sympy/core/expr.py`

The only coeff we are going to use for ordering is the Rational or Float coefficient.
```python
>>> (2.*x).as_coeff_Mul()
(2.00000000000000, x)
>>> (2.*pi*x).as_coeff_Mul()
(2.00000000000000, pi*x)
>>> (oo*x).as_coeff_Mul()
(oo, x)
>>> (nan*x).as_coeff_Mul()
(nan, 1)
```

### @smichr commented on `sympy/core/expr.py`

`decompose_power` is a re-building option. We are going to order based on what *is* not on what will be.

### @smichr commented on `sympy/core/numbers.py`

The omission of these trigger unecessary evalf.

### @smichr commented on `sympy/simplify/simplify.py`

With the above changes, one test allowed return value to be longer than input because the return value was not compared to the original expression. So in the test changes commit there is not a dedicated addition, only an omission that would have been wrong if this change were not made.

### @smichr commented on `doc/src/contributing/docstring.rst`

ChatGPT summary:

There are 194 changed files and more than 500 diff hunks, so grouping the changes by underlying ordering convention makes much more sense than listing individual tests.

### Representative changes in expression ordering and printing

This PR avoids numerical evaluation during expression ordering. Most changed expectations result from preserving symbolic numerical factors rather than converting them to Python complex numbers merely to determine their order.

Representative differences include:

**1. Two-term sums favor a positive leading term when printing.**

```
-x + z                 -> z - x
-t**3 + y**3           -> y**3 - t**3
-sin(a)*sin(b) + cos(a)*cos(b)
                       -> cos(a)*cos(b) - sin(a)*sin(b)
```

The printer handles this preference without imposing it on `as_ordered_terms()`. Explicit ordering options continue to use their requested order.

**2. Symbolic numerical constants participate in term ordering without numerical evaluation.**

```
1 + 2*pi               -> 2*pi + 1
1 + sqrt(2)            -> sqrt(2) + 1
-7 + 3*sqrt(2)         -> 3*sqrt(2) - 7
```

Constants such as `pi`, radicals, and `EulerGamma` retain their symbolic structure. This can change their relative order compared with ordinary numbers.

**3. The ordering of sums involving numerical functions can change.**

```
cos(5)/2 + cos(1)/2    -> cos(1)/2 + cos(5)/2
e + exp(2)             -> exp(2) + e
```

Previously, numerical evaluation could influence their ordering. These expressions are now ordered structurally.

**4. Symbolic numerical factors are handled separately from variable-dependent factors.**

For example:

```
str(zeta(3)*x**3) == 'x**3*zeta(3)'
str(log(2)*x) == 'x*log(2)'
```

Symbolic numerical factors no longer need evaluation merely to determine how products should be displayed.

**5. Series retain their special display conventions.**

Ordinary polynomial expressions generally display higher-degree terms first, while series with an `O` term display increasing powers and place `O` last.

```
x**2 + x + pi/4

pi/4 + x + x**2 + O(x**3)
```

The ordering of variable-dependent terms is preserved even when coefficients contain symbolic numerical constants.

**6. Imaginary coefficients and unevaluated products are handled structurally.**

A single literal `I` is recognized for imaginary-coefficient ordering, preserving conventional behavior:

```
(2 + 3*I).as_ordered_terms() == [2, 3*I]
```

Repeated unevaluated factors of `I` instead contribute to the monomial signature, without evaluating the product. Thus an unevaluated `I**2` and `I*I` receive consistent ordering information, including when powers and products are mixed.

**Canonical ordering and printing are deliberately separate.**

For example:

```
(z - a).as_ordered_terms() == [-a, z]
str(z - a) == 'z - a'
sstr(z - a, order='grlex') == '-a + z'
```

This allows display-specific conventions to be handled by printers rather than imposing their cost on general expression operations.

The sign-selection tie-breaker in `_could_extract_minus_sign()` also prefers a symbolic term over a known numerical term in two-term sums, avoiding changes to trigonometric canonicalization caused by the new ordering.

### What I found regarding the `I*I` tests

I checked current master directly.

Already in master: Conventional real/imaginary ordering tests such as `(2 + 3*I).as_ordered_terms() == [2, 3*I]`, including all four sign combinations with 2 and 4.

New in your branch: The `Pow(base, 2, evaluate=False)` versus `Mul(base, base, evaluate=False)` tests for both `pi` and `I`, and the mixed `I**2 * I * I` monomial comparison.

Those new tests are worthwhile because they check something master doesn't: consistency between structurally different but equivalent unevaluated representations.

See [[test_expr.py on quickstrb-clean](https://github.com/smichr/sympy/blob/quickstrb-clean/sympy/core/tests/test_expr.py?utm_source=chatgpt.com)](https://github.com/smichr/sympy/blob/quickstrb-clean/sympy/core/tests/test_expr.py?utm_source=chatgpt.com).

### Two additional observations from the review

Not every changed expectation is strictly a printing change. The PR also changes `could_extract_minus_sign()` results for numeric expressions such as `sqrt(2) - 1`, and some solver tests now compare results differently because equivalent solutions may have changed form or order. I would avoid saying that all changed tests reflect cosmetic changes.

Also, many changes in `test_pretty.py` are simply rewriting triple-quoted strings as escaped single-line literals. Those aren't separate ordering behaviors, and I wouldn't mention them in the PR summary. They do make the diff larger than necessary, though.
