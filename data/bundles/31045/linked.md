# Issues and pull requests referenced by this pull request

## Pull request #31018: core: add type annotations to @cacheit decorator to fix Pow typing as Any

- Opened by @Nabhag2507, state: closed

#### References to other Issues or PRs
Fixes #31008

#### Brief description of what is fixed or changed
- Added type annotations to `@cacheit`, `__cacheit`, `__cacheit_nocache`, and `__cacheit_debug` in `sympy/core/cache.py`.
- Introduced a `_CacheDecorator(Protocol)` with a generic `__call__` method using `ParamSpec('P')` and `TypeVar('R')` under `if TYPE_CHECKING:`.
- Registered `cfunc` (the `lru_cache` wrapper) directly in `CACHE` so global cache introspection (`print_cache` and `clear_cache`) functions properly without needing dynamically typed attributes on the wrapper.
- Resolves an issue where Mypy treated `Pow` (and expressions constructed with `Pow`) as `Any` due to `Pow.__new__` being decorated with an untyped decorator.

#### Other comments
- Existing caching unit tests (`sympy/core/tests/test_cache.py`) and power tests (`sympy/core/tests/test_power.py`) pass.
- Verified that `reveal_type(Pow)` and `reveal_type(Pow(x, 2))` now correctly retain their types in Mypy, and `isinstance(e, Pow)` properly narrows expressions.

#### AI Generation Disclosure
This pull request was created with assistance from Gemini and manually reviewed and tested.
