# Issues and pull requests referenced by this pull request

## Issue #30874: with evaluate(False): And(Eq(0, Add(x, Mul(-1, I)))) gets RecursionError exception

- Opened by @mrsoftware0, state: closed

Running sympy 1.14 in python 3.12 on ubuntu 24.04.5 LTS under WSL 2 on Windows 11, if I run this:

```
from sympy import *
x=symbols("x")
with evaluate(False):
    And(Eq(0, Add(x, Mul(-1, I))))
```

I get this exception:

`RecursionError: maximum recursion depth exceeded`

I get the same error running just the with evaluate part on live.sympy.org. The stack trace is too long to include in this issue text, but it's pretty easy to reproduce.

I made a small attempt to debug this and found that if I run this under the pycharm debugger and do the following it actually runs to completion without the exception.

- Set Variables Loading Policy (in the three-dots menu in the debugger pane toolbar) to Synchronously
- Every time you change that setting you have to restart the interactive python console and reattach the debugger
- Set a breakpoint on the final line of `Expr.__complex__` (line 380 of `core/expr.py`)
- Run the lines above
- Hit step into, step out, step into to get inside the float(im) call
- Hit resume program as many times as necessary (**don't** just remove the breakpoint: that doesn't work)

However, if Variables Loading Policy is instead set to either Synchronously or On-demand and you perform the same steps, you still get the exception.

There are other sequences of stepping/breaking you can do in the debugger (without changing the code or variables) to get the code to run without exception, but this has been the most reliable so far as it sometimes seems that the behavior changes.

## Pull request #30897: core: avoid infinite recursion in evalf_mul under evaluate(False)

- Opened by @ShivanshhhG, state: closed

#### References to other Issues or PRs

Fixes #30874

#### Brief description of what is fixed or changed

In `evalf_mul`, pure-imaginary and pure-real factors are already handled natively by `evalf` with exact integer arithmetic on `man`/`exp` and the `direction` power-of-I accumulator. Only complex factors with both non-zero real and imaginary parts (`pair[0]` and `pair[1]`) need to be folded together to prevent cancellation loss.

This change:
1. Guards folding on `pair and pair[0] and pair[1]`, ensuring pure imaginary factors (like `I`) are not folded into `args[-1]`. Expressions like `Mul(-1, I)` now leave `args[-1]` untouched (`S.One`), allowing the termination check `elif i == last and arg is S.One: continue` to succeed and preventing recursion.
2. Wraps the internal multiplication/expansion in `with evaluate(True):` so that legitimate complex factors evaluate properly even when evaluated inside an outer `with evaluate(False):` context.

#### Other comments

Added unit tests in `sympy/core/tests/test_evalf.py` verifying evaluation under `evaluate(False)`.

#### AI Generation Disclosure

NO AI USE
