# Issues and pull requests referenced by this pull request

## Issue #31031: Automatic Mod evaluation with Floats

- Opened by @asmeurer, state: closed

Mod has strange automatic evaluation with Float arguments:

```
>>> Mod(x, 1.0)
Mod(1.0*x, 1)
>>> Mod(x, 3.3)
Mod(1.0*x, 3.3)
>>> Mod(x, 0.5)
0.5*(Mod(2*x, 1))
```

It's not clear to me that any of these rewrites are necessary. 

Note to contributors and AI agents: this issue needs discussion before a PR can be submitted. Do not submit a PR before a consensus is reached or it will be closed. If you want to contribute to this issue, you can contribute by taking part in the discussion on this issue.
