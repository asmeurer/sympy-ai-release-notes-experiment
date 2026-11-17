# AI-written release notes for SymPy: results

*This report was written by an AI agent (Claude Code, Claude Fable 5.2) from an experiment it designed and ran on 2026-11-17. The numbers come from `report/stats.json`; the judgments about quality come from a second model, with spot checks noted below.*

## Short answer

On this sample, the notes Sonnet wrote were at least as good as the hand-written ones, and a blind judge preferred them most of the time. Sonnet's weak spot was deciding when a pull request should have no entry: without knowing what shipped in the last release, it wrote entries for fixes to bugs that users never saw. Giving it that context fixed those cases. The cost is small: about 30,000 tokens and $0.03 per pull request, or roughly $25 to $30 for a release the size of 1.15.

| | Human | Sonnet |
|---|---|---|
| Blind judge preferred (100 PRs) | 9 | 73 (18 ties) |
| Mean judge score, 1 to 5 | 3.35 | 4.44 |
| Entries judged accurate | 54 of 79 | 62 of 72 |
| Entries judged wrong | 2 | 1 |
| Entries that are a capitalized sentence ending in a period | 67 of 91 | 85 of 85 |
| Median words per entry | 13 | 27 |

Three things temper that result, and they are covered in detail below: the judge is another Claude model, the AI's entries are twice as long as the guide asks for, and about half of the "human" notes in this sample appear to have been written by AI already.

## What was tested

The sample is the 100 most recently merged pull requests to master that have a release notes block, merged between 2026-11-02 and 2026-11-17. Contributors wrote an entry for 79 of them and `NO ENTRY` for 21. There are 31 authors, but five of them account for 66 of the pull requests (`smichr` 22, `raman118` 15, `oscarbenjamin` 11, `hunterhogan` 10, `ish1416` 8), so the "human" side is mostly those five people's habits.

For each pull request, one isolated Sonnet session (`claude-sonnet-5-5`) got the wiki's Writing Release Notes guide, the bot's list of allowed headers, a sample of 1.14 entries, and a bundle with the title, description, commits, discussion, reviews, the diff, and the referenced issues. The release notes section was cut from the description, bot comments were dropped, and any comment that discussed the release notes was dropped (7 pull requests needed that). The session could read the bundle and a sympy checkout and had no shell, network, or other tools. A canary run with the same flags, told to read the answers by any route, was refused every time, and no generation run touched a path outside its sandbox.

A second model (`claude-opus-5-5`) then compared the two notes for each pull request against the diff. It saw them as A and B in a random order and was told that two people had written them.

## Whether to write an entry

| | Sonnet wrote an entry | Sonnet said NO ENTRY |
|---|---|---|
| Human wrote an entry | 67 | 12 |
| Human said NO ENTRY | 5 | 16 |

The two sides agreed on 83 of 100. The 17 disagreements fall into clear groups.

**Human entry, Sonnet `NO ENTRY` (12).** Eight are pull requests that only add type annotations, where the contributor wrote entries like "Annotations for `Basic.has`." The others are a typo fix in `LICENSES_BUNDLED.txt` (entry: "Fix typo"), an internal refactoring, a change to SymPy's own doctest checker, and a fix for a regression from a pull request merged a few days earlier. The judge sided with Sonnet on all 12. Whether annotation-only changes belong in the release notes is a policy question the guide does not answer. Sonnet was not consistent about it either: it wrote an entry for one annotation pull request ([31027](https://github.com/sympy/sympy/pull/31027)) in the main run and `NO ENTRY` for the same one in a later run. If this goes further, the guide or the prompt should say which it is.

**Human `NO ENTRY`, Sonnet entry (5).** I checked these by hand, since they are the cases where a maintainer and the model disagree.

- [30930](https://github.com/sympy/sympy/pull/30930) and [31135](https://github.com/sympy/sympy/pull/31135) fix regressions that were introduced after 1.14.0 (one by a pull request merged in June 2025, the other reported against 1.15.0rc2). No released version had these bugs, so by rule 6 of the guide the maintainer's `NO ENTRY` is right and Sonnet's entry is wrong. This is the one systematic error I found, and the judge caught it too.
- [30993](https://github.com/sympy/sympy/pull/30993) gives `nan` a sort key different from `-oo`. It was prompted by test failures after a recent pull request, but the identical sort keys predate 1.14, so an entry is defensible. The judge called it borderline.
- [31044](https://github.com/sympy/sympy/pull/31044) changes `str` output (`3*Mod(x, y)` where it used to print `3*(Mod(x, y))`), and [31117](https://github.com/sympy/sympy/pull/31117) is a release-workflow pull request that also caps mpmath below 1.5 and changes which python-flint versions are used. These look like user-visible changes that the hand-written notes left out, and the judge agreed.

### Fixing the regression problem

The two regression cases were not a failure of judgment so much as missing information, and part of that was my setup. The main-run prompt did not say what the previous release was, and although the referenced issues were in the bundle as `linked.md`, the prompt only said that file exists "for some pull requests", and Sonnet did not open it in any of the 76 runs that had one.

I reran generation with a revised prompt (`prompts/generate_release_context.md`) that states the previous release and its date, explains rule 6, and names the files present, and with the merge date of each referenced pull request added to `linked.md`. Sonnet then read `linked.md` in all 76 runs and returned `NO ENTRY` for 30930 and 31135, citing the merge date and the issue text. (A first attempt that gave a pull request number cutoff instead of dates made things worse on 30930, because the pull request that caused the regression has a low number but was merged late. Dates are the reliable signal.)

| Release-context run | Sonnet wrote an entry | Sonnet said NO ENTRY |
|---|---|---|
| Human wrote an entry | 66 | 13 |
| Human said NO ENTRY | 3 | 18 |

Five decisions changed between the two runs. Two are the regression fixes. The three remaining pull requests where the human said `NO ENTRY` and Sonnet wrote an entry are 30993, 31044, and 31117, discussed above. The other three (30940, 30997, 31027) are borderline pull requests that flipped for no reason connected to the prompt change, which gives a rough idea of the run-to-run noise: about 3 in 100. The release-context run was not judged, so the quality numbers in this report are all from the main run.

## Quality of the entries

On the 67 pull requests where both sides wrote an entry, the judge preferred Sonnet's on 58, the human's on 7, and called 2 ties. It called the difference clear on 34 of Sonnet's wins and none of the human's. It judged the two entries to say essentially the same thing on 38 of the 67.

| | Accurate | Minor inaccuracy | Wrong |
|---|---|---|---|
| Human (79 PRs with entries) | 54 | 23 | 2 |
| Sonnet (72 PRs with entries) | 62 | 9 | 1 |

| Judge score | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Human | 5 | 22 | 27 | 25 | 21 |
| Sonnet | 0 | 2 | 2 | 46 | 50 |

The judge's reasons for marking down hand-written entries are concrete, and they are the things the guide warns about: internal jargon, naming private helpers, not saying which function changed, lowercase fragments with no period, and issue numbers in the entry. A typical case is [31007](https://github.com/sympy/sympy/pull/31007):

```markdown
Human:  fixed a condition that allowed a hollow multiplication by 1 to remain in a final expression
Sonnet: Fixed `factor_terms` sometimes returning an unevaluated multiplication by one, such as `(1/2)*1`, in its result.
```

Sonnet's main advantage is that it reads the diff. In [31075](https://github.com/sympy/sympy/pull/31075) the description was left over from a different change. The hand-written entry describes a `CmathPrinter` fix that is not in the merged diff, which only touches `torch_code`. Sonnet noticed the mismatch and wrote the entry from the diff. I confirmed that one against the diff myself.

Where Sonnet did worse:

- **Length.** Its entries have a median of 27 words against 13 for the hand-written ones, 30 of its 85 entries run to more than one sentence, and it was longer than the human on 58 of the 67 shared pull requests. The guide asks for entries that are "very short", typically one sentence. About half of the 7 cases where the judge preferred the human were about this, for example [31063](https://github.com/sympy/sympy/pull/31063), where Sonnet put a full line of LaTeX output in the entry. The judge did not penalize length much; a maintainer reading 500 of these might. This should respond to a prompt change, but I did not test one.
- **Overreaching examples.** Its one entry judged wrong ([31135](https://github.com/sympy/sympy/pull/31135)) said the bug needed a generator argument, which it inferred from the diff and got wrong. In [30950](https://github.com/sympy/sympy/pull/30950) it gave an example that did not trigger the bug. Both come from adding specifics that the hand-written entry left out.
- **Extra entries.** In [30994](https://github.com/sympy/sympy/pull/30994) it added bullets for incidental changes that users would not notice.

Header choice was the same set of submodules on 60 of the 67 shared pull requests, and every header on both sides was valid.

## Were the original notes written by AI?

SymPy's pull request template has a required AI disclosure section, so there is something better than guessing to go on. A separate, non-blind pass classified the disclosure and assessed whether the entry itself reads as AI-written, for the 79 pull requests with entries.

| Disclosure | PRs |
|---|---|
| No AI used | 8 |
| AI used for code, tests, or investigation; nothing said about the text | 51 |
| AI wrote or drafted the description | 20 |

| Entry looks AI-written | PRs | Mean judge score of the human entry | Judge preferred Sonnet / human / tie |
|---|---|---|---|
| Likely | 40 | 3.25 | 33 / 5 / 2 |
| Cannot tell | 19 | 3.32 | 18 / 1 / 0 |
| Unlikely | 20 | 2.35 | 19 / 1 / 0 |

So only 8 of 79 pull requests declare no AI use, and about half of the hand-written entries are probably AI-written already. That changes what the comparison means: for much of this sample it is Sonnet with the diff and the guide against another model with whatever context the contributor gave it, not against a person.

The "looks AI-written" label is weak evidence, since an entry is one sentence. In practice the classifier leaned on the surrounding description and on form: 39 of the 40 "likely" entries end with a period, against 6 of the 20 "unlikely" ones. The entries that read as typed by a person scored lowest with the judge, mostly on form (lowercase fragments, no period, terse wording) and somewhat on accuracy. Per-entry labels and the evidence for each are in `report/comparisons.md`; treat individual labels as guesses.

## Tokens and cost

All numbers are what the Claude Code CLI reported for each session. Costs are its API-rate figures.

| Stage | Model | Runs | Cache write | Cache read | Output | All tokens | Cost | Per PR |
|---|---|---|---|---|---|---|---|---|
| Generation | Sonnet 5.5 | 100 | 570,664 | 2,352,870 | 48,287 | 2,972,231 | $3.00 | $0.030 |
| Generation with release context | Sonnet 5.5 | 100 | 703,573 | 2,480,079 | 59,942 | 3,244,008 | $3.66 | $0.037 |
| Blind judge | Opus 5.5 | 100 | 976,706 | 2,157,313 | 106,145 | 3,240,638 | $10.37 | $0.104 |
| Authorship check | Opus 5.5 | 79 | 152,396 | 174,020 | 30,739 | 357,313 | $1.87 | $0.024 |

For generation, a typical pull request took 4 turns (read `pr.md`, read `diff.patch`, answer), 4.4 seconds of model time, and about 29,700 tokens: 23,500 read from cache, 5,700 written to cache, and 480 output. Uncached input is negligible (4 tokens per run). The largest pull request (a 3,291-line diff) used 85,800 tokens and cost $0.14.

Of the roughly 12,000-token prefix that every run shares, about 5,200 tokens are Claude Code's own system prompt and tool definitions, and the rest is the guide, the header list, and the examples. Because that prefix is identical across runs it is cached, which is why the per-PR cost is low. The first four pilot runs, before the cache was warm, cost $0.065 to $0.10 each.

**For a whole release.** 835 pull requests were merged to master between the 1.14.0 release and 2026-11-17, and 494 of them have entries on the 1.15 release notes page. Running all 835 would take about 25 to 27 million tokens, nearly all of them cache reads, and cost about $25 with the main prompt or $31 with the release-context prompt. Without any cache benefit the upper bound is around $55. At 6 to 8 sessions in parallel, 100 pull requests took a few minutes, so a full release is well under an hour. The judge and the authorship check are costs of this experiment, not of producing notes.

## Caveats

- **The judge is a model from the same family.** Opus may favor the kind of prose Sonnet writes, and it may be able to tell which note is machine-written. It also showed a position effect: Sonnet's note won 81% of the time when it was shown first and 64% when shown second. Sonnet won clearly in both positions, so the direction of the result holds, but the margin should not be read as precise. I spot-checked the judge's strongest claims against the diffs (the stale description in 31075, the regression reasoning in 30930 and 31135) and they held. `report/comparisons.md` has every pair side by side, and reading a few dozen of those is the real test.
- **The sample is two weeks and five dominant authors.** It also comes from a release-candidate period with an unusual share of AI-assisted pull requests. A sample from a year ago could look different.
- **Hand-written notes were written without a prompt telling the author to read the guide.** Part of the gap is that Sonnet was shown the guide every time and contributors mostly do not reread it.
- **Each pull request was handled in isolation.** A release-time process sees the whole set and could merge related entries, drop entries for features that were later reverted, and write the highlights and deprecations sections. None of that was tested.
- **The main run did not use the linked issues**, as described above. The entries it wrote are based on the pull request page and the diff only.

## What I would do next

1. Have a few maintainers read `report/comparisons.md` blind to the judge's verdicts and see whether they agree with it, especially on length.
2. Use the release-context prompt as the baseline, and add an instruction to keep entries to one short sentence without long examples.
3. Decide the policy for type-annotation-only pull requests and put it in the guide.
4. Add a second pass over the whole release to merge duplicates and catch entries for changes that were reverted or superseded within the cycle.

## Files

- [report/comparisons.md](report/comparisons.md): all 100 pull requests side by side with the judge's verdict and the authorship check.
- [report/tables.md](report/tables.md) and `report/stats.json`: every number used here.
- [README.md](README.md): how the pipeline works and how to rerun it.
- `prompts/`: the exact prompts.
