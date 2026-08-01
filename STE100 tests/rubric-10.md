# Rubric: test-10

**Target: 24 violations** (12 ERROR, 12 WARNING) — three of every violation kind. The paragraph is otherwise perfect STE. Note: the three -ing violation lines (10-12) each also carry a Rule 3.7 while-join warning, so the linter reports 12 errors, 15 warnings; the required correction splits the sentence and fixes both.

| # | Line | Offending text | Rule | Correction |
|---|------|----------------|------|------------|
| 1 | 22 | "**Swap** the cover into position." | Rule 1.1/1.6 (unapproved word) | "Interchange the cover into position." or "Put the cover into position." |
| 2 | 24 | "**Grab** the wrench with the right hand." | Rule 1.1/1.6 (unapproved word) | "Hold the wrench with the right hand." |
| 3 | 25 | "**Fix** the pump after the test." | Rule 1.1/1.6 (unapproved word) | "Repair the pump after the test." or "Install the pump after the test." |
| 4 | 1 | 27-word sentence (line 1) | Rule 4.1/8.7 (sentence over 25 words) | Split into short sentences. |
| 5 | 2 | 29-word sentence (line 2) | Rule 4.1/8.7 (sentence over 25 words) | Split into short sentences. |
| 6 | 3 | 29-word sentence (line 3) | Rule 4.1/8.7 (sentence over 25 words) | Split into short sentences. |
| 7 | 4 | "Close the valve; drain the fluid." — **semicolon** | Rule 8.1 (semicolon misuse) | "Close the valve. Drain the fluid." |
| 8 | 5 | "Remove the cover; pull out the element." — **semicolon** | Rule 8.1 (semicolon misuse) | "Remove the cover. Pull out the element." |
| 9 | 6 | "Put the new element in the filter; close the cover." — **semicolon** | Rule 8.1 (semicolon misuse) | "Put the new element in the filter. Close the cover." |
| 10 | 7 | "Use a tool, **e.g.** a wrench, ..." | GR-6 (Latin abbreviation) | "Use a tool, for example a wrench, ..." |
| 11 | 8 | "Use a clean cloth, **etc.** to clean the valve." | GR-6 (Latin abbreviation) | "Use a clean cloth to clean the valve." |
| 12 | 9 | "Examine the seal **i.e.** the gasket for damage." | GR-6 (Latin abbreviation) | "Examine the seal, that is the gasket, for damage." |
| 13 | 10 | "while **holding** the valve" - **-ing form** | Rule 3.5 (-ing form) + 3.7 (while-join) | "Hold the wrench with the left hand. Hold the valve." |
| 14 | 11 | "while **checking** the fluid level" - **-ing form** | Rule 3.5 (-ing form) + 3.7 (while-join) | "Examine the seal. Examine the fluid level." |
| 15 | 12 | "while **draining** the fluid" - **-ing form** | Rule 3.5 (-ing form) + 3.7 (while-join) | "Operate the pump. Drain the fluid from the tank." |
| 16 | 13 | "The operator **has completed** the repair." — **present perfect** | Rule 3.2/3.4 (complex verb tense) | "The operator completed the repair." |
| 17 | 14 | "The technicians **have installed** the new pump." — **present perfect** | Rule 3.2/3.4 (complex verb tense) | "The technicians installed the new pump." |
| 18 | 15 | "The fluid **has drained** from the tank." — **present perfect** | Rule 3.2/3.4 (complex verb tense) | "The fluid drained from the tank." |
| 19 | 16 | "The cover **is removed by** the operator." — **passive** | Rule 3.6 (passive voice) | "The operator removes the cover." |
| 20 | 17 | "The pump **is installed by** the technician." — **passive** | Rule 3.6 (passive voice) | "The technician installs the pump." |
| 21 | 18 | "The valve **is closed by** the operator." — **passive** | Rule 3.6 (passive voice) | "The operator closes the valve." |
| 22 | 19 | "Examine the **high pressure hydraulic oil filter**..." — **noun cluster** | Rule 2.1 (noun cluster over 3 words) | "Examine the filter for the hydraulic oil at high pressure for damage." |
| 23 | 20 | "Measure the **low pressure hydraulic fluid level**..." — **noun cluster** | Rule 2.1 (noun cluster over 3 words) | "Measure the level of the hydraulic fluid at low pressure in the tank." |
| 24 | 21 | "Examine the **primary system hydraulic oil filter**..." — **noun cluster** | Rule 2.1 (noun cluster over 3 words) | "Examine the filter for the hydraulic oil in the primary system for leaks." |

**Pass criteria:** The model identifies all 24 violations and corrects each. Final text: 0 errors, 0 warnings from ste_check.py. Any other change that introduces a new violation fails the test.