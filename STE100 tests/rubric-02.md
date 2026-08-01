# Rubric: test-02

**Target: 2 violations** (2 ERROR, 0 WARNING). The paragraph is otherwise perfect STE.

| # | Line | Offending text | Rule | Correction |
|---|------|----------------|------|------------|
| 1 | 5 | "Swap the cover into position." — word **Swap** | Rule 1.1/1.6 (unapproved word) | Replace with an approved word: "Interchange the cover into position." or "Put the cover into position." |
| 2 | 1 | "Examine the pressure indicator on the hydraulic filter and measure the level of the fluid in the tank before you operate the system again after the test." — **27 words** | Rule 4.1/8.7 (sentence over 25 words) | Split into short sentences, e.g. "Examine the pressure indicator on the hydraulic filter. Measure the level of the fluid in the tank. Operate the system again after the test." |

**Pass criteria:** The model identifies both violations and corrects each. Final text: 0 errors, 0 warnings from ste_check.py. Any other change that introduces a new violation fails the test.
