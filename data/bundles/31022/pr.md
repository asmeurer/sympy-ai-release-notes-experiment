# Pull request #31022: Fix convolution empty input

- Author: @suchishah2807
- Merged: 2026-11-11T02:58:56Z into `master`
- Labels: (none)
- Size: +31 / -1 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs
No linked issue.
Found while testing edge cases myself.

#### Brief description of what is fixed or changed
convolution_fft([], [1, 2]) and convolution_ntt([], [1, 2], prime=...) return [0].
convolution([], [1, 2]) raises ValueError: max() iterable argument is empty.
Cause: the result length is computed as len(a) + len(b) - 1, which is 1 when one list is empty and the other has 2 items.
Fix in convolution_fft, convolution_ntt and convolution_int: return [] early if either input is empty.
Fix in convolution(): skip the zero padding when either list is empty.
File changed: sympy/discrete/convolutions.py, 11 lines added.

#### Other comments
Existing tests only covered [] with [] and [] with [1].
New test test_convolution_empty_input covers:
lengths 0 to 3, in both orders;
the prime, dyadic, subset and Rational paths;
non-empty inputs, which are unaffected.
The test fails before the fix and passes after it.
The cyclic case cycle=3 still returns [0, 0, 0].
sympy/discrete tests pass, and the doctests pass.

#### AI Generation Disclosure
AI helped find the bug by running edge-case tests.
AI wrote the first version of the fix and of the test.

## Commits

- 9cdd69c291 (suchishah2807): discrete: return [] when convolving with an empty sequence
- 6135b7934c (suchishah2807): add Suchi Shah to .mailmap
- b1941e117e (suchishah2807): Fix lint error in convolution test
- 295cbc975f (Christopher Smith): Apply batched suggestions from code review
      Co-authored-by: Christopher Smith <smichr@gmail.com>

## Conversation

(no comments)

## Reviews

### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr commented on `sympy/discrete/tests/test_convolutions.py`

```suggestion
    for kwargs in ({}, {'prime': p}):
        funcs = ((convolution, convolution_fft, convolution_int)
                 if not kwargs else (convolution, convolution_ntt))
        for func in funcs:
            for seq in ([], [1], [1, 2], [1, 2, 3]):
                assert func([], seq, **kwargs) == []
                assert func(seq, [], **kwargs) == []
    assert convolution([], [1, 2], cycle=3) == [0, 0, 0]
```

### @smichr commented on `sympy/discrete/convolutions.py`

```suggestion
    if not a or not b:
        return []
    a, b, p = a[:], b[:], as_int(prime)
```

### @smichr commented on `sympy/discrete/convolutions.py`

Quick return before copy like in the other functions.
