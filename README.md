<div align="center">

<img src="docs/assets/logo.png" alt="Occupational Transition" width="280" />

# Occupational Transition

**Public Federal data, AI, and US labor markets** — one reproducible research stack.

[![Repository](https://img.shields.io/badge/GitHub-Occupational--Transition-24292f?style=flat-square&logo=github)](https://github.com/fraware/Occupational-Transition)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)

</div>

A Python package, a stepwise empirical pipeline, and auditable outputs for measurement work on AI and the US labor market. The goal is a stack you can **copy, cite, and extend** — not a one-off script dump.

---

## Contents

- [What you get](#what-you-get)
- [Data sources](#data-sources)
- [Why reuse this repo](#why-reuse-this-repo)
- [Scope](#scope)
- [Choose your path](#choose-your-path)
- [Install](#install)
- [Build outputs](#build-outputs)
- [Highlights](#highlights)
- [Documentation map](#documentation-map)
- [Research pipeline](#research-pipeline)
- [Full replication](#full-replication)
- [Figures and visuals](#figures-and-visuals)
- [Robustness and freeze](#robustness-and-freeze)
- [Quality bar](#quality-bar)
- [Data, licensing, and scope](#data-licensing-and-scope)
- [How to cite](#how-to-cite)
- [Contributing](#contributing)
- [Project and license](#project-and-license)

---

## What you get

| | |
|:---|:---|
| **Package** | [`occupational_transition`](docs/library/README.md) — pull and transform public labor-market data. |
| **Pipeline** | Reproducible builds that regenerate indicators and figures from source data. |
| **Lineage** | Outputs tied to code, inputs, and run settings for audit and replication. |

---

## Data sources

The stack is built from **public** official releases only: published downloads, documented APIs, and public-use microdata where tickets require them. There is **no proprietary or restricted-use** data requirement for the default pipeline.

**Authoritative detail**

| Artifact | What it contains |
|:---|:---|
| [docs/data_registry.csv](docs/data_registry.csv) | One row per registered asset: `dataset_id`, HTTPS URLs, `extractor`, `update_cadence`, and notes. Use with `ot catalog` / `ot fetch`. |
| [docs/paper/methods_data.md](docs/paper/methods_data.md) | Consolidated universes, weights, limits, and ticket-to-source mapping (Figures 1–6, appendix T-011–T-026, AWES/ALPI). |
| `ot list-sources` | Short program list and mode hints from the installed package. |

**Programs and surveys this repository accesses**

| Source | Role in this repo |
|:---|:---|
| **BLS — OEWS** (Occupational Employment and Wage Statistics) | National (and industry-by-occupation where used) employment and wage files; employment weights for occupation groups and AWES sector weights. |
| **BLS — JOLTS** (Job Openings and Labor Turnover Survey) | LABSTAT time-series files: openings, hires, quits, layoffs/discharges (and reference tables); sector-mapped rates and stress metrics. |
| **BLS — CES** (Current Employment Statistics) | Payroll employment and hours series (LABSTAT); sector payroll index and hours context (main text and appendix). |
| **BLS — BED** (Business Employment Dynamics) | Establishment churn and gross job gains/losses (LABSTAT); appendix benchmarks. |
| **BLS — QCEW** (Quarterly Census of Employment and Wages) | Industry title reference files; quarterly single-file ZIP extracts for state/industry benchmarks; optional Virginia deep-dive outputs. |
| **BLS — SOC** (Standard Occupational Classification) | Official SOC structure / coding reference (PDF) aligned with occupation handling in the crosswalks. |
| **BLS — NLS** (National Longitudinal Surveys) | **NLSY97** public-use microdata bundle (BLS-hosted release ZIP) for long-run outcome appendix figures. |
| **Census Bureau — CPS** (Current Population Survey) | **Basic monthly** public-use microdata for hours, mobility, and exit-risk series; **January supplement** published CSV where used for validation; methodology and occupation-code documentation (e.g. PDFs on www2.census.gov). |
| **Census Bureau — CPS ASEC** (Annual Social and Economic Supplement) | March **ASEC** public-use files for welfare and related appendix indicators by AI-relevance group. |
| **Census Bureau — BTOS** (Business Trends and Outlook Survey) | **BTOS API** (national and sector strata) for AI-use trends; **published supplement tables** (e.g. workforce-effect shares) from Census downloads. |
| **Census Bureau — ABS** (Annual Business Survey) | **Census API** (`abstcb` and related) plus published ABS automation/technology tables for structural adoption appendix work. |
| **Census Bureau — SIPP** (Survey of Income and Program Participation) | **Public-use person-month** datasets from www2.census.gov for event-study appendix panels. |
| **Census Bureau — ACS** (American Community Survey) | **PUMS** microdata for local PUMA-level composition appendix figures; **TP78** industry–occupation time-series tables for crosswalk inputs (PR-000). |
| **Census Bureau — LEHD** (Longitudinal Employer-Household Dynamics) | **Job-to-Job (J2J)** public release files (e.g. `lehd.ces.census.gov` J2J extracts) for public benchmark appendix series. |
| **O\*NET Resource Center** (USDOL-sponsored) | Versioned **O\*NET database** text releases; **Work Activities** and scale documentation; **O\*NET-SOC ↔ SOC** crosswalk files for task content and exposure measures. |

Crosswalks and internal sector groupings (e.g. `occ22`, `sector6`) combine these inputs with committed CSVs under `crosswalks/`; methodology: [docs/methodology/pr000_crosswalk_methodology.md](docs/methodology/pr000_crosswalk_methodology.md).

---

## Why reuse this repo

Many labor-and-AI projects force a tradeoff: quick scripts that are hard to trust later, or heavy pipelines that resist new questions. This repository aims for both:

- **Fast entry** — run targeted analyses without adopting the entire stack.
- **Strong reproducibility** — suitable for papers, public releases, and peer review.
- **Clear boundaries** — descriptive measurement is first-class; causal interpretation stays in your hands.

If you work in labor economics, applied macro, AI-and-work measurement, or policy analysis on public data, the layout should map cleanly to that workflow.

---

## Scope

1. **Public data, AI, and US labor markets** — Official and public-use series (CPS, BTOS, JOLTS, OEWS, O\*NET, and related sources), documented for economists, ML researchers, and discovery.
2. **Measurement-first** — Documented universes, weights, crosswalks, and QA; not hype about “AI effects.” Causal claims remain your responsibility outside this stack.
3. **Reproducible indicators** — `build_*` / `qa_*` pairs, schema-checked outputs, and `intermediate/*_run_metadata.json` tracing indicators to inputs and a git commit or tag.
4. **Open pipeline** — Import the package, rerun single steps, or replicate the full stack. Main entry points: **[docs/README.md](docs/README.md)** and [docs/library/README.md](docs/library/README.md).
5. **Optional state studies** — National / federal measurement is the default. State slices (e.g. Virginia, FIPS 51) live under **[docs/states/README.md](docs/states/README.md)** so they stay separate from the core paper path.

---

## Choose your path

### Browse the catalog, then fetch

| Resource | Link / command |
|:---|:---|
| Dataset registry | [docs/data_registry.csv](docs/data_registry.csv) — `dataset_id`, URLs, `extractor`, `update_cadence` |
| CLI | `ot catalog`, `ot fetch --dataset-id …`, `ot refresh --cadence rolling` |
| Scheduled local runs | [docs/operations/local_scheduling.md](docs/operations/local_scheduling.md) |

### A — Use the package in your own project

```bash
pip install -e .
```

| Next step | Where |
|:---|:---|
| Stable APIs and examples | [docs/library/README.md](docs/library/README.md) |
| Practical scripts | [examples/README.md](examples/README.md) |

**CLI (optional):** `ot catalog` / `ot fetch` / `ot refresh` · `ot list-analyses` (add `--verbose` to regenerate `docs/meta/analysis_bundles.yaml`) · `ot list-sources` · `ot run --bundle quick-start` · `ot run --profile config/profiles/quick-start.toml`

### B — Rebuild only what you need

| Next step | Where |
|:---|:---|
| Step-by-step mapping | [docs/methodology/README.md](docs/methodology/README.md) |
| Outputs and checks | [docs/replication/acceptance_matrix.md](docs/replication/acceptance_matrix.md) |
| Methodology support files | [docs/methodology/tickets/](docs/methodology/tickets/) |

Builds and QA run through `python -m occupational_transition.run_step build|qa <TICKET>` (thin `scripts/build_*.py` wrappers remain for ad hoc use). See the [research pipeline](#research-pipeline) table in the docs for step names.

### C — Fully replicate the published stack

From a clean clone:

```bash
pip install -r requirements.txt
pip install -e .
python scripts/run_full_pipeline_from_raw.py
```

| Topic | Where |
|:---|:---|
| Runtime, recovery, conventions | [docs/replication/README.md](docs/replication/README.md) |
| Orientation | [docs/start_here.md](docs/start_here.md) |
| Analysis catalog | [docs/analysis_catalog.md](docs/analysis_catalog.md) |
| Source selection | [docs/source_selection.md](docs/source_selection.md) |

Expect large downloads, disk usage, and long runtimes.

### D — State-level case study (optional)

Virginia QCEW and related outputs (outside the main paper figure list): **[docs/states/README.md](docs/states/README.md)** · **[docs/states/virginia/README.md](docs/states/virginia/README.md)**

---

## Install

Python **3.10+** is supported; **3.11+** is recommended.

**Application / library**

```bash
pip install -e .
```

**Developer** (tests and linter)

```bash
pip install -e ".[dev]"
pytest
```

`requirements.txt` mirrors the editable install so `pip install -r requirements.txt` stays aligned with `pyproject.toml`.

| Versioning | Notes |
|:---|:---|
| Package | `occupational_transition.__version__` |
| API | Semantic versioning for the library surface |
| Papers | Pin a git tag for frozen builds |

---

## Build outputs

- Descriptive indicators for AI relevance, labor outcomes, transitions, and sector trends.
- Reproducible figure tables under `figures/`.
- Run metadata under `intermediate/` for auditability.
- Optional static exports under `visuals/`.

This stack is **measurement-first**: clean, documented empirical inputs; identification design stays separate.

---

## Highlights

| Pillar | What it is |
|:---|:---|
| **Library** | `occupational_transition` — HTTP helpers, source clients (BTOS, JOLTS, O\*NET, etc.), crosswalk loaders. |
| **Pipeline** | Ordered build and QA with `intermediate/*_run_metadata.json` history. Details: [docs/replication/README.md](docs/replication/README.md), [docs/methodology/README.md](docs/methodology/README.md). |
| **Documentation** | Hub: **[docs/README.md](docs/README.md)** — library, replication, methodology, figures, paper, policy, quality. |
| **Governance** | Schema-checked outputs, registry in [docs/data_registry.csv](docs/data_registry.csv), acceptance matrix and runbooks under [docs/replication/](docs/replication/). |

---

## Documentation map

| Audience | Start here |
|:---|:---|
| Everyone | **[docs/README.md](docs/README.md)** |
| Library usage | [docs/library/README.md](docs/library/README.md) |
| Replication | [docs/replication/README.md](docs/replication/README.md) |
| Methodology | [docs/methodology/README.md](docs/methodology/README.md) |
| Paper artifacts | [docs/paper/README.md](docs/paper/README.md) |
| Figure structure | [docs/figures/README.md](docs/figures/README.md) |
| Claim discipline | [docs/policy/claim_audit.md](docs/policy/claim_audit.md) |

**Quick links:** [crosswalk methodology](docs/methodology/pr000_crosswalk_methodology.md) · [data registry](docs/data_registry.csv) · [committed vs generated](docs/replication/README.md#committed-outputs-vs-build-generated)

---

## Research pipeline

The full step list, script mapping, and output contracts are documented in:

- [docs/replication/README.md](docs/replication/README.md)
- [docs/replication/acceptance_matrix.md](docs/replication/acceptance_matrix.md)
- [docs/methodology/README.md](docs/methodology/README.md)

Targeted work is supported: run only the `build_*.py` and matching `qa_*.py` steps you need.

---

## Full replication

End-to-end rebuild from the repository root needs network access and may require **large disk space** and **long runtime**. Operational detail: [docs/replication/README.md](docs/replication/README.md).

```bash
pip install -r requirements.txt
python scripts/run_full_pipeline_from_raw.py
```

Writes `intermediate/full_clean_rebuild_acceptance_<UTC>.md`. The run fails fast on the first failed build or QA step.

**Common flags**

| Flag | Effect |
|:---|:---|
| `--with-audit-summary` | Audit markdown from the log |
| `--with-visuals` | Runs `run_visuals_all.py` and `qa_visuals.py` |
| `--skip-install` | Skip install step |
| `--source-selection-mode freeze_mode` | Freeze-mode source selection |
| `--require-signoff` | Require signoff gates |

**Typical iterative run** (strict step order, audit summary, policy gates as configured):

```bash
pip install -r requirements.txt
python scripts/run_full_pipeline_from_raw.py --with-audit-summary
```

**Partial rebuilds** — Run only the `build_*.py` and matching `qa_*.py` scripts you need; per-step mapping: [docs/methodology/README.md](docs/methodology/README.md).

---

## Figures and visuals

From committed `figures/*.csv` (main text Figures 1–6, appendix A1–A10, and monitoring stems per `scripts/run_visuals_all.py`):

```bash
python scripts/run_visuals_all.py
python scripts/qa_visuals.py
```

**Outputs:** `visuals/png/` · `visuals/vector/` · `intermediate/visuals_run_manifest.json`

Authoritative map (CSV paths, stems, captions, sources): [docs/figures/figure_catalog.md](docs/figures/figure_catalog.md). Main-text redesigns include composite artifacts (e.g. `figure2_redesigned_composite`, `figure3_redesigned_composite`, `figure4_redesigned_composite`) and **Figure 6** (`figures/figure6_policy_roadmap.csv` → stem `policy_roadmap`).

| Topic | Where |
|:---|:---|
| Style guide | [docs/quality/README.md#visual-style-guide](docs/quality/README.md#visual-style-guide) |
| Caption coverage (Figures 1–6) | `python scripts/qa_visual_caption_coverage.py` |
| One-shot acceptance | `python scripts/run_visuals_acceptance.py` |

---

## Robustness and freeze

```bash
python scripts/run_robustness_all.py
python scripts/build_freeze_manifest.py
```

Robustness reports: `intermediate/robustness/`. The freeze manifest hashes figures, run metadata, and the visuals manifest when present.

---

## Quality bar

- JSON lineage under `intermediate/*run_metadata.json` for retained outputs.
- QA enforces schemas, domains, and SHA-256 checks against cached inputs where applicable.
- Policy-facing KPI tables include uncertainty fields and `evidence_directness` per project rules.
- Registry rows in [docs/data_registry.csv](docs/data_registry.csv) use canonical HTTPS URLs and explicit provenance.

More: [docs/README.md](docs/README.md) · [docs/replication/acceptance_matrix.md](docs/replication/acceptance_matrix.md)

---

## Known deviations and data notes

Method-specific caveats live under [docs/methodology/](docs/methodology/), with summary gates in [docs/replication/acceptance_matrix.md](docs/replication/acceptance_matrix.md).

---

## Data, licensing, and scope

- Built around **public** and public-use sources; the full program-by-program list is in **[Data sources](#data-sources)** above.
- **License:** [MIT](LICENSE)
- **Third-party materials:** [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- **Security:** [SECURITY.md](SECURITY.md)

---

## How to cite

Cite the repository and the **version** you used.

- Package version: `occupational_transition.__version__`
- For papers, record the **commit hash or results tag** next to any table reproduced from this pipeline.
- Machine-readable metadata: [CITATION.cff](CITATION.cff)
- Freeze and tagging: [docs/replication/project_maintenance.md#results-freeze-and-tagging](docs/replication/project_maintenance.md#results-freeze-and-tagging)

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

## Contributing

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

Extensions to data coverage, indicators, and reproducibility checks are welcome.

---

## Project and license

| | |
|:---|:---|
| **License** | [MIT](LICENSE) |
| **Cite** | [CITATION.cff](CITATION.cff) |
| **Code of Conduct** | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| **Third-party assets** | [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) |
| **Contributing** | [CONTRIBUTING.md](CONTRIBUTING.md) |
| **Security** | [SECURITY.md](SECURITY.md) |
| **Git size / hygiene** | [docs/replication/project_maintenance.md#git-history-size-and-hygiene](docs/replication/project_maintenance.md#git-history-size-and-hygiene) |

Full replication can require **many gigabytes** and **hours** of download and compute. Committed `figures/` snapshots and [committed vs build-generated outputs](docs/replication/README.md#committed-outputs-vs-build-generated) document what ships in git versus what builds locally.
