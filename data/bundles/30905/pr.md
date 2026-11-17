# Pull request #30905: Parenthesize frac in PythonCodePrinter

- Author: @Aryapatel-007
- Merged: 2026-11-05T17:13:18Z into `master`
- Labels: (none)
- Size: +16 / -3 in 5 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

None. I found this bug myself; it isn't reported anywhere.

#### Brief description of what is fixed or changed

`pycode(2*frac(x))` printed `2*x % 1`, which Python evaluates as `(2*x) % 1`, so `lambdify(x, 2*frac(x), "math")` returned wrong values (0.4 instead of 1.4 at x = 0.7). `frac` is now printed inside parentheses, so this becomes `2*(x % 1)`, and the NumPy printer keeps printing `numpy.mod(x, 1)`.

#### Other comments

#### AI Generation Disclosure

The code, tests and commit message were written with Claude (Anthropic, model Claude Opus 5.5) using Claude Code. This covers all changed lines in sympy/printing/pycode.py, sympy/printing/numpy.py, sympy/printing/tests/test_pycode.py and sympy/utilities/tests/test_lambdify.py. I reviewed the change and ran the tests myself. The PR description above is written by me.

## Commits

- ff5c72caa3 (Arya Patel): printing: parenthesize frac in PythonCodePrinter
      PythonCodePrinter prints frac(x) as the bare expression "x % 1", but the
      parent printer decides whether to add parentheses from the precedence of
      frac, which is a function and so binds tightly. As a result 2*frac(x)
      was printed as "2*x % 1", which Python evaluates as (2*x) % 1, and
      frac(x)**2 as "x % 1**2". lambdify with the "math" module then returned
      wrong values, e.g. 0.4 instead of 1.4 for 2*frac(x) at x = 0.7.
      The printed frac is now wrapped in parentheses, as is already done for
      other functions printed as operator expressions such as sign and
      KroneckerDelta. NumPyPrinter, which inherited this method, now prints
      frac directly as numpy.mod(x, 1) so it is unchanged.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- 238a6f362f (Arya Patel): Merge remote-tracking branch 'origin/master' into fix-pycode-frac-precedence

## Conversation

### @smichr commented

If you rebase on current master and force push here, I think zizmor test will pass.

And maybe add a test like `assert NumPyPrinter().doprint(2*frac(x)) == '2*numpy.mod(x, 1)'`

### @smichr commented

ping @Aryapatel-007

### @Aryapatel-007 commented

I have updated the branch with the latest master and the checks are running again.

### @smichr commented

Thanks for taking care of this. It's in!

### @Aryapatel-007 commented

I appreciate it!


## Reviews

(no reviews)
