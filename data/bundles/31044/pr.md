# Pull request #31044: print Mod like a Function w/o parens

- Author: @smichr
- Merged: 2026-11-12T06:38:12Z into `master`
- Labels: (none)
- Size: +20 / -1 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

Mod has precedence like Mul so it printed with parentheses surrounding it when it appeared as a factor in an expression. This is not necessary since it is not shown in inline form. The printing need for parentheses is now handled in the printers while leaving the global precedence unchanged.

#### Other comments

#### AI Generation Disclosure

Collaborative effort with ChatGPT after identifying the issue while working on other Mod related issues.

## Commits

- dbffeac4c5 (Christopher Smith): print Mod like a Function w/o parens

## Conversation

(no comments)

## Reviews

(no reviews)
