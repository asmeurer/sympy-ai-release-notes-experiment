# Issues and pull requests referenced by this pull request

## Issue #25419: [GSoC] `\leqq` and `\leqslant` for less-than-or-equal-to, `\geqq` and `\geqslant` for greater-than-or-equal-to

- Opened by @wermos, state: closed

## Background

The current ANTLR LaTeX parser supports using `\leqq` and `\leqslant` as the less-than-or-equal-to operator, and also supports `\geqq` and `\geqslant` for greater-than-or-equal-to operator.

While I have seen `\leqslant` and `\geqslant` used as the less-than-or-equal-to and the greater-than-or-equal-to operator respectively, I've never seen `\leqq` and `\geqq` used in this way.

## Lark Parser

Since I'm rewriting the LaTeX parser in Lark, I wanted to get the community's thoughts on supporting `\leqslant`, `\leqq`, `\geqslant`, and `\geqq` symbols for denoting these operators. For now, the Lark parser doesn't support any of these extra symbols for less-than-or-equal-to or greater-than-or-equal-to. However, if this is something that people want, it can easily be added.
