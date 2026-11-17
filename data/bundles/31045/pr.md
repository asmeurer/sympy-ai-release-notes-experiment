# Pull request #31045: typ(core): type annotations for @cacheit

- Author: @oscarbenjamin
- Merged: 2026-11-11T21:09:37Z into `master`
- Labels: typing
- Size: +177 / -79 in 29 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes gh-31018

#### Brief description of what is fixed or changed

Add type annotations to `@cacheit` so that mypy understands what it does. This allowed mypy to infer a lot more types (cacheit is widely used on basic things).

This exposed lots of other typing errors so there was wide fallout that needed to be addressed.

#### Other comments

#### AI Generation Disclosure

NO AI USE (more trouble than it is worth for this sort of thing).

## Commits

- 57ad210e2f (Oscar Benjamin): typ(core): type annotations for @cacheit
      Adding annotations to cacheit exposed lots of other typing errors so
      there was wide fallout that needed to be addressed.

## Conversation

### @oscarbenjamin commented

I'm going to merge this because it otherwise holds up many other typing things whenever `@cacheit` comes up which is a lot on the core bits of Expr.


## Reviews

(no reviews)
