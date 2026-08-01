# ASD-STE100 Skill

An AI coding assistant skill for **ASD-STE100 Simplified Technical English** - the international specification for clear, controlled-language technical documentation.

Based on **Issue 8 (April 2021)** of the ASD-STE100 specification, originally developed for the aerospace and defense industry.

Inspired by the video [The cure for AI slop is a 1986 aircraft manual](https://www.youtube.com/watch?v=uJblcC4lKYw).

## What It Does

This skill teaches AI assistants to:
- **Validate** technical text against all 53 STE writing rules
- **Rewrite** Non-STE text into compliant Simplified Technical English
- **Check** word choice against the full STE controlled dictionary (805 approved + 1,323 unapproved words)
- **Correct** sentence structure, verb tenses, noun clusters, and safety formatting

## Complete vs. Distilled

This is the **complete** implementation of the STE specification. The [distilled version](https://github.com/woosal1337/blog/tree/main/videos/ep01-the-cure-for-ai-slop) from woosal1337's "cure for AI slop" kit is the other way to ship it: a compact two-mode skill (strict and flavored) that teaches the mechanical rules and links out to the official standard.

| | Distilled (woosal1337) | This skill |
|---|---|---|
| Rules | Mechanical subset | All 53 rules, 9 sections |
| Dictionary | None, links to the official standard | Full controlled dictionary (86 KB, 805 approved + 1,323 unapproved words) |
| Strongest at | Quick rewriting | Validation, word lookup, rewriting |
| Install weight | Single small file | SKILL.md + 2 reference files |

The distilled version is the lighter fit when you only want everyday rewriting instructions. This skill is the reference implementation: it can validate a document against all 53 rules and answer word-level questions such as "Is 'utilize' an approved STE word?" against the controlled dictionary. I have a product coming out soon and after the youtube video introduced me to the concept of STE, It made me want to have the instructional documents adhere to the STE standard. Not because of regulatory reasons, I just thought it was a neat idea and effective for my customers.

The benchmark below shows both clear the anti-slop test at essentially the same level. The difference is that this skill makes text stick to the rules of the standard, not just sound less like AI.

## Benchmark: STE100 vs. the Distilled "Cure for AI Slop" Skill

Head-to-head test against the distilled STE skill from [woosal1337's "The cure for AI slop" experiment kit](https://github.com/woosal1337/blog/tree/main/videos/ep01-the-cure-for-ai-slop), using the kit's own deterministic anti-slop linter (`ste-lint.py`, violations per 100 words; lower is cleaner).

**Method:** 6 writing tasks (README intro, error message, PR description, API docs, getting-started guide, deprecation notice). Each AI-slop baseline was rewritten with both skills by the same model, then all texts were linted. Included as a third condition: the [Feynman Style skill](https://github.com/clayleopardlabs/feynman-style-skill), a mechanism-first writing skill (plain speech, terms come late, no hype words, no em/en dashes) for explaining and rewriting technical material.

| Condition | README | Error | PR | API | Getting started | Deprecation | **Avg** | **vs. baseline** |
|---|---|---|---|---|---|---|---|---|
| Baseline (AI slop) | 8.92 | 9.28 | 6.02 | 8.80 | 8.02 | 8.38 | **8.24** | n/a |
| Distilled skill (woosal1337) | 1.59 | 0.00 | 0.00 | 0.00 | 0.74 | 0.00 | **0.39** | −95.3% |
| **This skill (ste100)** | 1.35 | 0.00 | 0.00 | 0.00 | 0.74 | 0.00 | **0.35** | **−95.8%** |
| Feynman skill (with em-dash rule) | 2.34 | 2.41 | 2.31 | 1.59 | 1.78 | 2.19 | 2.10 | −74.5% |

**Caveats:** raw violation counts tied 3-3; the per-100-words margin comes from word-count normalization, not fewer violations. Both STE skills converge to near-zero because the linter is the machine-checkable subset of STE: a distilled skill and a dictionary-backed skill both clear it. n=6, single model, heuristic linter: directional, not proof.

## Skill Contents

```
ste100/
├── SKILL.md                       # Main skill - rule index, verification protocol, rewrite guidance
├── ste100-verify/
│   └── SKILL.md                   # Verification-only skill - lints existing text rule by rule
└── references/
    ├── dictionary.md              # Full controlled dictionary (805 approved, 1323 unapproved words)
    ├── lookup.py                  # Word lookup tool - queries the dictionary one word at a time
    ├── ste_check.py               # Mechanical linter - checks text against the machine-checkable rules
    ├── verb-tenses.md             # Approved/unapproved tenses, active vs passive, -ing rules
    └── rules/
        ├── 01-words.md            # Section 1 deep dive: words, technical names (20 categories), technical verbs
        ├── 02-noun-clusters.md    # Section 2 deep dive: 3-word limit, hyphens, articles
        ├── 03-verbs.md            # Section 3 deep dive: tenses, -ing, active voice, one action per sentence
        ├── 04-sentences.md        # Section 4 deep dive: word limits, vertical lists, connectors
        ├── 05-procedural-writing.md  # Section 5 deep dive: imperative steps, conditions, list structure
        ├── 06-descriptive-writing.md # Section 6 deep dive: description vs procedure, paragraph shape
        ├── 07-safety-instructions.md # Section 7 deep dive: WARNING vs CAUTION formatting
        ├── 08-punctuation.md      # Section 8 deep dive: semicolons, hyphens, list limits, abbreviations
        └── 09-writing-practices.md   # Section 9 deep dive: consistency, positive statements, GR rules
```

The agent loads only the rule index from SKILL.md and reads the per-section deep dives on demand, so it never needs to hold all 53 rules in context. Word checks run through `lookup.py` instead of reading the 86 KB dictionary, and the `ste_check.py` linter handles the mechanical rules in one pass.

### Mechanical verification

The skill enforces a mandatory write-then-verify loop:

1. Write the draft
2. Run the linter: `python references/ste_check.py draft.md`
3. Fix one rule at a time  -  query `python references/lookup.py <word>` for alternatives, or justify a word as a technical name with `--allow`
4. Re-lint until 0 errors AND 0 warnings, then judge the remaining rules against the section files
5. Run the technical-detail check: `python references/ste_check.py --details original.md corrected.md` - every number, unit, range, acronym, brand name, and condition from the original must survive in the corrected text (Rule 4.2)
6. Phase 6 guard: the exact artifact you publish must be the artifact you linted (hash + verbatim echo in the report), and it must have at least as many lines as the original  -  dropping content is a violation (Rule 4.2)

The fix loop is bounded (watchdog): at most 6 linter runs; if two consecutive lint outputs are identical, you are stuck  -  change the FIX, not the file; after 6 runs, deliver the best draft with remaining violations reported. Never loop.

Example:

```bash
$ python references/ste_check.py before.md
ERROR   [Rule 1.1/1.6] line 1: unapproved word: 'fashion' - use PROCEDURE (n)
ERROR   [Rule 1.1/1.6] line 1: unapproved word: 'via' - use THROUGH (prep)
ERROR   [Rule 1.1/1.6] line 1: unapproved word: 'adequate' - use SUFFICIENT (adj)
ERROR   [Rule 4.1/8.7] line 1: sentence has 193 words (limit 25)
ERROR   [Rule 8.1] line 1: semicolon used; prefer separate sentences
...
18 errors, 6 warnings

$ python references/ste_check.py after.md --allow port
0 errors, 0 warnings
```

Warnings are heuristics (-ing forms, passive voice, noun clusters, complex tenses) that always need a deliberate judgment call; errors are deterministic and must all be fixed. A result that reports warnings is not a pass.

### How the skill was refined: the 10-paragraph test corpus

The skill is verified against a graded regression corpus in [`STE100 tests/`](STE100%20tests/README.md): 10 test paragraphs with escalating violation counts - test-01 has exactly 1 violation, test-02 has 2, and so on up to test-08 which violates one of each kind, then test-09 (2 violations of every kind) and test-10 (3 of every kind). Each has a rubric identifying every violation with its rule citation and required correction. A fresh subagent (cold context) must identify and fix every violation in each paragraph; the grade is perfect only if all violations are found, all are corrected without introducing new ones, and the final text lints clean.

Refinement deliberately used a very small model - Qwen3.5-9B (Defiant Fable), served locally through LM Studio - rather than a frontier model, so passing the corpus with a 9B model is evidence the skill works with any capable model. All 10 tests pass against it. The tests ran in about 56k of context: the model's 100k window had ~44k already consumed by the opencode harness (system prompt, tool definitions, session state). The corpus and skill were refined over about 4.5 hours: ~2 hours of subagent grading runs (each failure → skill modification → fresh retest), plus corpus construction, rubric writing, and fixing the 18 defects below.

The loop: on any non-perfect score, the skill is modified so that specific mistake cannot recur, then the same paragraph is re-tested. The 18 defects this process caught (each now prevented by the skill):

| Failure observed | Prevention now in the skill |
|---|---|
| Agent reported a fabricated 0/0 lint for text that still had a violation | Phase 6: final artifact is linted verbatim (hash + echo evidence); never report an un-run lint |
| Agent never counted words, missed an over-25-word sentence | Phase 1 mandates counting every sentence's words; 21-25 words is a warning that must also be fixed |
| Agent cited invented rule numbers | Rule citations must be copied from the linter output exactly as printed |
| "Hold the wrench with the left hand and keep the valve closed"  -  two actions invisible to the linter | Mechanical Rule 3.7 check: command + "and"/"then" + content word = two-action join warning |
| Agent rewrote "holding" as a different verb | -ing fixes must use the SAME verb; lookup-verify the base verb is approved as a verb (CHECK is noun-only → EXAMINE) |
| Agent stopped at "0 errors" with warnings remaining | Phase 6 requires the output line to read exactly "0 errors, 0 warnings" |
| "etc." → "that is a rag" (wrong meaning) | Latin abbreviations map to exactly one replacement: e.g.→"for example", i.e.→"that is", etc.→"and so on" |
| "hydraulic oil of the filter"  -  cluster split inverted the meaning | Cluster splits keep every word, keep the head noun, keep the sentence verb; only add articles/hyphens/prepositions |
| Agent looped 55 minutes without running the linter | Watchdog: 20-minute cap, 25 tool-call cap, "STOPPED AT CAP" - deliver the best draft instead of looping |
| Agent wrote report text into the draft and deleted sentences | Line-count guard: draft must have ≥ the original's line count, containing only corrected text |
| "LOOSING" (uppercase -ing) bypassed the linter | -ing regex compiled case-insensitive |
| The linter's own suggestion "and so on" was flagged ("so") | Multi-word exception for "and so on" |
| Agent invented "Reattach" for Fix (dictionary says REPAIR) | Every replacement word must be lookup-verified  -  never invent words not in the dictionary |

Full details, all 18 defects, and the complete protocol are in [`STE100 tests/README.md`](STE100%20tests/README.md).

### Required Reference Files

The files in `references/` are required for the skill to work correctly. `SKILL.md` contains the rule index and verification protocol, but it depends on these files for word validation, mechanical checking, and detailed verb and sentence guidance:

- `references/dictionary.md` is required for approved-word, unapproved-word, part-of-speech, and alternative-word checks.
- `references/lookup.py` queries the dictionary one word at a time (the agent must not read the full dictionary into context).
- `references/ste_check.py` is the mechanical linter the verification protocol runs on every draft.
- `references/verb-tenses.md` is required for verb-tense, voice, `-ing`, sentence-length, and safety-format checks.
- `references/rules/` contains the per-section rule deep dives, read on demand.

Install the complete `ste100/` directory. Do not copy `SKILL.md` by itself. Keep the `references/` directory at the same level as `SKILL.md`:

```text
ste100/
├── SKILL.md
├── ste100-verify/
│   └── SKILL.md
└── references/
    ├── dictionary.md
    ├── lookup.py
    ├── ste_check.py
    ├── verb-tenses.md
    └── rules/
        ├── 01-words.md
        ├── 02-noun-clusters.md
        ├── 03-verbs.md
        ├── 04-sentences.md
        ├── 05-procedural-writing.md
        ├── 06-descriptive-writing.md
        ├── 07-safety-instructions.md
        ├── 08-punctuation.md
        └── 09-writing-practices.md
```

If any of these files is missing or moved, the assistant cannot perform complete STE validation. After installation, verify that the files exist at `ste100/references/` before using the skill. Python 3.8+ is required for `lookup.py` and `ste_check.py` (both scripts have no external dependencies).

### Coverage

| Section | Rules | Topic |
|---------|-------|-------|
| 1 | 1.1-1.14 | Words - approved words, parts of speech, technical names, spelling |
| 2 | 2.1-2.3 | Noun clusters - max 3 words, hyphens, articles |
| 3 | 3.1-3.7 | Verbs - approved tenses, active voice, -ing restrictions |
| 4 | 4.1-4.4 | Sentences - 20-25 word limit, vertical lists, connectors |
| 5 | 5.1-5.5 | Procedural writing - imperative mood, conditions, warnings |
| 6 | 6.1-6.6 | Descriptive writing - key phrases, topic sentences, paragraph limits |
| 7 | 7.1-7.3 | Safety instructions - WARNING vs CAUTION formatting |
| 8 | 8.1-8.7 | Punctuation & word counts - lists, abbreviations, hyphens |
| 9 | 9.1-9.4 + GR | Writing practices - terminology consistency, positive statements |
| Tech Verbs | 1.12 | 4 categories: manufacturing, computer, descriptions, operational |

### Dictionary (86 KB, 2,127 entries)

| Type | Count |
|------|-------|
| **Approved words** | 805 (with parts of speech and approved meanings) |
| **Unapproved words** | 1,323 (with approved alternatives) |

Each approved word is restricted to its specific part of speech and meaning. Example entries show approved and unapproved usage.

## Installation

### Codex

Install the complete repository as a skill directory in your user-level Codex skills folder:

```bash
git clone https://github.com/clayleopardlabs/ste100-skill.git ~/.agents/skills/ste100
```

Codex also supports repository-scoped skills at `.agents/skills/ste100/`. In both cases, keep `SKILL.md` and the complete `references/` directory together. Codex discovers the skill automatically. If it does not appear, restart Codex.

You can invoke it explicitly with `$ste100`, or let Codex activate it when your request matches the skill description.

### OpenCode / Claude Code

Place the complete `ste100/` folder, including `references/dictionary.md` and `references/verb-tenses.md`, in your skills directory:

```bash
# OpenCode (auto-scanned)
~/.agents/skills/ste100/SKILL.md

# Claude Code
~/.claude/skills/ste100/SKILL.md
```

Restart the assistant. It will auto-discover the skill and trigger when you mention STE, STE100, Simplified Technical English, controlled language writing, or ask to validate/convert technical documentation.

### Manual Config

Add to `opencode.json`:

```json
{
  "skills": {
    "paths": ["path/to/ste100"]
  }
}
```

## Usage Examples

```
"Rewrite this maintenance procedure in STE: [text]"
"Check this paragraph for STE compliance: [text]"
"Is 'utilize' an approved STE word?"
"Convert this instruction to Simplified Technical English: [text]"
"What's wrong with this sentence: [text]"
"Run the STE linter on procedure.md"
```

The `ste100-verify` skill (shipped alongside) is the verification-only mode: it lints existing text and walks through the findings one rule at a time. The `ste100` skill covers writing, rewriting, and verification together.

## Examples

The examples below are instructional text. That is what ASD-STE100 was designed for: maintenance and operating procedures that a reader must follow exactly, with no room for misunderstanding.

### Example 1: A Maintenance Procedure

Before:

> To ensure the optimum performance and longevity of your filtration system, it is essential that the filter element be replaced on a regular basis. Prior to commencing this procedure, ensure that the system is completely deactivated and disconnected from the main power supply. Then carefully remove the access cover, taking care not to damage the sealing surface. Once the cover has been removed, locate the old filter element and remove it from its housing. Prior to installing the new filter, inspect the housing for debris and clean it thoroughly. Finally, reinstall the access cover and reactivate the system, and your system will operate at peak efficiency once more.

After (strict STE):

> **WARNING:** Make sure that the switch is OFF before you open the cover.

Remove the used filter:
- Disconnect the primary supply.
- Set the switch to OFF.
- Open the cover.
- Remove the filter.
- Examine the housing.
- Clean the housing.

Install the new filter:
- Install the new filter.
- Close the cover.
- Set the switch to ON.

What changed:

- "ensure" -> MAKE SURE, "prior to" -> BEFORE, "inspect" -> EXAMINE, "commence" and "locate" are not approved words
- Passive voice became active voice: "it is essential that the filter element be replaced" -> "Remove the filter"
- One instruction per step; the longest step is 10 words, under the 20-word limit
- Steps are grouped into two vertical lists of at most 6 items, with bullets (Rules 4.3, 8.4, 8.5)
- The WARNING comes first and states the condition before the action
- "optimum", "longevity", "peak efficiency" are marketing claims, not instructions; they were removed
- Every step is preserved, including the technical details: "disconnected from the main power supply" -> "Disconnect the primary supply", "inspect the housing for debris and clean it thoroughly" -> "Examine the housing" + "Clean the housing"
- Verified with `ste_check.py --allow housing` (housing is a technical name): 0 errors, 0 warnings; `--details` confirms no technical detail was dropped

### Example 2: An Operating Procedure

Before:

> To commence operations, please ensure that all safety protocols have been reviewed and acknowledged. Prior to activating the pump, verify that all connections are secure and that the inlet valve is in the open position. When you are ready, proceed to power on the system by depressing the start button. During operation, it is critical to continuously monitor the pressure gauge, and if any anomalies are detected, immediately cease operations and consult the troubleshooting section of this manual.

After:

> **WARNING:** Make sure that all safety procedures are complete before you operate the pump.

Prepare the pump:
- Make sure that all connections are tight.
- Make sure that the inlet valve is OPEN.

Operate the pump:
- Set the switch to ON.
- Examine the pressure.

If the pressure is too high:
- Stop the pump.
- Read the troubleshooting section of the manual.

What changed:

- "commence", "activate", "depress", "monitor", "detect", "cease" are not approved words
- "When you are ready" and "please ensure that" are not instructions; they were removed
- "verify that all connections are secure" -> "Make sure that all connections are tight"
- "verify that the inlet valve is in the open position" -> "Make sure that the inlet valve is OPEN"
- The condition "if any anomalies are detected, immediately cease operations" -> the conditional list "If the pressure is too high: Stop the pump"
- "consult the troubleshooting section" -> "Read the troubleshooting section of the manual"
- Each step is one command in a vertical list of at most 6 items (Rules 4.3, 8.4, 8.5); the longest is 10 words, under the 20-word limit
- Verified with `ste_check.py`: 0 errors, 0 warnings; `--details` confirms no technical detail was dropped

### Example 3: A Surgical Procedure

Before:

> The patient is positioned supine and general anesthesia is administered, after which the abdomen is prepped and draped in the usual sterile fashion; a pneumoperitoneum is then established via Veress needle insertion at the umbilicus with CO2 insufflation to approximately 12-15 mmHg, and once adequate working space has been achieved, a 10 mm trocar is introduced for the camera while two additional 5 mm ports are placed in the left lower quadrant and suprapubic region under direct visualization; following abdominal exploration, the appendix is identified at its origin from the cecum by tracing the taeniae coli, and it is grasped with atraumatic forceps and retracted superiorly, after which the mesoappendix is divided with electrocautery and the appendicular artery is clipped; the base is then doubly ligated with Vicryl endoloops approximately 5 mm from the cecal wall, crushed with a Kelly clamp, and transected with scissors, with the specimen removed through the 10 mm port; finally, hemostasis is confirmed under direct vision, the CO2 is evacuated, and the fascia is closed with interrupted 0-Vicryl if the port site is greater than 10 mm, followed by skin closure with subcuticular 3-0 Monocryl and sterile dressings, and the patient is monitored in recovery.

After:

> **WARNING:** Do this operation only in a room for surgery. If you are not a surgeon, do not do this operation.

Prepare the patient:
- Put the patient on their back.
- Give the patient general anesthesia.
- Clean the abdomen with antiseptic solution.
- Cover the abdomen with sterile drapes.
- Make a small incision in the lower right abdomen at McBurney's point.

Access:
- Put the Veress needle at the umbilicus.
- Fill the abdomen with CO2 gas to a pressure of 12 to 15 mmHg.
- Wait until the abdominal wall rises.
- Put the 10 mm camera port at the umbilicus.
- Put two 5 mm ports in the left lower quadrant and the suprapubic region.

Find the appendix:
- Look at the abdominal organs on the monitor.
- Find the appendix where the appendix attaches to the cecum.
- Hold the appendix with the forceps.
- Pull the appendix up.
- Cut the mesoappendix with the cautery tool.
- Attach the blood vessels in the mesoappendix.

Remove the appendix:
- Attach the lower part of the appendix twice with Vicryl loops.
- Make the loops 5 mm from the cecum.
- Crush the appendix with a Kelly clamp.
- Cut the appendix with scissors between the two loops.
- Remove the appendix through the 10 mm camera port.

Close the wound:
- Examine the area for blood.
- Remove the CO2 gas from the abdomen.
- Close the muscle layer with 0-Vicryl suture if the port site is more than 10 mm.
- Close the skin with 3-0 Monocryl suture.
- Cover the wound with a sterile bandage.
- Send the patient to the recovery room.

What changed:

- A 120-word run-on paragraph became 27 one-command steps, each a single complete action
- The steps are grouped into 6 vertical lists of at most 6 items, as the spec requires (Rules 4.3, 8.4, 8.5)
- Passive voice became imperative commands: "it is grasped with atraumatic forceps" -> "Hold the appendix with the forceps"
- Jargon was replaced with plain wording: "pneumoperitoneum" -> "CO2 gas", "hemostasis is confirmed" -> "Examine the area for blood"
- Unapproved dictionary words were replaced with approved ones: INSERT -> PUT, GRASP -> HOLD, TIE -> ATTACH, JOIN -> ATTACH, UPWARD -> UP, LOCATE -> FIND
- "port" is not an approved word, but it is the standard name for the part in this procedure - it is kept as a technical name and passed to the linter with `--allow port`
- Ambiguous pronouns became repeated nouns: "it", "the specimen" -> "the appendix" every time
- The WARNING comes first and states who may do the operation (Rule 7.1)
- Every step from the original is preserved, including every technical detail: "12-15 mmHg" -> "12 to 15 mmHg", "10 mm trocar" -> "10 mm camera port", "two additional 5 mm ports" -> "two 5 mm ports", "Vicryl endoloops" -> "Vicryl loops", "crushed with a Kelly clamp" -> "Crush the appendix with a Kelly clamp", "0-Vicryl if the port site is greater than 10 mm" -> "0-Vicryl suture if the port site is more than 10 mm", "subcuticular 3-0 Monocryl" -> "3-0 Monocryl suture"
- Verified with `ste_check.py --allow port`: 0 errors, 0 warnings; `--details` confirms no technical detail was dropped

## About ASD-STE100

ASD-STE100 is an international specification maintained by the **AeroSpace and Defence Industries Association of Europe (ASD)**. It was originally developed in 1986 as the AECMA Simplified English Guide and is required by ATA for aerospace maintenance documentation.

The specification has two parts:
- **Part 1** - Writing rules (grammar, style, and structure)
- **Part 2** - Controlled dictionary (approved words, meanings, and examples)

This skill is based on **ASD-STE100 Issue 8, April 2021** (European Community Trade Mark No. 017966390).

## License

This skill is a reference implementation based on the public ASD-STE100 specification. The specification itself is copyright (c) ASD. The dictionary is an assembled reference listing of approved and unapproved terminology (word collections and factual terms are not copied verbatim as prose from the guide book), included to make the skill self-contained. This skill file is provided for reference and educational use.
