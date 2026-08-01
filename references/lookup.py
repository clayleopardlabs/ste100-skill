#!/usr/bin/env python3
"""STE100 dictionary lookup tool.

Queries the controlled dictionary (references/dictionary.md) one word at a time
instead of loading the full dictionary into context.

Usage:
    python lookup.py WORD [WORD ...]
    python lookup.py maintain "switch off" ADJUST

Exit code: 0 (all words found), 1 (one or more words not in the dictionary).
"""
import re
import sys
from pathlib import Path

DICT_PATH = Path(__file__).resolve().parent / "dictionary.md"

APPROVED_RE = re.compile(r"^\* \*\*(.+?) \((.+?)\)\*\*[\s\u2014-]+\s*(.*)$")
UNAPPROVED_RE = re.compile("^\\* (.+?) \\((.+?)\\) \u2192 (.*)$")


def load_dictionary(path=None):
    """Parse dictionary.md into (approved, unapproved) dicts.

    approved:   {lowercase word: (pos, meaning)}
    unapproved: {lowercase word: (pos, alternatives)}
    Keys can be multi-word ("switch off", "account for").
    """
    path = Path(path) if path else DICT_PATH
    approved = {}
    unapproved = {}
    section = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = "unapproved" if "Unapproved" in line else "approved"
            continue
        if not line.startswith("* "):
            continue
        if section == "approved":
            m = APPROVED_RE.match(line)
            if m:
                word, pos, meaning = m.group(1), m.group(2), m.group(3).strip()
                approved[word.lower()] = (pos, meaning)
        else:
            m = UNAPPROVED_RE.match(line)
            if m:
                word, pos, alt = m.group(1), m.group(2), m.group(3).strip()
                unapproved[word.lower()] = (pos, alt)
    return approved, unapproved


def normalize(word):
    """Strip trailing/leading punctuation for dictionary lookup."""
    return word.strip(".,;:!?()[]\"'`*").lower()


def lookup(word, approved, unapproved):
    """Return (status, detail) for a word: 'approved' | 'unapproved' | 'unknown'."""
    key = normalize(word)
    if key in approved:
        pos, meaning = approved[key]
        return "approved", f"{word}: APPROVED ({pos}) - {meaning}"
    if key in unapproved:
        pos, alt = unapproved[key]
        return "unapproved", f"{word}: UNAPPROVED ({pos}) - use {alt}"
    return "unknown", f"{word}: not in dictionary - OK only as a technical name or technical verb"


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    approved, unapproved = load_dictionary()
    statuses = []
    for word in argv:
        status, detail = lookup(word, approved, unapproved)
        print(detail)
        statuses.append(status)
    print()
    print(
        f"{len(statuses)} words: "
        f"{statuses.count('approved')} approved, "
        f"{statuses.count('unapproved')} unapproved, "
        f"{statuses.count('unknown')} technical names"
    )
    return 1 if "unapproved" in statuses else 0


if __name__ == "__main__":
    sys.exit(main())
