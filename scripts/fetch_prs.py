"""Fetch the most recently merged sympy pull requests and everything attached to them.

Writes one file per pull request to data/raw/. These files contain the
original release notes and must never be shown to the generating model.
"""

import argparse
import re
from concurrent.futures import ThreadPoolExecutor

from common import (
    RAW, REPO, gh, gh_api_list, gh_json, parse_release_notes, read_json, write_json,
)

MAX_LINKED = 6


def linked_numbers(pr, closing):
    numbers = [item["number"] for item in closing]
    body = pr["body"] or ""
    for match in re.finditer(r"(?:#|\bgh-|/issues/|/pull/)(\d{3,6})\b", body, re.IGNORECASE):
        numbers.append(int(match.group(1)))
    seen = []
    for number in numbers:
        if number != pr["number"] and number not in seen:
            seen.append(number)
    return seen[:MAX_LINKED]


def merge_date(number):
    return gh_json("api", f"repos/{REPO}/pulls/{number}")["merged_at"]


def add_merge_dates():
    """Add merge dates to linked pull requests in files fetched before this existed."""
    for path in sorted(RAW.glob("*.json")):
        record = read_json(path)
        changed = False
        for item in record["linked"]:
            if item["is_pull_request"] and "merged_at" not in item:
                item["merged_at"] = merge_date(item["number"])
                changed = True
        if changed:
            write_json(path, record)
            print("added merge dates to", path.stem)


def fetch_linked(number):
    result = gh_json("api", f"repos/{REPO}/issues/{number}")
    is_pull_request = "pull_request" in result
    return {
        "merged_at": merge_date(number) if is_pull_request else None,
        "number": number,
        "title": result["title"],
        "body": result["body"] or "",
        "state": result["state"],
        "is_pull_request": is_pull_request,
        "author": result["user"]["login"],
    }


def fetch_one(number):
    out = RAW / f"{number}.json"
    if out.exists():
        return number
    pr = gh_json("api", f"repos/{REPO}/pulls/{number}")
    closing = gh_json(
        "pr", "view", str(number), "-R", REPO, "--json", "closingIssuesReferences"
    )["closingIssuesReferences"]
    record = {
        "number": number,
        "title": pr["title"],
        "body": pr["body"] or "",
        "author": pr["user"]["login"],
        "labels": [label["name"] for label in pr["labels"]],
        "merged_at": pr["merged_at"],
        "created_at": pr["created_at"],
        "base": pr["base"]["ref"],
        "merge_commit_sha": pr["merge_commit_sha"],
        "additions": pr["additions"],
        "deletions": pr["deletions"],
        "changed_files": pr["changed_files"],
        "diff": gh(
            "api", f"repos/{REPO}/pulls/{number}",
            "-H", "Accept: application/vnd.github.diff",
        ),
        "commits": [
            {"sha": c["sha"], "message": c["commit"]["message"],
             "author": c["commit"]["author"]["name"]}
            for c in gh_api_list(f"repos/{REPO}/pulls/{number}/commits")
        ],
        "issue_comments": [
            {"author": c["user"]["login"], "created_at": c["created_at"], "body": c["body"] or ""}
            for c in gh_api_list(f"repos/{REPO}/issues/{number}/comments")
        ],
        "reviews": [
            {"author": r["user"]["login"], "state": r["state"],
             "submitted_at": r.get("submitted_at"), "body": r["body"] or ""}
            for r in gh_api_list(f"repos/{REPO}/pulls/{number}/reviews")
        ],
        "review_comments": [
            {"author": c["user"]["login"], "created_at": c["created_at"],
             "path": c["path"], "body": c["body"] or ""}
            for c in gh_api_list(f"repos/{REPO}/pulls/{number}/comments")
        ],
    }
    record["linked"] = [fetch_linked(n) for n in linked_numbers(record, closing)]
    write_json(out, record)
    return number


def select(count, base):
    candidates = gh_json(
        "pr", "list", "-R", REPO, "--state", "merged", "--base", base,
        "--limit", str(count * 2), "--json", "number,mergedAt,body",
    )
    candidates.sort(key=lambda p: p["mergedAt"], reverse=True)
    selected = []
    skipped = []
    for pr in candidates:
        status = parse_release_notes(pr["body"])["status"]
        if status in ("entry", "no_entry"):
            selected.append(pr["number"])
        else:
            skipped.append((pr["number"], status))
        if len(selected) == count:
            break
    print(f"selected {len(selected)} PRs; skipped without a usable block: {skipped}")
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("numbers", nargs="*", type=int,
                        help="refetch these pull requests instead of selecting new ones")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--base", default="master")
    parser.add_argument("--add-merge-dates", action="store_true",
                        help="only add merge dates to already fetched linked pull requests")
    args = parser.parse_args()

    if args.add_merge_dates:
        add_merge_dates()
        return
    if args.numbers:
        selected = args.numbers
        for number in selected:
            (RAW / f"{number}.json").unlink(missing_ok=True)
    else:
        selected = select(args.count, args.base)

    RAW.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        for number in pool.map(fetch_one, selected):
            print("fetched", number)


if __name__ == "__main__":
    main()
