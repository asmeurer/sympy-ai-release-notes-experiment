# Pull request #30931: Remove stale xfails

- Author: @tqa236
- Merged: 2026-11-03T14:23:46Z into `master`
- Labels: (none)
- Size: +6 / -19 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #14716

#### Brief description of what is fixed or changed

I noticed that there are more xfail tests that pass now, so I swept through the tests to identify them and bisect to the PR made them passed. 

| Test | First passing commit | Fixed by PR | Closes |
|---|---|---|---|
| `test_N8` | `82005f28bd` unequality splitting enabled | #25544 | — |
| `test_V13` | `bbd0c57686` integrals: add the atan floor terms only to evaluate definite integrals | #30558 | — |
| `test_V16` | `6856a0953e` manualintegrate: complete the square and rewrite trig products | #30311 | — |
| `test_issue_14716` | `ed5e2f9b47` manualintegrate: improve u-substitution for linear terms | #30311 | #14716 |

The `slow` decorator is also removed if the test is no longer slow now.

| Test | Time | `@slow` |
|---|---|---|
| `test_N8` | 0.04s | removed |
| `test_V16` | 1.56s | removed |
| `test_issue_14716` | 5.08s | kept |
| `test_V13` | 0.23s | never had it |

About the integration. Wolfram Alpha gives the same numerical answer but a different closed-form answer.

<img width="803" height="563" alt="image" src="https://github.com/user-attachments/assets/3c7ad111-1da6-41ea-af50-3cc4bb0f39c1" />

#### Other comments

I wonder if it's a good idea to make a passed xfailed test fail the CI instead, as it'll send a clear signal about past context and discussion.

#### AI Generation Disclosure

Claude ran the tests and the bisect. I checked the results.

## Commits

- 5894d94e78 (Trinh Quoc Anh): Move test_issue_14716 out of the failing integrals
      The integral is computed since manualintegrate improved u-substitution for
      linear terms (ed5e2f9b47, #30311), so the test has been passing as an XPASS.
      Assert the closed form that was previously left in a comment.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- ab826af690 (Trinh Quoc Anh): test_wester: remove XFAIL from test_N8
      ask() proves this since the LRA satisfiability handler learned to split
      unequalities (82005f28bd, #25544). The test runs in well under a second, so
      drop @slow too.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- 0f78c612c3 (Trinh Quoc Anh): test_wester: remove XFAIL from test_V13
      The antiderivative simplifies to the expected atan form since the atan
      floor terms are only added when evaluating definite integrals
      (bbd0c57686, #30558).
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- a1ecd05c30 (Trinh Quoc Anh): test_wester: remove XFAIL from test_V16
      manualintegrate computes this integral since it learned to rewrite trig
      products (6856a0953e, #30311). The test takes about 1.5s, so drop @slow too.
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

## Conversation

(no comments)

## Reviews

(no reviews)
