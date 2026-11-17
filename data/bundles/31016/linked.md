# Issues and pull requests referenced by this pull request

## Issue #30996: Wrong / missing results with modular solveset

- Opened by @joprodrigues, state: closed

I was trying to solve some modular equations of the form `Mod( n * (2**x) -  m, 42)`, for n and m varying from 0 to 42, and sympy can't handle this (mostly because of the missing handling of composite numbers for discrete_log (#27612)).

With that fixed (locally), it still does not work for some cases. Some of the examples I have tried and return wrong results.

`solveset(Mod( 2**x, 42), x, S.Integers)`, expected: `S.EmptySet`

`solveset(Mod( 2**x -  1, 42), x, S.Integers)`, expected: `FiniteSet(0)`

`solveset(Mod( 2**x - 22, 42), x, S.Integers)`, expected: `ImageSet(Lambda(n, 6*n + 6), S.Naturals0))`

`solveset(Mod( (2 * (2**x)) - 1, 42), x, S.Integers)`, expected: `S.EmptySet`

`solveset(Mod( (2 * (2**x)) - 2, 42), x, S.Integers)`, expected: `ImageSet(Lambda(n, 6*n), S.Naturals0))`
