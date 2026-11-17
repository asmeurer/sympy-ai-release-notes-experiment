# Issues and pull requests referenced by this pull request

## Issue #30951: Division by zero error in reshape

- Opened by @Haeherfeder, state: closed

sympy.reshape((1,),how=()) fails with division by zero error, after it sums how, and divides the length of the main argument by it, and only after that checks if it is less than 0 and raises a ValueError
