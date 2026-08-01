---
name: ste100-verify
description: "Verify that a text file complies with ASD-STE100 Simplified Technical English using the mechanical linter and rule-by-rule review. Use when the user asks to check/validate/audit/lint existing text against STE, STE100, Simplified Technical English, or says 'run the STE linter', 'is this STE compliant', 'check this manual/procedure/docs for STE'. For WRITING or REWRITING text into STE, use the ste100 skill instead."
---

# STE100 Verification

Your job: verify a text against ASD-STE100 Issue 8 (April 2021) — one rule at a time, using the mechanical linter plus targeted rule lookups. You do NOT need to hold the 53 rules in context; the linter and the rule files carry them.

## Step 1 — Locate the linter

Find the ste100 skill's references directory (it contains `ste_check.py`, `lookup.py`, `dictionary.md`). Likely locations:

- `~/.config/opencode/skills/ste100/references/`
- `~/.agents/skills/ste100/references/`
- `~/.claude/skills/ste100/references/`
- a repo clone of `clayleopardlabs/ste100-skill`

If you cannot find it, tell the user the ste100 skill must be installed first.

## Step 2 — Run the linter

```bash
python <references>/ste_check.py <file>
```

Output has two levels:

- **ERROR [Rule X.Y]** — deterministic violations: unapproved words, sentences over the limit, bad vertical lists (more than 6 items, items over 20 words or 2 sentences), semicolons, Latin abbreviations. These must ALL be fixed.
- **WARNING [Rule X.Y]** — heuristics needing judgment: -ing forms, possible passive voice, noun clusters, complex tenses, dangling "this". Each one gets a deliberate decision.

## Step 3 — Report violations one rule at a time

For each ERROR, in order:

1. **Unapproved word** — query the dictionary: `python <references>/lookup.py <word>` and give the approved alternative
2. **Sentence too long** — quote the sentence, give the word count, suggest the split
3. **List violation** — name the rule (8.4 items/words or 8.5 sentences) and where the list breaks
4. **Semicolon / Latin abbreviation** — quote it and give the replacement

For each WARNING, read the matching section file for the rule before deciding:

| Warning | Read |
|---------|------|
| `-ing` form (3.5) | `<references>/rules/03-verbs.md` |
| passive voice (3.6) | `<references>/rules/03-verbs.md` |
| complex tense (3.2/3.4) | `<references>/rules/03-verbs.md` |
| noun cluster (2.1) | `<references>/rules/02-noun-clusters.md` |
| dangling "this" (GR-1) | `<references>/rules/09-writing-practices.md` |
| sentence length (4.1/8.7) | `<references>/rules/04-sentences.md` |

Decision categories for a WARNING: (a) fix it, (b) justify it as a technical name (Rule 1.5), or (c) rephrase. State the decision per warning.

## Step 4 — Final report

Report the verdict:

- **PASS** — 0 errors, all warnings resolved or justified
- **FAIL** — errors remain. List each remaining violation: rule number, quoted text, fix or technical-name argument

Do not modify the user's file unless asked. Suggest fixes; apply them only on request.
