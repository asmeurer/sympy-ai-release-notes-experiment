# Pull request #30994: fix(core): remove non-Basic args workarounds

- Author: @oscarbenjamin
- Merged: 2026-11-08T21:04:01Z into `master`
- Labels: core, tensor, typing
- Size: +58 / -45 in 6 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

See https://github.com/sympy/sympy/pull/30990#discussion_r4507118047

#### Brief description of what is fixed or changed

Remove the hacky workaround in Basic.xreplace and other methods that try to allow non-Basic args in Basic. It should not be necessary to have to do things like that and it is better if non-Basic args lead to runtime errors so that people stop putting non-Basic in the args.

A few buggy classes were fixed.

#### Other comments

#### AI Generation Disclosure

Used codex for the tensor/codegen fixes.

## Commits

- 833048d456 (Oscar Benjamin): fix(core): remove non-Basic args workaround in xreplace
- 57b1aade23 (Oscar Benjamin): fix(core): remove workaround in Basic.sort_key
      All args should be Basic.
- dc6f2182a2 (Oscar Benjamin): fix(core): remove hacky subs workaround
      All args should be Basic
- 8e758a115b (Oscar Benjamin): fix(core): remove hacky workaround in Basic.replace
      The args should always be Basic.
- 94121be183 (Oscar Benjamin): fix(core): remove hacky workaround in Basic.doit
      All args should be Basic.
- 6f8d7a8152 (Oscar Benjamin): fix(core): remove hacy workaround in Expr._expand_hint
      All args should be Basic.
- 3ca9a0f568 (Oscar Benjamin): fix(codegen): handle nested arrays in reshape
- 6515187a7b (Oscar Benjamin): tst(codegen): regression tests for hash/sort_key/doit

## Conversation

### @oscarbenjamin commented

This is ready for review.

### @oscarbenjamin commented

@smichr I deliberately kept the commits in this PR separate and tested them separately. You have merged them but squashed them altogether into one commit e2e2ee4.

Now if this PR causes a problem it will not be possible for someone to bisect and find which of the different changes here is relevant. Please do not squash-merge my PRs. I will squash the commits manually if I think there is any value in doing that.

### @oscarbenjamin commented

To be clear: thank you for reviewing and merging.

I do appreciate that but please also check whether you are squash merging (github carries the setting over from one PR to another by default).


## Reviews

### @smichr reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @smichr commented on `sympy/codegen/fnodes.py`

In discussing with ChatGPT, we observe that you might need recursion here to process the elements of `arg`.

Consider adding a test like:

```python
def test_reshape_nested_lists():
    e = reshape([[1, 2], [3, 4]], [2, 2])
    e.sort_key()
    e.doit()
```

Both calls currently raise `AttributeError` because the nested Python lists are not converted to SymPy objects.

The defensive checks removed from `Basic` previously tolerated these non-`Basic` arguments, but their removal exposes the malformed `ArrayConstructor`. I'm not sure how `reshape` is intended to handle nested lists, so it may be better to normalize them recursively or reject them explicitly if they are unsupported.

### @oscarbenjamin commented on `sympy/codegen/fnodes.py`

Are those valid arguments to this function?

### @oscarbenjamin commented on `sympy/codegen/fnodes.py`

I've added something to handle this case.

### @smichr commented on `sympy/codegen/tests/test_fnodes.py`

These operations also passed before the changes in this PR. Since we're removing defensive checks from `Basic`, it would be good to add a regression test ensuring that they continue to work:

```python
from sympy.codegen.fnodes import reshape

e = reshape([[1, 2], [3, 4]], [2, 2])
hash(e)
e.sort_key()
e.doit()
```

In the event of (inlikely) future changes we don't want to inadvertently re-introduce non-`Basic` arguments or break operations that previously worked.

### @oscarbenjamin commented on `sympy/codegen/tests/test_fnodes.py`

I've added that.
