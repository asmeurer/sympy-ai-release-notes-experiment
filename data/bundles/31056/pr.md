# Pull request #31056: refactor(matrices): decouple MatrixExpr._eval_derivative by defining independently in MatAdd and MatMul

- Author: @ish1416
- Merged: 2026-11-13T11:19:47Z into `master`
- Labels: (none)
- Size: +44 / -10 in 4 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Follow-up to #31004 as discussed with @sylee957.
Addresses item E4-20 from #30900.

#### Brief description of what is fixed or changed

In #31004, we discussed decoupling `MatrixExpr._eval_derivative` from the core `Basic`/`Expr` fallback:
```python
# Removed from MatrixExpr._eval_derivative:
eval_derivative = getattr(super(), "_eval_derivative", None)
if eval_derivative is not None:
    return eval_derivative(x)
```

This PR decouples `MatrixExpr` by defining independent derivative evaluations directly on the container classes:

1. **`MatAdd._eval_derivative`**: Implements direct term-wise derivative:
   $$\frac{d}{dx} \sum_i A_i = \sum_i \frac{d A_i}{dx}$$
   without falling back through core `Add`.
2. **`MatMul._eval_derivative`**: Implements the non-commutative matrix product rule:
   $$\frac{d}{dx} (A_1 \dots A_k) = \sum_{i=1}^k A_1 \dots A_{i-1} \left(\frac{d A_i}{dx}\right) A_{i+1} \dots A_k$$
   preserving factor ordering and filtering out zero terms.
3. **`MatrixExpr._eval_derivative`**: Returns `None` when `self.has(x)` (leaving unevaluated `Derivative`), and `ZeroMatrix(*self.shape)` when independent of `x`.

#### Other comments

All 306 tests in `sympy/matrices/expressions/tests/` pass with zero regressions.

#### AI Generation Disclosure

I used an AI assistant to explore test cases. I reviewed the change, ran the tests and doctests locally, and I can explain the code and the reasoning behind it.

## Commits

- 2dfa71bc2e (Ishita Singh): refactor(matrices): decouple MatrixExpr._eval_derivative by defining independently in MatAdd and MatMul

## Conversation

(no comments)

## Reviews

(no reviews)
