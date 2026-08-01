# STE Section 9: Writing Practices (Rules 9.1–9.4 + General Recommendations)

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

## Deep Dive

**Rule 9.1 — the lookup rule:** When a word is not in the dictionary, first try a dictionary synonym ("ensure" -> MAKE SURE, "commence" -> START, "utilize" -> USE). Only if no synonym fits does it become a technical name or technical verb. Use `lookup.py` for every doubtful word:

```bash
python references/lookup.py ensure commence utilize port
```

**Rule 9.2 — terminology consistency:** Pick one name for one thing and never vary it. "The engine" cannot become "the powerplant" later in the same document. Repeat the noun instead of using a pronoun when there is any chance of confusion (GR-3).

**Rule 9.3 — positive over negative:** "Do not do the test unless the light is ON" -> "Do the test only when the light is ON". Negative commands are still allowed inside WARNING/CAUTION (safety text is the standard exception).

**GR-1/GR-4 — dangling "this":** "This is important" is a violation. "This switch is important" is correct ("this" + noun). The linter flags sentences starting with "This" + a verb.

**GR-6 — Latin abbreviations:** The linter flags i.e., e.g., etc., viz. as ERRORS. Replace with "that is", "for example", "and so on". Match the MEANING: "e.g." -> "for example", "i.e." -> "that is", "etc." -> "and so on". Do not use "that is" for "etc." or "for example" for "i.e.".
