# Pull request #30977: Remove nobreak from LaTeX index ranges

- Author: @raman118
- Merged: 2026-11-07T08:56:54Z into `master`
- Labels: (none)
- Size: +8 / -2 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #24593.

#### Brief description of what is fixed or changed

Removed `\nobreak` from the LaTeX output of bounded `Idx` objects. This prevents the command from appearing visibly in affected Jupyter notebook renderers while preserving the index label and range.

Added regression tests for bounded and unbounded indices and updated existing indexed-expression tests.

#### Other comments

Validation:
- LaTeX printer tests: 178 passed, 2 xfailed.
- Code-quality tests: 6 passed.
- Ruff and local author checks passed.

#### AI Generation Disclosure

The contributor used OpenAI Codex to generate changes in `sympy/printing/latex.py` and `sympy/printing/tests/test_latex.py` and draft this description. The exact runtime model identifier was unavailable.

## Commits

- bfddca3c32 (raman118): Remove nobreak from LaTeX index ranges
      Preserve bounded index notation while avoiding a command unsupported by older notebook math renderers.
      AI-generated changes by OpenAI Codex.

## Conversation

(no comments)

## Reviews

(no reviews)
