# STE Section 4: Sentences (Rules 4.1–4.4)

| Rule | Summary |
|------|---------|
| **4.1** | Write one topic per sentence. Maximum 20-25 words (procedural) / 25-27 words (descriptive) |
| **4.2** | Do not omit words to make short sentences — never sacrifice clarity for brevity |
| **4.3** | Use vertical lists for complex information. Separate items with colons, dashes, or bullet points |
| **4.4** | Use connecting words and phrases (and, but, then, thus, as a result, at the same time) to connect sentences that contain related topics |

## Deep Dive

**Rule 4.1 — the word count:** Count every word except numbers? No — count EVERY word, including numbers and units. "Set the pressure to 5 psi." = 6 words. The linter flags sentences over 25 words as ERRORS and 21-25 as WARNINGs.

**Rule 4.2 — never delete content:** STE simplifies the phrasing, never the information. Shortening "inspect the housing for debris and clean it thoroughly" to "clean the housing" is a violation — the inspection step must stay. If a sentence is too long, split it into two complete sentences that each keep their full information.

**Rule 4.3 — vertical lists:** Use a vertical list when a sentence has 3+ related items or steps. Format: a lead-in phrase ending in a colon, then one bullet per item.

```
Remove the panel:
- Disconnect the cable.
- Remove the 4 screws.
- Pull the panel forward.
```

Hard limits (Rules 8.4/8.5): maximum 6 items per list, 20 words per item, 2 sentences per item. If you have more than 6 steps, split them into multiple lists under grouped headings. The linter enforces all three.

**Rule 4.4 — connectors:** Use "and", "but", "then", "thus", "as a result", "at the same time" to join related sentences. Do not use them to chain more than one action into a single sentence (Rule 3.7).

- "Open the valve. Then fill the tank." (two sentences, one connector)
