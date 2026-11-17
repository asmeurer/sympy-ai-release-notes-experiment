# Pull request #30960: Allow two ULPs for Newton root accuracy on different platforms

- Author: @smichr
- Merged: 2026-11-05T20:57:26Z into `master`
- Labels: (none)
- Size: +3 / -1 in 1 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

The following failure can be averted by letting the uncertainty in the error be up to 2 ULP (units in last place); the current requirements make it about 1.61 ULP for the failing test. This is only changing the test criteria.

```
=============================================== short test summary info ===============================================
FAILED sympy/codegen/tests/test_algorithms.py::test_newtons_method_function__rtol_cse_nan - assert 2.86126401550282484098850784656751e-15 < 2.64523030128337532347187054305861e-15
================================== 1 failed, 2 passed, 2 skipped, 1 xfailed in 1.07s ==================================
```
#### Other comments

#### AI Generation Disclosure

Discussed with ChatGPT.

## Commits

- 82f9b8e3ad (Christopher Smith): Allow two ULPs for Newton root accuracy on different platforms

## Conversation

(no comments)

## Reviews

(no reviews)
