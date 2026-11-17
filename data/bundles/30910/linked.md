# Issues and pull requests referenced by this pull request

## Pull request #30858: Fix Derivative.subs with non-Symbol variables of differentiation

- Opened by @tqa236, state: open

#### References to other Issues or PRs

Fixes #28641

Fixes #19220

Fixes #14796

#### Brief description of what is fixed or changed

Fixes the `TypeError` crash in the linked issue, the direct cause is that `xreplace` renames by rebuilding, and the code crashes when attempting to rebuild a matrix expression with a scalar.

However, even if this works, this approach will also fail because renaming a non-`Symbol` differentiation variable hides whatever is inside it.

The fix follows more closely the comment above it, which was right all along.

```
            # for Derivative(f(x, g(y)), y), x cannot be replaced with
            # anything that has y in it; for f(g(x), g(y)).diff(g(y))
            # g(x) cannot be replaced with anything that has g(y)
```

It will now check for each variable of differentiation directly with `has_xfree` instead of renaming and rebuilding the expression.

The 3 added tests cover different purposes
- `test_derivative_subs_matrix_expr` is a direct regression test for the issue
- `test_derivative_subs_wrt_symbol_inside_wrt_function` covers a more general case where, take the example in the comment, there's a hidden variable that only appears inside `g(x)` that the `xreplace` approach can't detect.

Here's an illustrated example provided by Claude, which I also recalculated by hand to verify.

<img width="752" height="117" alt="image" src="https://github.com/user-attachments/assets/d84d609a-ca53-421e-b422-a341fa37ac3f" />

```
d = Derivative(y*g(x)**2, g(x), x)   # first ∂/∂g(x), then d/dx
d.subs(y, x)
```

<img width="766" height="588" alt="image" src="https://github.com/user-attachments/assets/5a5b89a8-7ac0-4164-8943-511e1aed0da7" />

- `test_derivative_subs_function_with_lambda` ensures that `old`/`new` can still be function classes such as `cos`, which `subs` allows. It's the `isinstance(e, Basic)` check on the `old` side here.

#### Other comments

#### AI Generation Disclosure

I used Claude Opus 5.5 to investigate the bug, implement the solution and write the tests. I'm heavily involved in all steps to ensure that the fix is generalized, concise and correct.

## Pull request #1234: Fix test failure in beginner/precision.py example

- Opened by @flacjacket, state: closed, merged 2012-04-14

Title says it all.
