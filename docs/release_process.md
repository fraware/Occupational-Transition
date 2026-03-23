# Results freeze and tagging

Use this procedure once main-text figures, manuscript draft, and QA logs align for a paper milestone.

## Preconditions

- `python scripts/run_full_pipeline_from_raw.py` completes with exit code 0.
- `docs/acceptance_matrix.md` main-text gate shows PASS or PASS WITH NOTE only.
- `python scripts/run_visuals_all.py` and `python scripts/qa_visuals.py` complete if visuals are in scope.
- `docs/claim_audit.md` reviewed for partial-support items.

## Tag name

Recommended pattern: `results-YYYY-MM-DD` (example: `results-2026-03-23`).

## What the tag should point to

- All committed `scripts/`, `crosswalks/`, `docs/` (including methodology and `data_registry.csv`).
- `requirements.txt`.
- Optional: generated logs under `intermediate/` if your workflow commits them; otherwise archive logs alongside the paper artifact.

Large `raw/` caches are often excluded from git; the tag still applies to the **code and registry** that reproduce downloads. Document local cache expectations in `docs/replication.md`.

## Manifest (optional but recommended)

Generate a file manifest with SHA-256 hashes:

```bash
python scripts/build_freeze_manifest.py
```

This writes `intermediate/freeze_manifest.json` listing hashes for `figures/*.csv`, key `intermediate/*run_metadata.json` files, and `intermediate/visuals_run_manifest.json` when present.

## Git commands (illustrative)

```bash
git add -A
git status
git commit -m "Results freeze: align figures, manuscript, QA logs"
git tag -a results-YYYY-MM-DD -m "Frozen research state for public-data AI labor paper"
```

Do not rewrite tags once shared; create a new dated tag for subsequent freezes.
