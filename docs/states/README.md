# State-level case studies

This repository is **federal and national first**: the paper pipeline, main figures, and default documentation describe **US-wide** measurement from public data (CPS, BTOS, JOLTS, QCEW state benchmark for cross-state comparison, and so on).

**State-level slices** are optional **case studies**. They reuse the same frozen crosswalks and build discipline as the national stack but surface one state’s profile, ranks, and peer tables for briefing or extension work. They are **descriptive** and **not** causal AI treatment effects.

## Available case studies

| State | FIPS | Index |
|-------|------|--------|
| Virginia | 51 | [states/virginia/README.md](virginia/README.md) |

## Relationship to the core pipeline

- National QCEW state benchmark (**T-017**) produces `figures/figureA7_qcew_state_benchmark.csv` for all retained states.
- A state deep dive selects one FIPS code from that file and writes state-namespaced CSVs and metadata; see each case study README for exact outputs and commands.
- Optional state memo charts (Virginia) are written under `docs/states/virginia/visuals/` so they stay separate from repository-root `visuals/` used for the federal paper pack.

## Policy and sensitive packs

Legislative or staff-facing narrative may live under `docs/policy/briefing/` in some workflows; those paths are often **local-only** (see repository `.gitignore`). Tracked methodology for Virginia lives under [states/virginia/](virginia/).

Cross-cutting claim discipline for the paper and referenced evidence: [policy/claim_audit.md](../policy/claim_audit.md).
