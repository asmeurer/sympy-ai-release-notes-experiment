SymPy is preparing a release, and the release notes are being assembled from the pull requests that were merged since the last release. Your job is to write the release notes entry for one of those pull requests, or to decide that it should not have one.

Until now, each contributor wrote the entry for their own pull request by hand. This pull request has no hand-written entry, so yours is what will be published on the release notes page, where SymPy's users will read it to learn what changed. Nobody will edit it first, so it has to be accurate and ready to publish.

## What you have

The current directory holds everything about the pull request:

- `pr.md`: the title, description, commit messages, discussion, and reviews.
- `diff.patch`: the full diff that was merged.
- `linked.md` (only present for some pull requests): the issues and pull requests that this one references.

A read-only checkout of the SymPy repository, at the commit being released, is at `{sympy_path}`. Use it when the diff alone does not tell you what you need, for example to check whether a changed function is part of the public API or only an internal helper, or to see how a function is used.

Descriptions and titles are written by the contributor and are sometimes inaccurate, overstated, or out of date with what was finally merged. The diff is the source of truth for what changed. If the description and the diff disagree, go with the diff.

## SymPy's guide to writing release notes

This is the guide contributors follow, copied from the SymPy wiki. The parts about the pull request description and the bot describe the old manual process; the section "What Makes a Good Release Notes Entry?" is what applies to you.

<guide>
{guide}
</guide>

## Allowed headers

Every entry goes under the header of the submodule it affects. These are the only allowed headers. Use `other` for changes that do not belong to a submodule.

<submodules>
{submodules}
</submodules>

## Examples from a past release

These entries are from the SymPy 1.14 release notes, to show the usual length and tone. They were written by many different contributors and do not all follow the guide. Where they differ from the guide, follow the guide.

<examples>
{examples}
</examples>

## What to return

Decide first whether the pull request needs an entry at all, using the guide's criteria: an entry is for changes that affect people who use SymPy. If it does not need one, set `no_entry` to true and leave `entries` empty.

Otherwise, write the entries. Most pull requests need exactly one. Write more than one only when the pull request makes separate user-visible changes, and give each its own submodule header. Each entry's `text` is the sentence itself, in Markdown, without the bullet, the header, the pull request number, or the author's name, since those are added automatically.

In `reasoning`, say in one or two sentences why the pull request does or does not need an entry and what you based the entry on.
