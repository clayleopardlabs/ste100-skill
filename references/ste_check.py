#!/usr/bin/env python3
"""STE100 mechanical compliance linter.

Checks a text file against the machine-checkable subset of the ASD-STE100
writing rules. Deterministic checks report as ERRORS; heuristic checks
(which may need human judgment, e.g. technical names) report as WARNINGS.

Usage:
    python ste_check.py FILE [FILE ...]
    python ste_check.py --allow port,clamp FILE
    python ste_check.py --report-unknown FILE
    cat FILE | python ste_check.py -

Options:
    --allow WORD[,WORD...]   extra technical names to suppress (e.g. --allow port)
    --strict                 also fail on WARNINGs (exit 2)
    --report-unknown         also list words not in the dictionary (they are
                             allowed only as technical names or technical
                             verbs; review them in the Phase 5 judgment check)

Exit code: 0 clean, 1 errors, 2 errors+strict warnings.

Rule mapping:
    ERROR   [1.1/1.6]  unapproved dictionary word used
    ERROR   [4.1/8.7]  sentence over the word limit
    ERROR   [8.1]      semicolon used outside a complex list
    ERROR   [8.4]      vertical list with more than 6 items
    ERROR   [8.4]      list item over 20 words
    ERROR   [8.5]      list item with more than 2 sentences
    ERROR   [GR-6]     Latin abbreviation (i.e., e.g., etc., viz.)
    WARNING [2.1]      noun cluster longer than 3 words
    WARNING [3.2/3.4]  complex verb tense (perfect/progressive/future passive)
    WARNING [3.5]      -ing form outside the 7 approved forms
    WARNING [3.6]      possible passive voice
    WARNING [GR-1]     sentence starts with dangling "This"

Words whose dictionary alternative contains "(TN)" (technical name) are
automatically suppressed, because the dictionary itself sanctions them.
Words NOT in the dictionary at all are also not flagged: under Rule 1.5/1.12
they may be valid technical names or technical verbs -- use --allow to
explicitly permit them, or judgment to remove them.
"""
import re
import sys
from pathlib import Path

from lookup import load_dictionary, normalize

APPROVED_ING = {
    "lighting", "opening", "routing", "servicing",  # nouns
    "mating", "missing", "remaining",                # adjectives
    "something",                                     # pronoun
    "during",                                        # preposition
}

FUNCTION_WORDS = {
    "the", "a", "an", "of", "in", "on", "at", "to", "with", "for", "and", "or",
    "but", "by", "from", "is", "are", "was", "were", "be", "been", "being",
    "its", "it", "this", "these", "that", "those", "as", "if", "then", "when",
    "while", "do", "does", "did", "not", "no", "yes", "you", "your", "we",
    "our", "they", "their", "he", "she", "his", "her", "one", "into", "onto",
    "over", "under", "than", "so", "such", "will", "can", "may", "must",
    "should", "would", "could", "shall", "has", "have", "had", "between",
    "through", "after", "before", "per", "each", "all", "some", "any", "both",
    "more", "most", "other", "only", "very", "too", "also", "off", "up",
    "down", "out", "again", "once", "twice", "there", "here",
}

NUMBERS = {
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety", "hundred", "thousand",
}

PERFECT_RE = re.compile(r"\b(has|have|had)\s+(\w+ed|been|gone|done)\b", re.I)
FUTURE_PASSIVE_RE = re.compile(r"\bwill be\s+\w+ed\b", re.I)
PROGRESSIVE_RE = re.compile(r"\b(is|are|was|were|be)\s+being\b", re.I)
PASSIVE_RE = re.compile(
    r"\b(is|are|was|were|be|been|being)\s+(applied|adjusted|closed|removed|"
    r"installed|opened|set|made|done|taken|given|put|secured|located|"
    r"identified|found|performed|completed|used|checked|examined)\b", re.I)
ING_RE = re.compile(r"\b(\w+ing)\b")
LATIN_ABBREV_RE = re.compile(r"\b(?:i\.e\.|e\.g\.|etc\.|viz\.)\b", re.I)
DANGLING_THIS_RE = re.compile(
    r"^\s*This\s+(is|will|can|does|was|has|had|must|should|may|shall)\b", re.I)
WORD_RE = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$")

MAX_SENTENCE_WORDS = 25
MAX_ITEM_WORDS = 20
MAX_ITEM_SENTENCES = 2
MAX_LIST_ITEMS = 6
MAX_NOUN_CLUSTER = 3


def singularize(word):
    """Return the likely singular form for dictionary lookup."""
    lower = word.lower()
    if lower.endswith("ies") and len(lower) > 4:
        return lower[:-3] + "y"
    if lower.endswith("es") and len(lower) > 4:
        return lower[:-2]
    if lower.endswith("s") and len(lower) > 3:
        return lower[:-1]
    return lower


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.unknown = set()

    def error(self, rule, line, message):
        self.errors.append((rule, line, message))

    def warning(self, rule, line, message):
        self.warnings.append((rule, line, message))


def find_unapproved(word, approved, unapproved, allow_set):
    """Return (status, alternative) for a token against the unapproved dict.

    Checks the word, then its singular form. Words approved in any part of
    speech are not flagged (the unapproved list also holds other-POS entries
    for approved words, e.g. CLOSE (v) vs close (prep)). Words whose
    dictionary alternative contains a TN marker are dictionary-sanctioned
    technical names and return None (suppressed).
    """
    forms = []
    for form in (normalize(word).lower(), singularize(word)):
        if form not in forms:
            forms.append(form)
    for form in forms:
        if form in allow_set:
            return None
    for form in forms:
        if form in approved:
            return None
    for form in forms:
        if form in unapproved:
            pos, alt = unapproved[form]
            if "TN" in alt.upper():
                return None
            return alt
    return None


def split_sentences(text):
    text = re.sub(r"\b(\d+)\.(\d+)\b", r"\1\2", text)
    return [s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()]


def count_words(text):
    return len(WORD_RE.findall(text))


def check_text(text, report, allow_set, report_unknown=False):
    approved, unapproved = load_dictionary()
    lines = text.splitlines()

    # --- unapproved words (Rules 1.1, 1.6) ---
    for lineno, line in enumerate(lines, 1):
        flagged = set()
        for word in WORD_RE.findall(line):
            key = normalize(word).lower()
            if key in flagged or singularize(key) in flagged:
                continue
            alt = find_unapproved(word, approved, unapproved, allow_set)
            if alt:
                flagged.add(key)
                report.error(
                    "1.1/1.6", lineno,
                    f"unapproved word: '{word}' - use {alt} (if this is a "
                    "technical name per Rule 1.5, add it with --allow)",
                )
            elif report_unknown:
                forms = [key, singularize(word)]
                if key not in FUNCTION_WORDS and key not in NUMBERS and not any(
                        f in approved or f in unapproved for f in forms):
                    report.unknown.add(word.lower())

    # --- -ing forms (Rule 3.5) ---
    for lineno, line in enumerate(lines, 1):
        for m in ING_RE.finditer(line):
            ing = m.group(1).lower()
            if ing not in APPROVED_ING:
                report.warning(
                    "3.5", lineno,
                    f"'-ing' form '{m.group(1)}' is not one of the approved "
                    "forms (lighting, opening, routing, servicing, mating, "
                    "missing, remaining, something, during); if it is part of "
                    "a technical name, that is permitted",
                )

    # --- sentence checks (Rules 4.1, 8.7, 3.2, 3.4, 3.6, GR-1) ---
    for lineno, line in enumerate(lines, 1):
        for sent in split_sentences(line):
            n = count_words(sent)
            if n > MAX_SENTENCE_WORDS:
                report.error(
                    "4.1/8.7", lineno,
                    f"sentence has {n} words (limit {MAX_SENTENCE_WORDS}): "
                    f"'{sent[:80]}...'",
                )
            elif n > 20:
                report.warning(
                    "4.1/8.7", lineno,
                    f"sentence has {n} words (over the 20-word procedural "
                    f"limit; max {MAX_SENTENCE_WORDS}): '{sent[:80]}...'",
                )
            if PERFECT_RE.search(sent) or FUTURE_PASSIVE_RE.search(sent) \
                    or PROGRESSIVE_RE.search(sent):
                report.warning(
                    "3.2/3.4", lineno,
                    f"possible complex verb tense (present/past perfect or "
                    f"future passive): '{sent[:80]}...'",
                )
            if PASSIVE_RE.search(sent):
                matches = PASSIVE_RE.finditer(sent)
                shown = 0
                for m in matches:
                    span = sent[max(0, m.start() - 20):m.end() + 20]
                    report.warning(
                        "3.6", lineno,
                        f"possible passive voice: '...{span.strip()}...'",
                    )
                    shown += 1
                    if shown >= 3:
                        break
                if shown == 0:
                    report.warning("3.6", lineno, "possible passive voice")
            if DANGLING_THIS_RE.search(sent):
                report.warning(
                    "GR-1", lineno,
                    "sentence starts with dangling 'This' (must be followed "
                    f"by a noun): '{sent[:80]}...'",
                )

    # --- punctuation (Rules 8.1, GR-6) ---
    for lineno, line in enumerate(lines, 1):
        if ";" in line:
            report.error(
                "8.1", lineno,
                "semicolon used; prefer separate sentences (semicolons are "
                "permitted only to separate items in a complex vertical list)",
            )
        for m in LATIN_ABBREV_RE.finditer(line):
            report.error(
                "GR-6", lineno,
                f"Latin abbreviation '{m.group(0)}' - use 'that is', 'for "
                "example', or 'and so on'",
            )

    # --- noun clusters (Rule 2.1) ---
    for lineno, line in enumerate(lines, 1):
        for sent in split_sentences(line):
            words = WORD_RE.findall(sent.lower())
            run = 0
            for i, w in enumerate(words):
                if w in FUNCTION_WORDS or w in NUMBERS or w.isdigit():
                    run = 0
                else:
                    run += 1
                    if run == MAX_NOUN_CLUSTER + 1:
                        start = max(0, i - MAX_NOUN_CLUSTER)
                        cluster = " ".join(words[start:i + 1])
                        report.warning(
                            "2.1", lineno,
                            f"noun cluster longer than {MAX_NOUN_CLUSTER} "
                            f"words in a row: '{cluster}'; split it with "
                            "articles, hyphens, or prepositions",
                        )
                        break

    # --- vertical lists (Rules 8.4, 8.5) ---
    group = []
    group_start = 0
    for lineno, line in enumerate(lines, 1):
        m = LIST_ITEM_RE.match(line)
        if m:
            if not group:
                group_start = lineno
            group.append((lineno, m.group(1)))
        else:
            check_list(group, group_start, report)
            group = []
    check_list(group, group_start, report)


def check_list(group, group_start, report):
    if not group:
        return
    if len(group) > MAX_LIST_ITEMS:
        report.error(
            "8.4", group_start,
            f"vertical list has {len(group)} items (max {MAX_LIST_ITEMS}); "
            "split it into several lists of 6 or fewer items",
        )
    for lineno, item in group:
        n = count_words(item)
        if n > MAX_ITEM_WORDS:
            report.error(
                "8.4", lineno,
                f"list item has {n} words (max {MAX_ITEM_WORDS}): "
                f"'{item[:60]}...'",
            )
        sentences = [s for s in split_sentences(item) if s]
        if len(sentences) > MAX_ITEM_SENTENCES:
            report.error(
                "8.5", lineno,
                f"list item has {len(sentences)} sentences "
                f"(max {MAX_ITEM_SENTENCES})",
            )


def check_file(path, report, allow_set, report_unknown=False):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    check_text(text, report, allow_set, report_unknown)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 2
    allow_set = set()
    strict = False
    report_unknown = False
    files = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--allow" and i + 1 < len(argv):
            allow_set.update(w.strip().lower() for w in argv[i + 1].split(",") if w.strip())
            i += 2
        elif arg == "--strict":
            strict = True
            i += 1
        elif arg == "--report-unknown":
            report_unknown = True
            i += 1
        else:
            files.append(arg)
            i += 1
    report = Report()
    for path in files:
        if path == "-":
            check_text(sys.stdin.read(), report, allow_set, report_unknown)
        else:
            check_file(path, report, allow_set, report_unknown)
    for rule, lineno, msg in report.errors:
        print(f"ERROR   [Rule {rule}] line {lineno}: {msg}")
    for rule, lineno, msg in report.warnings:
        print(f"WARNING [Rule {rule}] line {lineno}: {msg}")
    if report_unknown:
        print()
        print("NOT IN DICTIONARY (technical-name candidates for Phase 5 review):")
        for word in sorted(report.unknown):
            print(f"  {word}")
    print()
    print(f"{len(report.errors)} errors, {len(report.warnings)} warnings")
    if report.errors:
        return 1
    if strict and report.warnings:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
