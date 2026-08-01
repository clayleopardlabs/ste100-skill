# Rubric: test-09

**Target: 16 violations** (8 ERROR, 8 WARNING) — two of every violation kind. The paragraph is otherwise perfect STE.

| # | Line | Offending text | Rule | Correction |
|---|------|----------------|------|------------|
| 1 | 15 | "**Swap** the cover into position." | Rule 1.1/1.6 (unapproved word) | "Interchange the cover into position." or "Put the cover into position." |
| 2 | 17 | "**Grab** the wrench with the right hand." | Rule 1.1/1.6 (unapproved word) | "Hold the wrench with the right hand." or "Use the wrench with the right hand." |
| 3 | 1 | 27-word sentence (line 1) | Rule 4.1/8.7 (sentence over 25 words) | Split into short sentences (e.g. three sentences of 8, 8, and 8 words). |
| 4 | 2 | 29-word sentence (line 2) | Rule 4.1/8.7 (sentence over 25 words) | Split into short sentences. |
| 5 | 3 | "Close the valve; drain the fluid." — **semicolon** | Rule 8.1 (semicolon misuse) | "Close the valve. Drain the fluid." |
| 6 | 4 | "Remove the cover; pull out the element." — **semicolon** | Rule 8.1 (semicolon misuse) | "Remove the cover. Pull out the element." |
| 7 | 5 | "Use a tool, **e.g.** a wrench, ..." | GR-6 (Latin abbreviation) | "Use a tool, for example a wrench, ..." |
| 8 | 6 | "Use a clean cloth, **etc.** to clean the valve." | GR-6 (Latin abbreviation) | "Use a clean cloth to clean the valve." |
| 9 | 7 | "while **holding** the valve" — **-ing form** | Rule 3.5 (-ing form) + 3.7 (while-join) | "Hold the wrench with the left hand. Hold the valve." |
| 10 | 8 | "while **checking** the fluid level" — **-ing form** | Rule 3.5 (-ing form) + 3.7 (while-join) | "Examine the seal. Examine the fluid level." |
| 11 | 9 | "The operator **has completed** the repair." — **present perfect** | Rule 3.2/3.4 (complex verb tense) | "The operator completed the repair." |
| 12 | 10 | "The technicians **have installed** the new pump." — **present perfect** | Rule 3.2/3.4 (complex verb tense) | "The technicians installed the new pump." |
| 13 | 11 | "The cover **is removed by** the operator." — **passive** | Rule 3.6 (passive voice) | "The operator removes the cover." |
| 14 | 12 | "The pump **is installed by** the technician." — **passive** | Rule 3.6 (passive voice) | "The technician installs the pump." |
| 15 | 13 | "Examine the **high pressure hydraulic oil filter**..." — **noun cluster** | Rule 2.1 (noun cluster over 3 words) | "Examine the filter for the hydraulic oil at high pressure for damage." |
| 16 | 14 | "Measure the **low pressure hydraulic fluid level**..." — **noun cluster** | Rule 2.1 (noun cluster over 3 words) | "Measure the level of the hydraulic fluid at low pressure in the tank." |

**Pass criteria:** The model identifies all 16 violations and corrects each. Final text: 0 errors, 0 warnings from ste_check.py. Any other change that introduces a new violation fails the test.
