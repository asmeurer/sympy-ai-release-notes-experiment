# Pull request #30997: output checker checks for `...` before literal floats

- Author: @smichr
- Merged: 2026-11-08T22:56:25Z into `master`
- Labels: (none)
- Size: +49 / -2 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Problem was identified in #30918 when trying to use ellipses in long expressions containing Float.

#### Brief description of what is fixed or changed

When an expected docstring output contains floats *and* `...` the floats were checked without allowing for some of them to be missing because they were in the `...` portion. Now, if there are floats then normal Python doctest matching is attempted. If that fails then approximate testing *requiring all Float to be present* is employed.

*If ellipses are used then any visible floats left in the expectation must match the obtained value exactly.* If you want approximate matching of floats you can't use ... with this PR.

In addition, bracket delimiters and `:`, `=`, and `/` are now recognized.

#### Other comments

#### AI Generation Disclosure

Problem identified by author and solution/tests developed with ChatGPT.

## Commits

- 08a130215e (Christopher Smith): Honor doctest ellipses before approximate floating-point checks
- 57a2479a2e (Christopher Smith): Test numeric values hidden by doctest ellipses
- c0871f68f1 (Christopher Smith): Use standard doctest matching for outputs with ellipses
- 04f74fa152 (Christopher Smith): Use float positions recognized by existing doctest checker
- 8adfd21460 (Christopher Smith): Recognize floats inside parentheses in doctest output
- 9224f491b1 (Christopher Smith): Test approximate matching of parenthesized floats
- 91cfc81ebd (Christopher Smith): Recognize floats next to common punctuation in doctest output
- fee00a3837 (Christopher Smith): Test approximate floats around brackets and delimiters

## Conversation

(no comments)

## Reviews

(no reviews)
