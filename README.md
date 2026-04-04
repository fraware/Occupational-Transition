# Occupational Transition

<p align="center">
  <img src="docs/assets/logo.png" alt="Occupational Transition logo" width="320" />
</p>

**Public data, AI, and US labor markets** in one reproducible research stack.

This repository combines a reusable Python package, a step-by-step empirical pipeline, and auditable research outputs for work on AI and the US labor market.

Repository: [github.com/fraware/Occupational-Transition](https://github.com/fraware/Occupational-Transition)

---

## What this repository gives you

- A Python package (`occupational_transition`) for pulling and transforming public labor-market data.
- A reproducible build workflow that regenerates published indicators and figures from source data.
- Auditable outputs and metadata so you can trace results to code, inputs, and run settings.

This is designed to be **copied, cited, and extended**, not treated as a one-off script dump.

---

## Why this repo is worth reusing

Most labor/AI projects force you to choose between:

- Fast, one-off analysis scripts that are hard to trust later, or
- Heavy pipelines that are difficult to adapt for new research questions.

This repository is built to give you both:

- **Fast entry** for researchers who want to run targeted analyses now.
- **Strong reproducibility** for papers, public releases, and peer review.
- **Clear boundaries** between descriptive measurement and causal interpretation.

If you work in labor economics, applied macro, AI-and-work measurement, or policy analysis with public data, this stack is designed for your workflow.

---

## Scope and positioning

1. **Public data, AI, and US labor markets**  
   Official and public-use series (e.g. CPS, BTOS, JOLTS, OEWS, O*NET), not proprietary panels; written so economists, ML researchers, and search engines can find the topic quickly.

2. **US labor market measurement from public data**  
   The emphasis is on **measurement**: documented universes, weights, crosswalks, and QA, not hype about “AI effects.” Causal claims remain your responsibility outside this stack.

3. **Reproducible US labor & AI indicators**  
   Step-based `build_*` / `qa_*` pairs, schema-checked outputs, and `intermediate/*_run_metadata.json` so indicators trace to inputs and a git commit or tag.

4. **Open data pipeline for AI and labor economics**  
   Import the package for new work, rerun single build steps, or replicate the full stack. The main entry points are **[docs/README.md](docs/README.md)** and [docs/library/README.md](docs/library/README.md).

5. **State-level case studies (optional)**  
   The default story is **national / federal** measurement. Optional state slices (for example Virginia, FIPS 51) are compartmentalized under **[docs/states/README.md](docs/states/README.md)** so you can drill down without mixing them into the core paper path.

Broad, search-friendly scope: reproducible analytics from **public** official sources, delivered as both a **Python library** (`occupational_transition`) and a **step-by-step pipeline** that rebuilds tables, figures, and lineage metadata.

---

## Choose your path

### Browse the catalog, then fetch

- Canonical dataset list: [docs/data_registry.csv](docs/data_registry.csv) (`dataset_id`, URLs, `extractor`, `update_cadence`).
- CLI: `ot catalog`, `ot fetch --dataset-id …`, `ot refresh --cadence rolling` (scheduled local runs: [docs/operations/local_scheduling.md](docs/operations/local_scheduling.md)).

### A — Use the package in your own project

Install and start importing immediately:

```bash
pip install -e .
```

Start with:

- [docs/library/README.md](docs/library/README.md) for stable entry points and examples.
- [examples/README.md](examples/README.md) for practical scripts.

Optional CLI:

- `ot catalog` / `ot fetch` / `ot refresh`
- `ot list-analyses` (add `--verbose` to regenerate `docs/meta/analysis_bundles.yaml` and print outputs)
- `ot list-sources`
- `ot run --bundle quick-start`
- `ot run --profile config/profiles/quick-start.toml`

---

### B — Rebuild specific outputs you care about

Run only the build and QA scripts relevant to your analysis, without running the full stack.

Start with:

- [docs/methodology/README.md](docs/methodology/README.md) for step-by-step mapping.
- [docs/replication/acceptance_matrix.md](docs/replication/acceptance_matrix.md) for outputs and checks.
- [docs/methodology/tickets/](docs/methodology/tickets/) for methodology support files.

You can also find your step in the research pipeline table below. Builds and QA run through `python -m occupational_transition.run_step build|qa <TICKET>` (thin `scripts/build_*.py` wrappers remain for ad hoc use).

---

### C — Fully replicate the published stack

From a clean clone:

```bash
pip install -r requirements.txt
pip install -e .
python scripts/run_full_pipeline_from_raw.py
```

Full instructions, expected runtime, recovery guidance, committed-vs-generated outputs, and replication conventions are in:

- [docs/replication/README.md](docs/replication/README.md)
- [docs/start_here.md](docs/start_here.md)
- [docs/analysis_catalog.md](docs/analysis_catalog.md)
- [docs/source_selection.md](docs/source_selection.md)

Expect large downloads, large disk usage, and long runtimes.

---

### D — State-level case study (optional)

For a **Virginia** descriptive QCEW deep dive and related outputs (not part of the main paper figure list), start at **[docs/states/README.md](docs/states/README.md)** and **[docs/states/virginia/README.md](docs/states/virginia/README.md)**.

---

## Install

Python **3.10+** is supported. Python **3.11+** is recommended.

Basic install:

```bash
pip install -e .
```

Developer install (tests + linter):

```bash
pip install -e ".[dev]"
pytest
```

`requirements.txt` mirrors the editable install so `pip install -r requirements.txt` stays aligned with `pyproject.toml`.

Versioning:

- Package version: `occupational_transition.__version__`
- Library API changes follow semantic versioning
- For frozen paper builds, pin a git tag

---

## What you can build with this

- Descriptive indicators of AI relevance, labor outcomes, transitions, and sector trends.
- Reproducible figure tables under `figures/`.
- Run metadata under `intermediate/` for auditability.
- Optional static visual exports under `visuals/`.

This stack is **measurement-first**. It gives you clean, documented empirical inputs; causal identification remains a separate design decision.

---

## Highlights

| | |
|--|--|
| **Library** | `occupational_transition` — HTTP helpers, source clients (e.g. BTOS, JOLTS, O*NET), crosswalk loaders. Install with `pip install -e .`. |
| **Pipeline** | Ordered build and QA scripts with `intermediate/*_run_metadata.json` run history. Step-by-step details live in [docs/replication/README.md](docs/replication/README.md) and [docs/methodology/README.md](docs/methodology/README.md). |
| **Documentation** | Single hub: **[docs/README.md](docs/README.md)** (library, replication, methodology, figures, paper, policy, quality). |
| **Governance** | Schema-checked outputs, registry URLs in [docs/data_registry.csv](docs/data_registry.csv), acceptance matrix and replication runbooks under [docs/replication/](docs/replication/). |

---

## Documentation map

Use the docs hub to navigate by role:

- **Docs hub:** [docs/README.md](docs/README.md)
- **Library usage:** [docs/library/README.md](docs/library/README.md)
- **Replication guide:** [docs/replication/README.md](docs/replication/README.md)
- **Methodology mapping:** [docs/methodology/README.md](docs/methodology/README.md)
- **Paper artifacts:** [docs/paper/README.md](docs/paper/README.md)
- **Figure structure:** [docs/figures/README.md](docs/figures/README.md)
- **Policy and claim discipline:** [docs/policy/claim_audit.md](docs/policy/claim_audit.md)

Additional quick links:

- [crosswalk methodology](docs/methodology/pr000_crosswalk_methodology.md)
- [data registry](docs/data_registry.csv)
- [committed vs generated outputs](docs/replication/README.md#committed-outputs-vs-build-generated)

All Markdown is organized by audience in **[docs/README.md](docs/README.md)**. Start there for crosswalk notes, figure catalogs, claim audit, and manuscript drafts.

---

## Research pipeline

The full step list, script mapping, and detailed output contracts are documented in:

- [docs/replication/README.md](docs/replication/README.md)
- [docs/replication/acceptance_matrix.md](docs/replication/acceptance_matrix.md)
- [docs/methodology/README.md](docs/methodology/README.md)

Targeted work is fully supported: run only the specific `build_*.py` and matching `qa_*.py` scripts you need.

---

## Full replication

End-to-end rebuild from the repository root requires network access and may require **large disk space** and **long runtime**. See [docs/replication/README.md](docs/replication/README.md) for full operational details.

```bash
pip install -r requirements.txt
python scripts/run_full_pipeline_from_raw.py
```

This writes:

- `intermediate/full_clean_rebuild_acceptance_<UTC>.md`

The run fails fast on the first failed build or QA step.

### Common flags

- `--with-audit-summary` — generates audit markdown from the log
- `--with-visuals` — runs `run_visuals_all.py` and `qa_visuals.py`
- `--skip-install`
- `--source-selection-mode freeze_mode`
- `--require-signoff`

### Typical iterative run

Strict step order, audit summary, and policy gates:

```bash
pip install -r requirements.txt
python scripts/run_full_pipeline_from_raw.py --with-audit-summary
```

This also runs robustness checks, drift dashboard steps, and freeze-manifest steps as configured.

### Targeted work

For partial rebuilds, run only the `build_*.py` and matching `qa_*.py` scripts you need. Detailed per-step mappings are in [docs/methodology/README.md](docs/methodology/README.md).

---

## Quality bar

- JSON lineage under `intermediate/*run_metadata.json` for retained outputs.
- QA scripts enforce schemas, domains, and SHA-256 checks against cached inputs where applicable.
- Policy-facing KPI tables carry uncertainty fields and `evidence_directness` per project rules.
- Registry rows in [docs/data_registry.csv](docs/data_registry.csv) use canonical HTTPS URLs and explicit provenance fields.

Details:

- [docs/README.md](docs/README.md)
- [docs/replication/acceptance_matrix.md](docs/replication/acceptance_matrix.md)

---

## Known deviations and data notes

Method-specific caveats and exceptions are documented in the detailed methodology files under [docs/methodology/](docs/methodology/), with summary gates in [docs/replication/acceptance_matrix.md](docs/replication/acceptance_matrix.md).

---

## Figures and visuals

Render charts from committed `figures/*.csv` (main text **Figures 1–6**, appendix **A1–A10**, and monitoring stems as configured in `scripts/run_visuals_all.py`):

```bash
python scripts/run_visuals_all.py
python scripts/qa_visuals.py
```

Outputs:

- `visuals/png/`
- `visuals/vector/`
- `intermediate/visuals_run_manifest.json`

Authoritative map of paper figures to CSV paths, visual stems, captions, and source notes: [docs/figures/figure_catalog.md](docs/figures/figure_catalog.md). Main-text redesigns include composite manuscript artifacts (for example `figure2_redesigned_composite`, `figure3_redesigned_composite`, `figure4_redesigned_composite`) and **Figure 6** (`figures/figure6_policy_roadmap.csv` → stem `policy_roadmap`).

Additional references:

- Style guide: [docs/quality/README.md#visual-style-guide](docs/quality/README.md#visual-style-guide)
- Caption and source-note coverage (Figures 1–6): `python scripts/qa_visual_caption_coverage.py`
- One-shot acceptance: `python scripts/run_visuals_acceptance.py`

---

## Robustness and freeze

```bash
python scripts/run_robustness_all.py
python scripts/build_freeze_manifest.py
```

Outputs:

- Robustness reports under `intermediate/robustness/`

The freeze manifest hashes figures, run metadata, and the visuals manifest when present.

---

## Data, licensing, and scope

- Built around public and public-use sources (Census, BLS, O*NET, and related documentation).
- License: [MIT](LICENSE)
- Third-party materials and notices: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- Security reporting guidance: [SECURITY.md](SECURITY.md)

This repository is built around **public** official sources, not proprietary panels.

---

## How to cite

Cite both the repository and the **version** you used.

- Package version: `occupational_transition.__version__`
- For papers, also record the **commit hash or results tag** next to any table reproduced from this pipeline
- Machine-readable metadata is in [CITATION.cff](CITATION.cff)
- Results freeze and tagging guidance: [docs/replication/project_maintenance.md#results-freeze-and-tagging](docs/replication/project_maintenance.md#results-freeze-and-tagging)

### BibTeX

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

See:

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

If you want to extend data coverage, add new indicators, or harden reproducibility checks, contributions are welcome.

---

## Project and license

| | |
|--|--|
| **License** | [MIT](LICENSE) |
| **Cite** | [CITATION.cff](CITATION.cff) |
| **Code of Conduct** | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| **Third-party assets** | [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) |
| **Contributing** | [CONTRIBUTING.md](CONTRIBUTING.md) |
| **Security** | [SECURITY.md](SECURITY.md) |
| **Git size** | [docs/replication/project_maintenance.md#git-history-size-and-hygiene](docs/replication/project_maintenance.md#git-history-size-and-hygiene) |

Full replication can require **many gigabytes** and **hours** of download and compute.
Committed `figures/` snapshots and
[docs/replication/README.md#committed-outputs-vs-build-generated](docs/replication/README.md#committed-outputs-vs-build-generated)
document what ships in git versus what builds locally.
