# Library (`occupational_transition`)

**Audience:** Python integrators, economists and ML researchers pulling **public** US labor-market data through a documented API.

**Positioning (same as the root README):** **Public data, AI, and US labor markets** — broad, search-friendly. **US labor market measurement from public data** — construction and QA, not default causal claims. **Reproducible US labor & AI indicators** — stable entry points and lineage-friendly outputs. **Open data pipeline for AI and labor economics** — this document is the library lane of that pipeline.

**Prerequisites:** Python 3.10+, `pip install -e .` from the repository root.

## Contents

- [Package layout and stable entry points](#package-layout-and-stable-entry-points)
- [Reuse for researchers](#reuse-for-researchers)
- [Related work and positioning](#related-work-and-positioning)
- [API reference HTML (Sphinx)](#api-reference-html-sphinx)
- [Compatibility, PyPI, and versioning](#compatibility-pypi-and-versioning)
- [Registry and methodology pointers](#registry-and-methodology-pointers)
- [CLI](#cli)

---

## Package layout and stable entry points

The repository installs as an editable Python package (see `pyproject.toml`). Import path:

```python
import occupational_transition
from occupational_transition.sources import btos, jolts, onet
from occupational_transition import crosswalks, http
```

| Module | Role |
|--------|------|
| `occupational_transition.http` | Shared HTTP helpers: `fetch_text`, `fetch_bytes`, `download_to_path`, `sha256_bytes`, retries, `raw_cache_root` (env `OT_RAW_DIR` or `./raw`), and `fetch_text_cached` for lightweight endpoint caching. |
| `occupational_transition.sources.btos` | Census BTOS API: national `naics2=XX` AI trend extraction. |
| `occupational_transition.sources.jolts` | BLS LABSTAT JOLTS file fetch and TSV parsing helpers. |
| `occupational_transition.sources.onet` | O*NET text zip download and Work Activities (IM) parsing. |
| `occupational_transition.crosswalks` | Loaders for committed `crosswalks/*.csv` files. |

Prefer these for downstream code:

- `occupational_transition.sources.btos.build_btos_ai_trends_national_xx`
- `occupational_transition.pipelines.figure1_panelB_t002.build_figure1_panelB_t002`
- `occupational_transition.crosswalks.load_occ22_labels`
- `occupational_transition.crosswalks.load_sector6_jolts_labels`
- `occupational_transition.sources.onet.ensure_onet_text_zip`, `read_work_activities_im`, `load_soc_crosswalk`

Internal helpers may change; anything prefixed with `_` or documented as internal is not stable.

The top-level package exposes `__version__` and submodule handles (`crosswalks`, `http`, `btos`, `jolts`, `onet`, `oews`). The `figure1_panelB_t002` pipeline submodule is loaded on first access (`occupational_transition.figure1_panelB_t002`) to keep default imports light.

---

## Reuse for researchers

This repository is built for **transparent measurement** from **public** US labor-market data, not for proprietary panels or linked employer–employee identification strategies. Use it when you want **documented extraction**, **frozen crosswalks**, and **QA-checked tables** you can cite alongside a commit or tag.

### Who this is for

- **Empirical labor and macro (public micro):** CPS, OEWS, JOLTS, CES, QCEW, and related series with explicit universes and weights where applicable.
- **AI and jobs (measurement):** O*NET task scales, BTOS adoption series, and paper-defined composites (e.g. AI-relevance terciles)—always **descriptive** unless you supply your own identification strategy outside this repo.
- **Policy and briefings:** optional memo and Virginia-facing artifacts are **additive**; see [policy/briefing/](../policy/briefing/README.md) and keep them separate from core manuscript claims.

### Three reuse modes

| Mode | What you do | Time / disk (order of magnitude) | Entry points |
|------|-------------|-----------------------------------|--------------|
| **1. Library import** | `pip install -e .`, import `occupational_transition`, use HTTP helpers and source modules. | Minutes; no full pipeline. | This page, [examples/](../../examples/) |
| **2. One ticket** | Run one `scripts/build_*.py` + matching `qa_*.py` from the [root README pipeline table](../../README.md#research-pipeline-tickets). | Minutes to hours; depends on ticket (downloads). | [Methodology tickets](../methodology/README.md) |
| **3. Full replication** | `python scripts/run_full_pipeline_from_raw.py` (see [replication README](../replication/README.md)). | Hours to days; **many GB** possible. | [Replication](../replication/README.md) |

### What you can claim (and cannot)

- **Descriptive facts** from published outputs: follow wording in [methods and data](../paper/methods_data.md) and per-ticket methodology under [methodology/tickets/](../methodology/tickets/).
- **Causal inference:** this repo does **not** automatically deliver causal estimates for AI adoption or labor outcomes. Capability matrices and memos describe **data availability and resolution**, not treatment effects.
- **Language discipline:** use [claim audit](../policy/claim_audit.md) and [quality standards](../quality/README.md) for how policy-facing KPIs and visuals are labeled.

### How to attribute outputs in your paper

1. **Cite the software** using [CITATION.cff](../../CITATION.cff) / the BibTeX block in the [root README](../../README.md).
2. **Pin the build:** record the **git commit** or **annotated tag** (`results-YYYY-MM-DD` or library `vX.Y.Z`) used when generating figures.
3. **Point to CSVs:** name `figures/*.csv` and, where relevant, `intermediate/*_run_metadata.json` (hashes, URLs, selection rules).
4. **Evidence snapshot:** align prose with [evidence snapshot](../paper/evidence_snapshot.md) if you lock numbers to a specific run.

### Sensitive materials

Senate- and senator-facing narrative, Q&A, and Virginia-specific briefing packs live under **[policy/briefing/](../policy/briefing/)** (isolated from general policy). Treat distribution under your institution’s rules. The **claim audit** remains in [policy/claim_audit.md](../policy/claim_audit.md) as the cross-cutting ledger.

### FAQ

**Does this repo replace BLS or Census APIs?**  
No. It wraps reproducible downloads and parsing **for this project’s** figure contracts; you remain responsible for terms of use and citation of the underlying agencies.

**Why terciles and indices?**  
They are **ordinals** for grouping and visualization; see methodology tickets and [methods_data.md](../paper/methods_data.md) for definitions.

**Can I use only Virginia memo visuals?**  
Yes, but they are **descriptive** and **additive** to the paper stack; see [policy/briefing/README.md](../policy/briefing/README.md).

**Causal inference?**  
Not provided by default. Use your own design; this repo supplies **inputs** and **documented** descriptive series.

---

## Related work and positioning

This repo is a **software and reproducibility stack**: it combines **public data** (BLS, Census, O*NET, etc.) with **frozen crosswalks**, **ticketed build scripts**, **QA**, and **JSON lineage** for a specific research pipeline. It is not a substitute for agency documentation or for academic surveys of the literature.

### Official sources (always cite upstream)

- **BLS:** JOLTS, CES, OEWS, CPS-related products as used in each ticket; canonical URLs in [data_registry.csv](../data_registry.csv).
- **U.S. Census Bureau:** BTOS and other Census products as referenced in build scripts and registry.
- **O*NET / DOL:** O*NET database and crosswalks per `src/occupational_transition/sources/onet.py` usage and ticket methodology.

Researchers should cite the **underlying datasets** in addition to this software when publishing figures.

### What is distinctive here

- **Ticketed pipeline:** `PR-000` through `T-020` with explicit `build_*` / `qa_*` pairs and **acceptance** language in [acceptance_matrix.md](../replication/acceptance_matrix.md).
- **Lineage metadata:** `intermediate/*_run_metadata.json` ties outputs to inputs and hashes where applicable.
- **Single crosswalk layer:** committed `crosswalks/*.csv` with methodology in [pr000_crosswalk_methodology.md](../methodology/pr000_crosswalk_methodology.md).
- **Dual use:** importable Python package **and** full replication runner for the paper.

### Related resources (categories)

- **Agency portals:** BLS, Census, O*NET, and NLS public documentation (see [references/](../references/) for PDFs used in this project).
- **Other harmonization projects:** Many exist for occupations, industries, and time; this repo’s **occ22** and **sector6** definitions are **project-specific**—read PR-000 before merging with external schemes.

---

## API reference HTML (Sphinx)

HTML API documentation is **not** committed; build it locally.

**Prerequisites:** `pip install -e ".[dev]"` (includes Sphinx).

From the repository root:

```bash
sphinx-build -b html docs/sphinx docs/sphinx/_build/html
```

Open `docs/sphinx/_build/html/index.html` in a browser. Sphinx source lives under [docs/sphinx/](../sphinx/); configuration adds `src/` to `sys.path` so imports resolve during the build.

---

## Compatibility, PyPI, and versioning

- **Python:** `>=3.10` as declared in `pyproject.toml` (3.11+ recommended).
- **Semver:** bump **minor** for backward-compatible API additions, **major** for breaking public symbol or behavior changes in documented entry points.
- **Replication:** frozen paper builds should pin a **git tag** or **commit**; library semver does not replace ticket output contracts—run `qa_*.py` after upgrades.

**PyPI (optional):** The project name on PyPI is expected to be `occupational-transition` (see `pyproject.toml`). Publishing wheels is optional: many users will `git clone` + `pip install -e .` for full replication. When a release is published, document it in [CHANGELOG.md](../../CHANGELOG.md) and align `CITATION.cff` / root README BibTeX version fields.

Package version is `occupational_transition.__version__` (also in `pyproject.toml`). For frozen replication builds, pin a git tag or document the installed version next to `intermediate/*run_metadata.json` outputs.

---

## Registry and methodology pointers

Canonical URLs and snapshot notes remain in [data_registry.csv](../data_registry.csv). Per-ticket assumptions are in `docs/methodology/tickets/t*_methodology.md` (see [methodology README](../methodology/README.md)).

---

## CLI

`ot-fetch` prints BTOS and JOLTS base URLs, and can optionally download/cache raw inputs:

```bash
ot-fetch btos
ot-fetch jolts

ot-fetch btos --download
ot-fetch jolts --download
```
