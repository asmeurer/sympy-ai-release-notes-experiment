# Issues and pull requests referenced by this pull request

## Issue #14616: Discussion for computation of Stirling Numbers

- Opened by @sidhantnagpal, state: open

The current implementation uses the following recurrence for evaluation of Stirling Numbers of 1st Kind:
`s(n + 1, k) = n*s(n, k) + s(n, k - 1)` with memoization, and is hence `O(n**2)`.

Also, by definition:
`s(n, k) = coefficient of x**n in ff(x, k)`, where `ff` is falling factorial
Using this definition with `FFT` (Fast Fourier Transform) - `O(nlg(n))`
or Karatsuba - `O(n**lg(3))`, the coefficients for the same can be evaluated. 
The overall complexity for obtaining one entire row (corresponding to `n`) would be `O(nlg(n)**2)` or `O(n**lg(3) lg(n))` depending on the method used. The extra log factor is due to divide and conquer employed to calculate `x*(x - 1)*(x - 2)...(x - (k - 1))`.

Similar recurrence for Stirling Numbers of 2nd Kind:
`S(n + 1, k) = k*S(n, k) + S(n, k - 1)` with memoization, and is hence `O(n**2)`.

The closed form expression for `S(n, k)` is:
`S(n, k) = sum {0 <= i <= k} (i**n / i!) * ((-1)**(k - i) / (k - i)!)`
After a closer look it is evident that if `a(i) = i**n / i!` and `b(i) = (-1)**i / i!`, then the above sum just represents the `k^th term` in the `convolution` of `a` and `b`.
Hence, the overall computation for obtaining one entire row can be sped to match the complexity of doing convolution.
