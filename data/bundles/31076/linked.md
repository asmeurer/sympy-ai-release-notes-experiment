# Issues and pull requests referenced by this pull request

## Issue #25366: [GSoC] Improve LaTeX Parser tests

- Opened by @wermos, state: closed

Currently, there is [one test file](https://github.com/sympy/sympy/issues?q=is%3Aopen+is%3Aissue+label%3Aparsing.latex) which tests the LaTeX parser against a list of input strings.

This is fine for a starting point, but there are a few improvements that would make the testing experience better. Apart from this, there are many things which the ANTLR-based parser supports, which are not tested at all.

## Better Organization of Tests

Currently, the entire test suite is in a list of tuples where the first element is the input LaTeX string and the second element is the expected SymPy object.

This is a reasonable way to organize the tests overall. However, breaking up the test cases into separate categories, and testing the LaTeX parser against each category allows the developer to have a better understanding of where the parser is failing.

The current tests layout has most of its integral-related tests [here](https://github.com/sympy/sympy/blob/a9320ec9328d722417b5bcd3b5cd885ae2960eb1/sympy/parsing/tests/test_latex.py#L173-L192). However, for some reason, there is a lone integral test [here](https://github.com/sympy/sympy/blob/a9320ec9328d722417b5bcd3b5cd885ae2960eb1/sympy/parsing/tests/test_latex.py#L272), all by itself.

We should separate the tests into different functions, each of which stress-tests a specific aspect of the parser. For example, we can have a function which only tests the parser against integral expressions. Another function can test the parser against trigonometric functions, another against derivatives, and so on.

UPDATE: This was implemented for the Lark-based LaTeX parser, and the [PR which does this for the ANTLR-based LaTeX parser](https://github.com/sympy/sympy/pull/25381) is still open.

## Add More Tests

Organizing the tests by category also helps us visually see which aspects of the parser are thoroughly tested, and which parts are not so thoroughly tested. The current layout makes it hard to see, for example, that trigonometric expressions with superscripts like `\sin^2 x` are not tested at all.

### Add More Trigonometric Expression Tests

As mentioned above, expressions like `\sin^2 x` are not tested at all. Out of all the inverse trigonometric expressions, only [`\sin^{-1} x` is tested](https://github.com/sympy/sympy/blob/a9320ec9328d722417b5bcd3b5cd885ae2960eb1/sympy/parsing/tests/test_latex.py#L132). We should add tests for things like `\arcsin` as well.

### Add Hyperbolic Trigonometric Expression Tests

There are no tests for ensuring that expressions like `\sinh x` are parsed correctly. Tests for this should also be added.

### Add Tests for Subscripts

We should test that the parser handles things like `a_{2n}` or `a_{n+k}` correctly. That is, there should be tests which ensure that the parser correctly handles subscripts with expressions inside it.

### Add More Tests for Complex Conjugation

Even though this something of a corner case, we should ensure that the complex conjugate of single digits without curly braces is correctly handled. For example, `\overline1` should be handled the way we expect it to be handled.

### Add More Tests for Binomials

Once again, this is a corner case but we should check that things like `\binom1k` work as intended.

### Add More Tests for Sums

It'll be easy to add support for things like `\sum_{k = 0}^{k = n} k` to the Lark-based LaTeX parser. Once support for that is added, we should also add tests for it.

## Task List

- [x] Refactor the existing tests into separate functions for the Lark-based LaTeX parser. This can be done parallelly with the LaTeX parser work.
- [ ] Refactor the existing tests into separate functions for the ANTLR-based LaTeX parser.
- [ ] Add more Trigonometric Function Tests for things like `\sin^2 x`.
- [ ] Add more Inverse Trigonometric Function Tests for things like `\arcsin x`.
- [ ] Add tests for Hyperbolic Trigonometric Function Tests for things like `\sinh x` and `\cosh x`.
- [ ] Add tests for expressions inside subscripts.
- [ ] Add tests for corner cases in complex conjugation.
- [ ] Add tests for corner cases in binomial expressions (i.e., expressions which use `\binom`).
- [ ] Add tests for the "extended" sum expression syntax.
