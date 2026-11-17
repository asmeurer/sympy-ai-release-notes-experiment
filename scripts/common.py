"""Shared helpers for the release notes experiment."""

import json
import os
import re
import subprocess
from pathlib import Path

REPO = "sympy/sympy"

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW = DATA / "raw"
TRUTH = DATA / "truth"
BUNDLES = DATA / "bundles"
GENERATION = DATA / "generation"
JUDGE = DATA / "judge"
AI_FLAG = DATA / "ai_flag"
PROMPTS = ROOT / "prompts"
WORK = ROOT / "work"
SYMPY_CLONE = WORK / "sympy"

GENERATION_MODEL = "claude-sonnet-5-5"
JUDGE_MODEL = "claude-opus-5-5"

BEGIN_MARKER = "<!-- BEGIN RELEASE NOTES -->"
END_MARKER = "<!-- END RELEASE NOTES -->"

RELEASE_NOTES_MENTION = re.compile(
    r"release[\s_-]*notes?|no[\s_-]*entry|changelog", re.IGNORECASE
)


def clean_env():
    env = dict(os.environ)
    env.pop("CLICOLOR_FORCE", None)
    env["NO_COLOR"] = "1"
    return env


def gh(*args):
    result = subprocess.run(
        ["gh", *args], check=True, capture_output=True, text=True, env=clean_env()
    )
    return result.stdout


def gh_json(*args):
    return json.loads(gh(*args))


def gh_api_list(path):
    """Return every item of a paginated REST list endpoint."""
    out = gh("api", "--paginate", path, "--jq", ".[]")
    return [json.loads(line) for line in out.splitlines() if line.strip()]


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def load_submodules():
    lines = (PROMPTS / "submodules.txt").read_text().splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.startswith("#")]


def pr_numbers():
    return sorted(int(p.stem) for p in RAW.glob("*.json"))


def normalize(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def parse_release_notes(body):
    """Parse the release notes block of a PR description.

    Returns a dict with ``status`` (``entry``, ``no_entry``, ``empty`` or
    ``missing``), the raw block text, and the parsed entries.
    """
    start = body.find(BEGIN_MARKER)
    end = body.find(END_MARKER)
    if start == -1 or end == -1 or end < start:
        return {"status": "missing", "raw": "", "entries": []}
    raw = body[start + len(BEGIN_MARKER):end].replace("\r\n", "\n").strip("\n")
    if not raw.strip():
        return {"status": "empty", "raw": raw, "entries": []}
    if re.fullmatch(r"\s*NO ENTRY\s*", raw, re.IGNORECASE):
        return {"status": "no_entry", "raw": raw, "entries": []}

    entries = []
    header = None
    current = None
    for line in raw.split("\n"):
        if not line.strip():
            if current is not None:
                current["text"] += "\n"
            continue
        top = re.match(r"^[*-]\s+(\S.*)$", line)
        sub = re.match(r"^\s+[*-]\s+(\S.*)$", line)
        if top:
            header = top.group(1).strip()
            current = None
        elif sub:
            current = {"submodule": header, "text": sub.group(1).rstrip()}
            entries.append(current)
        elif current is not None:
            current["text"] += "\n" + line.rstrip()
    for entry in entries:
        entry["text"] = entry["text"].strip()
    return {"status": "entry", "raw": raw, "entries": entries}


def render_notes(no_entry, entries):
    """Render notes the way they would be written in a PR description."""
    if no_entry or not entries:
        return "NO ENTRY"
    by_header = {}
    for entry in entries:
        by_header.setdefault(entry["submodule"], []).append(entry["text"])
    lines = []
    for header, texts in by_header.items():
        lines.append(f"* {header}")
        for text in texts:
            first, *rest = text.split("\n")
            lines.append(f"  * {first}")
            lines.extend(f"    {ln}" if ln.strip() else "" for ln in rest)
        lines.append("")
    return "\n".join(lines).strip()


def scrub(obj):
    """Replace machine-specific paths so that saved results are portable."""
    text = json.dumps(obj)
    text = text.replace(str(ROOT), "<repo>").replace(str(Path.home()), "~")
    return json.loads(text)


def run_claude(prompt, *, cwd, model, schema, transcript, tools="Read,Grep,Glob",
               add_dirs=(), max_budget_usd=2.0, timeout=1200):
    """Run one headless, isolated Claude Code session and summarize it.

    The session runs with no user or project customizations, no MCP servers,
    and file tools confined to ``cwd`` and ``add_dirs``. The raw stream is
    saved to ``transcript`` and a summary dict is returned.
    """
    cmd = [
        "claude", "-p",
        "--model", model,
        "--restricted",
        "--safe-mode",
        "--strict-mcp-config",
        "--disable-slash-commands",
        "--permission-prompts", "none",
        "--no-session-persistence",
        "--output-format", "stream-json",
        "--verbose",
        "--max-budget-usd", str(max_budget_usd),
        "--json-schema", json.dumps(schema),
        "--tools", tools,
    ]
    for d in add_dirs:
        cmd += ["--add-dir", str(d)]
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, cwd=str(cwd),
        timeout=timeout, env=clean_env(),
    )
    transcript = Path(transcript)
    transcript.parent.mkdir(parents=True, exist_ok=True)
    transcript.write_text(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(
            f"claude exited with {result.returncode} in {cwd}\n"
            f"stderr: {result.stderr[-2000:]}\nstdout tail: {result.stdout[-2000:]}"
        )
    return scrub(summarize_transcript(result.stdout))


def summarize_transcript(stdout):
    events = [json.loads(line) for line in stdout.splitlines() if line.strip()]
    init = next(e for e in events if e.get("type") == "system" and e.get("subtype") == "init")
    final = next(e for e in events if e.get("type") == "result")
    tool_calls = []
    for event in events:
        if event.get("type") != "assistant":
            continue
        for block in event["message"]["content"]:
            if block.get("type") == "tool_use":
                tool_calls.append({"name": block["name"], "input": block["input"]})
    return {
        "model": init.get("model"),
        "tools_available": init.get("tools"),
        "mcp_servers": init.get("mcp_servers"),
        "claude_code_version": init.get("claude_code_version"),
        "is_error": final.get("is_error"),
        "subtype": final.get("subtype"),
        "structured_output": final.get("structured_output"),
        "result_text": final.get("result"),
        "num_turns": final.get("num_turns"),
        "duration_ms": final.get("duration_ms"),
        "total_cost_usd": final.get("total_cost_usd"),
        "usage": final.get("usage"),
        "model_usage": final.get("modelUsage"),
        "permission_denials": final.get("permission_denials"),
        "tool_calls": tool_calls,
    }
