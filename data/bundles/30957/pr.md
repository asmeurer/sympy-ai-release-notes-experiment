# Pull request #30957: Handle zero-rank tensor symmetry groups

- Author: @raman118
- Merged: 2026-11-05T19:08:36Z into `master`
- Labels: (none)
- Size: +17 / -3 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #17123.

#### Brief description of what is fixed or changed

`get_symmetric_group_sgs(0)` returned no generators, causing `bsgs_direct_product` to raise `IndexError`. It now returns the identity permutation on the two sign slots, matching `TensorSymmetry.fully_symmetric(0)`.

#### Other comments

Regression tests failed before the fix. Coverage includes symmetric and antisymmetric rank-zero groups, direct products in both orders, and `TensorSymmetry` construction. The tensor canonicalization and tensor suites passed (83 passed, 1 skipped, 1 xfailed), as did code-quality tests (6 passed), Ruff, and `bin/mailmap_check.py`.

#### AI Generation Disclosure

OpenAI Codex (GPT-6 Astra) generated all changes in `sympy/combinatorics/tensor_can.py`, `sympy/combinatorics/tests/test_tensor_can.py`, and `sympy/tensor/tests/test_tensor.py`. This PR description was also written by the AI agent at the account owner's request.

## Commits

- ddcda23f3e (raman118): Handle rank-zero symmetric tensor groups
      Return the degree-two identity generator for rank zero so signed direct products and TensorSymmetry construction work consistently.
      AI-generated code and tests by OpenAI Codex (GPT-6 Astra).

## Conversation

### @smichr commented

It's nice to see things that @jksuom recommended be handled. Thanks. If you are interested, Oscar wrote a rememberance [here](https://www.mail-archive.com/sympy%40googlegroups.com/msg38409.html?utm_source=chatgpt.com).


## Reviews

(no reviews)
