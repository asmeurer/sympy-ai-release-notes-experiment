# Pull request #30910: Lambda.subs no longer replaces expressions that contain its bound variable

- Author: @tqa236
- Merged: 2026-11-03T11:02:59Z into `master`
- Labels: (none)
- Size: +10 / -1 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

I discovered this bug and a few others when stress testing https://github.com/sympy/sympy/pull/30858.

#### Brief description of what is fixed or changed

Before, `Lambda.subs` only skipped old when it was one of the variables, like `Lambda(x, x + y).subs(x, z)`, so `Lambda(x, x**2).subs(x**2, z)` gave `Lambda(x, z)`. Now, it will return the Lambda unchanged whenever old contains a bound variable, so `Lambda(x, x**2).subs(x**2, z)` should give correctly the unchanged `Lambda(x, x**2)`.

#### Other comments

#### AI Generation Disclosure

Discovered and fixed by Claude Opus 5.5, reviewed by myself. PR description is written by myself.

## Commits

- f8a90c6b80 (Trinh Quoc Anh): core: don't substitute expressions containing a Lambda's bound variable
      Lambda._subs only skipped old when it was one of the variables, so
      Lambda(x, x**2).subs(x**2, z) gave Lambda(x, z). Any match of such an
      old inside the body refers to the bound variable, not to the outer one,
      so return the Lambda unchanged whenever old contains a bound variable.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

## Conversation

### @smichr commented

This appears to handle Symbols well. But Lambda admits foo.is_symbol (like Indexed and IndexedBase) and I don't know how those should behave with Lambda. Maybe @Upabjojr could help out:

Given

x=IndexedBase('x')
y=IndexedBase('y')
s = Symbol('s')
i, j = var('i,j')

Do these have meaning?

Lambda(x, x + 1)
Lambda(x[i], x[i] + s)

Can you replace x with x[i], x[j], y, s?
Can you replace x[i] with x, x[j], y, s?
Can you replace s with x, x[i], y, y[j]?

Beyond this there are a lot of things that would be allowed into Lambda. I'll open an issue (#30917) about that.

### @Upabjojr commented

I would guess x[i] should behave as a symbol itself., but I cannot see all implications this would entail right now.

### @smichr commented

Are Indexed used in some special way with lambdify/numpy?

### @Upabjojr commented

> Are Indexed used in some special with with lambdify/numpy?

Should be checked. IIRC, `Indexed` was not that well supported.

### @smichr commented

It think this is the right thing wrt symbols: the bound variables should be opaque to subs so if the old has any symbols in common with them, it should fail. I still don't know if the `i` of `x[i]` is bound outside the context if `x`, however. But this doesn't  need to resolve that.

### @smichr commented

If you rebase on current master and push back using `--force-with-lead` let's see if the zizmor error goes away.

### @tqa236 commented

I rebased and pushed. The CI is green now. According to my quick check, this PR at least makes `Lambda` behaves like `Sum` in `master` when it refuses to subs for cases like `Lambda(i, x[i]).subs(x[i], z)` or `Sum(x[i], (i, 0, 3)).subs(x[i], z)`. So, a slightly more consistent than before.


## Reviews

(no reviews)
