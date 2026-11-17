"""Compute the statistics and write the per-pull-request comparison.

Writes report/stats.json, report/tables.md (the summary tables), and
report/comparisons.md (every pull request side by side).
"""

import difflib
import math
import re
import statistics
from collections import Counter

from common import (
    AI_FLAG, DATA, GENERATION, JUDGE, ROOT, TRUTH, load_submodules,
    normalize, pr_numbers, read_json, render_notes, write_json,
)

REPORT = ROOT / "report"
TOKEN_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens",
              "output_tokens")

# Merged pull requests to master between the 1.14.0 release (2025-04-27) and
# 2026-11-17, from the GitHub search API, and the number of distinct pull
# requests with an entry on the 1.15 release notes wiki page on 2026-11-17.
RELEASE_CYCLE_PRS = 835
RELEASE_CYCLE_PRS_WITH_ENTRY = 494


def load(number):
    truth = read_json(TRUTH / f"{number}.json")
    gen = read_json(GENERATION / f"{number}.json")
    judge_path = JUDGE / f"{number}.json"
    flag_path = AI_FLAG / f"{number}.json"
    row = {
        "number": number,
        "title": truth["title"],
        "author": truth["author"],
        "human_no_entry": truth["status"] == "no_entry",
        "human_entries": truth["entries"],
        "human_text": render_notes(truth["status"] == "no_entry", truth["entries"]),
        "ai_no_entry": gen["structured_output"]["no_entry"] or not gen["structured_output"]["entries"],
        "ai_entries": gen["structured_output"]["entries"],
        "ai_reasoning": gen["structured_output"]["reasoning"],
        "overlap": truth["overlap"],
        "ai_disclosure_text": truth["ai_disclosure"],
        "gen": gen,
        "judge": None,
        "flag": None,
    }
    row["ai_text"] = render_notes(row["ai_no_entry"], row["ai_entries"])
    if judge_path.exists():
        judge = read_json(judge_path)
        verdict = judge["structured_output"]
        human_key = "candidate_a" if judge["human_is"] == "A" else "candidate_b"
        ai_key = "candidate_b" if judge["human_is"] == "A" else "candidate_a"
        if verdict["preferred"] == "tie":
            preferred = "tie"
        else:
            preferred = "human" if verdict["preferred"] == judge["human_is"] else "ai"
        row["judge"] = {
            "should_have_entry": verdict["should_have_entry"],
            "human": verdict[human_key],
            "ai": verdict[ai_key],
            "same_substance": verdict["same_substance"],
            "preferred": preferred,
            "strength": verdict["strength"],
            "rationale": verdict["rationale"],
            "human_was": judge["human_is"],
            "run": judge,
        }
    if flag_path.exists():
        row["flag"] = read_json(flag_path)
    return row


def sign_test(wins, losses):
    """Two-sided exact binomial p-value for wins versus losses."""
    n = wins + losses
    if n == 0:
        return None
    k = min(wins, losses)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def sentence_count(text):
    """Count sentences, ignoring code spans and abbreviations such as "e.g."."""
    text = re.sub(r"```.*?```|`[^`]*`", "CODE", text, flags=re.DOTALL)
    text = re.sub(r"\b(e\.g|i\.e|etc|vs)\.", r"\1", text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text.strip())
    return len([part for part in parts if part.strip()])


def mechanical(entries):
    checks = Counter()
    for entry in entries:
        text = entry["text"].strip()
        checks["entries"] += 1
        period = text.endswith((".", ".`", "```"))
        first = text.lstrip("`*_")[:1]
        capitalized = first.isupper() or text[:1] == "`"
        checks["ends_with_period"] += period
        checks["starts_capitalized"] += capitalized
        checks["capitalized_and_ends_with_period"] += period and capitalized
        checks["more_than_one_sentence"] += sentence_count(text) > 1
        checks["mentions_issue_number"] += bool(re.search(r"#\d{3,}", text))
        checks["multi_line"] += "\n" in text
    return checks


def words(entries):
    return [len(entry["text"].split()) for entry in entries]


def token_summary(runs):
    out = {"runs": len(runs)}
    for key in TOKEN_KEYS:
        values = [run["usage"][key] for run in runs]
        out[key] = {"total": sum(values), "mean": statistics.mean(values),
                    "median": statistics.median(values), "max": max(values)}
    totals = [sum(run["usage"][key] for key in TOKEN_KEYS) for run in runs]
    out["all_tokens"] = {"total": sum(totals), "mean": statistics.mean(totals),
                         "median": statistics.median(totals), "max": max(totals)}
    costs = [run["total_cost_usd"] for run in runs]
    out["cost_usd"] = {"total": sum(costs), "mean": statistics.mean(costs),
                       "median": statistics.median(costs), "max": max(costs)}
    out["turns"] = {"mean": statistics.mean(run["num_turns"] for run in runs),
                    "max": max(run["num_turns"] for run in runs)}
    out["duration_s"] = {"mean": statistics.mean(run["duration_ms"] for run in runs) / 1000,
                         "max": max(run["duration_ms"] for run in runs) / 1000}
    out["models"] = sorted({model for run in runs for model in run["model_usage"]})
    return out


def audit(runs, sandbox):
    """Check that no run touched anything outside its sandbox."""
    allowed = (f"<repo>/work/{sandbox}", "<repo>/work/sympy")
    outside = []
    denials = 0
    for gen in runs:
        denials += len(gen["permission_denials"] or [])
        for call in gen["tool_calls"]:
            if call["name"] == "StructuredOutput":
                continue
            target = call["input"].get("file_path") or call["input"].get("path")
            if target and target.startswith(("/", "~", "<")) and not target.startswith(allowed):
                outside.append((gen["number"], call["name"], target))
    return {
        "tool_calls_outside_sandbox": outside,
        "permission_denials": denials,
        "tools_available": sorted({t for gen in runs for t in gen["tools_available"]}),
        "mcp_servers": sorted({str(s) for gen in runs for s in gen["mcp_servers"]}),
        "reads_of_sympy_checkout": sum(
            any("<repo>/work/sympy" in str(call["input"]) for call in gen["tool_calls"])
            for gen in runs
        ),
        "reads_of_linked_issues": sum(
            any("linked.md" in str(call["input"]) for call in gen["tool_calls"])
            for gen in runs
        ),
    }


def compute(rows):
    stats = {"n": len(rows)}
    stats["human"] = Counter("no_entry" if r["human_no_entry"] else "entry" for r in rows)
    stats["ai"] = Counter("no_entry" if r["ai_no_entry"] else "entry" for r in rows)
    stats["decision_matrix"] = Counter(
        ("human_" + ("no_entry" if r["human_no_entry"] else "entry"),
         "ai_" + ("no_entry" if r["ai_no_entry"] else "entry"))
        for r in rows
    )
    stats["decision_matrix"] = {f"{a}/{b}": c for (a, b), c in stats["decision_matrix"].items()}

    both = [r for r in rows if not r["human_no_entry"] and not r["ai_no_entry"]]
    stats["both_entry"] = len(both)
    stats["same_headers"] = sum(
        {e["submodule"] for e in r["human_entries"]} == {e["submodule"] for e in r["ai_entries"]}
        for r in both
    )
    stats["entry_counts"] = {
        "human": Counter(len(r["human_entries"]) for r in both),
        "ai": Counter(len(r["ai_entries"]) for r in both),
    }
    human_entries = [e for r in rows for e in r["human_entries"]]
    ai_entries = [e for r in rows if not r["ai_no_entry"] for e in r["ai_entries"]]
    valid = set(load_submodules())
    stats["mechanical"] = {
        "human": dict(mechanical(human_entries)),
        "ai": dict(mechanical(ai_entries)),
    }
    stats["mechanical"]["human"]["invalid_header"] = sum(
        e["submodule"] not in valid for e in human_entries)
    stats["mechanical"]["ai"]["invalid_header"] = sum(
        e["submodule"] not in valid for e in ai_entries)
    stats["words"] = {
        "human_median": statistics.median(words(human_entries)),
        "ai_median": statistics.median(words(ai_entries)),
        "human_mean": statistics.mean(words(human_entries)),
        "ai_mean": statistics.mean(words(ai_entries)),
    }
    stats["human_note_equals_title"] = sum(
        bool(r["overlap"]["truth_quoted_in_title"]) for r in rows)
    stats["human_note_title_similarity_over_0.8"] = sum(
        (r["overlap"]["title_similarity"] or 0) > 0.8 for r in rows)
    stats["ai_note_title_similarity_over_0.8"] = sum(
        _similar_to_title(r) > 0.8 for r in rows if not r["ai_no_entry"])

    judged = [r for r in rows if r["judge"]]
    stats["judged"] = len(judged)
    if judged:
        stats["judge"] = judge_stats(judged)

    flagged = [r for r in rows if r["flag"]]
    if flagged:
        stats["ai_flag"] = {
            "n": len(flagged),
            "disclosure": Counter(r["flag"]["structured_output"]["disclosure"] for r in flagged),
            "entry_looks_ai_written": Counter(
                r["flag"]["structured_output"]["entry_looks_ai_written"] for r in flagged),
            "preference_by_look": {
                look: Counter(
                    r["judge"]["preferred"] for r in flagged
                    if r["judge"]
                    and r["flag"]["structured_output"]["entry_looks_ai_written"] == look
                )
                for look in ("likely", "unlikely", "cannot_tell")
            },
            "preference_by_disclosure": {
                d: Counter(
                    r["judge"]["preferred"] for r in flagged
                    if r["judge"] and r["flag"]["structured_output"]["disclosure"] == d
                )
                for d in ("no_ai", "ai_assist", "ai_wrote_text", "blank_or_unclear")
            },
        }
        stats["tokens_ai_flag"] = token_summary([r["flag"] for r in flagged])

    stats["tokens_generation"] = token_summary([r["gen"] for r in rows])
    if judged:
        stats["tokens_judge"] = token_summary([r["judge"]["run"] for r in judged])
    canary = read_json(DATA / "canary.json")
    stats["harness_overhead_tokens"] = sum(canary["trivial"]["usage"][k] for k in TOKEN_KEYS)
    mean_cost = stats["tokens_generation"]["cost_usd"]["mean"]
    mean_tokens = stats["tokens_generation"]["all_tokens"]["mean"]
    stats["extrapolation"] = {
        "release_cycle_prs": RELEASE_CYCLE_PRS,
        "release_cycle_prs_with_entry": RELEASE_CYCLE_PRS_WITH_ENTRY,
        "cost_usd": RELEASE_CYCLE_PRS * mean_cost,
        "tokens": RELEASE_CYCLE_PRS * mean_tokens,
    }
    stats["audit"] = {"generation": audit([r["gen"] for r in rows], "runs")}
    if judged:
        stats["audit"]["judge"] = audit([r["judge"]["run"] for r in judged], "judge-runs")
    variant = variant_stats(rows)
    if variant:
        stats["release_context_variant"] = variant
    return stats


def variant_stats(rows):
    """Compare the release-context prompt variant with the main run."""
    out = {"matrix": Counter(), "changed": []}
    runs = []
    for row in rows:
        path = DATA / "generation_release_context" / f"{row['number']}.json"
        if not path.exists():
            continue
        run = read_json(path)
        runs.append(run)
        result = run["structured_output"]
        no_entry = result["no_entry"] or not result["entries"]
        human = "human_no_entry" if row["human_no_entry"] else "human_entry"
        out["matrix"][f"{human}/ai_{'no_entry' if no_entry else 'entry'}"] += 1
        if no_entry != row["ai_no_entry"]:
            out["changed"].append({
                "number": row["number"],
                "title": row["title"],
                "human": "NO ENTRY" if row["human_no_entry"] else "entry",
                "main_run": "NO ENTRY" if row["ai_no_entry"] else "entry",
                "variant": "NO ENTRY" if no_entry else "entry",
                "judge_should_have_entry": row["judge"]["should_have_entry"] if row["judge"] else None,
                "variant_text": render_notes(no_entry, result["entries"]),
                "variant_reasoning": result["reasoning"],
            })
    if not runs:
        return None
    out["n"] = len(runs)
    out["tokens"] = token_summary(runs)
    out["audit"] = audit(runs, "runs")
    return out


def _similar_to_title(row):
    text = " ".join(e["text"] for e in row["ai_entries"])
    return difflib.SequenceMatcher(None, normalize(row["title"]), normalize(text)).ratio()


def judge_stats(judged):
    out = {}

    def prefs(subset):
        counts = Counter(r["judge"]["preferred"] for r in subset)
        clear = Counter(r["judge"]["preferred"] for r in subset
                        if r["judge"]["strength"] == "clear")
        return {
            "n": len(subset),
            "human": counts["human"], "ai": counts["ai"], "tie": counts["tie"],
            "clear_human": clear["human"], "clear_ai": clear["ai"],
            "sign_test_p": sign_test(counts["ai"], counts["human"]),
            "mean_score_human": statistics.mean(r["judge"]["human"]["overall"] for r in subset)
            if subset else None,
            "mean_score_ai": statistics.mean(r["judge"]["ai"]["overall"] for r in subset)
            if subset else None,
        }

    out["all"] = prefs(judged)
    out["both_entry"] = prefs([r for r in judged if not r["human_no_entry"] and not r["ai_no_entry"]])
    out["both_no_entry"] = prefs([r for r in judged if r["human_no_entry"] and r["ai_no_entry"]])
    out["human_entry_ai_none"] = prefs(
        [r for r in judged if not r["human_no_entry"] and r["ai_no_entry"]])
    out["human_none_ai_entry"] = prefs(
        [r for r in judged if r["human_no_entry"] and not r["ai_no_entry"]])
    out["should_have_entry"] = Counter(r["judge"]["should_have_entry"] for r in judged)
    out["score_distribution"] = {
        "human": Counter(r["judge"]["human"]["overall"] for r in judged),
        "ai": Counter(r["judge"]["ai"]["overall"] for r in judged),
    }
    out["accuracy"] = {
        "human": Counter(r["judge"]["human"]["accuracy"] for r in judged),
        "ai": Counter(r["judge"]["ai"]["accuracy"] for r in judged),
    }
    out["same_substance"] = sum(r["judge"]["same_substance"] for r in judged)
    out["decision_vs_judge"] = {
        who: Counter(
            (r["judge"]["should_have_entry"],
             "no_entry" if r[f"{who}_no_entry"] else "entry")
            for r in judged
        )
        for who in ("human", "ai")
    }
    out["decision_vs_judge"] = {
        who: {f"judge_{a}/{who}_{b}": c for (a, b), c in counts.items()}
        for who, counts in out["decision_vs_judge"].items()
    }
    out["human_was_a"] = sum(r["judge"]["human_was"] == "A" for r in judged)
    out["preferred_position"] = Counter(
        "A" if (r["judge"]["preferred"] == "human") == (r["judge"]["human_was"] == "A") else "B"
        for r in judged if r["judge"]["preferred"] != "tie"
    )
    return out


def fmt(x, digits=2):
    return f"{x:,.{digits}f}" if isinstance(x, float) else f"{x:,}"


def tables(stats):
    lines = ["# Summary tables", "", "Generated by `scripts/make_report.py`.", ""]
    m = stats["decision_matrix"]
    lines += [
        "## Entry or no entry",
        "",
        "| | AI wrote an entry | AI said NO ENTRY |",
        "|---|---|---|",
        f"| Human wrote an entry | {m.get('human_entry/ai_entry', 0)} | {m.get('human_entry/ai_no_entry', 0)} |",
        f"| Human said NO ENTRY | {m.get('human_no_entry/ai_entry', 0)} | {m.get('human_no_entry/ai_no_entry', 0)} |",
        "",
    ]
    if "judge" in stats:
        j = stats["judge"]
        lines += [
            "## Blind preference of the judge",
            "",
            "| Subset | PRs | Prefers human | Prefers AI | Tie | Clearly human | Clearly AI | Mean score human | Mean score AI | Sign test p |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
        names = {
            "all": "All",
            "both_entry": "Both wrote an entry",
            "both_no_entry": "Both said NO ENTRY",
            "human_entry_ai_none": "Human entry, AI NO ENTRY",
            "human_none_ai_entry": "Human NO ENTRY, AI entry",
        }
        for key, name in names.items():
            s = j[key]
            if not s["n"]:
                continue
            p = "" if s["sign_test_p"] is None else f"{s['sign_test_p']:.3f}"
            lines.append(
                f"| {name} | {s['n']} | {s['human']} | {s['ai']} | {s['tie']} | "
                f"{s['clear_human']} | {s['clear_ai']} | {s['mean_score_human']:.2f} | "
                f"{s['mean_score_ai']:.2f} | {p} |"
            )
        lines += [
            "",
            "## Accuracy according to the judge",
            "",
            "| | Accurate | Minor inaccuracy | Wrong | Not applicable (NO ENTRY) |",
            "|---|---|---|---|---|",
        ]
        for who in ("human", "ai"):
            a = j["accuracy"][who]
            lines.append(
                f"| {who.capitalize() if who == 'human' else 'AI'} | {a.get('accurate', 0)} | "
                f"{a.get('minor_inaccuracy', 0)} | {a.get('wrong', 0)} | {a.get('not_applicable', 0)} |"
            )
        lines += [
            "",
            "## Score distribution (1 to 5)",
            "",
            "| | 1 | 2 | 3 | 4 | 5 |",
            "|---|---|---|---|---|---|",
        ]
        for who in ("human", "ai"):
            d = j["score_distribution"][who]
            lines.append(f"| {'Human' if who == 'human' else 'AI'} | "
                         + " | ".join(str(d.get(i, 0)) for i in range(1, 6)) + " |")
        lines.append("")
    if "release_context_variant" in stats:
        v = stats["release_context_variant"]
        m = v["matrix"]
        lines += [
            "## Entry or no entry with the release-context prompt (`prompts/generate_release_context.md`)",
            "",
            "| | AI wrote an entry | AI said NO ENTRY |",
            "|---|---|---|",
            f"| Human wrote an entry | {m.get('human_entry/ai_entry', 0)} | {m.get('human_entry/ai_no_entry', 0)} |",
            f"| Human said NO ENTRY | {m.get('human_no_entry/ai_entry', 0)} | {m.get('human_no_entry/ai_no_entry', 0)} |",
            "",
            "Pull requests where the decision changed from the main run:",
            "",
            "| PR | Human | Main run | Release-context run | Judge: should have entry |",
            "|---|---|---|---|---|",
        ]
        for c in v["changed"]:
            lines.append(
                f"| [{c['number']}](https://github.com/sympy/sympy/pull/{c['number']}) | {c['human']} | "
                f"{c['main_run']} | {c['variant']} | {c['judge_should_have_entry']} |"
            )
        lines.append("")
    mech = stats["mechanical"]
    lines += [
        "## Mechanical checks on the entries",
        "",
        "| | Human | AI |",
        "|---|---|---|",
    ]
    for key in ("entries", "ends_with_period", "starts_capitalized",
                "capitalized_and_ends_with_period", "more_than_one_sentence",
                "mentions_issue_number", "invalid_header"):
        lines.append(f"| {key.replace('_', ' ')} | {mech['human'].get(key, 0)} | {mech['ai'].get(key, 0)} |")
    lines.append(f"| median words per entry | {stats['words']['human_median']} | {stats['words']['ai_median']} |")
    lines.append("")
    lines += [
        "## Tokens",
        "",
        "| Stage | Model | Runs | Fresh input | Cache write | Cache read | Output | All tokens | Cost (USD) | Mean cost per PR | Mean turns | Mean seconds |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    token_rows = [(stats.get(key), name) for key, name in (
        ("tokens_generation", "Generation"), ("tokens_judge", "Blind judge"),
        ("tokens_ai_flag", "AI-authorship flag"))]
    if "release_context_variant" in stats:
        token_rows.append((stats["release_context_variant"]["tokens"],
                           "Generation, release-context prompt"))
    for t, name in token_rows:
        if t is None:
            continue
        lines.append(
            f"| {name} | {', '.join(t['models'])} | {t['runs']} | {fmt(t['input_tokens']['total'])} | "
            f"{fmt(t['cache_creation_input_tokens']['total'])} | "
            f"{fmt(t['cache_read_input_tokens']['total'])} | {fmt(t['output_tokens']['total'])} | "
            f"{fmt(t['all_tokens']['total'])} | {t['cost_usd']['total']:.2f} | "
            f"{t['cost_usd']['mean']:.3f} | {t['turns']['mean']:.1f} | {t['duration_s']['mean']:.1f} |"
        )
    lines.append("")
    return "\n".join(lines)


def block(text):
    return "````markdown\n" + text.strip() + "\n````"


def comparisons(rows):
    lines = [
        "# Every pull request side by side",
        "",
        "Generated by `scripts/make_report.py`. The judge saw the two notes as A and B in a "
        "random order and did not know which one a person wrote. Scores are from 1 to 5.",
        "",
    ]
    for row in sorted(rows, key=lambda r: -r["number"]):
        n = row["number"]
        lines += [
            f"## [{n}](https://github.com/sympy/sympy/pull/{n}): {row['title']}",
            "",
            f"Author: `{row['author']}`",
            "",
            "**Human**",
            "",
            block(row["human_text"]),
            "",
            "**AI**",
            "",
            block(row["ai_text"]),
            "",
            f"AI's reasoning: {row['ai_reasoning']}",
            "",
        ]
        judge = row["judge"]
        if judge:
            preferred = {"human": "human", "ai": "AI", "tie": "tie"}[judge["preferred"]]
            lines += [
                f"**Judge**: should have an entry: {judge['should_have_entry']}. "
                f"Human {judge['human']['overall']}/5 ({judge['human']['accuracy']}), "
                f"AI {judge['ai']['overall']}/5 ({judge['ai']['accuracy']}). "
                f"Preferred: {preferred} ({judge['strength']}). "
                f"Same substance: {'yes' if judge['same_substance'] else 'no'}.",
                "",
                judge["rationale"],
                "",
            ]
            for who, label in (("human", "Human"), ("ai", "AI")):
                if judge[who]["problems"]:
                    lines.append(f"Problems with the {label} note:")
                    lines.extend(f"- {p}" for p in judge[who]["problems"])
                    lines.append("")
        if row["flag"]:
            flag = row["flag"]["structured_output"]
            lines += [
                f"**AI use**: disclosure classified as `{flag['disclosure']}`; "
                f"human entry looks AI-written: `{flag['entry_looks_ai_written']}`. "
                f"{flag['evidence']}",
                "",
            ]
        lines += ["---", ""]
    return "\n".join(lines)


def main():
    rows = [load(n) for n in pr_numbers() if (GENERATION / f"{n}.json").exists()]
    stats = compute(rows)
    REPORT.mkdir(exist_ok=True)
    write_json(REPORT / "stats.json", stats)
    (REPORT / "tables.md").write_text(tables(stats))
    (REPORT / "comparisons.md").write_text(comparisons(rows))
    print(tables(stats))
    print("audit:", stats["audit"])
    print("extrapolation:", stats["extrapolation"])


if __name__ == "__main__":
    main()
