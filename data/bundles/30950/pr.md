# Pull request #30950: core: fix evalf Abs recursion with evaluate(False)

- Author: @raman118
- Merged: 2026-11-08T20:48:01Z into `master`
- Labels: (none)
- Size: +15 / -5 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Addresses the `get_abs` recursion case reported in #30925.

#### Brief description of what is fixed or changed

Numerically evaluating an unevaluated absolute value of a complex number could recurse indefinitely when evaluation was disabled. This computes the magnitude from the evaluated numeric components and adds a regression test.

#### Other comments

Verification:
- `python -m pytest sympy/core/tests/test_evalf.py -q` — 61 passed
- `python bin/test quality` — 6 passed
- `ruff check sympy` — passed
- `python bin/mailmap_check.py` — passed

#### AI Generation Disclosure

OpenAI Codex using GPT-6 Astra generated changes in `.mailmap`, `sympy/core/evalf.py`, and `sympy/core/tests/test_evalf.py`.

## Commits

- 7027c3af12 (raman118): core: fix evalf Abs recursion with evaluate(False)
      Co-authored-by: OpenAI Codex (GPT-6 Astra) <noreply@openai.com>
- 0c016e1906 (raman118): author: add raman118 to .mailmap
      Co-authored-by: OpenAI Codex (GPT-6 Astra) <noreply@openai.com>
- 724bf6d994 (Doremon): Add GitHub noreply email to mailmap
- a95ab776a4 (Doremon): Fix mailmap ordering
- 614277ce37 (Doremon): Merge branch 'master' into fix-evalf-get-abs-recursion-30925
- c4828f0276 (Doremon): Add Doremon to .mailmap
- a38e53ab98 (raman118): Fix ordering of Doremon mailmap entry
      AI-assisted correction by OpenAI Codex (GPT-6 Astra).
- de3c150f83 (Christopher Smith): Apply suggestion from @smichr

## Conversation

### @smichr commented

check AUTHORS error

### @smichr commented

A simple rebase on master and the force push back to here might fix the error.

### @raman118 commented

@smichr try to give it a look

### @smichr commented

I'll mark that one off on the issue. Thanks for working on this.


## Reviews

### @smichr reviewed: COMMENTED



### @smichr commented on `sympy/core/tests/test_evalf.py`

```suggestion
def test_evalf_abs_evaluate_false():
    for z, expected in (
        (1 + I, sqrt(2)),
        (10**20 + I, sqrt(10**40 + 1)),
    ):
        with evaluate(False):
            result = Abs(z, evaluate=False).evalf(50)
        assert result == expected.evalf(50)
```
