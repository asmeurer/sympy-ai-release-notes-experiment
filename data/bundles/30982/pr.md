# Pull request #30982: printing: parenthesize Relational and Contains in Not for LaTeX, pretty, and MathML

- Author: @knowprasad
- Merged: 2026-11-10T09:56:36Z into `master`
- Labels: (none)
- Size: +48 / -12 in 6 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes some of #30844

#### Brief description of what is fixed or changed

When formatting `Not(x > y, evaluate=False)` or `Not(Contains(x, S), evaluate=False)`, `latex`, `pretty`, and presentation `mathml` printers omitted parentheses around the negated relational or containment condition, generating unparenthesized output such as `\neg x > y` instead of `\neg \left(x > y\right)`.

This PR updates `_print_Not` across `LatexPrinter`, `PrettyPrinter`, and `MathMLPresentationPrinter` to wrap arguments satisfying `(arg.is_Boolean or arg.is_Relational or arg.func.__name__ == 'Contains')` with parentheses, while preserving unparenthesized double negations (`\neg \neg x`, `¬¬x`).

#### Other comments

- Passed all 453 test functions across `test_latex`, `test_pretty`, and `test_mathml`.

#### AI Generation Disclosure

NO AI USE

## Commits

- f9fe36979e (prsdx): printing: parenthesize Relational and Contains in Not for LaTeX, pretty, and MathML
      Parenthesize Relational and Contains arguments when printed inside
      Not expressions in LaTeX, pretty, and MathML printers. Suppress
      extra parentheses when printing double negations.
      Fixes #30844
      Co-authored-by: Christopher Smith <smichr@gmail.com>
      Signed-off-by: prsdx <prsdx.dev@gmail.com>

## Conversation

### @smichr commented

ubuntu-latest appears to be causing an issue -- if you pull the current version, rebase on master (after this has been fixed) and force push back to here, it should be ready to go.

### @knowprasad commented

Thanks @smichr.

I found the issue in sympy/printing/latex.py: the suggestion was missing a closing parenthesis after Contains) on line 1164:
`python
if (arg.is_Boolean or arg.is_Relational or isinstance(arg, Contains)) and not arg.is_Not:
`

I fixed the syntax in latex.py, rebased the branch onto current master (commit 1e60306), and verified all 453 tests across 	est_latex, 	est_pretty, and 	est_mathml pass locally.

Pushed the updated branch back with your co-authorship. It should be ready to go now!

### @smichr commented

Got it, thanks.


## Reviews

### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr commented on `sympy/printing/pretty/pretty.py`

Recommendation: Small changes before approval
Finding
Importance
Incorrectly closes umbrella issue #30844
Must fix bc only one of many issues fixed. Don't  put close or fixes next to issue number

Class-name check instead of isinstance
Should fix

### @smichr commented on `sympy/printing/pretty/pretty.py`

```suggestion
            if (arg.is_Boolean or arg.is_Relational or isinstance(arg, Contains)) and not arg.is_Not:
```

### @smichr commented on `sympy/printing/mathml.py`

```suggestion
        if (arg.is_Boolean or arg.is_Relational or isinstance(arg, Contains)) and not arg.is_Not:
```

### @smichr commented on `sympy/printing/latex.py`

```suggestion
        from sympy.logic.boolalg import (Equivalent, Implies)
        from sympy.sets.contains import Contains
```

### @smichr commented on `sympy/printing/mathml.py`

```suggestion
        from sympy.sets.contains import Contains
        mrow = self.dom.createElement('mrow')
```

### @smichr commented on `sympy/printing/pretty/pretty.py`

```suggestion
        from sympy.logic.boolalg import (Equivalent, Implies)
        from sympy.sets.contains import Contains
```

### @smichr commented on `sympy/printing/latex.py`

```suggestion
        if (arg.is_Boolean or arg.is_Relational or isinstance(arg, Contains) and not arg.is_Not:
```
