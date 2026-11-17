# Pull request #31019: core: make subs faster by short-circuiting Basic.is_same

- Author: @deadstrobe5
- Merged: 2026-11-11T02:45:12Z into `master`
- Labels: (none)
- Size: +51 / -5 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Speeds up the cases in #10697 and #22240 (does not close them).

#### Brief description of what is fixed or changed

`Basic._subs` calls `_aresame(self, old)` on every node, and the fallback calls `_aresame` on every argument. Each call walked both subtrees in postorder, so a substitution cost roughly size times depth and was paid again for each pair in the mapping.

When `approx` is None, `is_same` now returns True for the same object, returns False when the root classes differ (the old walk always ended with that same class check at the root), and compares two arg-less Basic leaves with `==` directly. The loop also tests `a is None or b is None` instead of `None in t`, which called `Basic.__eq__(None)` twice per node. The `approx` path is unchanged.

Same-process A/B on CPython 3.14, median of 5 alternating runs, cache cleared before each run:

| case | before | after | speedup |
|---|---|---|---|
| 8x8 Matrix.subs with a 200-symbol dict | 4872 ms | 1062 ms | 4.6x |
| `((x+1)**2 + 1).subs(d)`, 3000-key dict (#10697) | 494 ms | 97 ms | 5.1x |
| expanded `(x+y+z+w+1)**10`, `subs(x, t+1)` | 117 ms | 59 ms | 2.0x |
| small expr subs x2000 | 652 ms | 454 ms | 1.4x |
| `x.subs(x, k)` x5000 | 72 ms | 25 ms | 2.9x |

#### Other comments

A differential fuzz of the old and new `is_same` (and `subs`, `subs(simultaneous=True)`) over about 14,500 random expression pairs, including numbers, Floats, Tuples, non-commutative symbols, Python ints and the `equal_valued` approx, found no difference. The new test covers equal-but-distinct `UndefinedFunction` classes, which must still compare the same.

#### AI Generation Disclosure

Claude Code (Claude Opus 5.5) wrote all of the code and tests in this PR and ran the benchmarks and the old-vs-new comparisons quoted above.

## Commits

- b83948e8e3 (deadstrobe5): core: make subs faster by short-circuiting Basic.is_same
- 00698092e2 (deadstrobe5): Sort .mailmap entry
- fc376ca925 (Christopher Smith): handle float('nan') like S.NaN
- 12452f0455 (Christopher Smith): handle float('nan') like S.NaN tests
- 9fa0787f78 (Christopher Smith): whitespace fix

## Conversation

### @smichr commented

Having worked on `ordered` it is nice to see this change here. Thanks!


## Reviews

### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @smichr reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @smichr commented on `sympy/core/basic.py`

```suggestion
            if not (a is b or a == b and a.__class__ == b.__class__):
```

### @smichr commented on `sympy/core/basic.py`

With that, then the following will pass (and should be added to tests):
```python
f1 = float('nan')
f2 = float('nan')
b1 = Basic(f1)
b2 = Basic(f1)

assert f1 is not f2
assert b1 is not b2

assert _aresame(f1, f1)
assert not _aresame(f1, f2)
assert _aresame(b1, b1)
assert _aresame(b1, b2)
assert not _aresame(b1, Basic(f2))

assert not _aresame(f1, S.NaN)
assert not _aresame(b1, Basic(S.NaN))
```

### @smichr commented on `sympy/core/tests/test_subs.py`

```suggestion
    assert _aresame(f1x, f2(x))
    # float('nan') behaves the same as S.NaN
    f1 = float('nan')
    f2 = float('nan')
    b1 = Basic(f1)
    b2 = Basic(f1)
    
    assert f1 is not f2
    assert b1 is not b2
    
    assert _aresame(f1, f1)
    assert not _aresame(f1, f2)
    assert _aresame(b1, b1)
    assert _aresame(b1, b2)
    assert not _aresame(b1, Basic(f2))
    
    assert not _aresame(f1, S.NaN)
    assert not _aresame(b1, Basic(S.NaN))
```

### @oscarbenjamin commented on `sympy/core/tests/test_subs.py`

This fails on PyPy.
