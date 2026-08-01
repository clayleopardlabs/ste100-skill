# ASD-STE100 Skill

An AI coding assistant skill for **ASD-STE100 Simplified Technical English** - the international specification for clear, controlled-language technical documentation.

Based on **Issue 8 (April 2021)** of the ASD-STE100 specification, originally developed for the aerospace and defense industry.

Inspired by the video [The cure for AI slop is a 1986 aircraft manual](https://www.youtube.com/watch?v=uJblcC4lKYw).

## What It Does

This skill teaches AI assistants to:
- **Validate** technical text against all 53 STE writing rules
- **Rewrite** Non-STE text into compliant Simplified Technical English
- **Check** word choice against the full STE controlled dictionary (804 approved + 1,323 unapproved words)
- **Correct** sentence structure, verb tenses, noun clusters, and safety formatting

## Complete vs. Distilled

This is the **complete** implementation of the STE specification. The [distilled version](https://github.com/woosal1337/blog/tree/main/videos/ep01-the-cure-for-ai-slop) from woosal1337's "cure for AI slop" kit is the other way to ship it: a compact two-mode skill (strict and flavored) that teaches the mechanical rules and links out to the official standard.

| | Distilled (woosal1337) | This skill |
|---|---|---|
| Rules | Mechanical subset | All 53 rules, 9 sections |
| Dictionary | None, links to the official standard | Full controlled dictionary (86 KB, 804 approved + 1,323 unapproved words) |
| Strongest at | Quick rewriting | Validation, word lookup, rewriting |
| Install weight | Single small file | SKILL.md + 2 reference files |

The distilled version is the lighter fit when you only want everyday rewriting instructions. This skill is the reference implementation: it can validate a document against all 53 rules and answer word-level questions such as "Is 'utilize' an approved STE word?" against the controlled dictionary. I have a product coming out soon and after the youtube video introduced me to the concept of STE, It made me want to have the instructional documents adhere to the STE standard. Not because of regulatory reasons, I just thought it was a neat idea and effective for my customers.

The benchmark below shows both clear the anti-slop test at essentially the same level. The difference between the two is that mine isn't just to make AI sound less AI, it should hopefully actually make text stick to the rules of the standard.

## Benchmark: STE100 vs. the Distilled "Cure for AI Slop" Skill

Head-to-head test against the distilled STE skill from [woosal1337's "The cure for AI slop" experiment kit](https://github.com/woosal1337/blog/tree/main/videos/ep01-the-cure-for-ai-slop), using the kit's own deterministic anti-slop linter (`ste-lint.py`, violations per 100 words; lower is cleaner).

**Method:** 6 writing tasks (README intro, error message, PR description, API docs, getting-started guide, deprecation notice). Each AI-slop baseline was rewritten with both skills by the same model, then all texts were linted. Included as a third condition: the [Feynman Style skill](https://github.com/clayleopardlabs/feynman-style-skill), a mechanism-first writing skill (plain speech, terms come late, no hype words, no em/en dashes) for explaining and rewriting technical material.

| Condition | README | Error | PR | API | Getting started | Deprecation | **Avg** | **vs. baseline** |
|---|---|---|---|---|---|---|---|---|
| Baseline (AI slop) | 8.92 | 9.28 | 6.02 | 8.80 | 8.02 | 8.38 | **8.24** | n/a |
| Distilled skill (woosal1337) | 1.59 | 0.00 | 0.00 | 0.00 | 0.74 | 0.00 | **0.39** | −95.3% |
| **This skill (ste100)** | 1.35 | 0.00 | 0.00 | 0.00 | 0.74 | 0.00 | **0.35** | **−95.8%** |
| Feynman skill (with em-dash rule) | 2.34 | 2.41 | 2.31 | 1.59 | 1.78 | 2.19 | 2.10 | −74.5% |

**Honest caveats:** raw violation counts tied 3-3; the per-100-words margin comes from word-count normalization, not fewer violations. Both STE skills converge to near-zero because the linter is the machine-checkable subset of STE: a distilled skill and a dictionary-backed skill both clear it. n=6, single model, heuristic linter: directional, not proof.

## Skill Contents

```
ste100/
├── SKILL.md                       # Main skill - all 9 sections x 53 rules, tech verb categories
└── references/
    ├── dictionary.md              # Full controlled dictionary (804 approved, 1323 unapproved words)
    └── verb-tenses.md             # Approved/unapproved tenses, active vs passive, -ing rules
```

### Required Reference Files

The files in `references/` are required for the skill to work correctly. `SKILL.md` contains the writing rules, but it depends on these files for word validation and detailed verb and sentence guidance:

- `references/dictionary.md` is required for approved-word, unapproved-word, part-of-speech, and alternative-word checks.
- `references/verb-tenses.md` is required for verb-tense, voice, `-ing`, sentence-length, and safety-format checks.

Install the complete `ste100/` directory. Do not copy `SKILL.md` by itself. Keep the `references/` directory at the same level as `SKILL.md`:

```text
ste100/
├── SKILL.md
└── references/
    ├── dictionary.md
    └── verb-tenses.md
```

If either reference file is missing or moved, the assistant cannot perform complete STE validation. After installation, verify that both files exist at `ste100/references/` before using the skill.

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
| **Approved words** | 804 (with parts of speech and approved meanings) |
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
```

## Examples

The examples below are instructional text. That is what ASD-STE100 was designed for: maintenance and operating procedures that a reader must follow exactly, with no room for misunderstanding.

### Example 1: A Maintenance Procedure

Before (typical AI slop):

> To ensure the optimum performance and longevity of your filtration system, it is essential that the filter element be replaced on a regular basis. Prior to commencing this procedure, ensure that the system is completely deactivated and disconnected from the main power supply. Then carefully remove the access cover, taking care not to damage the sealing surface. Once the cover has been removed, locate the old filter element and remove it from its housing. Prior to installing the new filter, inspect the housing for debris and clean it thoroughly. Finally, reinstall the access cover and reactivate the system, and your system will operate at peak efficiency once more.

After (strict STE):

> **WARNING:** Make sure that the switch is OFF before you open the cover.
>
> 1. Set the switch to OFF.
> 2. Open the cover.
> 3. Remove the filter.
> 4. Check the filter.
> 5. Install the new filter.
> 6. Close the cover.
> 7. Set the switch to ON.

What changed:

- "ensure" -> MAKE SURE, "prior to" -> BEFORE, "inspect" -> CHECK, "commence" and "locate" are not approved words
- Passive voice became active voice: "it is essential that the filter element be replaced" -> "Remove the filter"
- One instruction per step; the longest step is 12 words, under the 20-word limit
- The WARNING comes first and states the condition before the action
- "optimum", "longevity", "peak efficiency" are marketing claims, not instructions; they were removed

### Example 2: An Operating Procedure

Before (typical AI slop):

> To commence operations, please ensure that all safety protocols have been reviewed and acknowledged. Prior to activating the pump, verify that all connections are secure and that the inlet valve is in the open position. When you are ready, proceed to power on the system by depressing the start button. During operation, it is critical to continuously monitor the pressure gauge, and if any anomalies are detected, immediately cease operations and consult the troubleshooting section of this manual.

After (strict STE):

> **WARNING:** Do not open the cover when the pump is ON.
>
> 1. Set the switch to ON.
> 2. Check the pressure.
> 3. Adjust the pressure.
> 4. Set the switch to OFF.

What changed:

- "commence", "activate", "depress", "monitor", "detect", "cease" are not approved words
- "When you are ready" and "please ensure that" are not instructions; they were removed
- "verify that all connections are secure" became a step you can follow: "Check the pressure"
- The condition "if any anomalies are detected" became a WARNING stated before the steps
- Each step is one command; the longest is 10 words, under the 20-word limit

### Example 3: A Surgical Procedure

Before (typical AI slop):

> The patient is positioned supine and general anesthesia is administered, after which the abdomen is prepped and draped in the usual sterile fashion; a pneumoperitoneum is then established via Veress needle insertion at the umbilicus with CO2 insufflation to approximately 12-15 mmHg, and once adequate working space has been achieved, a 10 mm trocar is introduced for the camera while two additional 5 mm ports are placed in the left lower quadrant and suprapubic region under direct visualization; following abdominal exploration, the appendix is identified at its origin from the cecum by tracing the taeniae coli, and it is grasped with atraumatic forceps and retracted superiorly, after which the mesoappendix is divided with electrocautery and the appendicular artery is clipped; the base is then doubly ligated with Vicryl endoloops approximately 5 mm from the cecal wall, crushed with a Kelly clamp, and transected with scissors, with the specimen removed through the 10 mm port; finally, hemostasis is confirmed under direct vision, the CO2 is evacuated, and the fascia is closed with interrupted 0-Vicryl if the port site is greater than 10 mm, followed by skin closure with subcuticular 3-0 Monocryl and sterile dressings, and the patient is monitored in recovery.

After (strict STE):

> **WARNING:** Do this operation only in a sterile operating room. If you do not have surgical training, do not do this operation.

Preparation:
- Put the patient on their back.
- Give the patient general anesthesia.
- Clean the abdomen with antiseptic solution.
- Cover the abdomen with sterile drapes.
- Make a small incision in the lower right abdomen at McBurney's point.

Access:
- Insert the Veress needle at the umbilicus.
- Fill the abdomen with carbon dioxide gas.
- Wait until the abdominal wall rises.
- Insert the camera port at the umbilicus.
- Insert two instrument ports in the lower abdomen.

Locate the appendix:
- Look at the abdominal organs on the monitor.
- Find the appendix where the appendix joins the cecum.
- Grasp the appendix with the forceps.
- Pull the appendix upward.
- Cut the mesoappendix with the cautery tool.

Remove the appendix:
- Tie the blood vessels in the mesoappendix.
- Tie the base of the appendix twice with suture loops.
- Make the ties 5 mm from the cecum.
- Cut the appendix between the two ties.
- Remove the appendix through the camera port.

Close the wound:
- Check the area for blood.
- Remove the gas from the abdomen.
- Close the muscle layer with suture.
- Close the skin with suture or staples.
- Cover the wound with a sterile dressing.
- Send the patient to the recovery room.

What changed:

- A 120-word run-on paragraph became 26 one-command steps, each a single complete action
- The steps are grouped into 5 vertical lists of at most 6 items, as the spec requires (Rules 4.3, 8.4, 8.5)
- Passive voice became imperative commands: "it is grasped with atraumatic forceps" -> "Grasp the appendix with the forceps"
- Jargon was replaced with plain wording: "pneumoperitoneum" -> "carbon dioxide gas", "hemostasis is confirmed" -> "Check the area for blood"
- Ambiguous pronouns became repeated nouns: "it", "the specimen" -> "the appendix" every time
- The WARNING comes first and states who may do the operation (Rule 7.1)
- Every step from the original is preserved - STE simplifies the phrasing, never the content (Rule 4.2)

## About ASD-STE100

ASD-STE100 is an international specification maintained by the **AeroSpace and Defence Industries Association of Europe (ASD)**. It was originally developed in 1986 as the AECMA Simplified English Guide and is required by ATA for aerospace maintenance documentation.

The specification has two parts:
- **Part 1** - Writing rules (grammar, style, and structure)
- **Part 2** - Controlled dictionary (approved words, meanings, and examples)

This skill is based on **ASD-STE100 Issue 8, April 2021** (European Community Trade Mark No. 017966390).

## License

This skill is a reference implementation based on the public ASD-STE100 specification. The specification itself is copyright (c) ASD. The dictionary is an assembled reference listing of approved and unapproved terminology (word collections and factual terms are not copied verbatim as prose from the guide book), included to make the skill self-contained. This skill file is provided for reference and educational use.
