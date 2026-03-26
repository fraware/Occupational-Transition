# Occupational Transition

Public data, AI, and US labor markets in one reproducible research stack.

This repository gives you:

- A Python package (`occupational_transition`) for pulling and transforming public labor-market data.
- A reproducible build workflow that regenerates published indicators and figures from source data.
- Auditable outputs and metadata so you can trace results to code, inputs, and run settings.

Repository: [github.com/fraware/Occupational-Transition](https://github.com/fraware/Occupational-Transition)

---

## Why This Repo Is Worth Reusing

Most labor/AI projects force you to choose between:

- Fast, one-off analysis scripts that are hard to trust later, or
- Heavy pipelines that are difficult to adapt for new research questions.

This repo is designed to give you both:

- **Fast entry** for researchers who want to run targeted analyses now.
- **Strong reproducibility** for papers, policy memos, and peer review.
- **Clear boundaries** between descriptive measurement and causal interpretation.

If you work in labor economics, applied macro, AI-and-work measurement, or policy analysis with public data, this is built for your workflow.

---

## Choose Your Path

### 1) Use the package in your own project

Install and start importing immediately:

```bash
pip install -e .
```

Start with:

- [`docs/library/README.md`](docs/library/README.md) for stable entry points and examples.
- [`examples/README.md`](examples/README.md) for practical scripts.

### 2) Rebuild specific outputs you care about

Run only the build and QA scripts relevant to your analysis, without running the full stack.

Start with:

- [`docs/methodology/README.md`](docs/methodology/README.md) for step-by-step mapping.
- [`docs/replication/acceptance_matrix.md`](docs/replication/acceptance_matrix.md) for outputs and checks.

### 3) Fully replicate the published stack

From a clean clone:

```bash
pip install -r requirements.txt
python scripts/run_full_pipeline_from_raw.py
```

Full instructions, expected runtime, and recovery guidance:

- [`docs/replication/README.md`](docs/replication/README.md)

---

## What You Can Build With This

- Descriptive indicators of AI relevance, labor outcomes, transitions, and sector trends.
- Reproducible figure tables under `figures/`.
- Run metadata under `intermediate/` for auditability.
- Optional static visual exports under `visuals/`.

This stack is measurement-first. It gives you clean, documented empirical inputs; causal identification remains a separate design decision.

---

## Documentation Map

Use the docs hub to navigate by role:

- **Docs hub:** [`docs/README.md`](docs/README.md)
- **Library usage:** [`docs/library/README.md`](docs/library/README.md)
- **Replication guide:** [`docs/replication/README.md`](docs/replication/README.md)
- **Methodology mapping:** [`docs/methodology/README.md`](docs/methodology/README.md)
- **Paper artifacts:** [`docs/paper/README.md`](docs/paper/README.md)
- **Figure structure:** [`docs/figures/README.md`](docs/figures/README.md)
- **Policy and claim discipline:** [`docs/policy/claim_audit.md`](docs/policy/claim_audit.md)

Senator and Virginia briefing materials are intentionally isolated in:

- [`docs/policy/briefing/README.md`](docs/policy/briefing/README.md)

---

## Data, Licensing, and Scope

- Built around public and public-use sources (Census, BLS, O*NET, and related documentation).
- License: [MIT](LICENSE)
- Third-party materials and notices: [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)
- Security reporting guidance: [`SECURITY.md`](SECURITY.md)

---

## Contributing

See:

- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)

If you want to extend data coverage, add new indicators, or harden reproducibility checks, contributions are welcome.
# Occupational Transition

**Public data, AI, and US labor markets** — broad, search-friendly scope: reproducible analytics from **public** official sources, delivered as both a **Python library** (`occupational_transition`) and a **step-by-step pipeline** that rebuilds tables, figures, and lineage metadata.

## Scope and positioning

1. **Public data, AI, and US labor markets** — official and public-use series (e.g. CPS, BTOS, JOLTS, OEWS, O*NET), not proprietary panels; written so economists, ML researchers, and search engines can find the topic quickly.
2. **US labor market measurement from public data** — emphasizes **measurement**: documented universes, weights, crosswalks, and QA—not hype about “AI effects”; causal claims remain your responsibility outside this stack.
3. **Reproducible US labor & AI indicators** — step-based `build_*` / `qa_*` pairs, schema-checked outputs, and `intermediate/*_run_metadata.json` so indicators trace to inputs and a git commit or tag.
4. **Open data pipeline for AI and labor economics** — import the package for new work, rerun single build steps, or replicate the full stack; entry points are **[docs/README.md](docs/README.md)** and [docs/library/README.md](docs/library/README.md).

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
| **Pipeline** | Ordered build and QA scripts with `intermediate/*_run_metadata.json` run history. Step-by-step details live in [docs/replication/README.md](docs/replication/README.md) and [docs/methodology/README.md](docs/methodology/README.md). |
| **Documentation** | Single hub: **[docs/README.md](docs/README.md)** (library, replication, methodology, figures, paper, policy, quality). |
| **Governance** | Schema-checked outputs, registry URLs in [docs/data_registry.csv](docs/data_registry.csv), acceptance matrix and replication runbooks under [docs/replication/](docs/replication/). |

---

## Choose your path

**A — Use the package**  
Install (below), read [docs/library/README.md](docs/library/README.md), run scripts under [examples/](examples/) ([examples/README.md](examples/README.md)). Optional CLI: `ot-fetch` (see `pyproject.toml` `[project.scripts]`).

**B — Run one build step**  
Find your step in the [pipeline table](#research-pipeline-build-steps), then run the listed `scripts/build_*.py` and `scripts/qa_*.py`. Methodology: [docs/methodology/README.md](docs/methodology/README.md) and [docs/methodology/tickets/](docs/methodology/tickets/).

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

## Research pipeline

The full step list, script mapping, and detailed output contracts are documented in:

- [docs/replication/README.md](docs/replication/README.md)
- [docs/replication/acceptance_matrix.md](docs/replication/acceptance_matrix.md)
- [docs/methodology/README.md](docs/methodology/README.md)

---

## Full replication

End-to-end rebuild from the repo root (network required; **large disk and long runtime**—see [docs/replication/README.md](docs/replication/README.md)):

```bash
pip install -r requirements.txt
python scripts/run_full_pipeline_from_raw.py
```

Writes `intermediate/full_clean_rebuild_acceptance_<UTC>.md` and fails fast on the first failed build or QA step.

**Common flags:** `--with-audit-summary` (audit markdown from the log) · `--with-visuals` (runs `run_visuals_all.py` + `qa_visuals.py`) · `--skip-install` · `--source-selection-mode freeze_mode` · `--require-signoff`

**Typical iterative run** (strict step order + audit summary + policy gates):

```bash
pip install -r requirements.txt
python scripts/run_full_pipeline_from_raw.py --with-audit-summary
```

This also runs memo/brief build and QA, robustness, drift dashboard, and freeze manifest steps as configured.

**Targeted work:** run only the specific `build_*.py` and matching `qa_*.py` scripts you need. Detailed per-step mappings are in [docs/methodology/README.md](docs/methodology/README.md).

---

## Quality bar

- JSON lineage under `intermediate/*run_metadata.json` for retained outputs; QA scripts enforce schemas, domains, and SHA-256 checks against cached inputs where applicable.
- Policy-facing KPI tables carry uncertainty fields and `evidence_directness` per project rules.
- Registry rows in `docs/data_registry.csv` use canonical HTTPS URLs and explicit provenance fields.

Details: [docs/README.md](docs/README.md) and [docs/replication/acceptance_matrix.md](docs/replication/acceptance_matrix.md).

---

## Known deviations and data notes

Method-specific caveats and exceptions are documented in the detailed methodology files under [docs/methodology/](docs/methodology/), with summary gates in [docs/replication/acceptance_matrix.md](docs/replication/acceptance_matrix.md).

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
| **Cite** | [CITATION.cff](CITATION.cff) |
| **Code of Conduct** | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| **Third-party assets** | [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) |
| **Contributing** | [CONTRIBUTING.md](CONTRIBUTING.md) |
| **Security** | [SECURITY.md](SECURITY.md) |
| **Git size** | [docs/replication/project_maintenance.md#git-history-size-and-hygiene](docs/replication/project_maintenance.md#git-history-size-and-hygiene) |

Full replication can require **many gigabytes** and **hours** of download and compute; committed `figures/` snapshots and [docs/replication/README.md#committed-outputs-vs-build-generated](docs/replication/README.md#committed-outputs-vs-build-generated) document what ships in git versus what builds locally.
