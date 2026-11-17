# Pull request #31105: Fix PolificationFailed in trigsimp groebner

- Author: @jiyakaushik26
- Merged: 2026-11-15T02:18:39Z into `master`
- Labels: (none)
- Size: +15 / -1 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs
Fixes #31083

#### Brief description of what is fixed or changed
Calling `trigsimp` with `method='groebner'` or `method='combined'` raises a `PolificationFailed` exception on expressions whose coefficients do not contain any polynomial generators.

During generator discovery, if no generators are found, the expression cannot be converted into a polynomial ring as expected. This PR catches that edge case and falls back to an empty generator set so simplification can proceed without failing.

Regression tests covering the original issue and similar edge cases for both methods have been added.

#### Other comments
I ran the focused `trigsimp` test file locally: 30 tests passed and 1 test was expected to fail (`xfailed`). I also verified the reported examples.

#### AI Generation Disclosure
AI tools were used during investigation to help trace the `PolificationFailed` traceback and verify edge-case behavior. [Add details of any AI assistance with code, tests, or PR text, as applicable.]

## Commits

- aff183e515 (Jiya Kaushik): Fix PolificationFailed in trigsimp groebner

## Conversation

### @smichr commented

This seems reasonable. Although you can get PolificationError for other reasons I am not sure those reasons would be raised with this code. This is in.

### @jiyakaushik26 commented

Thanks for reviewing and merging this! I really enjoyed working on this issue and learned a lot while exploring the `trigsimp` implementation. Appreciate the review and feedback! 😊


## Reviews

(no reviews)
