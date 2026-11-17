# Pull request #31043: update Mod solving in solveset

- Author: @smichr
- Merged: 2026-11-13T19:14:05Z into `master`
- Labels: (none)
- Size: +78 / -14 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

This restores functionality removed in #31016 and extend solutions returned by solveset for Mod expressions.

#### Brief description of what is fixed or changed

Use the `cycle_length` to handle determining the leader and the repeater. When there is an Integer divisor greater than 1, see if expanding a power might resolve it. This is useful because `Mod(12**(x + 1), 21)` auto simplifies by extracting a 3 to become 3`*Mod(12**(x + 1)/3, 7)`.

#### Other comments

#### AI Generation Disclosure

This is a collaboration with ChatGPT.

## Commits

- 3bfb6714e6 (Christopher Smith): use cycle_length to solve concrete modular powers
- b12de1b19e (Christopher Smith): handle Pow expansion for denom != 1

## Conversation

(no comments)

## Reviews

(no reviews)
