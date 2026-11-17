# Issues and pull requests referenced by this pull request

## Pull request #30362: Use setuptools-scm for __version__ and PEP 639 license metadata

- Opened by @oscarbenjamin, state: closed, merged 2026-11-03

#### References to other Issues or PRs

Built on top of gh-30360

#### Brief description of what is fixed or changed

This sets the version when installing from git e.g. after `pip install -e .`
```console
>>> sympy.__version__
'1.15.0.dev2479+g93aa198f0'
```
That means that it is a development version that is 2479 commits after 1.14 and the commit is 93aa198f0.

There is a fallback so that sympy can still be imported directly from a development checkout (without any install step) but then the version will be `0.0.dev0+uninstalled`.

When building from a tagged commit the version gets set automatically by setuptools-scm.

One advantage of this is that it simplifies managing the version string in the release cycle (it never needs to be committed).

Using setuptools-scm also means that we don't need commit_hash.txt which makes it possible to remove setup.py in future and just use pyproject.toml (this is my actual motivation).

#### Other comments

#### AI Generation Disclosure

Mostly written by codex.
