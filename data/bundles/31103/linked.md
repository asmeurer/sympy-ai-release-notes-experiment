# Issues and pull requests referenced by this pull request

## Pull request #31095: printing: parenthesize a reciprocal denominator in code printers

- Opened by @Viranshul-P, state: closed

Part of #30844 (cause 2).

The Julia and Octave version(s) of CodePrinter._print_Mul print a single
A negative power of a denominator with no parentheses.
`Mul(x, Pow(Pow(y, -1), -1, evaluate=False), evaluate=False)` printed `x/1/y`
in pycode, `x/1.0/y` in ccode and `x ./ 1 ./ y` in julia_code. That is x/y,
not x*y. It now prints `x/(1/y)`.

I inserted a test in 4 test files (pycode, c, julia, octave). They fail
Before the change, pass after the change. 471 printing/CodeGen tests passed.

#### AI Generation Disclosure
The fix is in Claude Code's (Sonnet 5.5) code `sympy/printing/codeprinter.py`, and
A Julia program, julia.py, and an Octave program, octave.py, and the tests in test_pycode.py, test_c.py,
`test_julia.py` and `test_octave.py`.

## Issue #30844: Printers: systematic review of precedence and other defects across LaTeX, pretty, str/srepr, MathML and code printers (~230 findings)

- Opened by @Upabjojr, state: open

> **AI disclosure.** This issue text and the underlying review were produced by an AI agent (Claude Code, models Claude Opus 5.5 and Claude Fable 5.1) at the request of the account owner. Every finding below was executed on master `bfb177ed52` (2026-10-25); reviewer findings were re-run by an independent verification pass. Items whose target language had no compiler available here (Fortran, Rust, Octave, R, Maple, Mathematica, GLSL, torch) are marked **(R)**: the printer output was executed, the language semantics were checked against that language's documentation.

This is a systematic review of all printers for **wrong precedence** (missing parentheses that change the meaning of the printed expression) plus other defects (wrong output, invalid output, crashes on valid input, ignored settings). It is one umbrella issue so the findings can be triaged together; individual items can be split out as needed. Items marked **tested-buggy** have an existing test asserting the wrong output.

Method: code reading of every `_print_*`/`_latex`/`_pretty`/`_sympystr` method, ~5000 hand-built constructs (mostly `evaluate=False` / `UnevaluatedExpr` trees), random-tree fuzzers that evaluate the printed output numerically (Python/mpmath/NumPy via `eval`, C via gcc, JS via node, Julia 1.12) or round-trip it (`parse_expr` for str, `eval` for srepr, pdflatex for LaTeX validity).

Setup used in the reproducers:
```python
from sympy import *
x, y, z, n, k, i, j, a, b, s, t = symbols('x y z n k i j a b s t'); f, g = symbols('f g', cls=Function)
A, B = MatrixSymbol('A', 2, 2), MatrixSymbol('B', 2, 2)
P = lambda b, e: Pow(b, e, evaluate=False); M = lambda *a: Mul(*a, evaluate=False)
```

### 1. `precedence_traditional` never reaches `precedence_Mul` 
(`printing/precedence.py:145,181-183`): `PRECEDENCE_TRADITIONAL = PRECEDENCE.copy()` contains the key `"Mul"`, so the class-name lookup returns 50 for every `Mul` and never calls `precedence_Mul`, which returns Add (40) for negative Muls. `precedence_traditional(-x) == 50` but `precedence(-x) == 40`. Every LaTeX/pretty `parenthesize(..., PRECEDENCE['Mul'], strict=True)` misses negative Muls: `latex(Mod(-x,y)) == latex(-Mod(x,y)) == '- x \bmod y'`; `latex(Quaternion(x,-y,z,w))` gives `x + - y i + ...`.
### 2. `CodePrinter._print_Mul` re-evaluates denominators*; **fixed in #31103**
(`codeprinter.py:576`, `b.append(Pow(item.base, -item.exp))`): `Pow(Pow(y,-1),1)` evaluates back to `Pow(y,-1)`, which has Pow precedence but prints as `1/y`, so no parentheses are added. `M(x, P(P(y,-1),-1))` (= `parse_expr('x/(1/y)', evaluate=False)`) prints `x/1/y` in pycode, `x/1.0/y` in C/R/GLSL, `x ./ 1 ./ y` in Julia, `x./1./y` in Octave, `x/1d0/y` in Fortran, `x/1/y` in JS/Maple — wrong value in every CodePrinter subclass (Rust and Mathematica are fine). Executed in Python, C, JS, Julia.  
### 3. Relational lhs/rhs are never parenthesized in LaTeX 
(`latex.py:1721`), pretty (`pretty.py:223-229`) and most code printers (`c.py:392`, `jscode.py:129`, `julia.py:191`, `octave.py:209`, `rcode.py:238`, `rust.py:446`, `mathematica.py:166`, `glsl.py:296`, `fortran.py:376`): `ccode(Eq(x, Eq(y,z), evaluate=False))` gives `x == y == z`; `julia_code(Eq(x>1, y>1, evaluate=False))` gives `x > 1 == y > 1`, a chained comparison (executed: wrong value). See #11366.
### 4. `_print_Not` tests `arg.is_Boolean`*, which is False for `Relational` and `Contains` 
(`latex.py:1154`, `pretty.py:241`): `latex(Not(x>y, evaluate=False))` gives `\neg x > y`; `latex(Not(Contains(x, Interval(0,1))))` gives `\neg x \in \left[0, 1\right]`.
### 5. Pretty printer returns composite pictures with ATOM binding
(inline `p/q` Rationals, negative Floats, Union/`_print_seq`, MatAdd, Dot, TensorProduct, inline `sin²(x)`), so `prettyForm.__pow__`/`__mul__` add no parentheses: `pprint(P(Rational(2,3), x))` prints `2/3` with superscript `x` (reads 2/3ˣ); `Rational(-1,2)**n + x` prints `-1/2ⁿ + x`. Shows up in `fps(sin(x))`.
### 6. The Limit direction marker is glued to the printed point
(`latex.py:922`, `pretty.py:680-688`): `latex(Limit(f(x),x,a+b))` gives `\lim_{x \to a + b^+}`; `Limit(f(x),x,a**2)` gives `a^{2}^+` (TeX double-superscript error).
## LaTeX printer (`printing/latex.py` and external `_latex` methods)

<details><summary>Crashes / invalid TeX (every TeX claim confirmed with pdflatex)</summary>

- `latex(LaplaceTransform(f(t),t,s)**2)` → `TypeError: _print_LaplaceTransform() got an unexpected keyword argument 'exp'`. Same for all Mellin/Fourier/Sine/Cosine transforms and inverses, `Pow(Piecewise(...),2,evaluate=False)`, `Lambda(x,x**2)**2`, and any Function subclass with `_latex(self, printer)` (e.g. the biomechanics curves, user Functions). `latex.py:686,714` pass `exp=` for every `is_Function` base.
- `latex(Feedback(Series(t1,t2), t3))` prints a Python tuple in the denominator (`\left( \frac{1}{1}, \ ...\right)`): stray comma at `latex.py:2769`, `den_term_2 = tf, Series(...)`.
- Double superscripts (TeX error): `Limit(f(x),x,a**2)` → `a^{2}^+`; `Operator('A^a')**2` → `A^{a}^{2}` (`parenthesize_super` only for `is_Symbol` bases, `latex.py:726`); `adjoint(Symbol('A^a', commutative=False))` → `A^{a}^{\dagger}` (`complexes.py:1023-1028`); `RaisingOp('a')**2` → `a^{\dagger}^{2}`; `Die('D^6',6)**2` → `D^{6}^{2}`; `HadamardPower(MatrixSymbol('A^b',2,2),2)` → `A^{b}^{\circ {2}}` (`latex.py:1903`); `udivisor_sigma(n)**2` → `\sigma^*^{2}\left(n\right)` (`latex.py:3004`; **tested-buggy** `test_latex.py:789,791`); `units.degree**2` → `^\circ^{2}`; `UnevaluatedExpr(exp(z))**2` → `e^{z}^{2}` (the `is_Function` branch is skipped and `precedence_traditional` unwraps UnevaluatedExpr to Func precedence).
- `AntiSymmetricTensor('v_1',(i,),(j,))` → `{v_1^{i}_{j}}` (double subscript; `secondquant.py:218`).
- `latex(Array(list(range(24)),(2,12)))` → `\begin{array}{cc}` with 12 columns ("Extra alignment tab"): `latex.py:1970` uses `shape[0]` instead of `shape[-1]`. This is the fix for #26652 and fails on that issue's own reproducer `Arra
