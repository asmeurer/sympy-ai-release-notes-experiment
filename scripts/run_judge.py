"""Blind comparison of the human and generated release notes.

For each pull request, a judge model sees the blinded bundle and the two
candidate notes labeled A and B in a random order, and does not know which
one a person wrote. Results go to data/judge/<n>.json together with the
A/B assignment.

With --ai-flag, instead runs the separate, non-blind check of whether the
human-written entry looks AI-written. Results go to data/ai_flag/<n>.json.
"""

import argparse
import random
import re
import shutil
from concurrent.futures import ThreadPoolExecutor

from common import (
    AI_FLAG, BUNDLES, GENERATION, JUDGE, JUDGE_MODEL, PROMPTS, SYMPY_CLONE, TRUTH,
    WORK, load_submodules, pr_numbers, read_json, render_notes, run_claude,
    write_json,
)

SEED = 20261117

CANDIDATE = {
    "type": "object",
    "properties": {
        "accuracy": {"type": "string",
                     "enum": ["accurate", "minor_inaccuracy", "wrong", "not_applicable"]},
        "overall": {"type": "integer", "minimum": 1, "maximum": 5},
        "problems": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["accuracy", "overall", "problems"],
    "additionalProperties": False,
}

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "should_have_entry": {"type": "string", "enum": ["yes", "no", "borderline"]},
        "candidate_a": CANDIDATE,
        "candidate_b": CANDIDATE,
        "same_substance": {"type": "boolean"},
        "preferred": {"type": "string", "enum": ["A", "B", "tie"]},
        "strength": {"type": "string", "enum": ["none", "slight", "clear"]},
        "rationale": {"type": "string"},
    },
    "required": ["should_have_entry", "candidate_a", "candidate_b", "same_substance",
                 "preferred", "strength", "rationale"],
    "additionalProperties": False,
}

AI_FLAG_SCHEMA = {
    "type": "object",
    "properties": {
        "disclosure": {"type": "string",
                       "enum": ["no_ai", "ai_assist", "ai_wrote_text", "blank_or_unclear"]},
        "entry_looks_ai_written": {"type": "string",
                                   "enum": ["likely", "unlikely", "cannot_tell"]},
        "evidence": {"type": "string"},
    },
    "required": ["disclosure", "entry_looks_ai_written", "evidence"],
    "additionalProperties": False,
}


def candidates(number):
    truth = read_json(TRUTH / f"{number}.json")
    generated = read_json(GENERATION / f"{number}.json")["structured_output"]
    human = render_notes(truth["status"] == "no_entry", truth["entries"])
    ai = render_notes(generated["no_entry"], generated["entries"])
    return human, ai


def judge(number, model):
    out = JUDGE / f"{number}.json"
    if out.exists() and read_json(out).get("structured_output"):
        return number, "cached"
    human, ai = candidates(number)
    human_is_a = random.Random(f"{SEED}-{number}").random() < 0.5
    a, b = (human, ai) if human_is_a else (ai, human)
    prompt = (PROMPTS / "judge.md").read_text().format(
        sympy_path=SYMPY_CLONE,
        guide=(PROMPTS / "writing-release-notes.md").read_text().strip(),
        submodules="\n".join(load_submodules()),
        candidate_a=a,
        candidate_b=b,
    )
    run_dir = WORK / "judge-runs" / str(number)
    if run_dir.exists():
        shutil.rmtree(run_dir)
    shutil.copytree(BUNDLES / str(number), run_dir)
    summary = run_claude(
        prompt, cwd=run_dir, model=model, schema=JUDGE_SCHEMA,
        transcript=WORK / "transcripts" / f"judge-{number}.jsonl",
        add_dirs=[SYMPY_CLONE], max_budget_usd=4.0,
    )
    summary["number"] = number
    summary["human_is"] = "A" if human_is_a else "B"
    write_json(out, summary)
    return number, f"${summary['total_cost_usd']:.3f}, {summary['num_turns']} turns"


def ai_flag(number, model):
    out = AI_FLAG / f"{number}.json"
    if out.exists() and read_json(out).get("structured_output"):
        return number, "cached"
    truth = read_json(TRUTH / f"{number}.json")
    if truth["status"] != "entry":
        return number, "skipped (no entry)"
    pr_text = (BUNDLES / str(number) / "pr.md").read_text()
    description = re.search(
        r"\n## Description\n(.*?)\n## Commits\n", pr_text, flags=re.DOTALL
    ).group(1).strip()
    prompt = (PROMPTS / "ai_flag.md").read_text().format(
        title=truth["title"], description=description, notes=truth["raw"],
    )
    run_dir = WORK / "ai-flag-runs" / str(number)
    run_dir.mkdir(parents=True, exist_ok=True)
    summary = run_claude(
        prompt, cwd=run_dir, model=model, schema=AI_FLAG_SCHEMA,
        transcript=WORK / "transcripts" / f"ai-flag-{number}.jsonl", tools="",
    )
    summary["number"] = number
    write_json(out, summary)
    return number, summary["structured_output"]["entry_looks_ai_written"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("numbers", nargs="*", type=int)
    parser.add_argument("--model", default=JUDGE_MODEL)
    parser.add_argument("--concurrency", type=int, default=6)
    parser.add_argument("--ai-flag", action="store_true")
    args = parser.parse_args()

    task = ai_flag if args.ai_flag else judge
    numbers = args.numbers or pr_numbers()
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [pool.submit(task, n, args.model) for n in numbers]
        for future in futures:
            number, status = future.result()
            print(number, status, flush=True)


if __name__ == "__main__":
    main()
