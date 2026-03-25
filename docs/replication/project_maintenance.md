# Project maintenance

**Audience:** Maintainers auditing repository size, coordinating history rewrites, and cutting library or results freezes.

**Related:** [replication README](README.md), [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md), [CHANGELOG.md](../../CHANGELOG.md).

## Contents

- [Git history size and hygiene](#git-history-size-and-hygiene)
- [Results freeze and tagging](#results-freeze-and-tagging)

---

## Git history size and hygiene

### Observed state

`git count-objects -vH` on a typical checkout of this repository may report on the order of **several GiB** of object storage with a modest number of tracked files. That pattern usually indicates **large blobs present in the object database** (often under `raw/` or similar paths that were committed at some point, then removed from the index but not from history).

### Audit (run locally before a public push)

1. Install [git-sizer](https://github.com/github/git-sizer) or use built-in inspection:

   ```bash
   git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | sort -k3 -n -r | head -30
   ```

   On Windows PowerShell, use WSL or a short Python script to sort by the third column (size).

2. Identify paths associated with large blobs (often `git log --all --full-history -- <path>`).

### Remediation options

| Situation | Action |
|-----------|--------|
| Large file **still needed** in every clone | Prefer **Git LFS** for that path, or document an external data mirror and keep only small samples in git. |
| Large file was **committed by mistake** | Rewrite history with [`git filter-repo`](https://github.com/newren/git-filter-repo) (e.g. `--path` removal or `--strip-blobs-bigger-than N`) and coordinate a **force-push**; all forks/clones must re-clone or reset. |
| Loose objects only (no pack) | After cleanup, run `git gc --prune=now` and verify size again. |

### Prevention

- Keep [`.gitignore`](../../.gitignore) strict for `raw/` subtrees that hold multi-hundred-MiB downloads.
- Before `git add`, run `git status` and confirm no large binaries are staged.

This document does not replace legal review of what may be redistributed from third-party sources; see [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).

---

## Results freeze and tagging

Use this procedure once main-text figures, manuscript draft, and QA logs align for a paper milestone.

### Versioning for downstream users

- **Library releases** follow **semantic versioning** (`vMAJOR.MINOR.PATCH`, e.g. `v0.2.0`) when publishing the `occupational_transition` package API. See `occupational_transition.__version__` and [CHANGELOG.md](../../CHANGELOG.md) at the repo root.
- **Research freezes** often use **dated tags** `results-YYYY-MM-DD` (below). In papers, cite **both** the software version (or commit) and the **results tag** when numbers come from a frozen build.
- **Commit SHA:** Always valid for citing the exact file tree. Prefer an **annotated tag** when sharing with readers so the name is stable and human-meaningful.
- **Zenodo (optional):** After you enable the GitHub–Zenodo integration for this repository, each **GitHub Release** can mint a **DOI** for the archived tarball. Use that DOI in bibliographies when your publisher requires a persistent archive URL; the canonical code URL remains the git repository.

### Citation files

- Root [CITATION.cff](../../CITATION.cff) supplies machine-readable metadata (e.g. for GitHub’s “Cite this repository” and `cffconvert`).
- [README.md](../../README.md) includes a BibTeX block aligned with the same title and version.

### Preconditions

- `python scripts/run_full_pipeline_from_raw.py` completes with exit code 0.
- `docs/replication/acceptance_matrix.md` main-text gate shows PASS or PASS WITH NOTE only.
- `python scripts/run_visuals_all.py` and `python scripts/qa_visuals.py` complete if visuals are in scope.
- If senator memo visuals or Virginia brief outputs are in scope for the same milestone, `python scripts/run_memo_visuals_build.py` and `python scripts/run_memo_visuals_qa.py` complete (see [replication README](README.md#senator-memo-visuals-and-virginia-brief-pack-optional-additive)).
- `docs/policy/claim_audit.md` reviewed for partial-support items (including senator brief claim ledger rows when Virginia briefing is published).
- Drift checks pass with no critical alerts: `python scripts/build_drift_dashboard.py` and `python scripts/qa_drift_dashboard.py`.

#### Full freeze vs bounded validation

- **Full results freeze (recommended for tags):** use a complete `PR-000` through `T-020` acceptance run and full visuals run.
- **Bounded validation (faster, not a freeze):** allowed for drift checks if long appendix tickets are intentionally skipped, but must include an explicit scope note and cannot be tagged as a full freeze milestone.

### Tag name

Recommended pattern: `results-YYYY-MM-DD` (example: `results-2026-03-23`).

### What the tag should point to

- All committed `scripts/`, `crosswalks/`, `docs/` (including methodology and `data_registry.csv`).
- `requirements.txt`.
- Optional: generated logs under `intermediate/` if your workflow commits them; otherwise archive logs alongside the paper artifact.
- For full freezes, include the acceptance/visual evidence files for the same run window (or archive them with the tag metadata).

Large `raw/` caches are often excluded from git; the tag still applies to the **code and registry** that reproduce downloads. Document local cache expectations in [replication README](README.md).

### Manifest (optional but recommended)

Generate a file manifest with SHA-256 hashes:

```bash
python scripts/build_freeze_manifest.py
```

This writes `intermediate/freeze_manifest.json` listing hashes for `figures/*.csv`, key `intermediate/*run_metadata.json` files, and `intermediate/visuals_run_manifest.json` when present.
When available, the manifest also includes `intermediate/drift/drift_dashboard_run_metadata.json`.

### Git commands (illustrative)

```bash
git add -A
git status
git commit -m "Results freeze: align figures, manuscript, QA logs"
git tag -a results-YYYY-MM-DD -m "Frozen research state for public-data AI labor paper"
```

Do not rewrite tags once shared; create a new dated tag for subsequent freezes.
