# Issues and pull requests referenced by this pull request

## Issue #31130: algebras: Quaternion.from_rotation_matrix returns zero quaternion for 180-degree rotations

- Opened by @hardikkaurani, state: closed

### Problem Description

When converting a $3 \times 3$ rotation matrix corresponding to a $180^\circ$ ($\pi$ radians) rotation around any 3D axis to a `Quaternion` via `Quaternion.from_rotation_matrix(M)`, it returns the zero quaternion `0 + 0*i + 0*j + 0*k` instead of a valid unit quaternion.

As a consequence, round-tripping any $180^\circ$ rotation quaternion via `q.to_rotation_matrix()` and `Quaternion.from_rotation_matrix()` fails completely and yields `0`, whose `.to_rotation_matrix()` subsequently produces a matrix of `nan`s due to division by zero norm.

### Minimal Reproducible Example

```python
from sympy import Matrix, eye, sqrt
from sympy.algebras.quaternion import Quaternion

# 1. 180-degree rotation around z-axis: diag(-1, -1, 1)
Rz = Matrix([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
qz = Quaternion.from_rotation_matrix(Rz)
print("qz:", qz)
# Actual output:   0 + 0*i + 0*j + 0*k   (norm = 0)
# Expected output: 0 + 0*i + 0*j + 1*k   (norm = 1)

# Round-trip failure
q_orig = Quaternion(0, 0, 0, 1)
R = q_orig.to_rotation_matrix()
q_rec = Quaternion.from_rotation_matrix(R)
print("q_rec:", q_rec)
# Output: 0 + 0*i + 0*j + 0*k

# 2. 180-degree rotation around x-axis: diag(1, -1, -1)
Rx = Matrix([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
print("qx:", Quaternion.from_rotation_matrix(Rx))
# Actual:   0 + 0*i + 0*j + 0*k
# Expected: 0 + 1*i + 0*j + 0*k

# 3. 180-degree rotation around arbitrary unit axis u = (1, 1, 1)/sqrt(3):
# R = 2 * u * u.T - eye(3)
u = Matrix([1, 1, 1]) / sqrt(3)
R_arbitrary = 2 * u * u.T - eye(3)
print("q_arbitrary:", Quaternion.from_rotation_matrix(R_arbitrary))
# Actual:   0 + 0*i + 0*j + 0*k
# Expected: 0 + sqrt(3)/3*i + sqrt(3)/3*j + sqrt(3)/3*k
```

### Root Cause

In `sympy/algebras/quaternion.py` (lines 686–696):

```python
absQ = M.det()**Rational(1, 3)

a = sqrt(absQ + M[0, 0] + M[1, 1] + M[2, 2]) / 2
b = sqrt(absQ + M[0, 0] - M[1, 1] - M[2, 2]) / 2
c = sqrt(absQ - M[0, 0] + M[1, 1] - M[2, 2]) / 2
d = sqrt(absQ - M[0, 0] - M[1, 1] + M[2, 2]) / 2

b = b * sign(M[2, 1] - M[1, 2])
c = c * sign(M[0, 2] - M[2, 0])
d = d * sign(M[1, 0] - M[0, 1])

return cls(a, b, c, d)
```

For any $180^\circ$ rotation matrix around a unit axis $\vec{u}$, the matrix is symmetric ($M = 2\vec{u}\vec{u}^T - I = M^T$) with $\mathrm{trace}(M) = -1$:
1. Since $\mathrm{trace}(M) = -1$, the scalar part $a = \sqrt{1 + (-1)} / 2 = 0$.
2. Since $M$ is symmetric, all antisymmetric off-diagonal differences are zero:
   - $M[2, 1] - M[1, 2] = 0 \implies \mathrm{sign}(0) = 0$
   - $M[0, 2] - M[2, 0] = 0 \implies \mathrm{sign}(0) = 0$
   - $M[1, 0] - M[0, 1] = 0 \implies \mathrm{sign}(0) = 0$
3. Multiplying $b, c, d$ by `sign(...)` unconditionally multiplies them by $0$, wiping out the vector part of the quaternion.

Consequently, `cls(a, b, c, d)` always produces `Quaternion(0, 0, 0, 0)`.

### Proposed Solution

When $a = 0$ (or when all antisymmetric differences vanish / $M$ is symmetric), the signs and magnitudes of the vector components $(b, c, d)$ should be determined from the symmetric terms (e.g. standard Shepperd's / Shoemake's method: $M_{01} + M_{10} = 4bc$, $M_{02} + M_{20} = 4bd$, $M_{12} + M_{21} = 4cd$) using the largest diagonal component, rather than multiplying by `sign(M[j, k] - M[k, j])` which zeroes them out.
