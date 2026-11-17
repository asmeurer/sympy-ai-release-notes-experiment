"""Check that the isolated sessions really cannot reach the answers.

Runs a session with exactly the same flags as the generation runs and tells
it to read the ground truth by every route available. The check passes only
if every attempt is refused. Also runs a trivial session to measure the fixed
token overhead of the harness, and writes both results to data/canary.json.
"""

import argparse
from pathlib import Path

from common import (
    DATA, GENERATION_MODEL, RAW, SYMPY_CLONE, TRUTH, WORK, pr_numbers, read_json,
    run_claude, write_json,
)
from run_generation import prepare_run_dir

SCHEMA = {
    "type": "object",
    "properties": {
        "attempts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "target": {"type": "string"},
                    "tool": {"type": "string"},
                    "succeeded": {"type": "boolean"},
                    "what_came_back": {"type": "string"},
                },
                "required": ["target", "tool", "succeeded", "what_came_back"],
                "additionalProperties": False,
            },
        },
        "tools_you_have": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["attempts", "tools_you_have"],
    "additionalProperties": False,
}

TRIVIAL_SCHEMA = {
    "type": "object",
    "properties": {"ok": {"type": "boolean"}},
    "required": ["ok"],
    "additionalProperties": False,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extra", nargs="*", default=[],
                        help="other files that must be unreachable")
    args = parser.parse_args()

    number = pr_numbers()[-1]
    run_dir = prepare_run_dir(number)
    targets = [
        str(TRUTH / f"{number}.json"),
        f"../../../data/truth/{number}.json",
        str(RAW / f"{number}.json"),
        str(Path.home() / ".claude" / "CLAUDE.md"),
        *args.extra,
    ]
    prompt = (
        "This is a test of a file access sandbox. Please try as hard as you can to read "
        "each of the files below, using every tool you have (Read, Grep with the file or "
        "its directory as the path, Glob on its directory). Try each file with each tool, "
        "and report honestly what came back for every attempt. Also try to list the "
        f"directory {TRUTH} with Glob, and try any tool you have for fetching "
        f"https://github.com/sympy/sympy/pull/{number} from the web. List every tool "
        "available to you.\n\n" + "\n".join(f"- {t}" for t in targets)
    )
    canary = run_claude(
        prompt, cwd=run_dir, model=GENERATION_MODEL, schema=SCHEMA,
        transcript=WORK / "transcripts" / "canary.jsonl", add_dirs=[SYMPY_CLONE],
    )
    trivial = run_claude(
        "Reply that everything is ok. Do not use any tools.",
        cwd=run_dir, model=GENERATION_MODEL, schema=TRIVIAL_SCHEMA,
        transcript=WORK / "transcripts" / "trivial.jsonl", add_dirs=[SYMPY_CLONE],
    )
    write_json(DATA / "canary.json", {"canary": canary, "trivial": trivial})

    attempts = canary["structured_output"]["attempts"]
    for attempt in attempts:
        print(attempt["succeeded"], attempt["tool"], attempt["target"], "->",
              attempt["what_came_back"][:100])
    print("tools:", canary["tools_available"], "mcp:", canary["mcp_servers"])
    print("trivial usage:", trivial["usage"], trivial["total_cost_usd"])

    truth_text = read_json(TRUTH / f"{number}.json")["raw"]
    transcript = (WORK / "transcripts" / "canary.jsonl").read_text()
    assert truth_text.strip()[:40] not in transcript, "ground truth appeared in the transcript"
    assert not any(a["succeeded"] for a in attempts), "a canary read succeeded"
    assert not canary["mcp_servers"], canary["mcp_servers"]
    print("canary passed: no route to the answers")


if __name__ == "__main__":
    main()
