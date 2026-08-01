# Rubric: test-01

**Target: 1 violation** (1 ERROR, 0 WARNING). The paragraph is otherwise perfect STE.

| # | Line | Offending text | Rule | Correction |
|---|------|----------------|------|------------|
| 1 | 4 | "Swap the cover into position." — word **Swap** | Rule 1.1/1.6 (unapproved word) | Replace with an approved word: "Interchange the cover into position." (INTERCHANGE (v)) or "Put the cover into position." (PUT (v)) |

**Pass criteria:** The model identifies the single violation (Swap) and corrects it to an approved word, producing text with 0 errors and 0 warnings from ste_check.py. Any other change that introduces a new violation fails the test.
