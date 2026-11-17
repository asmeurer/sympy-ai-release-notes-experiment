# Pull request #30990: 🤖 Annotate Basic.xreplace

- Author: @hunterhogan
- Merged: 2026-11-13T17:21:24Z into `master`
- Labels: core, typing
- Size: +81 / -14 in 8 files (full diff in `diff.patch`)

## Description

🤖 *This description was drafted by an AI agent (Claude Code) and revised by Hunter Hogan.*

#### References to other Issues or PRs

Related typing PRs: #30946 (`solveset`), #30965 (`piecewise_fold`).

#### Brief description of what is fixed or changed

- Annotates `Basic.xreplace` and adds type-checking-only overloads for some subclasses. 
- `Atom.xreplace` replaced by `Atom._xreplace`
- Change `rule` parameter dictionary keys to TypeVars.

#### Other comments

<details><summary>Other</summary>
- `TensExpr.xreplace` needs `# type: ignore[override]`: mypy rejects a leading overload that `Expr.xreplace` lacks.
- Known gap: a `Symbol` statically typed as `Boolean` matches `Boolean`'s `Expr`-to-`Expr` overload, so `p.xreplace({p: sin(x)})` is typed `Boolean`.
</details>

#### AI Generation Disclosure

Generated with Claude Code (Claude Opus 5.5), Hunter Hogan, and Predator Energy Drink.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Commits

- 053727223c (Hunter Hogan): Annotate Basic.xreplace
      Basic.xreplace takes Mapping[Any, Basic] and returns Basic. Expr and
      Boolean get TYPE_CHECKING overloads next to their subs overloads: Expr
      values on an Expr give Expr, and Expr or Boolean values on a Boolean
      give Boolean. Keys are Any because Mapping keys are invariant.
      _xreplace no longer rebinds args from a list to a tuple, which mypy
      rejects; self.func(*args) unpacks either.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- dde7e7ae59 (Hunter Hogan): Ignore Poly.xreplace result types in summations
      numer and denom are Poly, which is a Basic but not an Expr, so the
      annotated xreplace returns Basic; at runtime it returns a Poly.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- b0c993cb39 (Hunter Hogan): Type xreplace rule keys as Basic instead of Any
      The public xreplace signatures take Mapping[Tbasic, Basic], with Tbasic
      bound to Basic, so keys must be Basic (xreplace does not sympify) and a
      dict[Symbol, Expr] is still accepted even though Mapping keys are
      invariant. The private _xreplace keeps Mapping[Any, Basic]: it looks up
      rule[self] with a Basic, which typeshed only allows for the mapping's own
      key type.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- eff72f140b (Hunter Hogan): Replace Atom.xreplace with Atom._xreplace
      Atom.xreplace was an untyped override with a hack2 parameter that nothing
      uses since Basic.xreplace dropped it. Because Atom precedes Expr in the
      MRO of AtomicExpr, it hid Expr's xreplace overloads, so x.xreplace(...)
      was untyped for every Symbol and number. Atoms now use Basic.xreplace and
      override _xreplace, which keeps them from recursing into args.
      Without the override, NewSymbol in test_tensor needs an xreplace stub to
      satisfy mypy, like its existing subs and simplify stubs.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- 3515b64aba (Hunter Hogan): Declare xreplace result types for Poly and Set
      Poly.xreplace returns the same kind of Poly, so a TYPE_CHECKING stub
      returns Self and the type: ignore comments in summations.py are no longer
      needed. Set gets overloads like Boolean's: Expr or Set values give a Set,
      other Basic values give Basic. As with Boolean, this is unsound only when
      a rule key is the whole set.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- 45d1ae1ea8 (Hunter Hogan): Type MatrixBase.xreplace rule values as Expr
      Matrix entries are Expr, so with Expr rule values each entry's xreplace
      returns Expr and applyfunc type checks without type: ignore. Keys are
      Basic, as in Basic.xreplace, since neither sympifies the rule.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- 7055f8ad6b (Hunter Hogan): troubleshooting Basic._xreplace. Basic.func property is the locus of the problem.
- 0e1fdc20e3 (Hunter Hogan): Derive xreplace result types from func returning type[Self]
      Basic.func returns self.__class__, so it is annotated as type[Self] and
      rebuilding a node with self.func(*args) gives the receiver's type. With
      that, Basic.xreplace takes Mapping[Tbasic, Tvalue] and returns
      Self | Tvalue: either the rebuilt node or a value from the rule. Self is
      resolved for every subclass, so the hand-written xreplace overloads in
      Expr, Boolean and Set are removed, along with the imports only they used.
      Poly keeps its stub returning Self.
      Like Expr.__new__ -> Self, this does not account for evaluation changing
      the class (Mul(2, S.Half) is 1).
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- 03adc634a6 (Hunter Hogan): Annotate Basic.func as Callable[..., Self]
      type[Self] made generic rebuilds like expr.func(*args) check args against
      one class's constructor signature (Add, Mul and Pow differ), which failed
      in simplify.py. func is used as a rebuild callable, so Callable[..., Self]
      states its contract.
      Add.as_numer_denom rebound n from a list to an Expr; the rebuilt
      numerator and denominator now go straight into the return.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- 96315c1b1d (Hunter Hogan): Add Tvalue doc target and fix docstring typos
      Sphinx needs a py:class target for the Tvalue TypeVar in the
      xreplace signature, as it has for Tbasic.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- dce710f3e5 (Hunter Hogan): Declare Set.xreplace as returning Set
      Basic.xreplace returns Self | Tvalue, where Tvalue covers a rule key that
      is the whole expression. For a Set that case would need the set itself as
      a key, so Set.xreplace returns Set, like Poly.xreplace returns Poly. This
      anticipates gh-30946, which annotates solveset as returning Set and
      assigns Set.xreplace results to Set variables.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- b83b7a881a (Hunter Hogan): Type xreplace results per family instead of with Self
      Rebuilding an expression evaluates, so (x + y).xreplace({y: x}) is a Mul
      although the receiver is an Add. Self promised an Add. The type that
      survives evaluation is the family, so Basic.xreplace returns Basic and
      Expr, Boolean, and Set declare overloads like their subs overloads.
      Basic.func is unannotated again, and Add.as_numer_denom is restored.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- 7a2a628f7a (Hunter Hogan): type-checking-only TensExpr.xreplace. Suppress "illegal" override diagnostic. Remove now-unnecessary suppressions.
- 5680699643 (Hunter Hogan): Add overloads to Set.xreplace and Boolean.xreplace and new tests to confirm the types.
- e6a3081b16 (Hunter Hogan): Split Poly.xreplace overloads and test xreplace result types
      Poly.xreplace({poly: sin(1)}) returns sin(1), so only rules mapping
      Expr keys to Expr values keep the Poly type; other rules give Basic.
      Add type tests (runtime asserts plus assert_type under TYPE_CHECKING)
      for Basic, Expr, Poly, MatrixBase, and TensExpr xreplace.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- 987230ac2a (Hunter Hogan): Remove xreplace typing tests
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

## Conversation

(no comments)

## Reviews

### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED

I'm checking where I'm at.

- [x] Any
- [x] Test failures
- [x] Update description
- [ ] Do not get frustrated with the AI

### @hunterhogan reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED



### @oscarbenjamin commented on `sympy/concrete/summations.py`

I think that Poly needs to have a dummy xreplace method for type checking only because Poly.xreplace always returns a Poly.

The most important thing when working on typing in sympy right now is ensuring that a type checker can infer the types correctly when reading valid (non-pathological) code. Calling xreplace here on a Poly is perfectly reasonable and the type is predictable as well.

### @oscarbenjamin commented on `sympy/core/basic.py`

We should avoid using Any when possible.

I think this should probably match the subs overload for the dict case although perhaps it should be strict and say that only Basic is allowed rather than also allowing complex (and implicitly flout/int/bool).

### @oscarbenjamin commented on `sympy/core/basic.py`

Since `xreplace` does not call `sympify` we should perhaps make it more strict about input types than `subs`.

### @oscarbenjamin commented on `sympy/core/basic.py`

The type checker thinks that `a` is Basic here so it should be possible to avoid using `getattr` here.

Actually this is the kind of hacky workaround that we should try to remove if improving typing. It should never have been allowed that the `a` here might not be `Basic` at runtime.

I just removed this `getattr` hack and called xreplace directly. Then I ran the test suite and there were a few failures but we should just fix those.

### @oscarbenjamin commented on `sympy/matrices/matrixbase.py`

The types should be declared so that this does not need type: ignore.

### @oscarbenjamin commented on `sympy/matrices/matrixbase.py`

I'm not sure if that means changing the types here or in Basic.xreplace.

### @oscarbenjamin commented on `sympy/core/basic.py`

The proper way to fix something like this is to remove the hacky workaround as in gh-30994.

### @oscarbenjamin commented on `sympy/core/basic.py`

This needs updating after gh-30994 was merged.

### @hunterhogan commented on `sympy/concrete/summations.py`

0d164a8e90acf35235ae96de06e9139d89fae3f1

### @oscarbenjamin commented on `sympy/core/add.py`

Why is this changed?

### @oscarbenjamin commented on `sympy/core/basic.py`

I don't think Self should be used. It implies that e.g. an Add would xreplace to an Add which is not the case.

### @oscarbenjamin commented on `sympy/matrices/matrixbase.py`

The values need not be Expr e.g.:
```python
In [11]: p = Piecewise((x, Ne(x, 0)), (0, True))

In [12]: M = Matrix([p, 0])

In [13]: M.xreplace({Ne(x, 0): True})
Out[13]: 
⎡x⎤
⎢ ⎥
⎣0⎦
```
The common case would for both key and value to be Expr (or for `complex | float | int | bool` in the value). I'm not sure if it is better to focus on the common case rather than type completeness which is likely impossible.

### @oscarbenjamin commented on `sympy/tensor/tensor.py`

Why is type: ignore used here?

### @hunterhogan commented on `sympy/tensor/tensor.py`

It returns TensorIndex. I tried messing with TensExpr, but I couldn't get it to work.

### @hunterhogan commented on `sympy/matrices/matrixbase.py`

Widening to Basic creates conflicts with SExpr. 

> type completeness which is likely impossible

I think it is premature today, but not impossible tomorrow.

### @oscarbenjamin commented on `sympy/tensor/tensor.py`

I think that maybe this type needs to have something like this to say what xreplace would return:
https://github.com/sympy/sympy/blob/9ada6de8fa0b7dd9258af2e181a51d2fd07c7f61/sympy/core/expr.py#L77-L78

### @oscarbenjamin commented on `sympy/sets/sets.py`

I think that the first case here needs to be split into two:
```python
        @overload
        def xreplace(self, rule: Mapping[Texpr, Expr]) -> Set: ...
        @overload
        def xreplace(self, rule: Mapping[Tbasic, Set]) -> Set: ...
        @overload
        def xreplace(self, rule: Mapping[Tbasic, Basic]) -> Basic: ...
```
Otherwise e.g.
```python
In [1]: s = S.Reals

In [2]: isinstance(s, Set)
Out[2]: True

In [3]: isinstance(s.xreplace({s:sin(1)}), Set)
Out[3]: False
```

### @oscarbenjamin commented on `sympy/sets/sets.py`

Boolean.xreplace is similar

### @hunterhogan commented on `sympy/sets/sets.py`

Good plan. I've checked the other xreplace and added some tests, too.

### @oscarbenjamin commented on `sympy/sets/sets.py`

Did you forget to push?

### @hunterhogan commented on `sympy/sets/sets.py`

Worse. My computer has crashed twice. 😞 I'm working on it.

### @oscarbenjamin commented on `sympy/core/tests/test_basic.py`

We should probably make a whole separate thing in the test suite for this sort of thing.

NumPy has a `numpy/typing/tests` suite that is primarily for testing how types are inferred by type checkers.

We probably need a `sympy/typing` package although I'm not sure what should or should not go in it or how it should be structured.

I would preer not to add this kind of thing ad-hoc throughout the normal test suite though.

### @oscarbenjamin commented on `sympy/core/tests/test_basic.py`

I'm not proposing to add `sympy/testing` in this PR. We should open an issue to discuss that first if going that route.

### @hunterhogan commented on `sympy/core/tests/test_basic.py`

I'll remove the tests.

Isolated _ad hoc_ is chaos; bounded trials are experience. Consider creating .../ad_hoc/typing to encourage devs to try things and look at what other people are doing, all with the knowledge that the directory is ephemeral.
