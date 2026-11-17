# Pull request #31097: matrices: use Q.H instead of Q.T in QRsolve for complex matrices

- Author: @hardikkaurani
- Merged: 2026-11-14T18:45:16Z into `master`
- Labels: (none)
- Size: +23 / -1 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #31096
Related to #30900 (item M2-2)

#### Brief description of what is fixed or changed

In `_QRsolve` (`sympy/matrices/solvers.py`), `y = Q.T * b` was used to solve $Rx = y$. For complex matrices, $Q$ from QR decomposition is unitary ($Q^H Q = I$) rather than orthogonal ($Q^T Q \neq I$), which caused `QRsolve` to return incorrect solutions where $Ax \neq b$, as well as incorrect matrix inverses in `A.inv(method='QR')`.

This patch updates line 426 to compute `y = Q.H * b`. Since $Q^H = Q^T$ for real matrices, behavior for real linear systems is identical, while complex linear systems now yield exact zero residuals. Regression tests have been added to `sympy/matrices/tests/test_solvers.py` covering single-column and multi-column complex systems and complex matrix inversion via QR.

#### Other comments

All tests in `sympy/matrices/tests/test_solvers.py` and `sympy/matrices/tests/test_decompositions.py` pass locally.

#### AI Generation Disclosure

Assisted by Google Gemini in tracing the residual error and structuring the regression test cases.

## Commits

- da45ad1761 (Hardik Kaurani): matrices: use Q.H instead of Q.T in QRsolve for complex matrices
      For complex matrices, Q from QR decomposition is unitary (Q.H * Q = I),
      but generally not orthogonal (Q.T * Q != I). Using y = Q.T * b in
      _QRsolve resulted in incorrect solutions where A * x != b and wrong
      inverses when calling A.inv(method='QR').
      This patch updates _QRsolve to use y = Q.H * b, ensuring exact solutions
      for complex linear systems and preserving identical behavior for real
      matrices. Also adds regression tests in test_solvers.py covering complex
      systems, multi-column RHS, and QR-based matrix inversion.
      Fixes #31096.

## Conversation

### @hardikkaurani commented

Hello @Upabjojr, @sylee957,

This PR resolves #31096 by updating `_QRsolve` in `sympy/matrices/solvers.py` to use `y = Q.H * b` instead of `y = Q.T * b`.

For complex matrices, $Q$ from QR decomposition is unitary ($Q^H Q = I$), whereas $Q^T Q \neq I$. Using transpose caused `QRsolve` to return incorrect solutions for non-real systems and resulted in invalid matrix inverses in `A.inv(method='QR')`.

With this fix:
- Complex linear systems now solve with exact zero residuals.
- Complex matrix inversion via `A.inv(method='QR')` satisfies `inv * A == eye(n)`.
- Real matrices remain completely unaffected since $Q^H = Q^T$ for real entries.
- Regression tests have been added to `test_solvers.py` covering single and multi-column complex systems as well as QR matrix inversion.

Whenever you have a chance, I would appreciate your review and feedback. Thank you!


## Reviews

(no reviews)
