# Issues and pull requests referenced by this pull request

## Issue #2834: Don't evalf while printing

- Opened by @asmeurer, state: closed

This comes from http://stackoverflow.com/q/21353081/161801. The act of printing `loss` takes forever, because it is trying to evalf it. It looks like the problem is in `as_terms`.

```
In [13]: loss
^COut[13]: ---------------------------------------------------------------------------
KeyboardInterrupt                         Traceback (most recent call last)
<ipython-input-13-4eb681f84119> in <module>()
----> 1 loss

/Users/aaronmeurer/anaconda3/envs/python2/lib/python2.7/site-packages/IPython/core/displayhook.pyc in __call__(self, result)
    245             self.start_displayhook()
    246             self.write_output_prompt()
--> 247             format_dict, md_dict = self.compute_format_data(result)
    248             self.write_format_data(format_dict, md_dict)
    249             self.update_user_ns(result)

/Users/aaronmeurer/anaconda3/envs/python2/lib/python2.7/site-packages/IPython/core/displayhook.pyc in compute_format_data(self, result)
    155
    156         """
--> 157         return self.shell.display_formatter.format(result)
    158
    159     def write_format_data(self, format_dict, md_dict=None):

/Users/aaronmeurer/anaconda3/envs/python2/lib/python2.7/site-packages/IPython/core/formatters.pyc in format(self, obj, include, exclude)
    150             md = None
    151             try:
--> 152                 data = formatter(obj)
    153             except:
    154                 # FIXME: log the exception

/Users/aaronmeurer/anaconda3/envs/python2/lib/python2.7/site-packages/IPython/core/formatters.pyc in __call__(self, obj)
    479                 type_pprinters=self.type_printers,
    480                 deferred_pprinters=self.deferred_printers)
--> 481             printer.pretty(obj)
    482             printer.flush()
    483             return stream.getvalue()

/Users/aaronmeurer/anaconda3/envs/python2/lib/python2.7/site-packages/IPython/lib/pretty.pyc in pretty(self, obj)
    345                 if cls in self.type_pprinters:
    346                     # printer registered in self.type_pprinters
--> 347                     return self.type_pprinters[cls](obj, self, cycle)
    348                 else:
    349                     # deferred printer

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/interactive/printing.pyc in _print_plain(arg, p, cycle)
     61         """caller for pretty, for use in IPython 0.11"""
     62         if _can_print_latex(arg):
---> 63             p.text(stringify_func(arg))
     64         else:
     65             p.text(IPython.lib.pretty.pretty(arg))

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/printing/pretty/pretty.pyc in pretty(expr, **settings)
   1793
   1794     try:
-> 1795         return pp.doprint(expr)
   1796     finally:
   1797         pretty_use_unicode(uflag)

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/printing/pretty/pretty.pyc in doprint(self, expr)
     48
     49     def doprint(self, expr):
---> 50         return self._print(expr).render(**self._settings)
     51
     52     # empty op so _print(stringPict) returns the same

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/printing/printer.pyc in _print(self, expr, *args, **kwargs)
    255                 printmethod = '_print_' + cls.__name__
    256                 if hasattr(self, printmethod):
--> 257                     return getattr(self, printmethod)(expr, *args, **kwargs)
    258
    259             # Unknown object, fall back to the emptyPrinter.

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/printing/pretty/pretty.pyc in _print_Add(self, expr, order)
   1113             terms = list(expr.args)
   1114         else:
-> 1115             terms = self._as_ordered_terms(expr, order=order)
   1116         pforms, indices = [], []
   1117

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/printing/printer.pyc in _as_ordered_terms(self, expr, order)
    269             return sorted(Add.make_args(expr), key=cmp_to_key(Basic._compare_pretty))
    270         else:
--> 271             return expr.as_ordered_terms(order=order)

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/core/expr.pyc in as_ordered_terms(self, order, data)
    818         """
    819         key, reverse = self._parse_order(order)
--> 820         terms, gens = self.as_terms()
    821
    822         if not any(term.is_Order for term, _ in terms):

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/core/expr.pyc in as_terms(self)
    856                     if factor.is_number:
    857                         try:
--> 858                             coeff *= complex(factor)
    859                         except TypeError:
    860                             pass

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/core/expr.pyc in __complex__(self)
    208
    209     def __complex__(self):
--> 210         result = self.evalf()
    211         re, im = result.as_real_imag()
    212         return complex(float(re), float(im))

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/core/evalf.pyc in evalf(self, n, subs, maxn, chop, strict, quad, verbose)
   1282             options['quad'] = quad
   1283         try:
-> 1284             result = evalf(self, prec + 4, options)
   1285         except NotImplementedError:
   1286             # Fall back to the ordinary evalf

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/core/evalf.pyc in evalf(x, prec, options)
   1182     try:
   1183         rf = evalf_table[x.func]
-> 1184         r = rf(x, prec, options)
   1185     except KeyError:
   1186         try:

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/core/evalf.pyc in evalf_integral(expr, prec, options)
    957     maxprec = options.get('maxprec', INF)
    958     while 1:
--> 959         result = do_integral(expr, workprec, options)
    960         # if a scaled_zero comes back accuracy will compute to -1
    961         # which will cause workprec to increment by 1

/Users/aaronmeurer/Documents/Python/sympy/symp

## Issue #10800: pretty printing gets stuck doing evalf

- Opened by @asmeurer, state: closed

```
In [147]: a = 2*integrate(sin(exp(x)), (x, 1, oo))+2*Si(E)

In [148]: a
^COut[148]: ---------------------------------------------------------------------------
KeyboardInterrupt                         Traceback (most recent call last)
<ipython-input-148-60b725f10c9c> in <module>()
----> 1 a

/Users/aaronmeurer/anaconda3/lib/python3.5/site-packages/IPython/core/displayhook.py in __call__(self, result)
    244             self.start_displayhook()
    245             self.write_output_prompt()
--> 246             format_dict, md_dict = self.compute_format_data(result)
    247             self.update_user_ns(result)
    248             self.fill_exec_result(result)

/Users/aaronmeurer/anaconda3/lib/python3.5/site-packages/IPython/core/displayhook.py in compute_format_data(self, result)
    150
    151         """
--> 152         return self.shell.display_formatter.format(result)
    153
    154     def write_format_data(self, format_dict, md_dict=None):

/Users/aaronmeurer/anaconda3/lib/python3.5/site-packages/IPython/core/formatters.py in format(self, obj, include, exclude)
    175             md = None
    176             try:
--> 177                 data = formatter(obj)
    178             except:
    179                 # FIXME: log the exception

<decorator-gen-10> in __call__(self, obj)

/Users/aaronmeurer/anaconda3/lib/python3.5/site-packages/IPython/core/formatters.py in catch_format_error(method, self, *args, **kwargs)
    220     """show traceback on failed format call"""
    221     try:
--> 222         r = method(self, *args, **kwargs)
    223     except NotImplementedError:
    224         # don't warn on NotImplementedErrors

/Users/aaronmeurer/anaconda3/lib/python3.5/site-packages/IPython/core/formatters.py in __call__(self, obj)
    697                 type_pprinters=self.type_printers,
    698                 deferred_pprinters=self.deferred_printers)
--> 699             printer.pretty(obj)
    700             printer.flush()
    701             return stream.getvalue()

/Users/aaronmeurer/anaconda3/lib/python3.5/site-packages/IPython/lib/pretty.py in pretty(self, obj)
    366                 if cls in self.type_pprinters:
    367                     # printer registered in self.type_pprinters
--> 368                     return self.type_pprinters[cls](obj, self, cycle)
    369                 else:
    370                     # deferred printer

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/interactive/printing.py in _print_plain(arg, p, cycle)
     66         """caller for pretty, for use in IPython 0.11"""
     67         if _can_print_latex(arg):
---> 68             p.text(stringify_func(arg))
     69         else:
     70             p.text(IPython.lib.pretty.pretty(arg))

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/printing/pretty/pretty.py in pretty(expr, **settings)
   2037
   2038     try:
-> 2039         return pp.doprint(expr)
   2040     finally:
   2041         pretty_use_unicode(uflag)

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/printing/pretty/pretty.py in doprint(self, expr)
     56
     57     def doprint(self, expr):
---> 58         return self._print(expr).render(**self._settings)
     59
     60     # empty op so _print(stringPict) returns the same

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/printing/printer.py in _print(self, expr, *args, **kwargs)
    255                 printmethod = '_print_' + cls.__name__
    256                 if hasattr(self, printmethod):
--> 257                     return getattr(self, printmethod)(expr, *args, **kwargs)
    258
    259             # Unknown object, fall back to the emptyPrinter.

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/printing/pretty/pretty.py in _print_Add(self, expr, order)
   1234             terms = list(expr.args)
   1235         else:
-> 1236             terms = self._as_ordered_terms(expr, order=order)
   1237         pforms, indices = [], []
   1238

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/printing/printer.py in _as_ordered_terms(self, expr, order)
    269             return sorted(Add.make_args(expr), key=cmp_to_key(Basic._compare_pretty))
    270         else:
--> 271             return expr.as_ordered_terms(order=order)

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/core/expr.py in as_ordered_terms(self, order, data)
    886         """
    887         key, reverse = self._parse_order(order)
--> 888         terms, gens = self.as_terms()
    889
    890         if not any(term.is_Order for term, _ in terms):

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/core/expr.py in as_terms(self)
    925                     if factor.is_number:
    926                         try:
--> 927                             coeff *= complex(factor)
    928                         except TypeError:
    929                             pass

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/core/expr.py in __complex__(self)
    227
    228     def __complex__(self):
--> 229         result = self.evalf()
    230         re, im = result.as_real_imag()
    231         return complex(float(re), float(im))

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/core/evalf.py in evalf(self, n, subs, maxn, chop, strict, quad, verbose)
   1384             options['quad'] = quad
   1385         try:
-> 1386             result = evalf(self, prec + 4, options)
   1387         except NotImplementedError:
   1388             # Fall back to the ordinary evalf

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/core/evalf.py in evalf(x, prec, options)
   1276     try:
   1277         rf = evalf_table[x.func]
-> 1278         r = rf(x, prec, options)
   1279     except KeyError:
   1280         try:

/Users/aaronmeurer/Documents/Python/sympy/sympy/sympy/core/evalf.py in evalf_integral(expr, prec, options)
   1006     maxprec = options.get('maxprec', INF)
   1007     while 1:
-> 1008         result = do_integral(expr, workprec, options)
   1009

## Issue #16090: Term reordering follow up from #15985

- Opened by @oscarbenjamin, state: closed

I just found this:
```julia
In [14]: integrate(2 * sqrt(-x**2 + 1)*(4*sqrt(2)*x**2 - sqrt(3)), (x, -1, +1))                                                   
Out[14]: -√3⋅π + √2⋅π
```
Haven't looked into the details yet but do you have any idea why this happens @nickovs:
```julia
In [18]: sqrt(2)-1                                                                                                                
Out[18]: -1 + √2
```

_Originally posted by @oscarbenjamin in https://github.com/sympy/sympy/pull/15985#issuecomment-467681751_

## Issue #17609: Out of memory on big expressions

- Opened by @glample, state: closed

For some particular expressions, SymPy eats my 512 GB of RAM, and ends up crashing without running any exceptions. But I'm not able to understand in which scenarios it crashes and does not crash. For instance:

```
from sympy.parsing.sympy_parser import parse_expr

parse_expr('sin((7**(exp(exp(exp(10*E)))))+1)')
# OOM (uses 512GB of RAM and crashes the server after a few seconds)

parse_expr('sin((7**(exp(exp(exp(10*E))))))')
# outputs sin(7**exp(exp(exp(10*E)))) without simplifications (what I want), and without issues

parse_expr('sin((7**(exp(exp(exp(10)))))+1)')
# raises "OverflowError: int too large to convert to float" immediately (also good)
```

How can I ensure that SymPy raises exceptions, or do not evaluate them when they are too large, without having it using too much CPU RAM?

Alternatively, how can I limit the RAM memory SymPy can access to?

Thank you

## Issue #17911: Printing an unevaluated Sum in Add can be unexpectedly slow

- Opened by @ethankward, state: closed

```
>>> from sympy import *
>>> from sympy.abc import q, z, n
>>> f1 = lambda z, q: -log(1 - q)
>>> f2 = lambda z, q: log(q) * Sum(q**(n + z) / (1 - q**(n + z)), [n, 0, oo])
>>> f1(z, q)
-log(1 - q)
>>> f2(z, q)
log(q)*Sum(q**(n + z)/(1 - q**(n + z)), (n, 0, oo))
>>> f1(z, q) + f2(z, q)
log(q)*Sum(q**(n + z)/(1 - q**(n + z)), (n, 0, oo)) - log(1 - q)
>>> f1(3, 4)
-log(3) - I*pi
>>> f2(3, 4)
log(4)*Sum(4**(n + 3)/(1 - 4**(n + 3)), (n, 0, oo))
>>> f1(3, 4) + f2(3, 4)
log(4)*Sum(4**(n + 3)/(1 - 4**(n + 3)), (n, 0, oo)) - log(3) - I*pi
```

The last line takes about 30 seconds.

## Issue #19790: Print hangs

- Opened by @proy87, state: closed

```
lst = [Sum(2**((k**2 + k - 5)/(k**4 - 5))*(k**2 + k), (k, 0, oo)), Sum(2**((k**2 - k - 5)/(k**4 - 5))*(k**2 - k), (k, 0, oo)), Sum(-2**((k**2 - k - 5)/(k**4 - 5))*(k**2 - k), (k, 0, 0))]
print(Add(*lst))
```

This hangs on printing.
