# Can AI write SymPy's release notes?

An experiment comparing release notes written by Claude Sonnet with the release notes that contributors wrote by hand in their pull request descriptions, for 100 recently merged pull requests to [sympy/sympy](https://github.com/sympy/sympy).

**The findings are in [REPORT.md](REPORT.md).** Every pull request is shown side by side in [report/comparisons.md](report/comparisons.md).

## How it works

1. `scripts/fetch_prs.py` fetches the 100 most recently merged pull requests to master that have a release notes block, with their diffs, commits, comments, reviews, and the issues they reference (`data/raw/`).
2. `scripts/build_bundles.py` splits each one into the ground truth (`data/truth/`) and a blinded bundle (`data/bundles/`) with every trace of the release notes removed. The blinding rules are in the docstring of that script, and `data/blinding_log.json` records what was removed from each pull request.
3. `scripts/canary.py` checks that the sandbox holds: a session with the same flags as the real runs is told to read the answers by every route it can find, and all of them must be refused.
4. `scripts/run_generation.py` runs one isolated headless Claude Code session per pull request with `claude-sonnet-5-5`. The session gets the prompt in `prompts/generate.md` (which embeds the wiki's [Writing Release Notes](https://github.com/sympy/sympy/wiki/Writing-Release-Notes) guide, the bot's list of allowed headers, and a sample of the 1.14 release notes), the blinded bundle, and a read-only sympy checkout. It has the Read, Grep, and Glob tools and nothing else: no shell, no network, no MCP servers, no user configuration.
   A second generation run with `--prompt generate_release_context.md --out generation_release_context` adds the previous release and its date to the prompt and names the files in the bundle. It was run after the main results showed that the model was writing entries for regressions that never shipped. That run was not judged.
5. `scripts/run_judge.py` has `claude-opus-5-5` compare the two notes for each pull request against the diff. The judge sees them as A and B in a random order and is not told that either one was written by a model. With `--ai-flag` it runs a separate, non-blind check of whether the hand-written entry itself looks AI-written.
6. `scripts/make_report.py` computes the statistics (`report/stats.json`, `report/tables.md`) and writes the side-by-side comparison (`report/comparisons.md`).

## Reproducing

Requires Python 3.11 or newer (standard library only), the GitHub CLI (`gh`) logged in, and Claude Code (`claude`) logged in. No API keys are stored anywhere in this repository; both tools use their own credential stores.

```
python scripts/fetch_prs.py --count 100
python scripts/make_style_examples.py path/to/sympy.wiki/Release-Notes-for-1.14.md
python scripts/build_bundles.py
python scripts/canary.py
python scripts/run_generation.py
python scripts/run_generation.py --prompt generate_release_context.md --out generation_release_context
python scripts/run_judge.py
python scripts/run_judge.py --ai-flag
python scripts/make_report.py
```

Every step is resumable: results that already exist are skipped. The `work/` directory (the sympy checkout, the per-run sandboxes, and the raw transcripts) is not committed.

## Layout

- `prompts/`: the prompts, the wiki guide as given to the model, the header list, and the style examples.
- `scripts/`: the pipeline.
- `data/raw/`: everything fetched from GitHub, including the original release notes.
- `data/truth/`: the hand-written release notes, parsed.
- `data/bundles/`: what the generating model saw.
- `data/generation/`: Sonnet's output, token usage, and tool calls for each pull request (main run).
- `data/generation_release_context/`: the same for the release-context prompt.
- `data/judge/`, `data/ai_flag/`: the judge's verdicts, with the A/B assignment.
- `report/`: the generated statistics and comparison.

## Notes on the data

- The merge dates of referenced pull requests in `linked.md` were added after the main generation run and the judging. The main run never opened `linked.md` (its tool calls are recorded in `data/generation/`), so this does not affect its results. The judge opened it in 6 runs, before the dates were added.
- Five pull requests whose descriptions reference issues as `gh-NNNN` were refetched, regenerated, and rejudged after the first pass, because the first version of the fetch script did not recognize that form.
- Saved results have local paths replaced with `<repo>` and `~`.
