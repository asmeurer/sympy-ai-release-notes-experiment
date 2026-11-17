# Pull request #31100: Add support for `\leqq` and  `\geqq` in the Lark LaTeX parser

- Author: @wermos
- Merged: 2026-11-14T16:31:19Z into `master`
- Labels: (none)
- Size: +5 / -2 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs
Fixes #25419.

#### Brief description of what is fixed or changed

This PR adds support for `\leqq` as less-than-or-equal-to, and `\geqq` as greater-than-or-equal-to. It also adds a test for `\geqslant`, which was previously not tested in the test suite.

#### AI Generation Disclosure

None.

## Commits

- 8d074a4d1a (wermos): Add \leqq and \geqq to the Lark LaTeX parser.
- 859c57ecee (wermos): Add tests for \leqq and \geqq in the Lark LaTeX parser.
- a2af2b2c16 (wermos): Add a test for \geqslant in the Lark LaTeX parser.

## Conversation

### @wermos commented

Ping @sylee957 for review

### @wermos commented

Since the tests are passing and @sylee957 said "I'm willing to merge any time after", I will go ahead and get this in.

### @sylee957 commented

I think that lark community should have added feature to detect regex conflict, using interregular. This should detect previous conflict like \left and \le.
Probably we should have more since we have added more grammar tokens.

### @wermos commented

Maybe we can put in a feature request at [Lark](https://github.com/lark-parser/lark)?


## Reviews

### @sylee957 reviewed: COMMENTED



### @wermos reviewed: COMMENTED



### @sylee957 reviewed: COMMENTED



### @sylee957 commented on `sympy/parsing/latex/lark/grammar/latex.lark`

What is this cryptic regex `\\le(?![a-zA-Z])/`?

### @wermos commented on `sympy/parsing/latex/lark/grammar/latex.lark`

That was added in #29489.

### @sylee957 commented on `sympy/parsing/latex/lark/grammar/latex.lark`

I see, that looks irrelevant to this PR anyway I'm willing to merge any time after
