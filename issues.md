# GitHub Issues — AI and Work Public Data Paper


Save the reusable template as:


```text
.github/ISSUE_TEMPLATE/figure-task.md
```


## PR-000 — Shared setup and crosswalks


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[PR-000] Build shared setup and crosswalks"
labels: ["data", "infrastructure", "needs-triage"]
assignees: []
---


## Summary
Create the common infrastructure used by all figures. This task builds the 22-group occupation crosswalk, the fixed six-sector crosswalk, and the dataset registry with source and snapshot metadata.


## Figure / output
- Figure ID: `Shared setup`
- Output file(s):
  - [ ] `crosswalks/occ22_crosswalk.csv`
  - [ ] `crosswalks/sector6_crosswalk.csv`
  - [ ] `docs/data_registry.csv`


## Why this matters
Supports every main-text and appendix figure by freezing the common occupation and sector definitions and by recording source provenance.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `CPS occupation recode documentation`
- `2018 SOC major groups`
- `BTOS sectors`
- `JOLTS industries`
- `CES industries`
- `BED industries`
- `QCEW industries`


## Dependencies
- [ ] No dependency


## Fixed design choices
- Occupation grouping: `22 broad occupation groups`
- Sector grouping: `fixed six-sector set`
- Geography: `not applicable`
- Time window: `not applicable`
- Weighting / normalization: `not applicable`


## Task checklist
- [ ] Gather source occupation and industry coding schemes
- [ ] Store raw files in `raw/`
- [ ] Create `occ22_crosswalk.csv`
- [ ] Create `sector6_crosswalk.csv`
- [ ] Create `data_registry.csv`
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `crosswalks/occ22_crosswalk.csv` meets its acceptance criterion:
  - Every source occupation code used in the paper maps to exactly one paper-wide 22-group occupation.
- [ ] `crosswalks/sector6_crosswalk.csv` meets its acceptance criterion:
  - Every sector used in BTOS, JOLTS, CES, BED, and QCEW maps to exactly one fixed six-sector group.
- [ ] `docs/data_registry.csv` meets its acceptance criterion:
  - Every raw data file used in the project has a recorded source URL, release date, and snapshot/download date.


## QA checklist
- [ ] Grouping variables match frozen design
- [ ] No duplicated source codes in crosswalk outputs
- [ ] No unmapped source codes in crosswalk outputs
- [ ] Output is tidy and reproducible
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
This ticket must be completed before any figure-specific issue can move to QA.
```


## T-001 — Build Figure 1 Panel A occupational baseline


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-001] Build Figure 1 Panel A occupational baseline"
labels: ["data", "figure", "baseline"]
assignees: []
---


## Summary
Build the national occupational baseline used in Figure 1 Panel A. This task produces employment share and median annual wage for the frozen 22 occupation groups using the latest OEWS national occupation data.


## Figure / output
- Figure ID: `Figure 1 Panel A`
- Output file(s):
  - [ ] `figures/figure1_panelA_occ_baseline.csv`


## Why this matters
Supports Claim 1 and provides the occupation baseline that anchors the rest of the paper.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `OEWS national occupation employment and wage estimates`


## Dependencies
- [ ] Depends on: `PR-000`


## Fixed design choices
- Occupation grouping: `22 broad occupation groups`
- Sector grouping: `not applicable`
- Geography: `national only`
- Time window: `latest available OEWS year`
- Weighting / normalization: `employment share = occupation employment / total OEWS employment`


## Task checklist
- [ ] Download latest OEWS national occupation data
- [ ] Store raw files in `raw/`
- [ ] Map detailed occupations to the 22-group occupation crosswalk
- [ ] Compute occupation employment totals
- [ ] Compute occupation employment shares
- [ ] Attach median annual wage
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figure1_panelA_occ_baseline.csv` meets its acceptance criterion:
  - File contains exactly 22 rows, one per occupation group, with columns for `occupation_group`, `employment`, `employment_share`, and `median_annual_wage`; employment shares sum to 1 within rounding tolerance.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Grouping variable matches frozen design
- [ ] Weighting / normalization rule implemented
- [ ] No unexpected missing values in final output
- [ ] Output is tidy and reproducible
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
Use the frozen 22-group occupation crosswalk from `crosswalks/occ22_crosswalk.csv`.
```


## T-002 — Build Figure 1 Panel B task heatmap and AI index


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-002] Build Figure 1 Panel B task heatmap and AI index"
labels: ["data", "figure", "baseline"]
assignees: []
---


## Summary
Build the task-profile matrix and AI Task Index used in Figure 1 Panel B. This task aggregates the six frozen O*NET task dimensions to the 22 occupation groups using OEWS employment weights and assigns AI-relevance terciles.


## Figure / output
- Figure ID: `Figure 1 Panel B`
- Output file(s):
  - [ ] `figures/figure1_panelB_task_heatmap.csv`
  - [ ] `intermediate/ai_relevance_terciles.csv`


## Why this matters
Supports Claim 1 and defines the AI-relevance bins reused by Figures 2 and the appendix.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `O*NET latest release`
- `OEWS national occupation employment and wage estimates`


## Dependencies
- [ ] Depends on: `PR-000`
- [ ] Depends on: `T-001`


## Fixed design choices
- Occupation grouping: `22 broad occupation groups`
- Sector grouping: `not applicable`
- Geography: `national only`
- Time window: `latest available O*NET release and OEWS year`
- Weighting / normalization: `OEWS employment-weighted aggregation; task dimensions standardized as z-scores; terciles from AI Task Index`


## Task checklist
- [ ] Download latest O*NET data
- [ ] Store raw files in `raw/`
- [ ] Extract the six frozen task dimensions
- [ ] Merge O*NET to detailed occupations
- [ ] Aggregate to the 22-group occupation system using OEWS employment weights
- [ ] Standardize task dimensions
- [ ] Compute AI Task Index
- [ ] Assign high / middle / low AI-relevance terciles
- [ ] Export final tidy CSVs
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figure1_panelB_task_heatmap.csv` meets its acceptance criterion:
  - File contains exactly 22 rows and the six frozen task-dimension z-scores for each occupation group.
- [ ] `intermediate/ai_relevance_terciles.csv` meets its acceptance criterion:
  - File contains exactly 22 rows, one tercile assignment per occupation group, and every occupation group is assigned to exactly one tercile.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Grouping variable matches frozen design
- [ ] Weighting / normalization rule implemented
- [ ] No unexpected missing values in final outputs
- [ ] Output is tidy and reproducible
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
This ticket must complete before Figure 2 and any appendix figures using AI-relevance terciles.
```


## T-003 — Build Figure 2 Panel A worker hours by AI-relevance tercile


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-003] Build Figure 2 Panel A worker hours by AI-relevance tercile"
labels: ["data", "figure", "workers"]
assignees: []
---


## Summary
Build the monthly CPS series for usual weekly hours by AI-relevance tercile. This task constructs the worker-side intensive-margin outcome for Figure 2 Panel A.


## Figure / output
- Figure ID: `Figure 2 Panel A`
- Output file(s):
  - [ ] `figures/figure2_panelA_hours_by_ai_tercile.csv`


## Why this matters
Supports Claim 2 by showing worker-side labor-market outcomes for high-, middle-, and low-AI-relevance occupations.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `Monthly CPS public-use files, January 2019 to latest available`


## Dependencies
- [ ] Depends on: `PR-000`
- [ ] Depends on: `T-002`


## Fixed design choices
- Occupation grouping: `CPS PRDTOCC1 mapped to 22 broad occupation groups`
- Sector grouping: `not applicable`
- Geography: `national only`
- Time window: `January 2019 to latest available month`
- Weighting / normalization: `PWCMPWGT / 10,000; employed civilian noninstitutional population age 16+; outcome = mean usual weekly hours`


## Task checklist
- [ ] Download monthly CPS public-use files
- [ ] Store raw files in `raw/`
- [ ] Restrict to civilian noninstitutional persons age 16+
- [ ] Keep employed respondents with valid occupation and usual-hours data
- [ ] Map occupations to AI-relevance terciles
- [ ] Compute weighted mean usual weekly hours by month and tercile
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figure2_panelA_hours_by_ai_tercile.csv` meets its acceptance criterion:
  - File contains one row per month × tercile with weighted mean usual weekly hours and no missing tercile-month combinations after the chosen start date.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Grouping variable matches frozen design
- [ ] Weighting / normalization rule implemented
- [ ] No unexpected missing values in final output
- [ ] Output is tidy and reproducible
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
Use the frozen AI terciles from `intermediate/ai_relevance_terciles.csv`.
```


## T-004 — Build Figure 2 Panel B transition counts


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-004] Build Figure 2 Panel B transition counts"
labels: ["data", "figure", "workers"]
assignees: []
---


## Summary
Build raw matched-month CPS transition counts across occupation groups, unemployment, and nonparticipation. This task creates the count backbone for Figure 2 Panel B.


## Figure / output
- Figure ID: `Figure 2 Panel B`
- Output file(s):
  - [ ] `figures/figure2_panelB_transition_counts.csv`


## Why this matters
Supports Claim 2 by constructing broad occupational and labor-force-state transitions from public worker-side data.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `Monthly CPS public-use files, January 2019 to latest available`


## Dependencies
- [ ] Depends on: `PR-000`
- [ ] Depends on: `T-002`


## Fixed design choices
- Occupation grouping: `22 broad occupation groups from PRDTOCC1`
- Sector grouping: `not applicable`
- Geography: `national only`
- Time window: `January 2019 to latest available month`
- Weighting / normalization: `PWCMPWGT / 10,000; public identifiers HRHHID + HRHHID2 + PULINENO; state space = 22 occupations + unemployed + NILF`


## Task checklist
- [ ] Download monthly CPS public-use files
- [ ] Store raw files in `raw/`
- [ ] Match adjacent months using public identifiers
- [ ] Define origin and destination states
- [ ] Compute weighted transition counts by month
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figure2_panelB_transition_counts.csv` meets its acceptance criterion:
  - File contains one row per origin × destination × month pair, and every origin state has positive total weighted mass for months retained in the analysis.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Grouping variable matches frozen design
- [ ] Weighting / normalization rule implemented
- [ ] Matching logic documented and reproducible
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
Do not row-normalize in this ticket; that happens in T-005.
```


## T-005 — Build Figure 2 Panel B transition probabilities


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-005] Build Figure 2 Panel B transition probabilities"
labels: ["data", "figure", "workers"]
assignees: []
---


## Summary
Convert matched CPS transition counts into row-normalized probabilities for Figure 2 Panel B. This task creates the transition heatmap-ready output and summary transition metrics.


## Figure / output
- Figure ID: `Figure 2 Panel B`
- Output file(s):
  - [ ] `figures/figure2_panelB_transition_probs.csv`


## Why this matters
Supports Claim 2 by turning public worker transition counts into interpretable transition probabilities.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `figure2_panelB_transition_counts.csv`


## Dependencies
- [ ] Depends on: `T-004`


## Fixed design choices
- Occupation grouping: `22 broad occupation groups`
- Sector grouping: `not applicable`
- Geography: `national only`
- Time window: `January 2019 to latest available month`
- Weighting / normalization: `row-normalized probabilities by origin state and month`


## Task checklist
- [ ] Load transition counts
- [ ] Row-normalize by origin state and month
- [ ] Create summary measures for retention, occupation switching, unemployment entry, and NILF entry
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figure2_panelB_transition_probs.csv` meets its acceptance criterion:
  - For every month × origin state, destination probabilities sum to 1 within numerical tolerance.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Grouping variable matches frozen design
- [ ] Row-normalization rule implemented
- [ ] No unexpected missing values in final output
- [ ] Output is tidy and reproducible
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
Keep both the full matrix and summary measures in the same tidy output if practical.
```


## T-006 — Build Figure 3 Panel A BTOS AI-use trends


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-006] Build Figure 3 Panel A BTOS AI-use trends"
labels: ["data", "figure", "firms"]
assignees: []
---


## Summary
Build national BTOS trends for current and expected AI use. This task creates the core business-side AI adoption time series for Figure 3 Panel A.


## Figure / output
- Figure ID: `Figure 3 Panel A`
- Output file(s):
  - [ ] `figures/figure3_panelA_btos_ai_trends.csv`


## Why this matters
Supports Claim 3 by providing direct public business-side AI adoption measures.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `BTOS core AI question outputs`


## Dependencies
- [ ] Depends on: `PR-000`


## Fixed design choices
- Occupation grouping: `not applicable`
- Sector grouping: `not applicable in main figure`
- Geography: `national only`
- Time window: `August 28, 2023 to latest available BTOS AI-core collection`
- Weighting / normalization: `use published BTOS firm-weighted shares`


## Task checklist
- [ ] Download BTOS core AI outputs
- [ ] Store raw files in `raw/`
- [ ] Extract current AI use rate
- [ ] Extract expected next-6-month AI use rate
- [ ] Build time series by collection period
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figure3_panelA_btos_ai_trends.csv` meets its acceptance criterion:
  - File contains one row per BTOS collection period with columns for date, current AI use rate, and expected AI use rate, all as published weighted shares.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Question definitions are consistent across the retained waves
- [ ] Published weighted shares used without incompatible recomputation
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
Keep the figure national in the main text; state detail belongs in the appendix only if needed.
```


## T-007 — Build Figure 3 Panel B BTOS workforce effects


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-007] Build Figure 3 Panel B BTOS workforce effects"
labels: ["data", "figure", "firms"]
assignees: []
---


## Summary
Build national BTOS supplement shares for the frozen workforce-effect categories. This task creates the direct public evidence on augmentation, substitution, and reported employment effects for Figure 3 Panel B.


## Figure / output
- Figure ID: `Figure 3 Panel B`
- Output file(s):
  - [ ] `figures/figure3_panelB_btos_workforce_effects.csv`


## Why this matters
Supports Claim 3 by measuring what AI-using businesses publicly report AI is doing to tasks and employment.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `BTOS AI supplement outputs`


## Dependencies
- [ ] Depends on: `PR-000`


## Fixed design choices
- Occupation grouping: `not applicable`
- Sector grouping: `not applicable in main figure`
- Geography: `national only`
- Time window: `pooled supplement window: December 4, 2023 through February 25, 2024`
- Weighting / normalization: `use published BTOS weighted shares for the supplement universe`


## Task checklist
- [ ] Download BTOS AI supplement outputs
- [ ] Store raw files in `raw/`
- [ ] Extract the six frozen workforce-effect categories
- [ ] Pool over the frozen supplement window
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figure3_panelB_btos_workforce_effects.csv` meets its acceptance criterion:
  - File contains exactly the six frozen categories, each as a published weighted share from the supplement universe.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Correct respondent universe used
- [ ] Published weighted shares used without incompatible recomputation
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
Do not expand this figure with sector or state cuts in the main text.
```


## T-008 — Build Figure 4 Panel A JOLTS sector rates


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-008] Build Figure 4 Panel A JOLTS sector rates"
labels: ["data", "figure", "demand"]
assignees: []
---


## Summary
Build monthly JOLTS openings, hires, quits, and layoffs/discharges rates for the frozen six sectors. This task creates the core labor-demand and turnover series for Figure 4 Panel A.


## Figure / output
- Figure ID: `Figure 4 Panel A`
- Output file(s):
  - [ ] `figures/figure4_panelA_jolts_sector_rates.csv`


## Why this matters
Supports Claim 4 by providing public labor-demand and turnover measures in AI-relevant sectors.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `JOLTS monthly industry series, seasonally adjusted`


## Dependencies
- [ ] Depends on: `PR-000`


## Fixed design choices
- Occupation grouping: `not applicable`
- Sector grouping: `fixed six-sector set`
- Geography: `national only`
- Time window: `January 2019 to latest available month`
- Weighting / normalization: `use published seasonally adjusted JOLTS rates`


## Task checklist
- [ ] Download JOLTS monthly industry series
- [ ] Store raw files in `raw/`
- [ ] Map industries to the fixed six-sector set
- [ ] Keep job openings, hires, quits, and layoffs/discharges rates
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figure4_panelA_jolts_sector_rates.csv` meets its acceptance criterion:
  - File contains one row per month × sector × rate, and all retained rates are seasonally adjusted published series.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Sector mapping matches frozen design
- [ ] Only published seasonally adjusted rates retained
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
Do not add occupation detail; that is explicitly outside what the public JOLTS core can support.
```


## T-009 — Build Figure 4 Panel B CES payroll employment index


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-009] Build Figure 4 Panel B CES payroll employment index"
labels: ["data", "figure", "demand"]
assignees: []
---


## Summary
Build CES payroll employment indexes aligned to the BTOS AI-monitoring window. This task creates the contextual payroll-employment panel for Figure 4 Panel B.


## Figure / output
- Figure ID: `Figure 4 Panel B`
- Output file(s):
  - [ ] `figures/figure4_panelB_ces_sector_index.csv`


## Why this matters
Supports Claim 4 by showing whether labor-demand and turnover shifts occur alongside broader payroll-employment changes.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `CES monthly industry employment series`


## Dependencies
- [ ] Depends on: `PR-000`


## Fixed design choices
- Occupation grouping: `not applicable`
- Sector grouping: `fixed six-sector set`
- Geography: `national only`
- Time window: `January 2019 to latest available month`
- Weighting / normalization: `index sector employment to August 2023 = 100`


## Task checklist
- [ ] Download CES monthly industry series
- [ ] Store raw files in `raw/`
- [ ] Map industries to the fixed six-sector set
- [ ] Build payroll employment index with August 2023 = 100
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figure4_panelB_ces_sector_index.csv` meets its acceptance criterion:
  - File contains one row per month × sector and every sector equals 100 in August 2023.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Sector mapping matches frozen design
- [ ] Index base month correctly applied
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
This is context only; keep the main demand-flow result centered on JOLTS.
```


## T-010 — Build Figure 5 capability matrix


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-010] Build Figure 5 capability matrix"
labels: ["data", "figure", "synthesis"]
assignees: []
---


## Summary
Build the condensed capability matrix for the five core datasets and seven fixed empirical objects. This is the paper's synthesis figure and should summarize the architecture without introducing new evidence.


## Figure / output
- Figure ID: `Figure 5`
- Output file(s):
  - [ ] `figures/figure5_capability_matrix.csv`


## Why this matters
Supports Claim 5 by making the public-data identification frontier explicit.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `CPS`
- `BTOS`
- `JOLTS`
- `OEWS`
- `O*NET`


## Dependencies
- [ ] Depends on: `T-001`
- [ ] Depends on: `T-002`
- [ ] Depends on: `T-003`
- [ ] Depends on: `T-006`
- [ ] Depends on: `T-008`


## Fixed design choices
- Occupation grouping: `not applicable`
- Sector grouping: `not applicable`
- Geography: `not applicable`
- Time window: `not applicable`
- Weighting / normalization: `categorical coding only: direct / partial / none`


## Task checklist
- [ ] Create rows for the five core datasets
- [ ] Create columns for the seven frozen empirical objects
- [ ] Populate cells using the locked direct / partial / none rules
- [ ] Add legend key
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figure5_capability_matrix.csv` meets its acceptance criterion:
  - File contains exactly 5 dataset rows × 7 empirical-object columns plus a legend key, with no extra datasets or empirical objects.


## QA checklist
- [ ] Matrix structure matches frozen design
- [ ] No extra datasets or columns added
- [ ] Cell coding follows locked rules only
- [ ] Output is tidy and reproducible
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
This figure is not an empirical result and should not be expanded.
```


## T-011 — Build Figure A1 annual welfare and income context


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-011] Build Figure A1 annual welfare and income context"
labels: ["data", "appendix", "workers"]
assignees: []
---


## Summary
Build annual worker welfare outcomes by AI-relevance tercile from CPS ASEC. This appendix figure deepens Figure 2 by adding annual income and poverty context.


## Figure / output
- Figure ID: `Figure A1`
- Output file(s):
  - [ ] `figures/figureA1_asec_welfare_by_ai_tercile.csv`


## Why this matters
Subordinate extension of Figure 2 for annual welfare and income context.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `CPS ASEC public-use files, 2019 to latest available`


## Dependencies
- [ ] Depends on: `PR-000`
- [ ] Depends on: `T-002`


## Fixed design choices
- Occupation grouping: `22 broad occupation groups, then AI terciles`
- Sector grouping: `not applicable`
- Geography: `national only`
- Time window: `2019 to latest available ASEC`
- Weighting / normalization: `use ASEC person weight; annual outcomes only`


## Task checklist
- [ ] Download ASEC files
- [ ] Store raw files in `raw/`
- [ ] Map occupations to the 22-group system and AI terciles
- [ ] Compute annual income, poverty, weeks worked, and unemployment incidence
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figureA1_asec_welfare_by_ai_tercile.csv` meets its acceptance criterion:
  - File contains one row per year × AI tercile with weighted values for all frozen welfare outcomes.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Grouping variable matches frozen design
- [ ] ASEC weight rule implemented
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
Keep this figure explicitly subordinate to Figure 2.
```


## T-012 — Build Figure A2 medium-run adjustment


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-012] Build Figure A2 medium-run adjustment"
labels: ["data", "appendix", "workers"]
assignees: []
---


## Summary
Build event-time outcomes around occupational change or nonemployment transition using SIPP. This appendix figure adds medium-run adjustment paths beyond the matched-month CPS results in Figure 2.


## Figure / output
- Figure ID: `Figure A2`
- Output file(s):
  - [ ] `figures/figureA2_sipp_event_study.csv`


## Why this matters
Subordinate extension of Figure 2 for richer longitudinal worker adjustment.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `Selected SIPP panel(s) covering the post-2019 period`


## Dependencies
- [ ] Depends on: `PR-000`
- [ ] Depends on: `T-002`


## Fixed design choices
- Occupation grouping: `22 broad occupation groups, then AI terciles`
- Sector grouping: `not applicable`
- Geography: `national only`
- Time window: `latest SIPP panel(s) covering post-2019 period`
- Weighting / normalization: `use SIPP person longitudinal or monthly weight; event time centered on transition month`


## Task checklist
- [ ] Download SIPP panel data
- [ ] Store raw files in `raw/`
- [ ] Define transition event
- [ ] Map baseline occupations to AI terciles
- [ ] Compute event-time employment, income, and program participation outcomes
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figureA2_sipp_event_study.csv` meets its acceptance criterion:
  - File contains one row per event time × AI tercile with weighted means for the frozen outcomes.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Event definition documented and reproducible
- [ ] Weighting / normalization rule implemented
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
Keep the figure focused on medium-run adjustment, not a new main result.
```


## T-013 — Build Figure A3 displacement, tenure, and mobility validation


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-013] Build Figure A3 displacement, tenure, and mobility validation"
labels: ["data", "appendix", "workers"]
assignees: []
---


## Summary
Build CPS supplement validation measures for displacement, tenure, and mobility. This appendix figure validates the worker-transition story in Figure 2 with direct supplement questions where available.


## Figure / output
- Figure ID: `Figure A3`
- Output file(s):
  - [ ] `figures/figureA3_cps_supp_validation.csv`


## Why this matters
Subordinate extension of Figure 2 that uses dedicated CPS supplement content for validation.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `Latest relevant CPS displaced worker / tenure / occupational mobility supplement files`


## Dependencies
- [ ] Depends on: `PR-000`
- [ ] Depends on: `T-002`


## Fixed design choices
- Occupation grouping: `22 broad occupation groups or AI terciles`
- Sector grouping: `not applicable`
- Geography: `national only`
- Time window: `most recent relevant supplement cycle(s)`
- Weighting / normalization: `use supplement-specific person weights`


## Task checklist
- [ ] Download relevant CPS supplement files
- [ ] Store raw files in `raw/`
- [ ] Map occupations to the paper-wide grouping
- [ ] Compute displacement, tenure, and mobility measures
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figureA3_cps_supp_validation.csv` meets its acceptance criterion:
  - File contains one row per occupation group or AI tercile with the frozen supplement-based measures and the correct supplement weight applied.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Grouping variable matches frozen design
- [ ] Supplement-specific weights applied
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
Do not over-harmonize across supplement cycles beyond what the frozen design requires.
```


## T-014 — Build Figure A4 ABS structural heterogeneity


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-014] Build Figure A4 ABS structural heterogeneity"
labels: ["data", "appendix", "firms"]
assignees: []
---


## Summary
Build annual structural comparisons in firm AI or advanced-technology use using ABS. This appendix figure deepens Figure 3 with industry and firm-size heterogeneity.


## Figure / output
- Figure ID: `Figure A4`
- Output file(s):
  - [ ] `figures/figureA4_abs_structural_adoption.csv`


## Why this matters
Subordinate extension of Figure 3 for annual structural business-side heterogeneity.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `ABS technology / innovation tables with workforce-impact content`


## Dependencies
- [ ] Depends on: `PR-000`


## Fixed design choices
- Occupation grouping: `not applicable`
- Sector grouping: `industry and firm size only`
- Geography: `national only`
- Time window: `latest available ABS technology / innovation module`
- Weighting / normalization: `use published ABS weighted shares or tables`


## Task checklist
- [ ] Download ABS tables
- [ ] Store raw files in `raw/`
- [ ] Extract adoption and workforce-effect measures
- [ ] Keep industry and firm-size cuts only
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figureA4_abs_structural_adoption.csv` meets its acceptance criterion:
  - File contains one row per industry × firm-size group with the frozen ABS adoption and workforce-effect measures.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Grouping variables match frozen design
- [ ] Published ABS values retained without incompatible recomputation
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
This figure should complement BTOS, not duplicate the main-text adoption figure.
```


## T-015 — Build Figure A5 CES payroll and hours context


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-015] Build Figure A5 CES payroll and hours context"
labels: ["data", "appendix", "demand"]
assignees: []
---


## Summary
Build appendix payroll-employment and average weekly hours series for the fixed six sectors. This figure adds establishment/payroll context to Figure 4.


## Figure / output
- Figure ID: `Figure A5`
- Output file(s):
  - [ ] `figures/figureA5_ces_payroll_hours.csv`


## Why this matters
Subordinate extension of Figure 4 for payroll and hours context.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `CES monthly industry employment and average weekly hours series`


## Dependencies
- [ ] Depends on: `PR-000`


## Fixed design choices
- Occupation grouping: `not applicable`
- Sector grouping: `fixed six-sector set`
- Geography: `national only`
- Time window: `January 2019 to latest available month`
- Weighting / normalization: `index employment and hours to August 2023 = 100`


## Task checklist
- [ ] Download CES employment and hours series
- [ ] Store raw files in `raw/`
- [ ] Map industries to six-sector set
- [ ] Build employment and hours indexes
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figureA5_ces_payroll_hours.csv` meets its acceptance criterion:
  - File contains one row per month × sector with both indexed employment and indexed average weekly hours.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Sector mapping matches frozen design
- [ ] August 2023 base index correctly applied
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
This is context only and should not displace JOLTS as the core demand-flow result.
```


## T-016 — Build Figure A6 BED establishment churn


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-016] Build Figure A6 BED establishment churn"
labels: ["data", "appendix", "demand"]
assignees: []
---


## Summary
Build sector-level establishment churn context using BED. This appendix figure adds gross job gains/losses and openings/closings context to Figure 4.


## Figure / output
- Figure ID: `Figure A6`
- Output file(s):
  - [ ] `figures/figureA6_bed_churn.csv`


## Why this matters
Subordinate extension of Figure 4 for establishment-level churn context.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `BED quarterly series`


## Dependencies
- [ ] Depends on: `PR-000`


## Fixed design choices
- Occupation grouping: `not applicable`
- Sector grouping: `fixed six-sector set at the broadest BED-compatible level`
- Geography: `national only`
- Time window: `2019 to latest available quarter`
- Weighting / normalization: `use published BED rates where available`


## Task checklist
- [ ] Download BED quarterly series
- [ ] Store raw files in `raw/`
- [ ] Map industries to the six-sector set
- [ ] Extract gross job gains, gross job losses, openings, and closings
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figureA6_bed_churn.csv` meets its acceptance criterion:
  - File contains one row per quarter × sector with all frozen BED measures present.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Sector mapping matches frozen design
- [ ] Published measures retained consistently
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
Keep sector mappings broad enough to remain stable across the full time window.
```


## T-017 — Build Figure A7 QCEW state benchmark


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-017] Build Figure A7 QCEW state benchmark"
labels: ["data", "appendix", "context"]
assignees: []
---


## Summary
Build state-level sector employment shares and wages using QCEW. This appendix figure provides local industry-size and payroll benchmarks for the sectors discussed in Figures 3 and 4.


## Figure / output
- Figure ID: `Figure A7`
- Output file(s):
  - [ ] `figures/figureA7_qcew_state_benchmark.csv`


## Why this matters
Subordinate extension of Figure 4 for local denominator and wage benchmarking.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `QCEW state-sector employment and wage data`


## Dependencies
- [ ] Depends on: `PR-000`


## Fixed design choices
- Occupation grouping: `not applicable`
- Sector grouping: `fixed six-sector set`
- Geography: `state`
- Time window: `latest available annualized quarter or latest full year`
- Weighting / normalization: `employment share by state; keep published average weekly wage`


## Task checklist
- [ ] Download QCEW state-sector data
- [ ] Store raw files in `raw/`
- [ ] Map industries to the six-sector set
- [ ] Compute state-level employment shares
- [ ] Keep average weekly wage
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figureA7_qcew_state_benchmark.csv` meets its acceptance criterion:
  - File contains one row per state × sector with employment share and average weekly wage.


## QA checklist
- [ ] Geography matches frozen design
- [ ] Sector mapping matches frozen design
- [ ] Employment-share normalization documented
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
Do not turn this into a county-level figure unless explicitly approved later.
```


## T-018 — Build Figure A8 LEHD public benchmark


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-018] Build Figure A8 LEHD public benchmark"
labels: ["data", "appendix", "benchmark"]
assignees: []
---


## Summary
Build an aggregate linked-admin benchmark series from public LEHD products. This appendix figure adds an aggregate worker-employer dynamics benchmark without relying on restricted microdata.


## Figure / output
- Figure ID: `Figure A8`
- Output file(s):
  - [ ] `figures/figureA8_lehd_benchmark.csv`


## Why this matters
Subordinate extension of Figure 4 and the identification discussion by showing what public linked-admin products can add in aggregate.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `Public LEHD / J2J benchmark series`


## Dependencies
- [ ] Depends on: `PR-000`


## Fixed design choices
- Occupation grouping: `not applicable`
- Sector grouping: `aggregate national benchmark only unless a stable sector split is straightforward`
- Geography: `national only`
- Time window: `2019 to latest available quarter`
- Weighting / normalization: `use published aggregate rate directly`


## Task checklist
- [ ] Download chosen LEHD public benchmark series
- [ ] Store raw files in `raw/`
- [ ] Keep national aggregate
- [ ] Align series to quarterly format
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figureA8_lehd_benchmark.csv` meets its acceptance criterion:
  - File contains one row per quarter for the chosen benchmark rate with source metadata attached.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Public series used directly without implied microdata reconstruction
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
This figure must remain a benchmark, not a new empirical spine.
```


## T-019 — Build Figure A9 ACS local occupational composition


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-019] Build Figure A9 ACS local occupational composition"
labels: ["data", "appendix", "baseline"]
assignees: []
---


## Summary
Build local occupational composition measures for occupation groups and AI-relevance terciles using ACS PUMS. This appendix figure deepens Figure 1 by showing where AI-relevant occupations are concentrated geographically.


## Figure / output
- Figure ID: `Figure A9`
- Output file(s):
  - [ ] `figures/figureA9_acs_local_composition.csv`


## Why this matters
Subordinate extension of Figure 1 for local descriptive geography and worker composition.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `Latest ACS PUMS 1-year or 5-year file`


## Dependencies
- [ ] Depends on: `PR-000`
- [ ] Depends on: `T-002`


## Fixed design choices
- Occupation grouping: `22 broad occupation groups and AI terciles`
- Sector grouping: `not applicable`
- Geography: `PUMA`
- Time window: `latest available ACS PUMS file`
- Weighting / normalization: `use ACS person weight; weighted shares only`


## Task checklist
- [ ] Download ACS PUMS
- [ ] Store raw files in `raw/`
- [ ] Map occupations to the 22-group system and AI terciles
- [ ] Compute PUMA-level shares for occupation groups and terciles
- [ ] Compute selected demographic composition measures
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figureA9_acs_local_composition.csv` meets its acceptance criterion:
  - File contains one row per PUMA with weighted shares for the 22 groups and the three AI terciles.


## QA checklist
- [ ] Geography matches frozen design
- [ ] Grouping variable matches frozen design
- [ ] ACS person weight applied
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
Keep the figure descriptive only; do not use ACS as a transition engine.
```


## T-020 — Build Figure A10 long-run career adaptation


```md
---
name: Figure task
about: Build one figure output or supporting file for the AI-and-work public data paper
title: "[T-020] Build Figure A10 long-run career adaptation"
labels: ["data", "appendix", "long-run"]
assignees: []
---


## Summary
Build long-run occupation-switching, training, and earnings trajectories from NLS public-use data. This appendix figure extends the paper forward in time without creating a new empirical spine.


## Figure / output
- Figure ID: `Figure A10`
- Output file(s):
  - [ ] `figures/figureA10_nls_longrun.csv`


## Why this matters
Subordinate long-horizon extension of the worker-side story in Figure 2.


## Source data
- [ ] Source dataset identified
- [ ] Download URL(s) recorded in `docs/data_registry.csv`
- [ ] Release date recorded
- [ ] Snapshot/download date recorded


Datasets:
- `NLSY97 / selected NLS public-use cohort data`


## Dependencies
- [ ] Depends on: `PR-000`
- [ ] Depends on: `T-002`


## Fixed design choices
- Occupation grouping: `baseline occupation mapped to AI terciles`
- Sector grouping: `not applicable`
- Geography: `national only`
- Time window: `latest public-use rounds available`
- Weighting / normalization: `use round-appropriate public-use NLS weight`


## Task checklist
- [ ] Download chosen NLS public-use data
- [ ] Store raw files in `raw/`
- [ ] Define baseline occupation and AI tercile
- [ ] Compute longitudinal outcomes for occupation switching, earnings, and training
- [ ] Export final tidy CSV
- [ ] Add/update source note in `docs/`
- [ ] Run QA checks


## Acceptance criterion
- [ ] `figures/figureA10_nls_longrun.csv` meets its acceptance criterion:
  - File contains one row per survey round × baseline AI tercile with weighted longitudinal outcomes.


## QA checklist
- [ ] Time window matches frozen design
- [ ] Geography matches frozen design
- [ ] Baseline AI-tercile classification documented
- [ ] Round-appropriate public-use weight applied
- [ ] No unexpected missing values in final output
- [ ] Interpretation sentence added to metadata / notes


## Assignee
- Primary assignee: `@<github-handle>`
- Reviewer: `@<github-handle>`
- Backup / support: `@<github-handle>`


## Status
- [ ] Backlog
- [ ] Ready
- [ ] In progress
- [ ] Blocked
- [ ] QA
- [ ] Done


## Notes
Keep this figure interpretive and long-run; it should not compete with the main-text empirical spine.
```




