# Pull request #31117: release: release from master on tag push

- Author: @oscarbenjamin
- Merged: 2026-11-15T17:39:09Z into `master`
- Labels: Releasing
- Size: +257 / -93 in 8 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

#### Brief description of what is fixed or changed

Change the release CI workflow that it can release directly from a tag push to the master branch.

#### Other comments

#### AI Generation Disclosure

GPT Astra wrote the changes and I have not yet reviewed them.

## Commits

- b0fa196781 (Oscar Benjamin): release: release from master on tag push
- 5ba2240ab8 (Oscar Benjamin): release: fix authors check and list all tags
- bed53f9905 (Oscar Benjamin): release: don't hardocde versions in benchmarks CI job
- 64ac29f6d9 (Oscar Benjamin): release: update version constraints for mpmath and python-flint
- bd6205bc3e (Oscar Benjamin): Add REDME for making releases
- 7c81a62777 (Oscar Benjamin): release: fix issues in the release workflow

## Conversation

(no comments)

## Reviews

### @Upabjojr reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @Upabjojr commented on `.github/workflows/release.yml`

python 3.15 ?

### @Upabjojr commented on `pyproject.toml`

not supporting the latest versions of `mpmath` ?

### @oscarbenjamin commented on `pyproject.toml`

Right now mpmath 1.4.1 is the newest version. This is a cap to prevent future versions of mpmath from being used.

### @oscarbenjamin commented on `.github/workflows/release.yml`

I'm updating this to 3.11 to 3.15 in gh-31161.
