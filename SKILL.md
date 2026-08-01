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

**Phase 1 — Write.** Draft the text. Keep sentences short, use imperative mood, one action per sentence. Count the words in every sentence as you write: more than 25 words is an ERROR (Rule 4.1), and procedures should stay at or below 20 words (Rule 8.7). If a sentence is over, split it now.

**Phase 2 — Lint the original, then draft.** Run the mechanical linter on the ORIGINAL text first. Its output is the authoritative violation list: every printed line is a violation you must report, with the rule number exactly as printed. Save the output: `python references/ste_check.py original.md > lint-original.txt` and echo `lint-original.txt` verbatim in your report — never reconstruct the violation list from memory. Then draft your corrected version:

```bash
python references/ste_check.py original.md
```

It reports ERRORS (deterministic rule violations) and WARNINGs (heuristics that need judgment: -ing forms, passive voice, noun clusters, complex tenses). Rule numbers in the output are authoritative — cite them exactly as printed (1.1/1.6, 4.1/8.7, 8.1, GR-6, 3.5, 3.2/3.4, 3.6, 2.1). Do not invent rule numbers.

**Phase 3 — Fix one rule at a time.** For each ERROR, from first to last:
1. If it is an unapproved word, run `python references/lookup.py <word>` to get the approved alternative. Replace the word with that alternative VERBATIM and keep the rest of the sentence unchanged — do not rewrite the sentence, do not rephrase around the word
2. If it is a Latin abbreviation (GR-6), the linter message names the ONE matching replacement phrase ("e.g." → "for example", "i.e." → "that is", "etc." → "and so on"). Copy that exact phrase into the sentence — the named phrase is the only acceptable replacement for that abbreviation. Never substitute a different phrase (e.g. never use "for example" for "etc.")
3. Replace the word, then re-run the linter for that line only
4. If a word is genuinely a technical name (Rule 1.5 categories), add it with `--allow` and re-run:
   ```bash
   python references/ste_check.py --allow port,clamp draft.md
   ```
5. For WARNINGs, read the relevant section file (see table below) and decide deliberately: fix, justify as a technical name, or rephrase

**Phase 4 — Re-lint until zero (bounded).** Loop Phase 3 until the linter reports 0 errors and 0 warnings. Do not stop at "mostly compliant". WATCHDOG — the loop MUST terminate: (1) never run the linter more than 6 times on your drafts; (2) before each re-lint, compare the new lint output to the previous one — if the output is IDENTICAL (same violations, same lines) to the previous run, you are stuck: STOP looping and instead FIX THE RULES, not the file — re-read the relevant section file, pick a different correction, then lint once more; (3) if you still have violations after 6 lint runs, STOP and deliver the best draft you have, clearly reporting the remaining violations and why you could not resolve them. Looping forever is never acceptable: a bounded imperfect answer beats an infinite loop.

**Phase 5 — Judgment check.** The linter cannot check everything. Verify with the section files:
- Imperative mood and one action per sentence (05)
- Conditions before actions, warnings before steps (05, 07)
- Terminology consistency, no dangling "this", no Latin abbreviations (09)
- Descriptive vs. procedural voice (06)
- GRAMMAR: read the final text aloud, one sentence at a time. Every sentence must be a complete, grammatical sentence (subject + predicate, correct word order). If a sentence reads broken or missing words ("before operate the system", "while hold the valve"), fix it — the linter cannot detect grammar.
- ONE ACTION PER SENTENCE: scan for the conjunction "and" (also "then", "while"). If "and" joins two commands or actions ("Hold the wrench and keep the valve closed"), split into two sentences — the linter cannot detect Rule 3.7.
- NO NONSENSE: every sentence must make sense as English. If a word replacement makes the sentence nonsensical ("keep the valve in PUT"), rewrite the sentence properly. Check the resulting text reads like a real procedure.
- NO DUPLICATE STEPS: after rewriting, check that no action appears twice ("Remove the cover." plus "Remove the cover from the filter."). Delete duplicates.
- STEP PRESERVATION (Rule 4.2): make a numbered list of EVERY verb occurrence in the ORIGINAL text — each imperative counts separately ("Hold the wrench with the left hand while holding the valve" contains HOLD twice = two rows). For each occurrence, mark where it appears in your corrected text. Every original occurrence must still appear — splitting and rephrasing are allowed, but NEVER drop an occurrence and NEVER invent one that was not in the original. If an occurrence is missing or new, fix the corrected text. The replacement must use the SAME VERB (or the dictionary-approved alternative of that verb) — substituting a different verb for the same action ("hold the valve" becoming "keep pressure on the valve") is a meaning change and is forbidden. COUNT the mapping: the number of corrected verb occurrences must equal the number of original verb occurrences — if your corrected text has fewer occurrences of a verb, content was dropped: restore it.
- PER-SENTENCE CHECKLIST: for EVERY sentence in the corrected text, answer all four aloud: (1) grammatical and meaningful? (2) one action only? (3) no passive voice? (4) no dangling reference? Any "no" means fix that sentence before Phase 6.

**Phase 6 — Final artifact verification (MANDATORY, never skip).** The text you publish must be exactly the text you linted. Write your FINAL corrected text to the draft file (overwriting it), run the linter one last time on that exact file. The final lint must report "0 errors, 0 warnings". WARNINGs are violations too — a result with any warning means you are NOT done: fix each warning, re-lint, and repeat until the output line reads exactly "0 errors, 0 warnings". NEVER report a linter result you did not obtain by running the command on the exact text you are about to deliver, and NEVER declare success while warnings remain. LINE COUNT GUARD: run `(Get-Content <draft>).Count` — the draft must have AT LEAST as many lines as the original file. Fewer lines means content was dropped: restore it. The draft file must contain ONLY the corrected STE text — no report text, no "examples:", no labels, no "a) b) c)" items, no commentary, no "..." placeholders. Every original line must be transformed into corrected sentences, never deleted. Your violation report must contain EVERY violation the linter printed for the original text — if you do not know why a printed line is a violation, read the section file for that rule before writing your report. Do not report violations the linter did not print.

**Phase 6 evidence (MANDATORY):** a report that claims "0 errors, 0 warnings" is only trustworthy if it is tied to the exact artifact. After the final lint, run `Get-FileHash <draft-file>` (or `sha256sum`) and include the hash, AND echo the file back with `Get-Content -Raw <draft-file>`, both in your report. The delivered text must be a character-for-character copy of that echoed file. If you rewrote or rephrased anything after the final lint, the test FAILS — re-run the whole Phase 6 loop on the new text instead. Never hand-edit the linted text in your report: copy it from the file.

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
Approved tenses only (imperative, simple present/past/future, past participle as adjective); no perfect/progressive/complex forms; -ing only as an approved -ing word or in a technical name; active voice only in procedures; one action per sentence.

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
| `references/dictionary.md` | Full controlled dictionary — 805 approved words (UPPERCASE) and 1,323 unapproved words (lowercase). Do NOT read in full; use `lookup.py` |
| `references/lookup.py` | Word lookup tool: `python references/lookup.py <word>` |
| `references/ste_check.py` | Mechanical compliance linter: `python references/ste_check.py --allow port draft.md` |
| `references/verb-tenses.md` | Approved verb tenses, active vs passive, -ing rules, sentence length limits, safety formatting |
| `references/rules/01-09` | Per-section rule deep dives with examples and fixes. Read on demand |
