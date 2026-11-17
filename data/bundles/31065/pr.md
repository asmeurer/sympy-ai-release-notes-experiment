# Pull request #31065: docs: typo, remove duplicated words

- Author: @ninglinLiu
- Merged: 2026-11-13T08:56:21Z into `master`
- Labels: (none)
- Size: +6 / -21 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

Removes a duplicated "to" in the `homomorphisms.py` docstring and in `doc/src/contributing/dependencies.md`. Docs/comments only; no behavior change.

#### Other comments

#### AI Generation Disclosure

This typo fix was identified and applied with assistance from Grok Bot, an automated coding assistant. The change itself is limited to removing duplicated words in the two files listed above.

## Commits

- 632a0edeed (ninglinLiu): docs: typo, remove duplicated words
      Signed-off-by: ninglinLiu <x07514475479@gmail.com>
- 201b2dc8d5 (NingLin Liu): docs: add NingLin Liu to .mailmap
- 9ed5655faa (NingLin Liu): docs: tighten recommended optional dependencies wording

## Conversation

### @smichr commented

Thanks. Many years ago I worked on cleanup of docstrings...brings back good memories. :-)


## Reviews

### @11350613 reviewed: APPROVED



### @smichr reviewed: COMMENTED



### @ninglinLiu reviewed: COMMENTED



### @smichr commented on `doc/src/contributing/dependencies.md`

What about replacing the 3 paragraphs with 

These optional dependencies are recommended for improved SymPy performance.

- **gmpy2**: [gmpy2](https://gmpy2.readthedocs.io/en/latest/)] provides faster large-integer arithmetic using the [GMP library](https://gmplib.org/). SymPy uses it automatically when installed, particularly in its [polynomial routines](https://github.com/sympy/sympy/pull/31065/polys-docs), which support integration, simplification, matrices, and other operations. See {ref}`polys-domainsref` for details. It remains optional because GMP is a non-Python library with a non-BSD license. We encourage all users who can install `gmpy2` to do so for a better SymPy experience.

### @ninglinLiu commented on `doc/src/contributing/dependencies.md`

Thanks — applied in 9ed5655. I used your wording, with two small cleanups so the links resolve: dropped the extra `]` on the gmpy2 docs URL, and kept the existing `(polys-docs)` target instead of a self-PR path.
