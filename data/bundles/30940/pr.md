# Pull request #30940: Remove setup.py and use pyproject.toml

- Author: @oscarbenjamin
- Merged: 2026-11-10T18:59:37Z into `master`
- Labels: Uncategorised
- Size: +98 / -567 in 26 files (full diff in `diff.patch`)

## Description

#### References to other Issues or PRs

Follws on from gh-30362
Includes gh-30939

#### Brief description of what is fixed or changed

Remove setup.py and use pyproject.toml instead.

#### Other comments

#### AI Generation Disclosure

Using codex

## Commits

- c2272b3315 (Oscar Benjamin): pkg: exclude AGENTS.md from sdist
- e017a27fd0 (Oscar Benjamin): pkg: move metadata from setup.py to pyproject.toml
- 2b842228d7 (Oscar Benjamin): pkg: remove the setup.py bits that list the modules
- e818cb56cd (Oscar Benjamin): pkg: remove setup.py and update doc references
- 3d64fd2287 (Oscar Benjamin): pkg: remove redundant rules from MANIFEST.in

## Conversation

### @oscarbenjamin commented

This is ready for review.

CC @asmeurer because this changes the GHA workflow files.

### @hunterhogan commented

By coincidence, I had prepared a PR with changes to "pyproject.toml".

In my opinion, [tombi](https://github.com/tombi-toml/tombi) is outstanding. I'm not affiliated with it.

### @oscarbenjamin commented

It's better to do these hings as a PR in the sympy repo. I wouldn't merge your PR into this branch because it is making unnecessary changes for the focus of this PR which is just about removing setup.py to migrate to the modern pyproject.toml PEP  517 standard. Once this is merged further changes could be made to pyproject.toml but I don't want overcomplicate this PR (potentially delaying the merge).

### @oscarbenjamin commented

Thanks you for the reviews @hunterhogan and @moorepants.

Can I just be clear that in this PR I am intentionally not changing anything apart from moving things from setup.py to pyproject.toml:

- The license expression is the same before and after the changes in this PR. It is just moved from setup.py to pyproject.toml.
- Same goes for the LICENSE etc files. The same files are included befor and after the change.
- The files that will be included in the sdist or wheel are almost (see below) exactly the same before and after the changes here (I have checked this).

Actually the sdist here is changed so that it no longer includes setup.py (obviously redundant here) and also no longer includes AGENTS.md and CLAUDE.md since those have no purpose in a source distribution rather than a development checkout. The PR that previously added those should have excluded them from the sdist. Those files were already excluded from the built wheel. This is the only change that is not purely about migrating from setup.py to pyproject.toml.

Since this PR is focussed purely on migrating from setup.py to pyproject.toml can we focus only on that change here?

Then if we want to change e.g. the license expression or license files then we can discuss/do that in followup issues/PRs by editing the metadata in pyproject.toml rather than in setup.py.

It is very deliberate that this PR does not change anything like the license expression because I don't want the discussion on merging this to be held up at all by making decisions about things like that.

### @oscarbenjamin commented

@hunterhogan and @moorepants your comments above are good but mostly not relevant to this particular PR. If I go to the dev meeting on Tuesday I will ask @asmeurer to merge this.

If you have any objections or suggestions about the actual change here (moving setup.py stuff to pyproject.toml without changing anything else) then please say so. Otherwise I assume that you are okay with that change.

### @asmeurer commented

For the license thing, the easiest way to resolve this would be to just rewrite the SymPy LaTeX ANTLR file. It's only 100 lines of code and would be trivial to get Claude or something to just rewrite it. Then we won't have the MIT file in the repo and we won't have to include that in the license.


## Reviews

### @hunterhogan reviewed: COMMENTED

I guess I should add this link https://github.com/oscarbenjamin/sympy/pull/32 or maybe I need to submit this differently. I haven't tried to piggyback a PR before.

### @moorepants reviewed: COMMENTED



### @moorepants reviewed: COMMENTED



### @moorepants reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED



### @moorepants reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED



### @moorepants reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @oscarbenjamin reviewed: COMMENTED



### @moorepants reviewed: COMMENTED



### @moorepants reviewed: COMMENTED



### @moorepants reviewed: COMMENTED



### @moorepants reviewed: COMMENTED



### @hunterhogan reviewed: COMMENTED



### @asmeurer reviewed: DISMISSED

This looks good. setup.py is deprecated and we need to move over to pyproject.toml.

### @asmeurer reviewed: DISMISSED



### @asmeurer reviewed: APPROVED



### @moorepants commented on `MANIFEST.in`

Do these changes mean the docs and the various other inclusions are not included in the tarball?

If so, I don't think these things should be removed from the source tarball.

### @moorepants commented on `pyproject.toml`

SymPy is licensed only BSD. MIT is compatible with BSD, so we should not be advertising that SymPy is licensed MIT.

### @moorepants commented on `pyproject.toml`

These seem like development dependencies. The optional dependencies for sympy are things like numpy, matplotlib, cython, etc.

### @hunterhogan commented on `pyproject.toml`

> so we should not be advertising that SymPy is licensed MIT

Correct. This field is a statement of the license(s) in the `[project]`. At least one part of the project is licensed as MIT, which requires notice of the license, therefore this field must contain "MIT".

### @hunterhogan commented on `pyproject.toml`

The current array is incomplete.

```toml
license-files = [
    "LICENSE",                          
    "LICENSES_BUNDLED.txt",             
    "AUTHORS",                          # BSD-3-Clause names "SymPy Development Team", therefore "AUTHORS" is part of the license by incorporation; this is a programmatic declaration of the license(s) and the incorporated documents ought to be included programmatically
    "data/TeXmacs/LICENSE",             # BSD-3-Clause
    "sympy/parsing/latex/LICENSE.txt",  # MIT
]
```

### @moorepants commented on `pyproject.toml`

SymPy is licensed BSD-3-Clause and if we include any code in the distribution that is from compatible licenses (MIT is compatible with BSD-3-Clause) we are effectively relicensing that compatibly licensed code as BSD-3-Clause because the terms of BSD-3 are a superset of MIT's terms. We have to retain the MIT notice text in the distributed code, but that's it. We do not have to say that any of our code is licensed MIT and confuse the users.

### @hunterhogan commented on `pyproject.toml`

First,
These phrases and the statements that contain them are not valid claims about law.
> ... effectively relicensing ...
> ... superset ...

Second,
[License-Expression](https://packaging.python.org/en/latest/specifications/core-metadata/#core-metadata-license-expression)

Despite the horrible drafting, this field is patently a programmatic notice of the copyright categories that apply to one or more files in the "Distribution Archive." Full stop.

Third,
> We do not have to say that any of our code is licensed MIT

Notwithstanding the poor drafting, [LICENSE](https://github.com/sympy/sympy/blob/master/LICENSE) is unambiguously the _only_ notice of copyrights claimed by the "SymPy Development Team."

Fourth,
```toml
license = "BSD-3-Clause AND MIT"  # A true statement
license = "BSD-3-Clause"          # A false statement
# omitting the license key        # A true statement
```

Fifth,
### This is not legal advice.

Sixth,
When discussing law with me, please temper your condescension.

### @moorepants commented on `pyproject.toml`

>  These phrases and the statements that contain them are not valid claims about law.

I'm reasonably certain that that these are valid claims about copyright law. I'm not writing in legalese here, just trying to express the reasoning. If [licenses are compatible](https://en.wikipedia.org/wiki/License_compatibility), you may include compatibly licensed code in your derivative and license it as you wish as long as there is compatibility with your final license choice. For example, I can download a MIT licensed software, make some modifications, and redistribute it under the BSD-3-Clause license as long as I include the MIT notice in the distribution.

If you were to distribute code where there are two files and the files are incompatible licenses, then you would need to state that the source is partially licensed under one license and partially under another, i.e. somehow keeping the incompatible sources separate.

> Despite the horrible drafting, this field is patently a programmatic notice of the copyright categories that apply to one or more files in the "Distribution Archive." Full stop.

The SPDX defines the AND, OR, and WITH for these license expressions. I agree that they intend them to be used as programmatic (or mathematical) boolean operations. But the definitions fail to consider license compatibility, maybe purposely so. I agree that if your code is made up of multiple incompatibly licensed files, that using AND is necessary.

> Notwithstanding the poor drafting, LICENSE is unambiguously the only notice of copyrights claimed by the "SymPy Development Team."

I think some of the issue is that the pyproject.toml file standard entries may not be well thought out. Firstly, do the PyPA devs intend that the "license" entry only applies to the source in the associated PyPi tarball distribution? Or to the various wheels that may be present also? Wheels can be licensed differently than source tarballs due to vendored dependencies, for example. Is the "license" entry only to express the overall license of the source (taking compatibility into account) or are they expecting you to list all compatible and incompatible licenses that make up your sources. What if I created a distribution made up of 50 different compatible licenses, should I have 49 ANDs in the "license" entry? I would think not. But if I had 50 different incompatible licenses, then yes I guess so. I've read the PyPA docs and these nuances do not seem present.

We have expressed the license of SymPy as BSD-3-Clause for 20 years now and when we merged some of the compatibly licensed code over the years we consciously did not change the license of SymPy at those moments. We've discussed this nuance then. The only difference then was that these SPDX license expressions were not encoded into the standards for the setup.py metadata fields. I think we made the correct decision on the license of SymPy on multiple past occasions, so the concern I raise here is that this change seems to undo the careful thought and decisions we have made in the past.

>  When discussing law with me, please temper your condescension.

I apologize if you feel condescended. I do not intend anything personal and maybe you have read tone in my text that I do not intend. I am simply trying to state facts as I understand them. I teach copyright in my university course (as small modules) and have studied this quite a lot. I'm not just trying to be a thorn anyone's side here.

### @oscarbenjamin commented on `pyproject.toml`

Let's not discuss the licence in this PR since it does not change the license expression. That already happened in https://github.com/sympy/sympy/pull/30362 but I think it would be better to open a new issue rather than discuss it there.

For context I was involved in lengthy discussions about this in the Python forums:
https://discuss.python.org/t/expressing-project-vs-distribution-licenses-post-pep-639/90314

This PR just moves the license expression from setup.py to pyproject.toml so is not the place to discuss what that license expression should be.

### @oscarbenjamin commented on `MANIFEST.in`

After https://github.com/sympy/sympy/pull/30362 setuptools-scm already supplies the list of git-tracked files. I should have removed these lines in that PR because they are redundant when using setuptools-scm.

### @hunterhogan commented on `pyproject.toml`

You have made many excellent points. I suspect that we agree on every substantive issue, or almost every issue.

In "[A Hohfeldian Primer](https://hunterthinks.com/opinion/a-hohfeldian-primer)," I break down Hohfeld's semiotics of jural relationships. His work is most closely associated with property law, so you might already be familiar with it.

First, we need to avoid the word "license" and use precise terms. Usually, license is a synonym for privilege, but in this situation, we are mostly talking about duty. 

Second, "notice" (in the legal-term-of-art sense) is nauseatingly omnipresent here. 

That leads to the difficult third issue: omission. In some situations, an incomplete notice can create liability (in the Hohfeldian sense) even though no notice could not create liability. For example, `license = "BSD-3-Clause"          # A false statement` is incomplete notice. 

Notice, however, is also why this situation is (relatively) clear. The file, LICENSE, is the only document that contains a notice of copyright. Everything else is evidence of notice of copyright at most.

Point of law that may help you. A person cannot abandon real property. In general, however, a person can abandon personal property, whether intentionally or unintentionally. One of the many stupid things about copyright as property is that it is probably impossible to abandon a property interest in copyright. That is a massive problem because it punts "copyleft" disputes into contract law, which is not equipped to handle them. The MIT license cannot be subsumed because the property interest cannot be abandoned, so no one has the power to remove the duty of notice. It's all stupid.

My brain faded before I wrote the word "second," so I'm sure a lot of this comment is difficult to interpret. If there are actual notices in the distribution, then I think the pyproject.toml file is an automated system for providing notice of notice. It doesn't have enough information to be a notice of copyright(s). For a corporate lawyer, though, the toml fields could save countless hours of work. Imagine having to find all of the notice of copyright files in the sympy sdist. Lawyers can use the license-expression field to prioritize the inspection of packages.

Good luck with everything--especially trying to justify contemporary copyright law to students.


### This is not legal advice.

### @oscarbenjamin commented on `pyproject.toml`

Do you know of other examples that include the AUTHORS file?

I checked numpy which lists copyright as NumPy Developers and does not include any associated AUTHORS file.

The other two licenses seem the same as the ones already included.

I think we should have a separate issue to discuss which license files should be included since as for the license expression this PR is just moving this metadata from setup.py to pyproject.toml.

### @oscarbenjamin commented on `MANIFEST.in`

To be clear the list of files that is included is the same with or without this change (I have checked). It is just removing redundant lines that do not affect what is actually included.

### @oscarbenjamin commented on `pyproject.toml`

This is just preserving what is in setup.py as `extras_require`.

### @moorepants commented on `pyproject.toml`

> Do you know of other examples that include the AUTHORS file?

The PyPa documentation page that @hunterhogan linked about shows the AUTHORS file listed in their example.

### @moorepants commented on `MANIFEST.in`

Ok, great, thanks.

### @moorepants commented on `pyproject.toml`

Yes, I misread that, that's why I resolved the comment.

### @moorepants commented on `pyproject.toml`

>  https://discuss.python.org/t/expressing-project-vs-distribution-licenses-post-pep-639/90314

Maybe the most interesting observation so far is that Paul and Jason both end with Moore :smile:.

### @hunterhogan commented on `pyproject.toml`

Exactly. I like your plan to not change any content in this PR. So only as FYI https://packaging.python.org/en/latest/specifications/core-metadata/#license-file-multiple-use
