# Pull request #30991: printing: close the for( parenthesis in rcode of For loops

- Author: @Swayam-27
- Merged: 2026-11-08T15:50:06Z into `master`
- Labels: (none)
- Size: +2 / -2 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

See #30844

#### Brief description of what is fixed or changed

The R code printer was missing a closing parenthesis when printing a For loop. Because of this, the generated R code was invalid:

```python
>>> from sympy import symbols, Range, rcode
>>> from sympy.codegen.ast import For, aug_assign
>>> x, y = symbols('x y')
>>> print(rcode(For(x, Range(0, 10, 2), [aug_assign(y, '*', x)])))
for(x in seq(from=0, to=9, by=2){
   y *= x;
}
```

The closing `)` was missing before the `{`, which caused R to report an unexpected `{` error. I added the missing parenthesis in `_print_For`, so the generated output now starts with:

```r
for(x in seq(from=0, to=9, by=2)){
```

#### Other comments

The existing `test_rcode_For` was checking for the same incorrect output, so I updated it to expect the correct output.

I don't have R installed, so I couldn't run the generated code in R. I checked the output manually instead.

Also, `y *= x;` is not valid R syntax, since R does not support `*=`, but I have left that unchanged to keep this PR focused on the missing parenthesis.

#### AI Generation Disclosure

I used Claude Code (Claude Opus 5.5) to identify this bug from the list in #30844 and help implement the change in `sympy/printing/rcode.py` (`_print_For`) and update the test in `sympy/printing/tests/test_rcode.py` (`test_rcode_For`). I reviewed the changes, checked the generated output myself, and understand what was changed.

## Commits

- 6f45419617 (Swayam Prajapati): printing: close the for( parenthesis in rcode of For loops
      RCodePrinter._print_For produced `for(x in seq(...){`, which is missing
      the `)` that closes `for(` and is a syntax error in R. The existing test
      asserted this output and is updated.
      AI-assisted: the change and test update were generated with Claude Code
      (Claude Opus 5.5) and reviewed by the author.

## Conversation

### @smichr commented

Thanks. It's in.


## Reviews

(no reviews)
