# Pull request #30930: fix(matrices): restore default Frobenius norm

- Author: @oscarbenjamin
- Merged: 2026-11-03T11:42:07Z into `master`
- Labels: matrices
- Size: +10 / -2 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

This is point 0.12 from gh-30900

Restores behaviour of norm after a regression introduced in gh-27373.

#### Brief description of what is fixed or changed

Ensures that the default Matrix.norm gives the Frobenius norm instead of the spectral norm. This was changed unintentionally in gh-27373.

#### Other comments

#### AI Generation Disclosure

NO AI USE

## Commits

- 361db994af (Oscar Benjamin): fix(matrices): restore default Frobenius norm

## Conversation

### @oscarbenjamin commented

Thanks


## Reviews

(no reviews)
