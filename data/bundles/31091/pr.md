# Pull request #31091: Type Expr.coeff

- Author: @hunterhogan
- Merged: 2026-11-15T22:11:35Z into `master`
- Labels: typing
- Size: +10 / -10 in 1 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

- Annotate `Expr.coeff`

#### Other comments

With the signature annotated, MyPy checks the function body, requiring the following changes:

- rv.is_Add becomes isinstance(rv, Add).
- elif co2: becomes else:.
- reused loop variable `n` is renamed to nc.

#### AI Generation Disclosure

Claude Code

## Commits

- 3ea9949508 (Hunter Hogan): Annotate Expr.coeff.
      Use isinstance for guard.
      Replace `elif co2:` with `else:` so mypy knows `return None` will not happen.
      Rename reused loop identifier `n` due to changed type.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

## Conversation

### @oscarbenjamin commented

Looks good.


## Reviews

### @oscarbenjamin reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin commented on `sympy/core/expr.py`

This potentially constructs returnMe multiple times discarding the previous created expressions.

Generally I would prefer that a PR that is for typing should just be about typing. There can be a need to make other changes when working on typing but it is not clear to me why this change is here and it does not seem that the code is equivalent.

### @hunterhogan commented on `sympy/core/expr.py`

Why

> it is not clear to me why this change is here

> * In `Expr.coeff`, [Refactor "look for single match"](https://github.com/sympy/sympy/commit/0db54dfdd79498ceef18c7ae1411cc82b92a3cfa) because I couldn't figure out what it did, so I couldn't type it.

How

> This potentially constructs returnMe multiple times discarding the previous created expressions.

The statements that start with `returnMe = Mul(...` cannot run more than one time because of the guard `if returnMe is None:`.

Same

> it does not seem that the code is equivalent.

You might be right. I sincerely cannot fully decipher the code block I replaced. Claude Code said the old code block and the new code block had the same behavior on 400,000 random inputs (IIRC). I _think_ I understand what the code block is supposed to do. If I do understand, then I have high confidence in the loop and conditional checks. I did not second-guess the `Mul` statements.

### @oscarbenjamin commented on `sympy/core/expr.py`

It is better not to change the code if you don't fully understand it. Best just to leave it as it is.

### @hunterhogan commented on `sympy/core/expr.py`

I agree. 

I believe I understand the function. I've been trying not to write, "The code block I replaced was horrible code," because I didn't want to be unnecessarily harsh.

I replaced the code block because it was substandard code. I couldn't vouch for my typing proposal because the poor-quality code block prevented me from understanding the flow.

## My reasoning for my code

```python
# Return `Expr` IFF the list `nx` appears in only one list of non-commutative terms (`nc`).
# Else return the special form of 0, `S.Zero`.
returnMe: Expr | Zero | None = None

while co and returnMe != S.Zero:  # `while` conditions avoid using `break` as flow control.
    r, nc = co.pop()  # consume `co`.
    index: int | None = find(nc, nx, first=right)  # if `nx` is in `nc`, index will be `int`.

    if index is not None:  # Conditional check avoids using `continue` as flow control.
        if returnMe is None:  # If `True`, this is the first match, so evaluate the desired value.
            if right:  # Changed from the original `if not right:`
                returnMe = Mul(*nc[index + len(nx):None])
            else:
                returnMe = Mul(*r, *nc[0:index])
        else:  # Because `returnMe` has a value and `index` has a value, IFF must be false.
            returnMe = S.Zero

return returnMe or S.Zero  # If `returnMe` is None, then IFF must be false, so return S.Zero.
```

### @oscarbenjamin commented on `sympy/core/expr.py`

Was it necessary to change the code for mypy checks to pass?

Here is another reason not to change the code:

It makes it significantly harder for *me* to review the changes because now I need to understand both the old and the new code and think carefully about what the differences might be. If this PR only had all of the other changes I would have just merged it immediately the first time I looked at it.

### @hunterhogan commented on `sympy/core/expr.py`

> Was it necessary to change the code for mypy checks to pass?

No.

I would not have submitted it, however, because I would have been relying on Claude's "promise" that everything was correct. 

Ironically, Claude reminded me repeatedly that you preferred smaller changes. Claude tried to get me to scale back. But I lacked the training, experience, or knowledge to parse the code. 

I was too incompetent to submit the PR without refactoring, and I was too idealistic to submit an LLM-generated PR while claiming I understood the code when I didn't fully understand the code.

I may have unknowingly written something that assigned fault to you. I do not feel or think you are at fault for anything. I apologize for anything I wrote that faulted you. I agree with everything you wrote.

### @oscarbenjamin commented on `sympy/core/expr.py`

I'm not opposed to larger changes. It is just harder for me to find the time to review them.

### @oscarbenjamin commented on `sympy/core/expr.py`

If you want to more efficiently add type annotations to lots of things I'm happy to merge a large PR that adds many type annotations where every annotation is simple, uncontroversial and easy to review. It doesn't have to be all small PRs.
