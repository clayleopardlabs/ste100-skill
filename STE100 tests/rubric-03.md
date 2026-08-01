# Rubric: test-03

**Target: 3 violations** (3 ERROR, 0 WARNING). The paragraph is otherwise perfect STE.

| # | Line | Offending text | Rule | Correction |
|---|------|----------------|------|------------|
| 1 | 6 | "Swap the cover into position." — word **Swap** | Rule 1.1/1.6 (unapproved word) | Replace with an approved word: "Interchange the cover into position." or "Put the cover into position." |
| 2 | 1 | "Examine the pressure indicator on the hydraulic filter and measure the level of the fluid in the tank before you operate the system again after the test." — **27 words** | Rule 4.1/8.7 (sentence over 25 words) | Split into short sentences. |
| 3 | 2 | "Close the valve; drain the fluid." — **semicolon** | Rule 8.1 (semicolon misuse) | Split into two sentences: "Close the valve. Drain the fluid." |

**Pass criteria:** The model identifies all three violations and corrects each. Final text: 0 errors, 0 warnings from ste_check.py. Any other change that introduces a new violation fails the test.
