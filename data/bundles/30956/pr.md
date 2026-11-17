# Pull request #30956: mailmap and code quality must pass before other tests are run

- Author: @smichr
- Merged: 2026-11-12T01:31:08Z into `master`
- Labels: CI
- Size: +7 / -8 in 1 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

This makes the existing author and code quality checks prerequisites for running further tests.

#### Other comments

#### AI Generation Disclosure

Author's idea was implemented and iterated over with ChatGPT that wrote all code. It was further simplified at the request of @oscarbenjamin .

## Commits

- 27a2003e8f (Christopher Smith): ci: gate test jobs on existing Check Authors and Code Quality

## Conversation

### @oscarbenjamin commented

I don't like overcomplicating CI. Can we not just make other checks wait for the mailmap check that is already there?

### @smichr commented

@oscarbenjamin , I was only thinking with so many new contributors that there is no sense running testing resources needlessly when the .mailmap is not ready. I suspect this would hardly need any maintenance once it is in place. I am +1/3 to adding it, so if you just want to close with WontFix that is ok with me.

### @oscarbenjamin commented

The mailmap check has needed a lot of maintenance over the years.

I'm just suggesting a simpler approach: make it so that other jobs wait for .mailmap and code quality checks before running.

### @smichr commented

How about squashing this as an option?

### @smichr commented

@asmeurer @oscarbenjamin this no longer does anything to any scripts, just makes the author check a prereq.

### @smichr commented

@asmeurer it looks like both maintainers need to approve the change.

### @oscarbenjamin commented

I think it is approved already. The problem is the checks haven't completed. I'm not sure why they are not running but it seems like GitHub Actions is a bit paused or something.


## Reviews

### @oscarbenjamin reviewed: APPROVED
