# Changelog

All notable changes to the **library API** and **documented replication contracts** will be documented here. Internal-only script refactors may omit entries if `figures/` and `intermediate/*_run_metadata.json` schemas stay unchanged.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for the `occupational_transition` package.

## [0.1.0] — 2026-03-25

### Added

- Initial packaged release: `occupational_transition` with `http`, `sources` (BTOS, JOLTS, O*NET, OEWS), `crosswalks`, and `pipelines.figure1_panelB_t002`.
- Public top-level exports and lazy load for `figure1_panelB_t002`.
- Researcher documentation: consolidated in `docs/library/README.md` (reuse, related work, API build).
- Citation metadata: `CITATION.cff`, README BibTeX block.
- Examples index: `examples/README.md` and scripts `01`–`05`.
- Sphinx API scaffold under `docs/sphinx/`; build instructions in `docs/library/README.md` (API section).
- GitHub Actions CI (pytest + ruff) and issue templates.

[0.1.0]: https://github.com/fraware/Occupational-Transition/releases
