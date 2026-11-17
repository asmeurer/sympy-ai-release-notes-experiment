# Pull request #31089: use TemporaryDirectory instead of TemporaryFile

- Author: @smichr
- Merged: 2026-11-14T13:14:03Z into `master`
- Labels: (none)
- Size: +5 / -5 in 1 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

A latex test fails under Windows when trying to create a TemporaryFile instead of doing work in a TemporaryDirectory

#### Other comments

No test is added except for noting that with the change the tests pass locally and without the change they fail.

#### with
```
> python -m pytest -v sympy/parsing/tests/test_custom_latex.py
...
sympy/parsing/tests/test_custom_latex.py::test_custom1 PASSED                                                    [ 50%]
sympy/parsing/tests/test_custom_latex.py::test_custom2 PASSED                                                    [100%]
```
#### without
```
sympy/parsing/tests/test_custom_latex.py::test_custom1 FAILED                                                    [ 50%]
sympy/parsing/tests/test_custom_latex.py::test_custom2 FAILED                                                    [100%]
```

#### AI Generation Disclosure

My work, advised by ChatGPT.

## Commits

- fdeb28c81c (Christopher Smith): use TemporaryDirectory

## Conversation

(no comments)

## Reviews

(no reviews)
