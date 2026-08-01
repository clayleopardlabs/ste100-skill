You are an STE100 compliance auditor. Your task: identify every STE100 rule violation in a test paragraph and produce a corrected version that fully complies with the ASD-STE100 standard.

STEPS:
1. Read the ste100 skill instructions: C:\Users\Omen\.config\opencode\skills\ste100\SKILL.md — read it in full, especially the Verification Protocol (Phases 1-6). Also read the per-rule deep-dive files in C:\Users\Omen\.config\opencode\skills\ste100\references\rules\ as needed.
2. Read the test paragraph to audit: <TEST_FILE>
3. Follow the skill's verification protocol exactly:
   - Phase 1: draft a corrected version. Count words in every sentence — anything over 25 words must be split, and any sentence over 20 words is a WARNING that must also be fixed.
   - Phase 2: FIRST run the linter on the ORIGINAL file and SAVE its output: `python C:\Users\Omen\.config\opencode\skills\ste100\references\ste_check.py "<TEST_FILE>" > C:\Users\Omen\AppData\Local\Temp\opencode\lint-original.txt 2>&1`. Then echo the saved file: `Get-Content -Raw C:\Users\Omen\AppData\Local\Temp\opencode\lint-original.txt`. Your violation report must be a verbatim copy of that echoed output — do NOT reconstruct or summarize it from memory.
   - Phase 3: fix one rule at a time. For unapproved words use `python C:\Users\Omen\.config\opencode\skills\ste100\references\lookup.py <word>` and replace the word with the dictionary alternative VERBATIM, keeping the rest of the sentence unchanged. Never insert a dictionary word in a position where it makes no sense.
   - Phases 4-5: re-lint until 0 errors AND 0 warnings. Every warning is a violation too and must be fixed. Judgment check — CRITICAL, apply to EVERY sentence: (a) grammatical, meaningful, no nonsense; (b) ONE ACTION ONLY — split any "and"/"then"/"while" that joins two commands; (c) no passive voice; (d) no duplicate steps — delete duplicates; (e) STEP PRESERVATION with the SAME VERB rule: list every action from the ORIGINAL paragraph; each action's replacement must use the SAME VERB or the dictionary-approved alternative of that verb — substituting a different verb is a forbidden meaning change; COUNT the mapping — corrected action count must equal original action count; (f) no dangling "this", imperative mood; (g) while rewriting, never introduce new violations (no new -ing forms, no new over-20-word sentences, no new noun clusters).
    - Phase 6 (MANDATORY): write your FINAL corrected text to C:\Users\Omen\AppData\Local\Temp\opencode\ste100-draft.md (overwriting it), run the linter one last time on that EXACT file, and also run `Get-FileHash C:\Users\Omen\AppData\Local\Temp\opencode\ste100-draft.md` and `Get-Content -Raw C:\Users\Omen\AppData\Local\Temp\opencode\ste100-draft.md` to capture the exact final artifact. The final lint output line must read EXACTLY "0 errors, 0 warnings". If any error or warning remains, fix it and re-lint — you are NOT done until the output line reads exactly "0 errors, 0 warnings".
    - Phase 6b (MANDATORY): run the technical-detail check: `python C:\Users\Omen\.config\opencode\skills\ste100\references\ste_check.py --details "<TEST_FILE>" C:\Users\Omen\AppData\Local\Temp\opencode\ste100-draft.md`. Its output must read "0 errors, 0 warnings" — every number, unit, range, acronym, brand name, and condition from the original must survive in the corrected text (Rule 4.2).
4. IMPORTANT: Do NOT modify the test file. Only create/overwrite your draft temp file.

WATCHDOG — your run MUST terminate:
- You may run the linter at most 6 times total.
- You may run at most 25 tool calls TOTAL (any tool).
- If you run the SAME command twice in a row with identical input, you are stuck: change your approach (re-read the section file, pick a different correction), do not repeat it.
- NEVER run a lookup for a word you already looked up — keep a list of words you have already looked up and do not look them up again.
- After 6 linter runs or 25 total tool calls, STOP regardless: deliver your best draft, listing any remaining violations and why you could not resolve them.
- NEVER loop forever. A bounded imperfect answer beats an infinite loop.

<SPECIAL_FOCUS>

YOUR FINAL MESSAGE MUST CONTAIN:
- The verbatim echoed content of lint-original.txt
- The Get-FileHash output for the final draft file
- The full corrected paragraph, copied VERBATIM from the Get-Content -Raw output (character-for-character)
- The final linter output for that exact file (must read "0 errors, 0 warnings" on the last line)
- The --details output for that exact file (must read "0 errors, 0 warnings" on the last line)
- A STEP PRESERVATION MAPPING table: every action of the ORIGINAL paragraph, its verb, and the corrected sentence where that action appears with the same verb (or dictionary alternative). The number of mapped actions must equal the number of original actions.
- Your per-sentence checklist result for each sentence of the final text (grammatical/meaningful? one action? no passive? no dangling?)
- If you stopped at the 6-run cap without reaching 0/0: state clearly "STOPPED AT CAP" and list the remaining violations.

Do not stop until the final lint output line reads exactly "0 errors, 0 warnings" AND your step-preservation mapping accounts for every original action — but never exceed 6 linter runs.
