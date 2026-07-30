# ASD-STE100 Skill

An AI coding assistant skill for **ASD-STE100 Simplified Technical English** - the international specification for clear, controlled-language technical documentation.

Based on **Issue 8 (April 2021)** of the ASD-STE100 specification, originally developed for the aerospace and defense industry.

## What It Does

This skill teaches AI assistants to:
- **Validate** technical text against all 53 STE writing rules
- **Rewrite** Non-STE text into compliant Simplified Technical English
- **Check** word choice against the STE controlled dictionary
- **Correct** sentence structure, verb tenses, noun clusters, and safety formatting

## Skill Contents

```
ste100/
├── SKILL.md                       # Main skill - all 9 sections x 53 rules
└── references/
    ├── dictionary.md              # Dictionary structure, parts of speech, common replacements
    └── verb-tenses.md             # Approved/unapproved tenses, active vs passive, -ing rules
```

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
| Dictionary | - | Controlled dictionary reference, common word replacements |

## Installation

### OpenCode / Claude Code

Place the `ste100/` folder in your skills directory:

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
"Convert this instruction to Simplified Technical English: [text]"
"What's wrong with this sentence in STE: [text]"
"Explain why 'utilize' is not approved in STE"
```

## Example Rewrites

| Non-STE | STE |
|---------|-----|
| "Follow the safety instructions below." | "Obey the safety instructions below." |
| "Ensure the valve is operable." | "Make sure that the valve can operate." |
| "The temperature must be adjusted." | "Adjust the temperature." |
| "Test the system for leaks." | "Do a leak test of the system." |
| "The engine utilizes fuel injection." | "The engine uses fuel injection." |

## About ASD-STE100

ASD-STE100 is an international specification maintained by the **AeroSpace and Defence Industries Association of Europe (ASD)**. It was originally developed in 1986 as the AECMA Simplified English Guide and is required by ATA for aerospace maintenance documentation.

The specification has two parts:
- **Part 1** - Writing rules (grammar, style, and structure)
- **Part 2** - Controlled dictionary (approved words, meanings, and examples)

This skill is based on **ASD-STE100 Issue 8, April 2021** (European Community Trade Mark No. 017966390).

## License

This skill is a reference implementation based on the public ASD-STE100 specification. The specification itself is copyright (c) ASD. This skill file is provided for reference and educational use.