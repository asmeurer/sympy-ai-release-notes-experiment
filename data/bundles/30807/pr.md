# Pull request #30807: PurePoly(rootof) has fastpath to 0

- Author: @smichr
- Merged: 2026-11-02T21:18:06Z into `master`
- Labels: (none)
- Size: +38 / -0 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

In #15753 there is a discussion about how powers of RootOf might be handled to allow for better simplification. In general, this can lead to symbolic explosion. In case of evaluating a PurePoly at one of its roots, however, we have an opportunity to recognize the zero right away.

#### Brief description of what is fixed or changed

#### Other comments

#### AI Generation Disclosure

I identified the issue and discussed the proposed solution. Code and tests written by ChatGPT.

## Commits

- 280e5f9783 (Christopher Smith): polys: detect roots of univariate PurePoly during evaluation
- bc3f630145 (Christopher Smith): tests: cover PurePoly evaluation at defining and unrelated roots
- ac9dbf166e (Christopher Smith): polys: restrict RootOf divisibility shortcut to characteristic zero

## Conversation

(no comments)

## Reviews

(no reviews)
