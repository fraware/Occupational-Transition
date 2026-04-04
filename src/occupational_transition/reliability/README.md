# Reliability helpers

Small, shared utilities for policy-facing tables: load thresholds from the repo config, attach basic uncertainty fields (SE and CI from CV), evaluate publishability flags, and align DataFrames to the canonical reliability column set.

## Configuration

Default thresholds path: `config/reliability_thresholds.json` (resolved via `occupational_transition.paths.repo_root`). Pass an explicit `Path` to `load_thresholds` when needed.

## Public API

Import from `occupational_transition.reliability`:

| Symbol | Role |
|--------|------|
| `load_thresholds` | Load JSON thresholds (weighted_n, effective_n, CV limits, CI level). |
| `add_basic_uncertainty_fields` | Derive `se`, `ci_lower`, `ci_upper`, `ci_level`, `variance_method` from a value column and CV. |
| `evaluate_publishability` | Set `publish_flag`, `suppression_reason`, `reliability_tier`, etc. |
| `ensure_reliability_columns` | Add missing columns from `RELIABILITY_COLUMNS` as NaN. |
| `RELIABILITY_COLUMNS` | Ordered list of canonical column names. |

## Documentation

Human-facing policy and interpretation: `docs/quality/README.md` (reliability framework section).
