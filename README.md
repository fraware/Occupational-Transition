# Occupational Transition

**Public data, AI, and US labor markets** — broad, search-friendly scope: reproducible analytics from **public** official sources, delivered as both a **Python library** (`occupational_transition`) and a **ticket-gated pipeline** that rebuilds tables, figures, and lineage metadata.

## Scope and positioning

1. **Public data, AI, and US labor markets** — official and public-use series (e.g. CPS, BTOS, JOLTS, OEWS, O*NET), not proprietary panels; written so economists, ML researchers, and search engines can find the topic quickly.
2. **US labor market measurement from public data** — emphasizes **measurement**: documented universes, weights, crosswalks, and QA—not hype about “AI effects”; causal claims remain your responsibility outside this stack.
3. **Reproducible US labor & AI indicators** — ticketed `build_*` / `qa_*` pairs, schema-checked outputs, and `intermediate/*_run_metadata.json` so indicators trace to inputs and a git commit or tag.
4. **Open data pipeline for AI and labor economics** — import the package for new work, rerun single tickets, or replicate the full stack; entry points are **[docs/README.md](docs/README.md)** and [docs/library/README.md](docs/library/README.md).

**Repository:** [github.com/fraware/Occupational-Transition](https://github.com/fraware/Occupational-Transition) (PyPI/install name: `occupational-transition`; import: `occupational_transition`).

The repository is meant to be **copied, cited, and extended**—not a one-off script dump.

## How to cite

**Software:** cite this repository and the **version** you used (`occupational_transition.__version__` or git tag). Machine-readable metadata is in [CITATION.cff](CITATION.cff). For papers, also record the **commit hash or results tag** next to any table reproduced from this pipeline ([docs/replication/project_maintenance.md#results-freeze-and-tagging](docs/replication/project_maintenance.md#results-freeze-and-tagging)).

```bibtex
@software{occupational_transition,
  title        = {Occupational Transition: Public-data extraction and paper pipeline for {AI} and {US} labor markets},
  author       = {{Occupational-Transition contributors}},
  year         = {2026},
  version      = {0.1.0},
  url          = {https://github.com/fraware/Occupational-Transition},
  license      = {MIT},
}
```

The `url` field matches [CITATION.cff](CITATION.cff).

---

## Highlights

| | |
|--|--|
| **Library** | `occupational_transition` — HTTP helpers, source clients (e.g. BTOS, JOLTS, O*NET), crosswalk loaders. Install with `pip install -e .`. |
| **Pipeline** | Ordered tickets `PR-000` → `T-020` (and extensions), each with `build_*` / `qa_*` scripts and `intermediate/*_run_metadata.json` lineage. |
| **Documentation** | Single hub: **[docs/README.md](docs/README.md)** (library, replication, methodology, figures, paper, policy, quality). |
| **Governance** | Schema-checked outputs, registry URLs in [docs/data_registry.csv](docs/data_registry.csv), acceptance matrix and replication runbooks under [docs/replication/](docs/replication/). |

---

## Choose your path

**A — Use the package**  
Install (below), read [docs/library/README.md](docs/library/README.md), run scripts under [examples/](examples/) ([examples/README.md](examples/README.md)). Optional CLI: `ot-fetch` (see `pyproject.toml` `[project.scripts]`).

**B — Run one ticket**  
Find your ticket in the [pipeline table](#research-pipeline-tickets), then run the listed `scripts/build_*.py` and `scripts/qa_*.py`. Methodology: [docs/methodology/README.md](docs/methodology/README.md) and [docs/methodology/tickets/](docs/methodology/tickets/).

**C — Replicate the full stack**  
From a clean clone, follow [docs/replication/README.md](docs/replication/README.md) and run `python scripts/run_full_pipeline_from_raw.py`. Expect large downloads and long runtimes.

---

## Install

Python **3.10+** (3.11+ recommended).

```bash
pip install -e .
```

Developers (tests + linter):

```bash
pip install -e ".[dev]"
pytest
```

`requirements.txt` mirrors the editable install so `pip install -r requirements.txt` stays aligned with `pyproject.toml`. Version: `occupational_transition.__version__` (semantic versioning for library API changes; pin a git tag for frozen paper builds).

---

## Documentation

All Markdown is organized by audience in **[docs/README.md](docs/README.md)**—start there for crosswalk notes, figure catalog, claim audit, briefing materials, and manuscript drafts.

Quick links: [crosswalk methodology](docs/methodology/pr000_crosswalk_methodology.md) · [data registry](docs/data_registry.csv) · [committed vs generated outputs](docs/replication/README.md#committed-outputs-vs-build-generated)

---

## Research pipeline (tickets)

Each row is the contract: build script, QA script, and primary artifacts under `figures/` and `intermediate/`.

| Ticket | Scripts (build / QA) | Primary outputs |
|--------|----------------------|-----------------|
| PR-000 | `build_crosswalks.py` / `qa_crosswalks.py` | `crosswalks/occ22_crosswalk.csv`, `crosswalks/sector6_crosswalk.csv`, `docs/data_registry.csv` |
| T-001 | `build_figure1_panelA.py` / `qa_figure1_panelA.py` | `figures/figure1_panelA_occ_baseline.csv`, `intermediate/figure1_panelA_occ_baseline_meta.csv`, `intermediate/figure1_panelA_run_metadata.json` |
| T-002 | `build_figure1_panelB.py` / `qa_figure1_panelB.py` | `figures/figure1_panelB_task_heatmap.csv`, `intermediate/ai_relevance_terciles.csv`, `intermediate/figure1_panelB_meta.csv`, `intermediate/figure1_panelB_run_metadata.json` |
| T-003 | `build_figure2_panelA.py` / `qa_figure2_panelA.py` | `figures/figure2_panelA_hours_by_ai_tercile.csv`, `intermediate/figure2_panelA_run_metadata.json` |
| T-004 | `build_figure2_panelB_counts.py` / `qa_figure2_panelB_counts.py` | `figures/figure2_panelB_transition_counts.csv`, `intermediate/figure2_panelB_counts_run_metadata.json` |
| T-005 | `build_figure2_panelB_probs.py` / `qa_figure2_panelB_probs.py` | `figures/figure2_panelB_transition_probs.csv`, `intermediate/figure2_panelB_probs_run_metadata.json` |
| T-006 | `build_figure3_panelA_btos_ai_trends.py` / `qa_figure3_panelA_btos_ai_trends.py` | `figures/figure3_panelA_btos_ai_trends.csv`, `intermediate/figure3_panelA_btos_ai_trends_run_metadata.json` |
| T-007 | `build_figure3_panelB_btos_workforce_effects.py` / `qa_figure3_panelB_btos_workforce_effects.py` | `figures/figure3_panelB_btos_workforce_effects.csv`, `intermediate/figure3_panelB_btos_workforce_effects_run_metadata.json` |
| T-008 | `build_figure4_panelA_jolts_sector_rates.py` / `qa_figure4_panelA_jolts_sector_rates.py` | `figures/figure4_panelA_jolts_sector_rates.csv`, `intermediate/figure4_panelA_jolts_sector_rates_run_metadata.json` |
| T-009 | `build_figure4_panelB_ces_sector_index.py` / `qa_figure4_panelB_ces_sector_index.py` | `figures/figure4_panelB_ces_sector_index.csv`, `intermediate/figure4_panelB_ces_sector_index_run_metadata.json` |
| T-010 | `build_figure5_capability_matrix.py` / `qa_figure5_capability_matrix.py` | `figures/figure5_capability_matrix.csv`, `intermediate/figure5_capability_matrix_run_metadata.json` |
| T-011 | `build_figureA1_asec_welfare_by_ai_tercile.py` / `qa_figureA1_asec_welfare_by_ai_tercile.py` | `figures/figureA1_asec_welfare_by_ai_tercile.csv`, `intermediate/figureA1_asec_welfare_by_ai_tercile_run_metadata.json` |
| T-012 | `build_figureA2_sipp_event_study.py` / `qa_figureA2_sipp_event_study.py` | `figures/figureA2_sipp_event_study.csv`, `intermediate/figureA2_sipp_event_study_run_metadata.json` |
| T-013 | `build_figureA3_cps_supp_validation.py` / `qa_figureA3_cps_supp_validation.py` | `figures/figureA3_cps_supp_validation.csv`, `intermediate/figureA3_cps_supp_validation_run_metadata.json` |
| T-014 | `build_figureA4_abs_structural_adoption.py` / `qa_figureA4_abs_structural_adoption.py` | `figures/figureA4_abs_structural_adoption.csv`, `intermediate/figureA4_abs_structural_adoption_run_metadata.json` |
| T-015 | `build_figureA5_ces_payroll_hours.py` / `qa_figureA5_ces_payroll_hours.py` | `figures/figureA5_ces_payroll_hours.csv`, `intermediate/figureA5_ces_payroll_hours_run_metadata.json` |
| T-016 | `build_figureA6_bed_churn.py` / `qa_figureA6_bed_churn.py` | `figures/figureA6_bed_churn.csv`, `intermediate/figureA6_bed_churn_run_metadata.json` |
| T-017 | `build_figureA7_qcew_state_benchmark.py` / `qa_figureA7_qcew_state_benchmark.py` | `figures/figureA7_qcew_state_benchmark.csv`, `intermediate/figureA7_qcew_state_benchmark_run_metadata.json` |
| T-018 | `build_figureA8_lehd_benchmark.py` / `qa_figureA8_lehd_benchmark.py` | `figures/figureA8_lehd_benchmark.csv`, `intermediate/figureA8_lehd_benchmark_run_metadata.json` |
| T-019 | `build_figureA9_acs_local_composition.py` / `qa_figureA9_acs_local_composition.py` | `figures/figureA9_acs_local_composition.csv`, `intermediate/figureA9_acs_local_composition_run_metadata.json` |
| T-020 | `build_figureA10_nls_longrun.py` / `qa_figureA10_nls_longrun.py` | `figures/figureA10_nls_longrun.csv`, `intermediate/figureA10_nls_longrun_run_metadata.json` |

Extension tickets **T-021–T-026** (AWES, ALPI, related intermediates) are documented in [docs/paper/methods_data.md](docs/paper/methods_data.md). Senator memo visuals (`t101`–`t108`) and Virginia pack outputs (`va01`–`va08`) are additional gates in strict acceptance.

---

## Full replication

End-to-end rebuild from the repo root (network required; **large disk and long runtime**—see [docs/replication/README.md](docs/replication/README.md)):

```bash
pip install -r requirements.txt
python scripts/run_full_pipeline_from_raw.py
```

Writes `intermediate/full_clean_rebuild_acceptance_<UTC>.md` and fails fast on the first failed build or QA step.

**Common flags:** `--with-audit-summary` (audit markdown from the log) · `--with-visuals` (runs `run_visuals_all.py` + `qa_visuals.py`) · `--skip-install` · `--source-selection-mode freeze_mode` · `--require-signoff`

**Typical iterative run** (strict ticket order + audit summary + policy gates):

```bash
pip install -r requirements.txt
python scripts/run_full_pipeline_from_raw.py --with-audit-summary
```

This also runs memo/brief build and QA, robustness, drift dashboard, and freeze manifest steps as configured.

**Targeted work:** single ticket = run that ticket’s `build_*.py` then `qa_*.py`. Acceptance only: `python scripts/run_full_clean_rebuild_acceptance.py`. Summarize an existing log: `python scripts/build_acceptance_audit_summary.py --log <path>`.

**PR-000 outputs:** `crosswalks/occ22_crosswalk.csv`, `crosswalks/sector6_crosswalk.csv`, `docs/data_registry.csv`.

---

## Quality bar (summary)

- JSON lineage under `intermediate/*run_metadata.json` for retained outputs; QA scripts enforce schemas, domains, and SHA-256 checks against cached inputs where applicable.
- Policy-facing KPI tables carry uncertainty fields and `evidence_directness` per project rules.
- Registry rows in `docs/data_registry.csv` use canonical HTTPS URLs and explicit provenance fields.

Details: [docs/README.md](docs/README.md) and [docs/replication/acceptance_matrix.md](docs/replication/acceptance_matrix.md).

---

## Known deviations from issue templates

- **T-006:** BTOS AI core rows for the national series first appear at `2023-09-11` (`PERIOD_ID 31`), not the template’s `2023-08-28`. See [t006 methodology](docs/methodology/tickets/t006_figure3_panelA_btos_ai_trends_methodology.md).
- **T-007:** Public `AI_Supplement_Table.xlsx` lacks item-25 option rows; Scope 2 proxy mappings apply to task-related keys while employment-effect rows stay published. See [t007 methodology](docs/methodology/tickets/t007_figure3_panelB_btos_workforce_effects_methodology.md).

---

## Figures and visuals

Render charts from committed `figures/*.csv`:

```bash
python scripts/run_visuals_all.py
python scripts/qa_visuals.py
```

Outputs: `visuals/png/`, `visuals/vector/`, `intermediate/visuals_run_manifest.json`. Style: [docs/quality/README.md#visual-style-guide](docs/quality/README.md#visual-style-guide). Caption coverage: `python scripts/qa_visual_caption_coverage.py`. One-shot: `python scripts/run_visuals_acceptance.py`.

**Senator memo and Virginia pack** (additive to main-text stems `t001`–`t020`):

```bash
python scripts/run_memo_visuals_build.py
python scripts/run_memo_visuals_qa.py
```

Precision rules: [docs/quality/README.md#memo-visuals-t-101-to-t-108-precision-and-non-invention-rules](docs/quality/README.md#memo-visuals-t-101-to-t-108-precision-and-non-invention-rules). Virginia: [docs/policy/briefing/virginia_deep_dive.md](docs/policy/briefing/virginia_deep_dive.md). Policy lane index: [docs/README.md](docs/README.md).

---

## Robustness and freeze

```bash
python scripts/run_robustness_all.py
python scripts/build_freeze_manifest.py
```

Robustness reports: `intermediate/robustness/`. Freeze manifest hashes figures, run metadata, and visuals manifest when present.

---

## Project and license

| | |
|--|--|
| **License** | [MIT](LICENSE) |
| **Changelog** | [CHANGELOG.md](CHANGELOG.md) |
| **Cite** | [CITATION.cff](CITATION.cff) |
| **Code of Conduct** | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| **Third-party assets** | [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) |
| **Contributing** | [CONTRIBUTING.md](CONTRIBUTING.md) |
| **Security** | [SECURITY.md](SECURITY.md) |
| **Git size** | [docs/replication/project_maintenance.md#git-history-size-and-hygiene](docs/replication/project_maintenance.md#git-history-size-and-hygiene) |

Full replication can require **many gigabytes** and **hours** of download and compute; committed `figures/` snapshots and [docs/replication/README.md#committed-outputs-vs-build-generated](docs/replication/README.md#committed-outputs-vs-build-generated) document what ships in git versus what builds locally.
