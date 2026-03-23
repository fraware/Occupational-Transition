# Figure 5 memo — Capability matrix

## Question

For the five core public datasets used in the paper, which empirical objects (worker outcomes, transitions, firm AI adoption, demand flows, occupational structure, task mechanism, local exposure) can public data support directly, partially, or not at all?

## Datasets

- None in the estimation sense; inputs are `issues.md` and `paper-notes.md` rules implemented in `scripts/build_figure5_capability_matrix.py`.

## Construction

T-010 writes a 5 x 7 categorical matrix (direct / partial / none) plus repeated legend columns for plotting. QA enforces shape and allowed symbols. Metadata records hashes of rule-source files.

## Main takeaway

The public system is strongest when sources are used for what they actually measure; the matrix makes identification boundaries explicit for policy and methods discussion.

## What the figure does not identify

- Any numerical treatment effect or empirical magnitude.
- Firm-worker causal links or AI-specific labor demand.

## Possible reviewer objections

- **Subjectivity of “partial”:** Cells follow locked symbols from `paper-notes.md`; changes require updating the rule text and rebuilding, not ad hoc edits to the CSV.
