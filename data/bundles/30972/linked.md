# Issues and pull requests referenced by this pull request

## Issue #12629: Sequences with variable limits cannot be pretty-printed

- Opened by @dniku, state: closed

Sympy version 1.0-2 from Manjaro repository.

```python
In [1]: import sympy as sp

In [2]: sp.init_session()
IPython console for SymPy 1.0 (Python 3.6.0-64-bit) (ground types: gmpy)

These commands were executed:
>>> from __future__ import division
>>> from sympy import *
>>> x, y, z, t = symbols('x y z t')
>>> k, m, n = symbols('k m n', integer=True)
>>> f, g, h = symbols('f g h', cls=Function)
>>> init_printing()

Documentation can be found at http://docs.sympy.org/1.0/

In [3]: k, i = sp.symbols('k, i', integer=True)

In [4]: sp.sequence(i, (i, 0, k))
Out[4]: ---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
/usr/lib/python3.6/site-packages/IPython/core/formatters.py in __call__(self, obj)
    670                 type_pprinters=self.type_printers,
    671                 deferred_pprinters=self.deferred_printers)
--> 672             printer.pretty(obj)
    673             printer.flush()
    674             return stream.getvalue()

/usr/lib/python3.6/site-packages/IPython/lib/pretty.py in pretty(self, obj)
    366                 if cls in self.type_pprinters:
    367                     # printer registered in self.type_pprinters
--> 368                     return self.type_pprinters[cls](obj, self, cycle)
    369                 else:
    370                     # deferred printer

/usr/lib/python3.6/site-packages/sympy/interactive/printing.py in _print_plain(arg, p, cycle)
     66         """caller for pretty, for use in IPython 0.11"""
     67         if _can_print_latex(arg):
---> 68             p.text(stringify_func(arg))
     69         else:
     70             p.text(IPython.lib.pretty.pretty(arg))

/usr/lib/python3.6/site-packages/sympy/printing/pretty/pretty.py in pretty(expr, **settings)
   2037 
   2038     try:
-> 2039         return pp.doprint(expr)
   2040     finally:
   2041         pretty_use_unicode(uflag)

/usr/lib/python3.6/site-packages/sympy/printing/pretty/pretty.py in doprint(self, expr)
     56 
     57     def doprint(self, expr):
---> 58         return self._print(expr).render(**self._settings)
     59 
     60     # empty op so _print(stringPict) returns the same

/usr/lib/python3.6/site-packages/sympy/printing/printer.py in _print(self, expr, *args, **kwargs)
    255                 printmethod = '_print_' + cls.__name__
    256                 if hasattr(self, printmethod):
--> 257                     return getattr(self, printmethod)(expr, *args, **kwargs)
    258 
    259             # Unknown object, fall back to the emptyPrinter.

/usr/lib/python3.6/site-packages/sympy/printing/pretty/pretty.py in _print_SeqFormula(self, s)
   1613             printset = (dots, s.coeff(stop - 3), s.coeff(stop - 2),
   1614                 s.coeff(stop - 1), s.coeff(stop))
-> 1615         elif s.stop is S.Infinity or s.length > 4:
   1616             printset = s[:4]
   1617             printset.append(dots)

/usr/lib/python3.6/site-packages/sympy/core/relational.py in __nonzero__(self)
    193 
    194     def __nonzero__(self):
--> 195         raise TypeError("cannot determine truth value of Relational")
    196 
    197     __bool__ = __nonzero__

TypeError: cannot determine truth value of Relational
```
