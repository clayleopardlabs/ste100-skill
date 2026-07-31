# ASD-STE100 Skill

An AI coding assistant skill for **ASD-STE100 Simplified Technical English** - the international specification for clear, controlled-language technical documentation.

Based on **Issue 8 (April 2021)** of the ASD-STE100 specification, originally developed for the aerospace and defense industry.

Inspired by the video [The cure for AI slop is a 1986 aircraft manual](https://www.youtube.com/watch?v=uJblcC4lKYw).

## What It Does

This skill teaches AI assistants to:
- **Validate** technical text against all 53 STE writing rules
- **Rewrite** Non-STE text into compliant Simplified Technical English
- **Check** word choice against the full STE controlled dictionary (543 approved + 1,323 unapproved words)
- **Correct** sentence structure, verb tenses, noun clusters, and safety formatting

## Complete vs. Distilled

This is the **complete** implementation of the STE specification. The [distilled version](https://github.com/woosal1337/blog/tree/main/videos/ep01-the-cure-for-ai-slop) from woosal1337's "cure for AI slop" kit is the other way to ship it: a compact two-mode skill (strict and flavored) that teaches the mechanical rules and links out to the official standard.

| | Distilled (woosal1337) | This skill |
|---|---|---|
| Rules | Mechanical subset | All 53 rules, 9 sections |
| Dictionary | None, links to the official standard | Full controlled dictionary (86 KB, 543 approved + 1,323 unapproved words) |
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
    ├── dictionary.md              # Full controlled dictionary (543 approved, 1323 unapproved words)
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

### Dictionary (86 KB, 1,866 entries)

| Type | Count |
|------|-------|
| **Approved words** | 543 (with parts of speech and approved meanings) |
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

## About ASD-STE100

ASD-STE100 is an international specification maintained by the **AeroSpace and Defence Industries Association of Europe (ASD)**. It was originally developed in 1986 as the AECMA Simplified English Guide and is required by ATA for aerospace maintenance documentation.

The specification has two parts:
- **Part 1** - Writing rules (grammar, style, and structure)
- **Part 2** - Controlled dictionary (approved words, meanings, and examples)

This skill is based on **ASD-STE100 Issue 8, April 2021** (European Community Trade Mark No. 017966390).

## License

This skill is a reference implementation based on the public ASD-STE100 specification. The specification itself is copyright (c) ASD. The dictionary is an assembled reference listing of approved and unapproved terminology (word collections and factual terms are not copied verbatim as prose from the guide book), included to make the skill self-contained. This skill file is provided for reference and educational use.
