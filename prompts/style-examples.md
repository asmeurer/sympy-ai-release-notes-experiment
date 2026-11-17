* assumptions
  * Now ```ask(Q.integer(x/y), Q.integer(x) & Q.integer(y))``` gives ```None``` instead of wrongly giving ```True```.
  * Now ```ask(Q.integer(1/x), Q.integer(x))``` gives ```None``` instead of wrongly giving ```True```.
* codegen
  * new classes mapping to numpy's functions: amin, amax, minimum, maximum
  * Added `isinf` in `.codegen.cfunctions`.
* combinatorics
  * Add pickle support to FreeGroup.
* concrete
  * Gives **_evaluated_** result when **lower limit > upper limit** in summation, especially in case if either of them is `infinite` (following Karr convention)
  * Fix Ratio test to check if limit ratio is NaN.
* core
  * DEPRECATION: The gcd parameter for Rational is now deprecated. This parameter is used to create "unevaluated rationals" but those are impossible to represent if SymPy uses any more efficient implementation of rational numbers (e.g. from gmpy2 or python-flint). This parameter is deprecated and using it will likely become a hard error much quicker than usual deprecation timelines because keeping this behaviour even with a deprecation warning prevents making Rational much faster.
  * The output of `igcdex(0, 0)` has been changed from `(0, 1, 0)` to `(0, 0, 0)`.
* functions
  * Added caching to speed up harmonic number computation.
  * Fixed inconsistent behavior of the `primitive` method for the zero polynomial.
* integrals
  * rules containing `sqrt(a*t)` and `sqrt(a/t)` and their test cases have been removed from the rule-based `laplace_transform` method, they will be re-instated after a mathematical investigation into the validity of the respective table entries in Bateman54
  * Fixed incorrect inverse laplace transforms of polynomials in s.
* interactive
* logic
  * Fixed hanging issue with `satisfiable` queries involving complex expressions where `use_lra_theory` is True.
* matrices
  * Fixed Matrix.is_hermitian for matrices of quantum operators.
  * Added fraction-free LU Decomposition method for DomainMatrix.
* ntheory
  * The output of `qs` is a set of factors of `N`, but until now, their product could exceed `N`. We have fixed it to ensure that it does not exceed `N`.
  * We have implemented a new function, `qs_factor`. Like the existing `qs`, it performs prime factorization using the quadratic sieve. However, the difference is that `qs_factor` returns the results as a dictionary.
* parsing
  * Introduced matrix and literal complex number parsing.
* physics.biomechanics
  * Moved files in the API Reference to Explanation
* physics.continuum_mechanics
  * add a draw method for the Arch class
  * adds solver for arch class in continuum_mechanics module
* physics.control
  * Added Nichols plot to control.
  * Added Nyquist plot to control.
* physics.mechanics
  * Add a redirect to the top level explanation page from the old url in the reference section.
  * KanesMethod requires linear speed constraints, but it does not check whether they indeed are linear. Using _linear_eq_to_matrix_ instead of the Jacobian serves two purposes: 1) it makes solving the constraints faster and 2) it will raise an error in the speed constraints are not linear.
* physics.quantum
  * Removed custom `__mul__` and `__pow__` methods from quantum classes. This logic has been replaced by `_constructor_postprocessor_mapping` based transforms that are more complete and consistent.
  * Created kinds for bras, kets and operators, with kind dispatch resolution.
* physics.secondquant
  * Add support for Dagger of a Function
* physics.vector
  * Add a redirect to the top level explanation page from the old url in the reference section.
  * A bug in pretty printing of vectors was fixed. Previously an exception would be raised when printing the zero vector.
* physics.wigner
  * Explained how to index the matrices output by `wigner_d` and `wigner_d_small`.
  * Noted discrepancy in angles compared to cited reference.
* polys
  * Fixed a bug where `primitive_element` returned non-canonical minimal polynomials.
  * New `rs_asinh` function in `ring_series` module to compute `arcsinh` Taylor series at x=0.
* printing
  * Breaking change: The aesaracode in sympy.printing has been deprecated.
  * Updates the rust printer to reflect the reserved words in the 2024 edition.
* series
  * Fixed `sign` in gruntz for better handling of terms having negative bases in power expressions with symbolic exponents.
  * Fixing cdir for limit & leadterm calculation.
* simplify
  * Refactored `forward_jacobian` function to be private and handle `dynamicsymbols`.
  * Optimized DAG to canonical expression tree transformations.
* solvers
  * `solve` will now reject matrices with symbolic shape. Previously it would go into an infinite loop.
  * Added `extension=True` option to `solve_triangulated` for computing solutions in algebraic fields using `CRootOf`.
* stats
  * Fixed expectation calculation for Poisson Distribution
* tensor
  * `doit` is no longer automatically called on the result of `TensExpr.expand`
  * Calling `expand` on `TensMul` whose coeff is an `Add` now results in a `TensAdd` (earlier, no expansion would  be performed)
* utilities
  * Added PyTorch backend support to lambdify
  * Enhanced lambdify to support Python's built-in cmath module.
* vector
  * A bug in VectorAdd causing terms to be dropped was fixed. Previously incorrect results were returned.
  * Vector.equals has been fixed so that vectors can be compared with `v1.equals(v2)`. Previously incorrect results were returned.
* other
  * Python 3.8 is no longer supported.
