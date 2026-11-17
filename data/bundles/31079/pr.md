# Pull request #31079: Fix Integer pow overload ordering

- Author: @jiyakaushik26
- Merged: 2026-11-13T22:09:25Z into `master`
- Labels: core.numbers, typing
- Size: +3 / -2 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs
Fixes #31069

#### Brief description of what is fixed or changed
Type checkers weren't resolving 3-argument calls like `pow(i, 2, 5)` properly. After looking through the type overloads, I moved the modular exponentiation overload above the `mod=None` ones so it gets matched first. The actual runtime behavior hasn't been touched.

#### Other comments
None

#### AI Generation Disclosure
I used ChatGPT to help break down the issue .I also used Antigravity to help reorder the overloads in `sympy/core/numbers.py`. I checked the final diff manually and ran the relevant test suite locally to make sure everything passes.

## Commits

- 673fae012d (Jiya Kaushik): Fix Integer pow overload ordering
- 39192632c5 (Jiya Kaushik): author: add Jiya Kaushik to .mailmap

## Conversation

### @oscarbenjamin commented

Looks good. Thanks!

### @hunterhogan commented

@jiyakaushik26, well done! I didn't want to untangle that issue, so I personally thank you for conquering it!

### @jiyakaushik26 commented

Thank you for the review and for merging this! Really glad to have made my first contribution to SymPy. Looking forward to contributing more!


## Reviews

(no reviews)
