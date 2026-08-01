# Rubric: test-05

**Target: 5 violations** (4 ERROR, 1 WARNING). The paragraph is otherwise perfect STE.

| # | Line | Offending text | Rule | Correction |
|---|------|----------------|------|------------|
| 1 | 8 | "Swap the cover into position." — word **Swap** | Rule 1.1/1.6 (unapproved word) | Replace with an approved word: "Interchange the cover into position." or "Put the cover into position." |
| 2 | 1 | "Examine the pressure indicator on the hydraulic filter and measure the level of the fluid in the tank before you operate the system again after the test." — **27 words** | Rule 4.1/8.7 (sentence over 25 words) | Split into short sentences. |
| 3 | 2 | "Close the valve; drain the fluid." — **semicolon** | Rule 8.1 (semicolon misuse) | Split into two sentences: "Close the valve. Drain the fluid." |
| 4 | 3 | "Use a tool, e.g. a wrench, to loosen the bolt." — **"e.g."** | GR-6 (Latin abbreviation) | Replace with "for example": "Use a tool, for example a wrench, to loosen the bolt." |
| 5 | 4 | "Hold the wrench with the left hand while **holding** the valve." — **-ing form "holding"** | Rule 3.5 (-ing form) | "Holding" is not one of the 9 approved -ing forms. Rewrite with an approved form: "Hold the wrench with the left hand. Hold the valve." or "Hold the wrench with the left hand and hold the valve with the right hand." (two separate actions). |

**Pass criteria:** The model identifies all five violations and corrects each. Final text: 0 errors, 0 warnings from ste_check.py. Any other change that introduces a new violation fails the test.
