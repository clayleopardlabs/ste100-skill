# Rubric: test-08

**Target: 8 violations** (4 ERROR, 4 WARNING). The paragraph is otherwise perfect STE.

| # | Line | Offending text | Rule | Correction |
|---|------|----------------|------|------------|
| 1 | 11 | "Swap the cover into position." — word **Swap** | Rule 1.1/1.6 (unapproved word) | Replace with an approved word: "Interchange the cover into position." or "Put the cover into position." |
| 2 | 1 | "Examine the pressure indicator on the hydraulic filter and measure the level of the fluid in the tank before you operate the system again after the test." — **27 words** | Rule 4.1/8.7 (sentence over 25 words) | Split into short sentences. |
| 3 | 2 | "Close the valve; drain the fluid." — **semicolon** | Rule 8.1 (semicolon misuse) | Split into two sentences: "Close the valve. Drain the fluid." |
| 4 | 3 | "Use a tool, e.g. a wrench, to loosen the bolt." — **"e.g."** | GR-6 (Latin abbreviation) | Replace with "for example": "Use a tool, for example a wrench, to loosen the bolt." |
| 5 | 4 | "Hold the wrench with the left hand while **holding** the valve." — **-ing form "holding"** | Rule 3.5 (-ing form) + 3.7 (while-join) | Rewrite with an approved form: "Hold the wrench with the left hand. Hold the valve." |
| 6 | 5 | "The operator **has completed** the repair." — **present perfect tense** | Rule 3.2/3.4 (complex verb tense) | Use simple past: "The operator completed the repair." |
| 7 | 6 | "The cover **is removed by** the operator." — **passive voice** | Rule 3.6 (passive voice) | Rewrite in active voice: "The operator removes the cover." |
| 8 | 10 | "Examine the **high pressure hydraulic oil filter** for damage." — **noun cluster (5 words in a row)** | Rule 2.1 (noun cluster over 3 words) | Split the cluster with prepositions or hyphens: "Examine the filter for the hydraulic oil at high pressure for damage." or use a hyphenated technical name: "Examine the high-pressure hydraulic-oil filter for damage." |

**Pass criteria:** The model identifies all eight violations and corrects each. Final text: 0 errors, 0 warnings from ste_check.py. Any other change that introduces a new violation fails the test.
