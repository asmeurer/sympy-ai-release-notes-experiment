# Pull request #30941: avoid inference when counting operations and extracting fractions

- Author: @smichr
- Merged: 2026-11-04T02:05:18Z into `master`
- Labels: (none)
- Size: +50 / -20 in 9 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

No outstanding issue; this is being removed from #30918 where, when testing, it was noticed that `count_ops` was obviously traversing a different path than `_nodes` and was encountering unintended evaluation. This was traced back to `fraction` and `radsimp`. Both have been updated to use structural information when appropriate.

Changing those changes what term-ordering sees and a few tests give different results; a besselsimp test failed and suggested the rewrite adjustment to account for the different terms that are now encountered.

#### Other comments

#### AI Generation Disclosure

This was a collaboration with ChatGPT.

## Commits

- e3c5cc75bc (Christopher Smith): avoid inference in count_ops and fraction
- 8e275f0c4c (Christopher Smith): Update expectations for structural fraction counting
- 6d98c68e12 (Christopher Smith): Restrict exptrigsimp rewrite to trigonometric functions

## Conversation

(no comments)

## Reviews

(no reviews)
