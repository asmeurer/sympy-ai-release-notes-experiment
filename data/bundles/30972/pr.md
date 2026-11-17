# Pull request #30972: Pretty-print sequences with symbolic bounds

- Author: @raman118
- Merged: 2026-11-06T21:58:03Z into `master`
- Labels: (none)
- Size: +35 / -4 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #12629.

#### Brief description of what is fixed or changed

Pretty-print sequences with symbolic bounds using constructor notation instead of raising `NotImplementedError`. For example, `sequence(n, (n, 0, k))` prints as `SeqFormula(n, (n, 0, k))`. This preserves the definition and bounds without enumerating an unknown number of terms, and also handles periodic sequences, sums, and products. Numeric-bound sequences retain their existing list output.

#### Other comments

The regression failed before the fix. The pretty-printer and sequence suites passed (178 passed, 1 deselected), along with code-quality tests and Ruff. Tests cover ASCII and Unicode output, symbolic lower and upper bounds, infinite endpoints, and compound sequences.

#### AI Generation Disclosure

The contributor used OpenAI Codex (GPT-6 Astra) to generate the changes in `sympy/printing/pretty/pretty.py` and `sympy/printing/pretty/tests/test_pretty.py` and draft this description.

## Commits

- 694151f929 (raman118): Pretty-print sequences with symbolic bounds
      Use constructor notation when symbolic endpoints prevent enumerating a sequence. Cover formula and periodic sequences, sums and products, and finite and infinite symbolic ranges.
      AI-generated changes by OpenAI Codex (GPT-6 Astra).

## Conversation

(no comments)

## Reviews

(no reviews)
