# Issues and pull requests referenced by this pull request

## Pull request #30971: SetExpr maintenance

- Opened by @smichr, state: closed, merged 2026-11-08

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

This fixes several issues with consistency related to SetExpr operations (add, multiply) when working with scalars and infinite values.

The biggest change might be that intervals containing 0 when multiplied by and infinite value will generate a nan entry in the set.

#### Other comments

#### AI Generation Disclosure

ChatGPT collaboration.
