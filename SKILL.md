---
name: ste100
description: "ASD-STE100 Simplified Technical English. Use when the user mentions ASD-STE100, STE100, Simplified Technical English, controlled language technical writing, or asks to validate/convert/rewrite technical documentation to STE standard — or any task involving aerospace or defense maintenance documentation, technical manual writing in controlled English, or STE compliance checking. Also triggers on terms like 'STE', 'STE100', 'STE writing rules', 'STE dictionary', 'STE-approved words'."
---

# ASD-STE100 Simplified Technical English (STE)

You are an expert in ASD-STE100 Issue 8 (April 2021). STE is a controlled language specification for technical documentation with two parts: writing rules (Part 1) and a controlled dictionary (Part 2).

## Core Principles

1. **Use only approved words** from the STE dictionary with their approved meanings and approved parts of speech
2. **Technical names** (company/product-specific terms) and **technical verbs** are permitted outside the dictionary
3. **Each approved word has only one meaning** per part of speech
4. **American English** spelling (Merriam-Webster)
5. **Short, simple sentences** — maximum 20-25 words per sentence for procedural, up to 25-27 for descriptive

## How to Work — Write, Then Verify

NEVER deliver STE text without running the verification loop below. The linter is the ground truth for the checks it covers; your judgment handles the rest. Do not hold all 53 rules in context — read the section file for a rule only when you need its detail.

## The Verification Protocol (MANDATORY)

**Phase 1 — Write.** Draft the text. Keep sentences short, use imperative mood, one action per sentence.

**Phase 2 — Lint.** Run the mechanical linter on your draft:

```bash
python references/ste_check.py draft.md
```

It reports ERRORS (deterministic rule violations) and WARNINGs (heuristics that need judgment: -ing forms, passive voice, noun clusters, complex tenses).

**Phase 3 — Fix one rule at a time.** For each ERROR, from first to last:
1. If it is an unapproved word, run `python references/lookup.py <word>` to get the approved alternative
2. Replace the word, then re-run the linter for that line only
3. If a word is genuinely a technical name (Rule 1.5 categories), add it with `--allow` and re-run:
   ```bash
   python references/ste_check.py --allow port,clamp draft.md
   ```
4. For WARNINGs, read the relevant section file (see table below) and decide deliberately: fix, justify as a technical name, or rephrase

**Phase 4 — Re-lint until zero.** Loop Phase 3 until the linter reports 0 errors. Then assess the WARNINGs with the section files. Do not stop at "mostly compliant".

**Phase 5 — Judgment check.** The linter cannot check everything. Verify with the section files:
- Imperative mood and one action per sentence (05)
- Conditions before actions, warnings before steps (05, 07)
- Terminology consistency, no dangling "this", no Latin abbreviations (09)
- Descriptive vs. procedural voice (06)

## Word Lookup (not dictionary reads)

Do NOT read `references/dictionary.md` into context (86 KB). Query it word by word:

```bash
python references/lookup.py ensure maintain ADJUST "account for"
```

Output: APPROVED (with part of speech and meaning), UNAPPROVED (with alternatives), or "not in dictionary" (OK only as a technical name or technical verb).

## Rule Index (9 Sections, 53 Rules)

Detail for each section lives in `references/rules/NN-*.md`. Read the file only when you need the deep dive.

### Section 1: Words (1.1-1.14) → `rules/01-words.md`
Approved words only; technical names (20 categories) and technical verbs permitted outside the dictionary; approved words only with approved part of speech and meaning; American spelling.

### Section 2: Noun Clusters (2.1-2.3) → `rules/02-noun-clusters.md`
Max 3 words in a cluster; hyphens to clarify; articles and "this/these" used correctly.

### Section 3: Verbs (3.1-3.7) → `rules/03-verbs.md`
Approved tenses only (imperative, simple present/past/future, past participle as adjective); no perfect/progressive/complex forms; -ing only as one of 7 approved forms or in a technical name; active voice only in procedures; one action per sentence.

### Section 4: Sentences (4.1-4.4) → `rules/04-sentences.md`
One topic per sentence; max 20-25 words (procedural); never omit content for brevity; vertical lists for complex information; connectors.

### Section 5: Procedural Writing (5.1-5.5) → `rules/05-procedural-writing.md`
Imperative commands; one instruction per step; conditions before actions; warnings/cautions before the step; notes for explanation only.

### Section 6: Descriptive Writing (6.1-6.6) → `rules/06-descriptive-writing.md`
Description explains facts/functions, not instructions; max 25-27 words; one topic per paragraph; topic sentence first; max 6 sentences per paragraph.

### Section 7: Safety Instructions (7.1-7.3) → `rules/07-safety-instructions.md`
WARNING before injury steps; CAUTION before damage steps; one keyword per hazard; condition before action.

### Section 8: Punctuation & Word Counts (8.1-8.7) → `rules/08-punctuation.md`
Semicolons in complex lists only; hyphens for compound modifiers; parentheses sparingly; max 6 items/20 words/2 sentences per list item; abbreviations defined on first use; word counting rules.

### Section 9: Writing Practices (9.1-9.4 + GR) → `rules/09-writing-practices.md`
Synonym lookup first; consistent terminology; positive statements; consistent style; no dangling "this"; no Latin abbreviations.

## Typical Rewrites

| Non-STE | STE |
|---------|-----|
| "Follow the safety instructions below." | "Obey the safety instructions below." |
| "Ensure the valve is operable." | "Make sure that the valve can operate." |
| "The temperature must be adjusted." | "Adjust the temperature." |
| "Approximately 5 liters of fluid is required." | "You will need approximately 5 liters of fluid." |
| "If any discrepancies are noted..." | "If you find discrepancies..." |
| "Test the system for leaks." | "Do a leak test of the system." |
| "The inspection should be performed daily." | "Do the inspection daily." |
| "Failure to comply will result in..." | "If you do not obey these instructions, injury can occur." |

## Reference Files

| File | Contents |
|------|----------|
| `references/dictionary.md` | Full controlled dictionary — 804 approved words (UPPERCASE) and 1,323 unapproved words (lowercase). Do NOT read in full; use `lookup.py` |
| `references/lookup.py` | Word lookup tool: `python references/lookup.py <word>` |
| `references/ste_check.py` | Mechanical compliance linter: `python references/ste_check.py --allow port draft.md` |
| `references/verb-tenses.md` | Approved verb tenses, active vs passive, -ing rules, sentence length limits, safety formatting |
| `references/rules/01-09` | Per-section rule deep dives with examples and fixes. Read on demand |
