# Pull request #30983: fix(matrices): restrict MatPow adjoint and conjugate to nonnegative integer powers

- Author: @ish1416
- Merged: 2026-11-08T04:57:40Z into `master`
- Labels: (none)
- Size: +32 / -2 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes item E1-6 from #30900.

#### Brief description of what is fixed or changed

In `MatPow._eval_adjoint` and `MatPow._eval_conjugate`, evaluating powers for general complex exponents or negative exponents can be mathematically invalid:
- For general complex exponents $z$, $(M^z)^\dagger \neq (M^\dagger)^{\bar{z}}$ whenever eigenvalues lie on the negative real branch cut (e.g. for $M = [-1]$, $(-1)^i = e^{-\pi} \in \mathbb{R}$, so its conjugate is $e^{-\pi}$, whereas $(-1)^{-i} = e^\pi$).
- For negative powers ($n < 0$), $M^n$ is not well-defined if $M$ is singular.

This PR restricts `MatPow._eval_adjoint` and `MatPow._eval_conjugate` to non-negative integer powers (`exp.is_integer and exp.is_nonnegative`):
- For non-negative integers ($n \ge 0$), $M^n$ is defined as repeated matrix multiplication for all square matrices (with $M^0 = I$), where $(M^n)^\dagger = (M^\dagger)^n$ and $(M^n)^* = (M^*)^n$ hold unconditionally.
- Negative powers and non-integer powers remain unevaluated when matrix spectrum or invertibility is unknown.
- (Explicit matrix inverses defined via `Inverse` continue to handle their own adjoints and conjugates in `inverse.py`).
- Added regression tests covering non-negative integer powers and verifying that negative/complex powers remain unevaluated.

#### Other comments

All tests in `test_matpow.py` and `sympy/matrices/expressions/tests/` pass locally.

#### AI Generation Disclosure

Prepared and verified with an AI coding assistant (Antigravity). Tested against SymPy's explicit matrix evaluation and local test suite.

## Commits

- 34d402c29b (Ishita Singh): fix(matrices): conjugate scalar exponent in MatPow._eval_adjoint and _eval_conjugate
- 3449f375f2 (Ishita Singh): fix(matrices): restrict MatPow adjoint and conjugate to nonnegative integer powers

## Conversation

### @sylee957 commented

I think that this can be mathematically incorrect:

for 1*1 matrix the matrix power should be trivially same as scalar power
and `conjugate((-1)**I)` which is `(-1)**I` is not same as `(-1)**conjugate(I)` which is `(-1)**(-I)`
and similar as diagonal matrix
maybe the general class of problems happen when eigenvalues of matrix are negative (which is delicate condition that we cannot represent with assumptions)

so probably instead we should restrict the exponent to `is_real` and don't use conjugate

### @sylee957 commented

Also if you used AI to generate code even not for PR description you should add them for AI disclosure. 
I notice that in the history you disclosed about using Antigravity and then that comment is removed to "NO AI USE" but should not be

### @ish1416 commented

Thank you for pointing that out @sylee957, and apologies for the confusion regarding the disclosure! I had mistakenly thought the section was only meant for AI-generated text in the PR description rather than coding assistance, but I completely understand and respect the policy now and have restored the full disclosure in the description.

Regarding the mathematics, you are completely right. For $M = [-1]$, $(-1)^i = \exp(i \cdot i\pi) = e^{-\pi}$, which is purely real, so its conjugate is $e^{-\pi}$. Meanwhile, $(-1)^{-i} = \exp(-i \cdot i\pi) = e^{\pi}$ — they differ by $e^{2\pi} \approx 535.49$ because of the branch cut on the negative real axis.

Looking further into restricting to `is_real`: even for a real fractional power like $r = 1/2$, we run into the same branch cut issue on negative eigenvalues:
$$((-1)^{1/2})^* = \bar{i} = -i$$
$$((-1)^*)^{1/2} = (-1)^{1/2} = +i$$
So $((-1)^{1/2})^* \neq ((-1)^*)^{1/2}$ even when the exponent is real.

In `sympy/core/power.py`, scalar `Pow._eval_conjugate` handles this exact problem by only distributing conjugation if `exp.is_integer` (or if `base.is_positive`), and returning `None` otherwise to leave `conjugate(base**exp)` safely unevaluated.

Would you prefer that we align with that core convention in `MatPow`?
```python
def _eval_adjoint(self):
    base, exp = self.args
    if exp.is_integer:
        return MatPow(base.adjoint(), exp)
    return None

def _eval_conjugate(self):
    base, exp = self.args
    if exp.is_integer:
        return MatPow(base.conjugate(), exp)
    return None
```
This would safely evaluate all integer powers (where $(M^n)^\dagger = (M^\dagger)^n$ holds for all matrices regardless of spectrum) while keeping non-integer powers unevaluated whenever the spectrum is unknown.

### @sylee957 commented

For negative integers matrix power for singular matrix is not well-defined. So sufficient condition should be only natural numbers `is_nonnegative`. Zero can be fine

### @ish1416 commented

Thanks for the guidance @sylee957! That makes complete sense. Since $M^n$ for $n < 0$ requires invertibility, restricting the simplification strictly to non-negative integers (`exp.is_integer and exp.is_nonnegative`) guarantees that $M^n$ is well-defined as repeated matrix multiplication for all square matrices (including singular ones, with $M^0 = I$), without risking undefined inverses or branch-cut issues.

I have updated the implementation in commit 3449f37 to restrict `_eval_adjoint` and `_eval_conjugate` to `exp.is_integer and exp.is_nonnegative`, returning `None` otherwise. I also updated the regression tests to check non-negative integer powers and verify that negative and complex powers remain safely unevaluated.


## Reviews

(no reviews)
