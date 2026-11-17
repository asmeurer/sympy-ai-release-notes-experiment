"""Build prompts/style-examples.md from a finished release notes page.

Usage: python scripts/make_style_examples.py path/to/Release-Notes-for-1.14.md

Only a release that was finished before the test pull requests were merged
may be used, so that the examples cannot contain any of the answers.
"""

import re
import sys
from pathlib import Path

from common import PROMPTS

PER_MODULE = 2


def main():
    text = Path(sys.argv[1]).read_text()
    changes = text[text.index("## Changes"):text.index("## Authors")]
    lines = []
    count = 0
    for line in changes.split("\n")[1:]:
        if re.match(r"^\* \S", line):
            lines.append(line)
            count = 0
        elif re.match(r"^  \* \S", line):
            count += 1
            if count <= PER_MODULE:
                entry = re.sub(r"\s*\(\[#\d+\]\(https://github\.com/sympy/sympy/pull/.*$", "", line)
                lines.append(entry)
    (PROMPTS / "style-examples.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {len(lines)} lines")


if __name__ == "__main__":
    main()
