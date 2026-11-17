# Issues and pull requests referenced by this pull request

## Pull request #30918: avoid numerical evaluation when ordering expression terms

- Opened by @smichr, state: closed, merged 2026-11-10

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
