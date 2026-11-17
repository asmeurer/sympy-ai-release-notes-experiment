# Pull request #31076: Update tests in Lark LaTeX parser, add tests

- Author: @wermos
- Merged: 2026-11-13T18:51:23Z into `master`
- Labels: (none)
- Size: +160 / -17 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs
Closes #25366.

#### Brief description of what is fixed or changed
Added tests as described in #25366. I added tests for various features of the LaTeX parser such as Hyperbolic Trigonometric Expressions, Complex Conjugation, etc.

#### AI Generation Disclosure
This PR was created in collaboration with Claude Opus 5.5. I manually looked over all the code before opening the PR.

## Commits

- a9748587fb (wermos): parsing.latex.lark: remove stale expected failures from the tests
      The symbol and simple-expression tests skipped cases by index that now
      pass, or whose index did not exist in the list.
      The symbol tests expected y''_1 and y_1'' to give different symbols,
      although they render the same. Primes written after and before the
      subscript are now tested by two matching lists expecting the same
      symbols, the latter as an XFAIL.
- 8c741a619c (wermos): parsing.latex.lark: test trigonometric functions with superscripts
      Test a braced exponent, a symbol as exponent, a negative exponent other
      than -1, which is a power and not the inverse function, and a power of
      a function applied to an argument in parentheses.
      \sin^2 x^2 is read as ambiguous, with sin(x)**4 as a second reading,
      and is tested as an XFAIL.
- 1151171b98 (wermos): parsing.latex.lark: test the inverse trigonometric function commands
      Only \sin^{-1} was tested, and none of the \arc commands.
- d9c6c0ca51 (wermos): parsing.latex.lark: test the hyperbolic function commands
      Test \sech, \csch and the inverse hyperbolic commands not tested yet.
      \arcoth, \arsech and \arcsch are not supported, although the other
      inverse hyperbolic commands are, and are tested as an XFAIL.
- a4b852ab47 (wermos): parsing.latex.lark: test expressions inside subscripts
      A subscript may hold letters, digits, commas, plus and minus signs, and
      spaces, which are removed. A superscript, a division, a Greek letter
      next to other characters or a nested subscript is not supported, and is
      tested as an XFAIL.
- bb8094f9c5 (wermos): parsing.latex.lark: test the conjugate of a digit without braces
      Without braces only a digit is accepted. \overline x and \overline12,
      where the conjugate applies to the first digit, are not supported, and
      are tested as an XFAIL.
- ab34a84bb9 (wermos): parsing.latex.lark: test binomials with arguments without braces
      Test a digit argument, two digits read as two arguments, an argument in
      braces followed by one without them and the reverse, and Greek letters.
- 7f0d4b5482 (wermos): parsing.latex.lark: test sums and products repeating the index in the upper limit
      \sum_{k = 0}^{k = n} and the same form of \prod are not supported, and
      are tested as an XFAIL.
- 866835d64f (wermos): Update mailmap.

## Conversation

### @wermos commented

Pinging @sylee957 and @Upabjojr for review since they have reviewed my changes to the Lark LaTeX parser before; this PR only touches the tests-related stuff.

### @Upabjojr commented

@wermos thanks for the fix, good to see you back!


## Reviews

(no reviews)
