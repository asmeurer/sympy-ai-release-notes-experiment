You are evaluating release notes for the SymPy project. Two people were each asked to write the release notes entry for the same merged pull request, working independently. Your job is to work out what the pull request really changed and then judge how good each candidate's answer is.

The result feeds a study of how release notes should be written for SymPy, so what matters is that your judgment is accurate. Either candidate may be the better one, both may be fine, and both may be wrong.

## What you have

The current directory holds everything about the pull request:

- `pr.md`: the title, description, commit messages, discussion, and reviews.
- `diff.patch`: the full diff that was merged.
- `linked.md` (only present for some pull requests): the issues and pull requests that this one references.

A read-only checkout of the SymPy repository is at `{sympy_path}`. Use it to check claims, for example whether a function a candidate names is public and behaves the way the entry says.

Read the diff before you look closely at the candidates. The diff is the source of truth: descriptions and titles are sometimes inaccurate or out of date with what was merged, and a candidate who repeated an inaccurate description is still inaccurate.

## SymPy's guide to writing release notes

This is the standard both candidates were asked to meet. The parts about the pull request description and the bot describe mechanics that do not matter here; the section "What Makes a Good Release Notes Entry?" is the standard.

<guide>
{guide}
</guide>

Entries go under a submodule header. The allowed headers are:

<submodules>
{submodules}
</submodules>

## The two candidates

`NO ENTRY` means the candidate decided the pull request should not appear in the release notes at all.

<candidate_a>
{candidate_a}
</candidate_a>

<candidate_b>
{candidate_b}
</candidate_b>

## What to return

`should_have_entry`: your own judgment, from the diff and the guide, of whether this pull request belongs in the release notes. Use `borderline` when reasonable maintainers could go either way.

For each candidate:

- `accuracy`: whether what the entry says is true of the merged change. `accurate` means every claim holds. `minor_inaccuracy` means it is imprecise or slightly overstated but would not mislead a user in a way that matters. `wrong` means it says something false or would mislead a user about what changed. Use `not_applicable` for `NO ENTRY`.
- `overall`: a score from 1 to 5 for how well this answer serves as the published release notes for this pull request, taking everything into account: whether the entry/no-entry decision is right, accuracy, whether an end user would understand it and learn what changed for them, the right submodule header, and the guide's rules (short, a complete sentence, past tense, no issue numbers, no implementation details users would not know). 5 is an answer you would publish as is. 3 is acceptable but with clear room for improvement. 1 is wrong or misleading, or a wrong entry/no-entry decision on a pull request where the right decision is clear. A `NO ENTRY` on a pull request that clearly needs no entry is a 5.
- `problems`: a short list of concrete problems, empty if there are none.

`same_substance`: true if the two candidates tell the user essentially the same thing (including both being `NO ENTRY`), even if the wording differs.

`preferred`: which candidate you would rather publish, or `tie` if there is no meaningful difference. `strength` says how big the difference is: `none` for a tie, `slight` when either would be fine, `clear` when one is plainly better.

`rationale`: two to four sentences explaining the verdict, specific enough that someone who has not read the diff can follow why.
