"""Have the generating model write release notes for each blinded bundle.

One isolated headless Claude Code session runs per pull request. Its working
directory is a copy of the bundle under work/runs/, and it can also read a
sympy checkout under work/sympy. It has no other tools and no network.

Results go to data/generation/<n>.json. Raw transcripts stay in
work/transcripts/ and are not committed.
"""

import argparse
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

from common import (
    BUNDLES, DATA, GENERATION, GENERATION_MODEL, PROMPTS, SYMPY_CLONE, WORK,
    load_submodules, pr_numbers, read_json, run_claude, write_json,
)


def ensure_sympy_clone():
    if not SYMPY_CLONE.exists():
        WORK.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth", "1", "https://github.com/sympy/sympy.git",
             str(SYMPY_CLONE)],
            check=True,
        )
    sha = subprocess.run(
        ["git", "-C", str(SYMPY_CLONE), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    return sha


def schema():
    return {
        "type": "object",
        "properties": {
            "no_entry": {"type": "boolean"},
            "entries": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "submodule": {"type": "string", "enum": load_submodules()},
                        "text": {"type": "string"},
                    },
                    "required": ["submodule", "text"],
                    "additionalProperties": False,
                },
            },
            "reasoning": {"type": "string"},
        },
        "required": ["no_entry", "entries", "reasoning"],
        "additionalProperties": False,
    }


def build_prompt(name, number):
    template = (PROMPTS / name).read_text()
    files = sorted(path.name for path in (BUNDLES / str(number)).iterdir())
    return template.format(
        files=", ".join(f"`{name}`" for name in files),
        sympy_path=SYMPY_CLONE,
        guide=(PROMPTS / "writing-release-notes.md").read_text().strip(),
        submodules="\n".join(load_submodules()),
        examples=(PROMPTS / "style-examples.md").read_text().strip(),
    )


def prepare_run_dir(number):
    run_dir = WORK / "runs" / str(number)
    if run_dir.exists():
        shutil.rmtree(run_dir)
    shutil.copytree(BUNDLES / str(number), run_dir)
    return run_dir


def generate(number, prompt_name, model, out_dir):
    out = out_dir / f"{number}.json"
    if out.exists() and read_json(out).get("structured_output"):
        return number, "cached"
    run_dir = prepare_run_dir(number)
    summary = run_claude(
        build_prompt(prompt_name, number), cwd=run_dir, model=model, schema=schema(),
        transcript=WORK / "transcripts" / f"{out_dir.name}-{number}.jsonl",
        add_dirs=[SYMPY_CLONE],
    )
    summary["number"] = number
    write_json(out, summary)
    return number, f"${summary['total_cost_usd']:.3f}, {summary['num_turns']} turns"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("numbers", nargs="*", type=int)
    parser.add_argument("--model", default=GENERATION_MODEL)
    parser.add_argument("--concurrency", type=int, default=6)
    parser.add_argument("--prompt", default="generate.md",
                        help="prompt template in prompts/")
    parser.add_argument("--out", default=GENERATION.name,
                        help="output directory under data/")
    args = parser.parse_args()

    sha = ensure_sympy_clone()
    write_json(DATA / "sympy_commit.json", {"sympy_commit": sha})
    out_dir = DATA / args.out
    numbers = args.numbers or pr_numbers()
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [pool.submit(generate, n, args.prompt, args.model, out_dir) for n in numbers]
        for future in futures:
            number, status = future.result()
            print(number, status, flush=True)


if __name__ == "__main__":
    main()
