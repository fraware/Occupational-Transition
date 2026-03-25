# Figure 5 memo — Capability matrix

## Question

For the five core public datasets used in the paper, which empirical objects (worker outcomes, transitions, firm AI adoption, demand flows, occupational structure, task mechanism, and worker-firm AI linkage) are supported directly, partially, or not at all?

## Datasets

- None in the estimation sense; inputs are `docs/lineage/t010_issues.md` and `docs/lineage/t010_paper_notes_matrix.md` rules implemented in `scripts/build_figure5_capability_matrix.py`.

## Construction

T-010 writes a 5-by-7 categorical matrix (direct / partial / none) plus repeated legend columns for plotting. QA enforces shape and allowed symbols. Metadata records hashes of rule-source files.

## Main takeaway

The public system is strongest when sources are used for what they measure directly. The matrix makes identification boundaries explicit for policy and methods discussion.

## How to read quickly

- Read across a dataset row to see which empirical objects that source can and cannot support.
- Read down a measurement-object column to identify where the public stack is strongest versus weakest.
- Interpret `partial` as proxy or incomplete support, not full direct observation.
- Separate the empirical diagnosis (missing integrated worker-firm AI linkage) from policy recommendations about survey design.

## What the figure does not identify

- Any numerical treatment effect, elasticity, or point estimate.
- Causal mechanisms linking worker outcomes to firm AI adoption.
- Evidence that directly resolves the missing public worker-firm AI linkage.

## Possible reviewer objections

- **Subjectivity of “partial”:** Cells follow locked symbols from `docs/lineage/t010_paper_notes_matrix.md`; changes require updating the rule text and rebuilding, not ad hoc edits to the CSV.
