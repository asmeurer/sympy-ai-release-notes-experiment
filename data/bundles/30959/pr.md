# Pull request #30959: Fix copying of symbols and other atoms

- Author: @raman118
- Merged: 2026-11-05T18:43:08Z into `master`
- Labels: (none)
- Size: +22 / -1 in 2 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Fixes #19324.

#### Brief description of what is fixed or changed

`Symbol('s').copy()` raises `TypeError` because the inherited method reconstructs it from empty arguments. `Atom.copy()` now returns the immutable atom itself, preserving symbol assumptions, dummy identity, wildcard exclusions, and numeric precision. Nonatomic expressions retain their existing shallow-copy behavior.

#### Other comments

The regression reproduced the original `TypeError`. Basic, symbol, and number tests passed (156 tests), along with code-quality tests (6 passed), Ruff, and `bin/mailmap_check.py`.

#### AI Generation Disclosure

OpenAI Codex (GPT-6 Astra) generated all changes in `sympy/core/basic.py` and `sympy/core/tests/test_basic.py`. This PR description was also written by the AI agent at the account owner's request.

## Commits

- e1f739537c (raman118): Allow copying immutable atoms
      Return the atom itself instead of reconstructing it from empty args, preserving symbol assumptions, dummy identity, wildcard exclusions, and numeric precision.
      AI-generated changes by OpenAI Codex (GPT-6 Astra).

## Conversation

### @Peter230655 commented

Just curiosity: you have opened 4 - 5 PR within one hour or so on very different subjects it seemed to me. As you state, they were opened by AI. But do you, the human behind these PRs understand all of this in depth? Admirable!!

### @raman118 commented

@Peter230655 I genuinely appreciate the concern! I first tried contributing last October but failed repeatedly and eventually took a long break. Now I'm giving it another shot. Yes, I use AI, but not to blindly generate PRs. I use it as a tool, while making sure I understand, review, and learn from my contributions. I'm here to improve, not flood repositories with AI slop.

### @smichr commented

@Peter230655 , when the issue gives a straightforward solution and a person or AI implements that solution as a small targeted change, that is a nice way to close out an issue.

### @Peter230655 commented

> @Peter230655 I genuinely appreciate the concern! I first tried contributing last October but failed repeatedly and eventually took a long break. Now I'm giving it another shot. Yes, I use AI, but not to blindly generate PRs. I use it as a tool, while making sure I understand, review, and learn from my contributions. I'm here to improve, not flood repositories with AI slop.

I was not concerned. I have to admire a person who can fully understand such diverse issues within an hour!


## Reviews

(no reviews)
