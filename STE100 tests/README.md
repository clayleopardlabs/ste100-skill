# STE100 tests

Automated regression corpus for the ste100 skill, built to validate that a cold-context agent (the `omnicoder` subagent, Qwen3.5-9B-The-Defiant-Fable via LM Studio) can identify and correct STE100 violations against the skill's own rules.

## How the corpus is graded

Each `test-NN.md` paragraph is designed to contain an EXACT number of violations, verified mechanically with `references/ste_check.py`:

| Test | Violations | Errors | Warnings | Contents |
|------|-----------|--------|----------|----------|
| test-01 | 1 | 1 | 0 | one unapproved word (Swap) |
| test-02 | 2 | 2 | 0 | + one over-long sentence |
| test-03 | 3 | 3 | 0 | + one semicolon |
| test-04 | 4 | 4 | 0 | + one Latin abbreviation (e.g.) |
| test-05 | 5 | 4 | 1 | + one -ing form (holding) |
| test-06 | 6 | 4 | 2 | + one complex tense (has completed) |
| test-07 | 7 | 4 | 3 | + one passive voice (is removed by) |
| test-08 | 8 | 4 | 4 | + one noun cluster  -  one of EVERY kind |
| test-09 | 16 | 8 | 8 | TWO violations of every kind |
| test-10 | 24 | 12 | 12 | THREE violations of every kind |

The 8 violation kinds map 1:1 to the linter's rule classes: unapproved word (1.1/1.6), sentence over 25 words (4.1/8.7), semicolon (8.1), Latin abbreviation (GR-6), -ing form (3.5), complex tense (3.2/3.4), passive voice (3.6), noun cluster (2.1).

## Rubrics

`rubric-NN.md` lists every violation in `test-NN.md` with: the offending text, the rule it violates (cited), and the correction the model should produce. A perfect score requires identifying ALL violations and correcting each without introducing any new violation (final text lints clean with 0 errors and 0 warnings).

## Protocol

1. Assign a fresh subagent (same model, cold context) test-01 with instructions to identify and fix all violations, outputting only the corrected text (never modifying the test file).
2. Grade the output against rubric-01.
3. On failure: modify the skill (SKILL.md, rules, ste_check.py, dictionary) so the mistake cannot recur; sync to `~/.config/opencode/skills/ste100/`; re-test the same paragraph with a fresh subagent.
4. On success: advance to the next test.
5. Stop when all 10 tests pass.

## Watchdog (bounded loop)

A stuck subagent can loop forever in the fix-re-lint cycle (observed on test-09: the agent re-linted the same draft repeatedly). Two layers of watchdog are mandatory:

1. **In the skill** (SKILL.md Phase 4): the fix loop is bounded - at most 6 linter runs; if two consecutive lint outputs are identical the agent is stuck and must change its FIX, not re-lint; after 6 runs it must stop and deliver the best draft with remaining violations reported.
2. **In the test prompt**: the prompt template (`test-prompt-template.md`) repeats the cap: "run the linter at most 6 times; after 6 runs, stop and report the current draft and latest lint output even if violations remain."

A run is declared STUCK (and killed) if the agent exceeds the cap or produces identical consecutive lint outputs. A bounded imperfect answer is preferred over an infinite loop.

## History

- 2026-07-31: corpus built; ste_check.py Latin-abbreviation regex bug found and fixed during corpus construction (`\be\.g\.\b` failed on trailing space  -  replaced with `(?![A-Za-z])` lookahead).
- 2026-07-31: watchdog added after test-09 retry-3 subagent looped indefinitely: Phase 4 bounded iteration (max 6 lints, stuck-detection, deliver-don't-loop), prompt template carries the same cap.
- 2026-07-31 → 2026-08-01: first full refinement run (omnicoder subagent, 10 paragraphs, 44 graded attempts total). All 10 tests pass. Defects found and fixed in the skill:

  | # | Failure observed | Skill modification | Where |
  |---|-----------------|--------------------|-------|
  | 1 | test-02: agent reported a fabricated 0/0 lint for text that still had a violation | Phase 6 mandates the final artifact is linted verbatim (hash + echo evidence in report); never report an un-run lint | SKILL.md |
  | 2 | test-02: agent never counted words, missed the over-25-word sentence | Phase 1 mandates counting words in every sentence; 21-25 words is a warning that must also be fixed | SKILL.md |
  | 3 | test-03: agent cited invented rule numbers | Rule citations must be copied from the linter output exactly as printed | SKILL.md |
  | 4 | test-04: agent kept "e.g." in the text and reported 0/0  -  the repo copy of ste_check.py lacked the Latin-abbreviation fix (sync had reverted it) | Fixed the regex in the repo source, not the installed copy; verified linter can see the violation before trusting a 0/0 | ste_check.py |
  | 5 | test-06: agent's corrected text still contained "Swap" while claiming 0/0 | Phase 6 evidence: Get-FileHash + Get-Content -Raw of the exact linted artifact | SKILL.md |
  | 6 | test-06: "Hold the wrench with the left hand and keep the valve closed"  -  one action per sentence violated but invisible to the linter | Mechanical Rule 3.7 check: sentence starting with an approved verb + "and"/"then" + content word = two-action join warning | ste_check.py |
  | 7 | test-07: agent kept "and hold" joins, rationalizing them past the rule text | Rule 3.7 becomes a linter WARNING (cannot be argued past); Phase 5 "and"-scan; warnings are violations (Phase 6 wording) | ste_check.py + SKILL.md |
  | 8 | test-07: agent rewrote "holding" as a different verb ("keep pressure on the valve") | 03-verbs.md -ing fix rule: replace with the SAME verb, preserving meaning; step-preservation count check | 03-verbs.md |
  | 9 | test-07: agent stopped at "0 errors" with warnings remaining | Phase 6 now requires the output line to read exactly "0 errors, 0 warnings"; a result with warnings is a failed submission | SKILL.md |
  | 10 | test-09: agent wrote "Check the fluid level"  -  CHECK is noun-only; the -ing fix rule led it into a Rule 1.2 violation | 03-verbs.md CHECK→EXAMINE rule: -ing fixes must lookup-verify the base verb is approved as a verb; noun-only bases use the approved verb (EXAMINE) | 03-verbs.md |
  | 11 | test-09: "etc." → "that is a rag" (wrong meaning) | Latin abbreviations must match meanings exactly: e.g.→"for example", i.e.→"that is", etc.→"and so on"; the linter message names the exact phrase per abbreviation | SKILL.md + ste_check.py |
  | 12 | test-09: "hydraulic oil of the filter"  -  cluster split inverted the meaning | 02-noun-clusters.md: keep EVERY word of the cluster, keep the head noun (last word) as the object, keep the sentence verb untouched; only add articles/hyphens/prepositions | 02-noun-clusters.md |
  | 13 | test-09: cluster fix changed the sentence verb ("Interchange the filter ... for damage") | Verb-preservation rule in the cluster-split guidance (verb column of the mapping must match the original verb) | 02-noun-clusters.md + SKILL.md |
  | 14 | test-10: agent looped 55 minutes without running the linter (watchdog counted lints, not wall-clock) | Hard limits in the test prompt: 20-minute cap, 25 tool-call cap, deliver best draft at any cap ("STOPPED AT CAP") | test-prompt-template.md |
  | 15 | test-10: agent wrote report text ("These are examples: a) ... b) ...") into the draft and deleted real sentences | Phase 6 line-count guard: draft must have ≥ original's line count; draft may contain only corrected STE text, never report text | SKILL.md |
  | 16 | test-10: "LOOSING" (uppercase -ing) bypassed the linter | ING_RE compiled case-insensitive (re.I) | ste_check.py |
  | 17 | test-10: the linter's own suggested phrase "and so on" was flagged as an unapproved word ("so") | Multi-word exception: "so" inside "and so on" is not flagged | ste_check.py |
  | 18 | test-10: agent invented "Reattach" for Fix (dictionary says REPAIR) | Phase 3: verify EVERY replacement word with lookup.py  -  never invent a word not in the dictionary | SKILL.md |

  Final skill state after the run: protocol = draft → lint original (verbatim report) → fix one rule at a time with lookup verification → re-lint to exactly "0 errors, 0 warnings" (bounded: 6 lints max) → line-count guard → hash+echo evidence; linter enforces 8 rule classes mechanically (unapproved words, sentence length, semicolons, Latin abbreviations, -ing forms, complex tenses, passive voice, noun clusters) plus Rule 3.7 and-join detection; rules deep-dive files loaded on demand.
