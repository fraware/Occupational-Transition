# Git history size and hygiene

## Observed state

`git count-objects -vH` on a typical checkout of this repository may report on the order of **several GiB** of object storage with a modest number of tracked files. That pattern usually indicates **large blobs present in the object database** (often under `raw/` or similar paths that were committed at some point, then removed from the index but not from history).

## Audit (run locally before a public push)

1. Install [git-sizer](https://github.com/github/git-sizer) or use built-in inspection:

   ```bash
   git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | sort -k3 -n -r | head -30
   ```

   On Windows PowerShell, use WSL or a short Python script to sort by the third column (size).

2. Identify paths associated with large blobs (often `git log --all --full-history -- <path>`).

## Remediation options

| Situation | Action |
|-----------|--------|
| Large file **still needed** in every clone | Prefer **Git LFS** for that path, or document an external data mirror and keep only small samples in git. |
| Large file was **committed by mistake** | Rewrite history with [`git filter-repo`](https://github.com/newren/git-filter-repo) (e.g. `--path` removal or `--strip-blobs-bigger-than N`) and coordinate a **force-push**; all forks/clones must re-clone or reset. |
| Loose objects only (no pack) | After cleanup, run `git gc --prune=now` and verify size again. |

## Prevention

- Keep [`.gitignore`](../.gitignore) strict for `raw/` subtrees that hold multi-hundred-MiB downloads.
- Before `git add`, run `git status` and confirm no large binaries are staged.

This document does not replace legal review of what may be redistributed from third-party sources; see [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).
