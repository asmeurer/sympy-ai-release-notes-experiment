# Pull request #31144: create lists without explicit loops

- Author: @smichr
- Merged: 2026-11-17T16:06:50Z into `master`
- Labels: (none)
- Size: +14 / -40 in 6 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

Use list operations instead of loops to create [x, x, x, x, ... x] type lists.

#### Other comments

#### AI Generation Disclosure

Found one instance and used ChatGPT to find others and make the changes.

## Commits

- 3d87f692cb (Christopher Smith): Avoid append loops when padding subresultant coefficients
- e4794deb94 (Christopher Smith): Build matrix representations with a nested comprehension
- b39b7f590a (Christopher Smith): Construct default subgroup tests without an append loop
- 7f5cffe7b7 (Christopher Smith): Use a comprehension for table column headings
- f8e7f9f946 (Christopher Smith): Expand repeated quantum operators without per-item appends
- 59f16e334e (Christopher Smith): Preallocate flags for vector pretty printing

## Conversation

(no comments)

## Reviews

(no reviews)
