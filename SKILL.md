---
name: ste100
description: "ASD-STE100 Simplified Technical English. Use when the user mentions ASD-STE100, STE100, Simplified Technical English, controlled language technical writing, or asks to validate/convert/rewrite technical documentation to STE standard — or any task involving aerospace or defense maintenance documentation, technical manual writing in controlled English, or STE compliance checking. Also triggers on terms like 'STE', 'STE100', 'STE writing rules', 'STE dictionary', 'STE-approved words'."
---

# ASD-STE100 Simplified Technical English (STE)

You are an expert in ASD-STE100 Issue 8 (April 2021). STE is a controlled language specification for technical documentation with two parts: writing rules (Part 1) and a controlled dictionary (Part 2).

## Core Principles

STE's goal: make technical texts clear, simple, and unambiguous for readers worldwide — especially non-native English speakers.

1. **Use only approved words** from the STE dictionary with their approved meanings and approved parts of speech
2. **Technical names** (company/product-specific terms) and **technical verbs** are permitted outside the dictionary
3. **Each approved word has only one meaning** per part of speech
4. **American English** spelling (Merriam-Webster)
5. **Short, simple sentences** — maximum 20-25 words per sentence for procedural, up to 25-27 for descriptive

## The Controlled Dictionary (Part 2)

The full STE dictionary is in `references/dictionary.md` — **543 approved words** (UPPERCASE) and **1,323 unapproved words** (lowercase) with their meanings and alternatives.

| Type | Format | Example |
|------|--------|---------|
| **Approved word** | `* **WORD (pos)** → Approved meaning` | `* **ADJUSTMENT (n)** → The effect of adjusting` |
| **Unapproved word** | `* word → ALTERNATIVE (pos)` | `* maintain → KEEP (v); HOLD (v); MAINTENANCE (n)` |
| **Verb with forms** | Entry shows `VERB (v), VERBS, VERBED, VERBED` | `ADAPT (v), ADAPTS, ADAPTED, ADAPTED` |

**How to use:** Look up every word in the dictionary file. If not found, it must be a technical name or technical verb. Each approved word is restricted to its listed part of speech and meaning.

## Part 1 — Writing Rules (9 Sections, 53 Rules)

### Section 1: Words (Rules 1.1–1.14)

| Rule | Summary |
|------|---------|
| **1.1** | Use words approved in dictionary, technical names, or technical verbs |
| **1.2** | Use approved words only as their specified part of speech |
| **1.3** | Use approved words only with their approved meanings |
| **1.4** | Use only the approved forms of verbs and adjectives (given in dictionary) |
| **1.5** | Words are technical names if they fit one of 20 categories (see below) |
| **1.6** | Unapproved dictionary words are permitted only as technical names |
| **1.7** | Do not use technical names as verbs |
| **1.8** | Technical names must agree with approved nomenclature |
| **1.9** | Choose short, easy-to-understand technical names |
| **1.10** | Do not use slang or jargon as technical names |
| **1.11** | Do not use different technical names for the same item |
| **1.12** | Technical verbs are verbs within standard categories (manufacturing, computer, descriptions, operational). See full list below |
| **1.13** | Do not use technical verbs as nouns |
| **1.14** | Use American English spelling |

### Section 2: Noun Clusters (Rules 2.1–2.3)

| Rule | Summary |
|------|---------|
| **2.1** | Maximum 3 words in a noun cluster (do not make long noun strings) |
| **2.2** | Use hyphens to clarify relationships between words in a cluster |
| **2.3** | Use articles (a/an/the) and demonstrative adjectives (this/these) correctly to make meaning clear |

### Section 3: Verbs (Rules 3.1–3.7)

| Rule | Summary |
|------|---------|
| **3.1** | Use only verb tenses from the approved list: imperative, simple present, simple past, past participle (as adjective), simple future |
| **3.2** | Do not use: present perfect, past perfect, present/past progressive, or other complex forms |
| **3.3** | Use past participle as an adjective (before noun or after "to be"/"to become") — this is NOT passive voice |
| **3.4** | Do not use helping verbs to make complex verb structures (e.g., "has adjusted", "is adjusted", "will be adjusted") |
| **3.5** | Use "-ing" form only as a technical name or modifier in a technical name. Only 7 approved "-ing" words exist: lighting, opening, routing, servicing (nouns); mating, missing, remaining (adjectives); something (pronoun); during (preposition) |
| **3.6** | Use ONLY active voice in procedural writing. Use active voice as much as possible in descriptive writing |
| **3.7** | Write one action per sentence. Each sentence has ONE verb that describes ONE action |

### Section 4: Sentences (Rules 4.1–4.4)

| Rule | Summary |
|------|---------|
| **4.1** | Write one topic per sentence. Maximum 20-25 words (procedural) / 25-27 words (descriptive) |
| **4.2** | Do not omit words to make short sentences — never sacrifice clarity for brevity |
| **4.3** | Use vertical lists for complex information. Separate items with colons, dashes, or bullet points |
| **4.4** | Use connecting words and phrases (and, but, then, thus, as a result, at the same time) to connect sentences that contain related topics |

### Section 5: Procedural Writing (Rules 5.1–5.5)

| Rule | Summary |
|------|---------|
| **5.1** | Write instructions as direct commands (imperative mood): "Remove the screw." "Do the test." |
| **5.2** | Give one instruction per step. Each step must be a single, complete action |
| **5.3** | Put conditions before the action: "If the pressure is too low, fill the reservoir." |
| **5.4** | Use warnings and cautions before the step they apply to |
| **5.5** | Use notes to give explanatory information, not instructions or safety information |

### Section 6: Descriptive Writing (Rules 6.1–6.6)

| Rule | Summary |
|------|---------|
| **6.1** | Use descriptive writing to explain facts, functions, and conditions — not to give instructions |
| **6.2** | Use key words and key phrases to make the text easy to scan |
| **6.3** | Keep descriptive sentences to maximum 25-27 words |
| **6.4** | Use paragraphs to group related information. One topic per paragraph |
| **6.5** | Start each paragraph with a topic sentence that introduces the subject |
| **6.6** | Maximum 6 sentences per paragraph. Keep paragraphs short |

### Section 7: Safety Instructions (Rules 7.1–7.3)

| Rule | Summary |
|------|---------|
| **7.1** | Put WARNING before steps where injury or death can occur. Format: WARNING symbol + text, then the step |
| **7.2** | Put CAUTION before steps where equipment damage can occur. Format: CAUTION symbol + text, then the step |
| **7.3** | Use standard safety keywords. WARNING for personal safety, CAUTION for equipment damage. Do not use both for the same hazard |

### Section 8: Punctuation & Word Counts (Rules 8.1–8.7)

| Rule | Summary |
|------|---------|
| **8.1** | Use semicolons to separate items in complex lists only; prefer separate sentences |
| **8.2** | Use hyphens only to form compound modifiers and clarify noun clusters |
| **8.3** | Use parentheses sparingly — prefer commas or restructure the sentence |
| **8.4** | Maximum 6 items in a vertical list. Maximum 20 words per list item |
| **8.5** | Maximum 2 sentences per list item in a vertical list |
| **8.6** | Use standard abbreviations and acronyms. Define on first use. Do not abbreviate approved STE words |
| **8.7** | Count words as in standard English. Maximum 20-25 per procedural sentence, 25-27 per descriptive sentence. Hyphenated compounds count as one word |

### Section 9: Writing Practices (Rules 9.1–9.4 + General Recommendations)

| Rule | Summary |
|------|---------|
| **9.1** | When a word is not in the dictionary, find the best synonym from the dictionary. Do a word-for-word replacement or change the sentence construction |
| **9.2** | Always maintain consistent terminology. Use the same word for the same thing throughout a document |
| **9.3** | Write positive statements when possible. Negative statements can be harder to understand |
| **9.4** | Use a consistent style throughout the document (same tense, same voice, same format) |
| **GR-1** | Do not start a sentence with "this" unless it is followed by a noun ("This switch...") — a "dangling this" is ambiguous |
| **GR-2** | WITH (prep) has three approved meanings: association, help/sharing, or means/instrument. Avoid ambiguous constructions — re-read to ensure the sentence cannot be misunderstood |
| **GR-3** | Limit pronoun use. Repeat the noun when there is risk of ambiguity |
| **GR-4** | Use "this" and "these" as adjectives + nouns, not as standalone pronouns |
| **GR-5** | Avoid false friends (words that look similar to a word in another language but have different meanings) |
| **GR-6** | Do not use Latin abbreviations (e.g., i.e., e.g., etc.). Use "that is," "for example," "and so on" |

## Technical Name Categories (Rule 1.5)

| # | Category |
|---|----------|
| 1 | Names in official parts information (bolts, cables, filters, switches, etc.) |
| 2 | Names of vehicles/machines and locations on them (aircraft, cabin, wing, etc.) |
| 3 | Names of tools and support equipment (clamps, jacks, test rigs, torque wrenches, etc.) |
| 4 | Names of materials, consumables, and unwanted material (fuel, grease, oil, debris, etc.) |
| 5 | Names of facilities, infrastructure, and logistic procedures (hangar, apron, shipping, etc.) |
| 6 | Names of systems, components, circuits, functions, configurations, and parts |
| 7 | Names of operational and functional states (closed position, emergency, maintenance mode, etc.) |
| 8 | Names of persons according to function or specialization (pilot, mechanic, electrician, etc.) |
| 9 | Names of documents and document identifiers |
| 10 | Names of companies, organizations, manufacturers, and their abbreviations |
| 11 | Official names of procedures, methods, specifications, and standards |
| 12 | Names of software, computer programs, commands, files, and databases |
| 13 | Units of measurement (mm, psi, V, A, °C, etc.) and their symbols |
| 14 | Proper names, brand names, and trade names |
| 15 | Titles of publications, chapters, sections, figures, and tables |
| 16 | Text quoted from other sources, warnings, cautions, and notes |
| 17 | Colors (red, blue, green, yellow, white, black, gray, etc.) |
| 18 | Letters and numbers used as identifiers or names |
| 19 | Parts of a whole when each part is standard terminology in the industry |
| 20 | Military terms (NATO designations, military time, threat levels, mission types, etc.) |

## Technical Verb Categories (Rule 1.12)

Technical verbs are outside the dictionary but permitted in specific contexts. They must obey all other STE rules.

### 1. Manufacturing Processes
| Subcategory | Example Verbs |
|-------------|---------------|
| Remove material | drill, grind, mill, ream |
| Add material | flame, insulate, remetal, retread |
| Attach material | braze, crimp, rivet, solder, weld |
| Change strength/structure | anneal, cure, decay, freeze, heat-treat, magnetize, normalize, vaporize |
| Change surface finish | buff, burnish, dress, passivate, plate, polish |
| Change shape | blend, cast, extrude, spin, stamp |

### 2. Computer Processes and Applications
| Subcategory | Example Verbs |
|-------------|---------------|
| Input/output | click, digitize, enter, press, print, swipe, tap, type |
| UI/application | clear, close, copy, cut, delete, deselect, disable, drag, drag and drop, enable, encrypt, erase, filter, highlight, maximize, minimize, navigate, open, paste, save, scroll, sort, store, zoom in, zoom out |
| System operations | abort, boot, communicate, debug, download, format, install, load, manage, process, reboot, update, upgrade, upload |

### 3. Descriptions (descriptive texts only, NOT procedures)
| Subcategory | Example Verbs |
|-------------|---------------|
| Math/science/engineering | bisect, compensate for, convert, detect, emit, modulate, radiate, transform |
| Military processes | aim, arm, detect, disable, enable, explode, fire, intercept, load, lock on, parachute, unload |
| Regulatory language | waive, comply with, conform to, supersede, meet (a requirement) |

### 4. Operational Language
| Context | Example Verbs |
|---------|---------------|
| Operations (aircrew, medical, device manuals, etc.) | airdrop, alert, approach, authorize, brief, call, contact, crank, descend, deviate, disembark, drift, dry-motor, enable, evacuate, fasten, ferry, fly, hover, inform, inhibit, land, load, maintain, navigate, observe, provide, reach, respond, retard, retrim, return, rotate, serve, sanitize, shut down, sideslip, sit, sleep, sterilize, switch off, switch on, take off, take over, taxi, tie, trigger, trim, unfasten, unlatch, unload, verify, wet-motor |

**Reminder:** If an approved verb in the dictionary accurately gives the instruction, use it instead of a technical verb.

## Typical Rewrites

| Non-STE | STE |
|---------|-----|
| "Follow the safety instructions below." | "Obey the safety instructions below." |
| "Ensure the valve is operable." | "Make sure that the valve can operate." |
| "The temperature must be adjusted." | "Adjust the temperature." |
| "Approximately 5 liters of fluid is required." | "You will need approximately 5 liters of fluid." |
| "If any discrepancies are noted..." | "If you find discrepancies..." |
| "Test the system for leaks." | "Do a leak test of the system." |
| "The manufacturer recommends that you replace the filter." | "The manufacturer recommends that you replace the filter." |
| "The engine uses fuel for injection." | "The engine uses fuel for injection." |
| "The inspection should be performed daily." | "Do the inspection daily." |
| "Failure to comply will result in..." | "If you do not obey these instructions, injury can occur." |

## How to Write in STE

When asked to write or validate STE:

1. **Check every word** against the STE dictionary in `references/dictionary.md`. If the word is approved, use it only with its listed meaning and part of speech. If unapproved, use the listed alternative. If not in the dictionary at all, it must be a justified technical name or technical verb
2. **Verify part of speech** — an approved noun cannot be used as a verb and vice versa. The dictionary lists the part of speech for each word
3. **Keep sentences short** — count words rigorously. Split long sentences
4. **Use active voice** exclusively in procedures, predominantly in descriptions
5. **Use imperative mood** for instructions. Start each step with a command verb
6. **Check noun clusters** — no more than 3 words in a row modifying a noun
7. **Avoid -ing words** unless they are one of the 7 approved forms or part of a technical name
8. **No complex tenses** — only simple present, simple past, simple future, imperative, and past participle as adjective
9. **One action per verb** — each sentence should describe one primary action
10. **Safety structure** — WARNING before injury hazard steps, CAUTION before damage hazard steps

## Reference Files

| File | Contents |
|------|----------|
| `references/dictionary.md` | **Full controlled dictionary** — 543 approved words (with parts of speech and meanings) and 1,323 unapproved words (with approved alternatives). Check this for every word |
| `references/verb-tenses.md` | Approved verb tenses, active vs passive, -ing rules, sentence length limits, safety formatting |
