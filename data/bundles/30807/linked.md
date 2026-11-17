# Issues and pull requests referenced by this pull request

## Pull request #1234: Fix test failure in beginner/precision.py example

- Opened by @flacjacket, state: closed, merged 2012-04-14

Title says it all.

## Issue #15753: Powers of CRootOf don't reduce

- Opened by @oscarbenjamin, state: open

It should be possible to simplify expressions involving `CRootOf` where they are substituted into the polynomial that they solve:
```julia
In [1]: r = CRootOf(x**5 - x + 1, 0)                                                                                                                          

In [2]: r**5 - r + 1                                                                                                                                          
Out[2]: 
                      5                             
       ⎛ 5           ⎞               ⎛ 5           ⎞
CRootOf⎝x  - x + 1, 0⎠  + 1 - CRootOf⎝x  - x + 1, 0⎠

In [3]: simplify(r**5 - r + 1)                                                                                                                                
Out[3]: 
                      5                             
       ⎛ 5           ⎞               ⎛ 5           ⎞
CRootOf⎝x  - x + 1, 0⎠  + 1 - CRootOf⎝x  - x + 1, 0⎠
```

It should be straightforward to do this by reducing e.g. `CRootOf(x**5-x+1,0)**n` where `n >= 5` e.g.:

```
CRootOf(x**5 - x + 1, 0)**5    ----->   CRootOf(x**5 - x + 1, 0) - 1
```

With that reduction the expressions above would cancel to zero.
