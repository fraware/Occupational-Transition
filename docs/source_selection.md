# Source Selection

This repository supports two source policies:

## `latest_mode`

- Uses current rolling public releases where applicable.
- Best for monitoring and exploratory analysis.
- Tradeoff: reruns can drift as source vintages update.

## `freeze_mode`

- Uses pinned/comparability-safe behavior for strict replication and release.
- Best for publication snapshots, acceptance runs, and reproducibility.
- Tradeoff: may skip newest in-flight updates when they conflict with freeze constraints.

## How to set

### CLI

```bash
ot run --bundle full-replication --source-selection-mode freeze_mode
```

### Profile

Set in TOML profile:

```toml
[run]
source_selection_mode = "freeze_mode"
```

## Recommendation

- Use `latest_mode` during development.
- Use `freeze_mode` for final numbers, QA signoff, and release artifacts.
