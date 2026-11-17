# Pull request #31041: fix(ci): remove CI job that checks PRs for merge conflicts

- Author: @oscarbenjamin
- Merged: 2026-11-11T19:26:34Z into `master`
- Labels: CI
- Size: +2 / -36 in 3 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

This is causing CI errors on all PRs:
https://github.com/sympy/sympy/actions/runs/43056018373/job/130645561865

#### Brief description of what is fixed or changed

Remove the checkconflict.yml workflow file. This workflow runs a script that checks all PRs to see if they are mergeable and adds a label indicating whether the PR has merge conflicts. It stopped working for some reason and I've decided that the fix is just to delete it.

I don't think that we need to explicitly labels PRs with merge conflicts with a label that says that they have merge conflicts (I don't think I've ever made use of as a feature).

Also I don't like that this workflow uses the risky `pull_request_target` event that has been exploited by hackers in other repos so removing it makes me a little happier about the security of CI.

Another change here is to fix a test that was recently added that fails on PyPy.

#### Other comments

#### AI Generation Disclosure

NO AI USE

## Commits

- 0a2b85ec9b (Oscar Benjamin): fix(ci): remove CI job that checks PRs for merge conflicts
- c7f2d0f52d (Oscar Benjamin): test(core): fix test that failed under pypy
- d961d5ccb9 (Oscar Benjamin): Remove checkconflict.yml from whitelist

## Conversation

### @smichr commented

Did you try change the `read` to `write`?
```
permissions:
  pull-requests: write
  issues: write
```
ChatGPT notes, "I inspected the pinned action's TypeScript source. It queries GitHub's API and updates labels. It does not check out or execute contributor code."

### @oscarbenjamin commented

> Did you try change the `read` to `write`?

No, but those things have not changed since 2 days ago when this started breaking. This workflow has never been particularly useful and I don't want to maintain it and I don't like the security risk.

I don't care what ChatGPT says about the pinned action: it is simpler and safer not to have any pull_request_target anywhere in CI.


## Reviews

(no reviews)
