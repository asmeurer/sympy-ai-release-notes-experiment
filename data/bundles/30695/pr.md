# Pull request #30695: make Stirling numbers take `Θ(k*(n-k))` ops instead of `Θ(k*(n-k/2))`

- Author: @DroneBetter
- Merged: 2026-11-11T16:12:32Z into `master`
- Labels: ntheory, functions
- Size: +27 / -9 in 1 files (full diff in `diff.patch`)

## Description

i have [another branch](https://github.com/DroneBetter/sympy/tree/stirling_D-finitude) where i started working on a more meaningful change making both `stirling` functions cached, but that meant dealing with the recursion limit, and switching to the formula for `n` over some threshold causes a sudden jump to lower performance than currently (and deciding on a strategy to get around this without making the code size too unwieldy will be nontrivial), so i decided to make an extremely easy-to-review drop-in PR in the meantime.

#### References to other Issues or PRs
the only one vaguely applicable to this is #14616 which presents more advanced strategies; my PR from the interesting branch will discuss those in detail in this section.

#### Brief description of what is fixed or changed
the existing version generates all Stirling numbers `stirling(h,j)` with `h<=n,j<=k`, forming a trapezoid (triangle with a rectangle beneath it), then throws away all but `stirling(n,k)`; in fact, we can cut out a triangle to form a parallelogram by adding the additional constraint `h-j<=n-k`.

this implements that by changing `row` to be a row of the array `T(h,j) = stirling(h+j,j)` instead of a row of the number triangle, so the length is constant and it can be implemented as a prefix sum.

#### Other comments
it is about twice as fast to generate each element of a full row, since $\int_{k=0}^nk(n-k)=\frac{n^3}6$ instead of $\int_{k=0}^nk(n-k/2)=\frac{n^3}3$.

this is approximately evidenced by unrigorous profiling:
```python
>>> from sympy.functions.combinatorial.numbers import _stirling1 as cycle,_stirling2 as subset
>>> n=400;from time import time;t=time();print(hash(tuple(subset(n,k) for k in range(n+1))),time()-t)
-1829327518960325621 7.069313049316406 #before
-1829327518960325621 3.110057830810547 #after
>>> #after restarting the shell to clear cache:
>>> n=400;from time import time;t=time();print(hash(tuple(cycle(n,k) for k in range(n+1))),time()-t)
-1165711630153352067 7.355808973312378 #before
-1165711630153352067 3.1521079540252686 #after
```
(in fact, it seems slightly better than twice as fast, since operations are not constant-time; most of the 'weight' (measured in bit length) of the Stirling triangles is towards the left side, since the first kind are asymptotically Poisson with rate parameter $\sim\log n$ while the second kind are asymptotically normal with expectation $\sim{n\over\log n}$ and variance $\sim{n\over\log^2n}$.)

this is of course still very slow (since most of the computation is still being duplicated), but i will handle that Later ahaha

#### AI Generation Disclosure
NO AI USE

## Commits

- 9811af084e (DroneBetter): make Stirling numbers take `Θ(k*(n-k))` ops instead of `Θ(k*(n-k/2))`
      going to do a bigger change that replaces it with a `cache` but this shall be much easier to review
- e50f58fab5 (DroneBetter): make `_stirling` output `Integer` always
      oops thank you for catching

## Conversation

### @oscarbenjamin commented

Okay, looks good. Thanks


## Reviews

### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @DroneBetter reviewed: COMMENTED



### @DroneBetter reviewed: COMMENTED



### @oscarbenjamin commented on `sympy/functions/combinatorial/numbers.py`

This should return Integer rather than int e.g. `return S.Zero` or return `Integer(n == 0)`.

### @oscarbenjamin commented on `sympy/functions/combinatorial/numbers.py`

Same in other places.

### @DroneBetter commented on `sympy/functions/combinatorial/numbers.py`

I somewhat disagree, on the basis that
* it doesn't do so already
* its only use either way is wrapped in another function that converts its output to `Integer`
* `Integer` is faster (with gmpy or flint) when you need to multiply large bigints with each other, but (aiui) Toom-Cook/FFT-based multiplication algorithms require both numbers to be large for them to be effective; the coefficients are always small because they're bounded by the number of iterations taken
(this is the same philosophy as #30687)

### @DroneBetter commented on `sympy/functions/combinatorial/numbers.py`

wait nvm it does do so already sorry
