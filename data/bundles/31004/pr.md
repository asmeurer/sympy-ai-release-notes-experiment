# Pull request #31004: fix(matrices): implement scalar derivative for Inverse and safe dispatch in Trace

- Author: @ish1416
- Merged: 2026-11-12T09:42:05Z into `master`
- Labels: (none)
- Size: +49 / -5 in 4 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes item E4-20 from #30900.
Also addresses item 31 in #30902.

#### Brief description of what is fixed or changed

When taking the derivative of a trace of an inverse with respect to a scalar, like `Trace(Inverse(x*X + Z)).diff(x)`, SymPy currently crashes with:
```pytb
TypeError: input to Trace, Derivative((x*X + Z)**(-1), x), is not a matrix
```

##### Why this happens
1. `Trace._eval_derivative` calls `trace(expr.arg.diff(v))`.
2. `Inverse` didn't have its own `_eval_derivative`, so it inherited from `MatPow`. But `MatPow._eval_derivative` only handles non-negative powers, returning `None` for `-1`.
3. When `_eval_derivative` returns `None`, SymPy wraps it in an `ArrayDerivative`, which has `is_Matrix = False`.
4. Passing that into `trace(...)` causes `Trace.__new__` to raise `TypeError` because it expects a matrix.

##### How this PR fixes it
1. **Added `Inverse._eval_derivative` for scalar variables:** Uses $(M^{-1})' = -M^{-1} M' M^{-1}$, keeping the non-commutative order. Matrix derivatives (`hasattr(x, "shape")`) still return `None` so the tensor array engine handles them as before.
2. **Safe fallback in `Trace._eval_derivative`:** Before calling `trace(...)`, it checks `getattr(darg, 'is_Matrix', False)`. If the inner derivative isn't a matrix, it returns `None` so `diff()` leaves it as an unevaluated `Derivative(Trace(...), v)` instead of raising an error.

Added tests in `test_trace.py` and `test_inverse.py`.

#### Other comments

All tests in `sympy/matrices/expressions/tests/` pass locally.

#### AI Generation Disclosure

I used an AI assistant (Antigravity) to help explore the math and draft the code. I have personally worked through and verified the derivation and the problem myself, checked it against explicit matrix derivatives, and understand all the changes here. I'm happy to explain any part or make adjustments during review.

## Commits

- adfdae0bc8 (Ishita Singh): fix(matrices): implement scalar derivative for Inverse and safe dispatch in Trace
- 70adfd8b0e (Ishita Singh): style: import S in trace.py
- 845edbc5c8 (Ishita Singh): ci: re-trigger tests
- ff9f854d48 (Ishita Singh): style(matrices): remove hasattr and getattr from inverse and trace derivative dispatch
- 25f5f890bd (Ishita Singh): style(matrices): simplify inverse derivative dispatch and format tests
      - Remove redundant is_ZeroMatrix check in Inverse._eval_derivative
      - Format test lines to conform to PEP8 line length limits
- 38eadf4648 (Ishita Singh): Merge remote-tracking branch 'upstream/master' into fix-trace-inverse-derivative
- 8624f9f81a (Ishita Singh): refactor(matrices): simplify Trace._eval_derivative dispatch
- 43d8964e59 (Ishita Singh): style: remove unused imports in trace and test_trace
- f49906eccd (Ishita Singh): refactor(matrices): simplify Inverse._eval_derivative to single expression

## Conversation

### @sylee957 commented

Can you avoid using `getattr, hasattr` if possible? in runtime the objects should mostly be sympy Basic or MatrixExpr where they are not necessary

### @ish1416 commented

Makes total sense, thanks! I went through both files and replaced `hasattr`/`getattr` with direct property checks:

- Switched `hasattr(x, 'shape')` to `if x.is_Matrix: return None` in `Inverse._eval_derivative` so matrix-wrt-matrix derivatives still pass through to `ArrayDerivative`.
- Since all `Basic` instances have `is_Matrix` and `MatrixExpr` has `is_ZeroMatrix`, I replaced `getattr` with direct `.is_Matrix` and `.is_ZeroMatrix` checks in both `Inverse` and `Trace`.

All 291 matrix expressions tests and flake8 pass cleanly.

### @sylee957 commented

Can you ask AI to investigate alternative.

The PR seems like it reveals more fundamental issue than.
Generally, `_eval_derivative` should either return None or definite expression and should not recursively call _eval_derivative.

```
        expr = self.doit()
        if isinstance(expr, Trace):
            # Avoid looping infinitely:
```
Although this guard works on direct recursion, this raises concern that this may not work on indirect recursion.

Also we have many concern that more special-case rules are added inside `_eval_derivative` than necessary.
The dispatcher being able to handle them generally or we may intend to fix that.

The derivative of Trace should be as simple as:
```
        if isinstance(v, MatrixElement):
            return self.rewrite(Sum).diff(v)
        return trace(self.arg.diff(v))
```

We should also consider removing general eval_derivative fallback in `MatrixExpr` but define `_eval_derivative` independently in MatAdd/MatMul
```
            eval_derivative = getattr(super(), "_eval_derivative", None)
            if eval_derivative is not None:
                return eval_derivative(x)
```

Please investigate if this is better alternative and how much scope of changes/tests it may anticipate.

### @ish1416 commented

Good point! I went ahead and simplified `Trace._eval_derivative` to:

```python
    if isinstance(v, MatrixElement):
        return self.rewrite(Sum).diff(v)
    return trace(self.arg.diff(v))
```

Since `Inverse._eval_derivative` now gives `- M**-1 * M' * M**-1`, `trace(self.arg.diff(v))` works directly without needing `doit()` or extra guards. All 291 matrix expressions tests pass cleanly, pushed the update!

About removing the `super()` fallback from `MatrixExpr._eval_derivative`:
I looked into it, and we'd just need to give `MatAdd` a term-wise derivative and `MatMul` a non-commutative product rule ($\sum_i A_1 \dots A_i' \dots A_k$). That would cleanly decouple `MatrixExpr` from core's MRO. 

Do you want to do that in a follow-up PR to keep this one focused on `Inverse`, or happy for me to bundle it here?

### @sylee957 commented

> About removing the `super()` fallback from `MatrixExpr._eval_derivative`:
I looked into it, and we'd just need to give `MatAdd` a term-wise derivative and `MatMul` a non-commutative product rule ($\sum_i A_1 \dots A_i' \dots A_k$). That would cleanly decouple `MatrixExpr` from core's MRO. 

> Do you want to do that in a follow-up PR to keep this one focused on `Inverse`, or happy for me to bundle it here?

Sure we should do it but we want to do it in follow up PR

### @ish1416 commented

Sounds good, I'll open a follow-up PR for that once this lands!


## Reviews

### @sylee957 reviewed: COMMENTED



### @ish1416 reviewed: COMMENTED



### @sylee957 commented on `sympy/matrices/expressions/inverse.py`

Can you ask AI if it can simplify to `return -self * self.arg.diff(x) * self`

### @ish1416 commented on `sympy/matrices/expressions/inverse.py`

Simplified! Just tested `return -self * self.arg.diff(x) * self` directly — constant matrices cleanly evaluate to 0 through `MatMul` and all 291 matrix expressions tests pass. Pushed the update.
