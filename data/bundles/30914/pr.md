# Pull request #30914: series: define bound_symbols on Limit

- Author: @Nabhag2507
- Merged: 2026-11-03T06:43:49Z into `master`
- Labels: (none)
- Size: +30 / -0 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs
Fixes #30913

#### Brief description of what is fixed or changed
As suggested by @smichr in #30913, I added the `bound_symbols` property to `Limit`, which returns `(self.args[1],)`.

Earlier, accessing `Limit(x + y, x, 0).bound_symbols` raised an `AttributeError` because this property was not defined for `Limit`.

After adding it, `Limit` now behaves more like other expressions such as `Integral`, `Sum`, and `Lambda`, which also bind variables.

This also fixes a few related issues:

- `Limit.as_dummy()` can now replace bound variables with dummy symbols like `_0`, `_1`, etc.
- `Limit.dummy_eq()` can now correctly compare limits even if their bound variables have different names.
- `Limit.canonical_variables` can now return the correct dummy variables instead of an empty dictionary.

#### Other comments
None.

#### AI Generation Disclosure

Used ChatGPT for improving PR. Since all changes were instructed by @smichr no AI required for code.

## Commits

- 6b05e5b5a2 (Nabhag2507): series: define bound_symbols on Limit
      Fixes #30913

## Conversation

### @Nabhag2507 commented

Hi @TiloRC 

In this PR all i do is just as instructed by smichr if we don't consider the testing code this changes only contains 4 5 lines of code but it is complete as per requirement. So, i wanted to ask you do you consider this kind of PR a low quality PR? Should i make PR which have some minimum code line criteria? Or it should solve multiple Issues in one PR?

### @TiloRC commented

Please don't tag people. I guess I don't mind it that much but most maintainers will find it very annoying. It comes off as if you think you're entitled to our time. 

> So, i wanted to ask you do you consider this kind of PR a low quality PR? Should i make PR which have some minimum code line criteria? Or it should solve multiple Issues in one PR?

There's no easy answer to what's a high quality PR. There isn't some sort of number or rubric for determining if a PR is high quality or not. I wouldn't be able to tell without reviewing this PR. Skimming your PR description, it seems fairly readable though. 

> In this PR all i do is just as instructed by smichr if we don't consider the testing code this changes only contains 4 5 lines of code but it is complete as per requirement. So, i wanted to ask you do you consider this kind of PR a low quality PR? Should i make PR which have some minimum code line criteria? Or it should solve multiple Issues in one PR?

This message seems kind of low quality though. When you don't write with proper capitalization etc so consistently it appears as if you haven't put very much effort into your message.

### @smichr commented

If it fixes something it is not too small to consider. Thanks for taking this on.


## Reviews

(no reviews)
