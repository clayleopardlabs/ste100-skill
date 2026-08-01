# STE Section 8: Punctuation & Word Counts (Rules 8.1–8.7)

| Rule | Summary |
|------|---------|
| **8.1** | Use semicolons to separate items in complex lists only; prefer separate sentences |
| **8.2** | Use hyphens only to form compound modifiers and clarify noun clusters |
| **8.3** | Use parentheses sparingly — prefer commas or restructure the sentence |
| **8.4** | Maximum 6 items in a vertical list. Maximum 20 words per list item |
| **8.5** | Maximum 2 sentences per list item in a vertical list |
| **8.6** | Use standard abbreviations and acronyms. Define on first use. Do not abbreviate approved STE words |
| **8.7** | Count words as in standard English. Maximum 20-25 per procedural sentence, 25-27 per descriptive sentence. Hyphenated compounds count as one word |

## Deep Dive

**Rule 8.1 — semicolons:** The linter flags every semicolon as an ERROR. A semicolon is only allowed to separate items in a complex vertical list whose items already contain commas. In normal text, split into separate sentences.

- Violation: "Open the valve; fill the tank."
- OK (complex list item): "- Set the switch to ON, and wait 2 seconds; set the switch to OFF"

**Rule 8.2 — hyphens:** Compound modifiers get hyphens: "a 3-psi pressure", "the 5-mm screw". Hyphens are the main tool for taming noun clusters (Rule 2.2). Do not hyphenate ordinary adjective-noun pairs: "the red cover" (no hyphen).

**Rule 8.3 — parentheses:** Restructure instead. "The filter (part no. 12345) is installed" -> "Install the filter, part no. 12345." Parentheses are acceptable for part numbers and cross-references, nothing else.

**Rules 8.4/8.5 — the vertical list limits (the ones the linter enforces hard):**
- Maximum 6 items per list
- Maximum 20 words per item
- Maximum 2 sentences per item
- More than 6 steps? Split into multiple lists with headings ("Remove the old filter:" / "Install the new filter:")

**Rule 8.6 — abbreviations:** Define an abbreviation on first use: "the Emergency Power Supply (EPS)". Never abbreviate an approved STE word ("approx.", "temp."). Units of measurement (mm, psi) are technical names, not abbreviations — no definition needed.

**Rule 8.7 — counting:** Numbers and units count as words: "Set the pressure to 5 psi" = 6 words. Hyphenated compounds count as one: "the 5-mm screw" = 4 words. The linter counts the same way.
