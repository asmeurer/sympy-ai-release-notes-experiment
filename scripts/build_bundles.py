"""Split each fetched pull request into ground truth and a blinded bundle.

data/truth/<n>.json holds the release notes the author wrote.
data/bundles/<n>/ holds what the generating model is allowed to see: the
pull request with every trace of the release notes removed.

Blinding rules:

- The whole "Release Notes" section of the description is cut out, and all
  HTML comments (the template boilerplate) are removed.
- Comments by bots are dropped (sympy-bot echoes the release notes).
- Any comment, review, or commit message that talks about release notes is
  dropped, since it would leak the entry/no-entry decision.
- Linked pull requests get the same treatment for their descriptions.
- Any remaining comment, review, or linked item that quotes a ground truth
  entry verbatim is dropped.

The title, the rest of the description, and commit messages are kept even if
they overlap with the release notes, because those would still exist if
nobody wrote release notes by hand. The overlap is recorded for the report.
"""

import difflib
import re
import shutil

from common import (
    BEGIN_MARKER, BUNDLES, DATA, END_MARKER, RAW, RELEASE_NOTES_MENTION, TRUTH,
    normalize, parse_release_notes, pr_numbers, read_json, write_json,
)

MAX_LINKED_BODY = 6000


def is_bot(login):
    return login == "sympy-bot" or login.endswith("[bot]")


def strip_release_notes(body):
    """Remove the release notes section and HTML comments from a description."""
    body = body.replace("\r\n", "\n")
    start = body.find(BEGIN_MARKER)
    end = body.find(END_MARKER)
    if start != -1 and end != -1 and end > start:
        body = body[:start] + body[end + len(END_MARKER):]
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    body = re.sub(r"^#+\s*Release Notes\s*$", "", body, flags=re.MULTILINE | re.IGNORECASE)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def disclosure_section(body):
    match = re.search(
        r"#+\s*AI Generation Disclosure\s*\n(.*?)(?=\n#+ |\Z)", body, flags=re.DOTALL
    )
    return match.group(1).strip() if match else None


def quotes_truth(text, truth_entries):
    norm = normalize(text)
    for entry in truth_entries:
        needle = normalize(entry["text"])
        if len(needle) >= 25 and needle in norm:
            return True
    return False


def filter_items(items, truth_entries, log, kind):
    kept = []
    for item in items:
        if is_bot(item["author"]):
            log["dropped_bot"] += 1
        elif not item["body"].strip():
            kept.append(item)
        elif RELEASE_NOTES_MENTION.search(item["body"]):
            log["dropped_mentions_release_notes"].append(kind)
        elif quotes_truth(item["body"], truth_entries):
            log["dropped_quotes_truth"].append(kind)
        else:
            kept.append(item)
    return kept


def build(number):
    raw = read_json(RAW / f"{number}.json")
    truth = parse_release_notes(raw["body"])
    log = {
        "dropped_bot": 0,
        "dropped_mentions_release_notes": [],
        "dropped_quotes_truth": [],
        "redacted_description_lines": 0,
    }

    description = strip_release_notes(raw["body"])
    kept_lines = []
    for line in description.split("\n"):
        if RELEASE_NOTES_MENTION.search(line):
            log["redacted_description_lines"] += 1
        else:
            kept_lines.append(line)
    description = "\n".join(kept_lines)

    commits = []
    for commit in raw["commits"]:
        if RELEASE_NOTES_MENTION.search(commit["message"]):
            log["dropped_mentions_release_notes"].append("commit")
        else:
            commits.append(commit)

    comments = filter_items(raw["issue_comments"], truth["entries"], log, "comment")
    reviews = filter_items(raw["reviews"], truth["entries"], log, "review")
    review_comments = filter_items(
        raw["review_comments"], truth["entries"], log, "review_comment"
    )

    linked = []
    for item in raw["linked"]:
        body = strip_release_notes(item["body"])
        body = "\n".join(
            ln for ln in body.split("\n") if not RELEASE_NOTES_MENTION.search(ln)
        )
        if quotes_truth(body, truth["entries"]) or quotes_truth(item["title"], truth["entries"]):
            log["dropped_quotes_truth"].append("linked")
            continue
        linked.append({**item, "body": body[:MAX_LINKED_BODY]})

    note_text = " ".join(entry["text"] for entry in truth["entries"])
    overlap = {
        "title_similarity": difflib.SequenceMatcher(
            None, normalize(raw["title"]), normalize(note_text)
        ).ratio() if note_text else None,
        "truth_quoted_in_description": quotes_truth(description, truth["entries"]),
        "truth_quoted_in_title": quotes_truth(raw["title"], truth["entries"]),
        "truth_quoted_in_commits": any(
            quotes_truth(c["message"], truth["entries"]) for c in commits
        ),
    }

    write_json(TRUTH / f"{number}.json", {
        "number": number,
        "author": raw["author"],
        "title": raw["title"],
        "merged_at": raw["merged_at"],
        **truth,
        "ai_disclosure": disclosure_section(strip_release_notes(raw["body"])),
        "overlap": overlap,
    })

    out = BUNDLES / str(number)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    parts = [
        f"# Pull request #{number}: {raw['title']}",
        "",
        f"- Author: @{raw['author']}",
        f"- Merged: {raw['merged_at']} into `{raw['base']}`",
        f"- Labels: {', '.join(raw['labels']) or '(none)'}",
        f"- Size: +{raw['additions']} / -{raw['deletions']} in {raw['changed_files']} files"
        " (full diff in `diff.patch`)",
        "",
        "## Description",
        "",
        description or "(empty)",
        "",
        "## Commits",
        "",
    ]
    for commit in commits:
        first, *rest = commit["message"].strip().split("\n")
        parts.append(f"- {commit['sha'][:10]} ({commit['author']}): {first}")
        parts.extend(f"      {ln}" for ln in rest if ln.strip())
    parts += ["", "## Conversation", ""]
    if not comments:
        parts.append("(no comments)")
    for comment in comments:
        parts += [f"### @{comment['author']} commented", "", comment["body"].strip(), ""]
    parts += ["", "## Reviews", ""]
    if not reviews and not review_comments:
        parts.append("(no reviews)")
    for review in reviews:
        body = review["body"].strip()
        parts += [f"### @{review['author']} reviewed: {review['state']}", "", body, ""]
    for comment in review_comments:
        parts += [
            f"### @{comment['author']} commented on `{comment['path']}`", "",
            comment["body"].strip(), "",
        ]
    (out / "pr.md").write_text("\n".join(parts).rstrip() + "\n")
    (out / "diff.patch").write_text(raw["diff"])

    if linked:
        parts = ["# Issues and pull requests referenced by this pull request", ""]
        for item in linked:
            kind = "Pull request" if item["is_pull_request"] else "Issue"
            parts += [
                f"## {kind} #{item['number']}: {item['title']}",
                "",
                f"- Opened by @{item['author']}, state: {item['state']}"
                + (f", merged {item['merged_at'][:10]}" if item.get("merged_at") else ""),
                "",
                item["body"].strip() or "(empty)",
                "",
            ]
        (out / "linked.md").write_text("\n".join(parts).rstrip() + "\n")

    return log, truth


def verify(number, truth):
    """Fail loudly if the bundle still contains the answer."""
    bundle = BUNDLES / str(number)
    text = (bundle / "pr.md").read_text()
    conversation = text[text.index("\n## Conversation"):]
    linked = (bundle / "linked.md").read_text() if (bundle / "linked.md").exists() else ""
    whole = text + linked
    assert BEGIN_MARKER not in whole and END_MARKER not in whole, number
    assert "sympy-bot" not in conversation, number
    assert not RELEASE_NOTES_MENTION.search(conversation), number
    assert not RELEASE_NOTES_MENTION.search(linked), number
    assert not quotes_truth(conversation, truth["entries"]), number
    assert not quotes_truth(linked, truth["entries"]), number
    description = text[text.index("\n## Description"):text.index("\n## Commits")]
    assert not RELEASE_NOTES_MENTION.search(description), number


def main():
    logs = {}
    for number in pr_numbers():
        log, truth = build(number)
        verify(number, truth)
        logs[str(number)] = log
    write_json(DATA / "blinding_log.json", logs)
    affected = {
        n: log for n, log in logs.items()
        if log["dropped_mentions_release_notes"] or log["dropped_quotes_truth"]
        or log["redacted_description_lines"]
    }
    print(f"built {len(logs)} bundles; {len(affected)} needed redaction beyond bot comments")
    for n, log in affected.items():
        print(n, log)


if __name__ == "__main__":
    main()
