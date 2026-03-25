# Contributing

## Scope

This repository is a reproducible research pipeline (Python scripts, frozen CSV outputs, methodology markdown, and visuals). Changes should preserve ticket-by-ticket build and QA contracts described in [README.md](README.md) and [docs/replication/acceptance_matrix.md](docs/replication/acceptance_matrix.md).

Community interactions follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Citation metadata for the software lives in [CITATION.cff](CITATION.cff); update version fields when you cut a release ([CHANGELOG.md](CHANGELOG.md)).

## Environment

- Python 3.10 or newer.
- Install dependencies: `pip install -r requirements.txt` (editable install of `occupational_transition` from `pyproject.toml`) or `pip install -e ".[dev]"` when running tests.
- Full replication downloads large public microdata into `raw/`; see [docs/replication/README.md](docs/replication/README.md) for disk and network expectations. Optional cache root: set `OT_RAW_DIR` to override the default `./raw` used by helpers in `occupational_transition.http`.

## Adding a data source

1. Implement fetch/parse logic under `src/occupational_transition/sources/<name>.py` (reuse `occupational_transition.http` for HTTP).
2. Add or update rows in [docs/data_registry.csv](docs/data_registry.csv) with canonical HTTPS URLs.
3. Add a short methodology note under `docs/methodology/tickets/t*_methodology.md` or extend an existing ticket doc.
4. Add unit tests with **offline** fixtures under `tests/fixtures/` (avoid live network in default CI).
5. Wire thin `scripts/build_*.py` and `scripts/qa_*.py` scripts that preserve existing CSV and `intermediate/*run_metadata.json` contracts.

See [docs/library/README.md](docs/library/README.md) for the package layout and stable entry points.

## Making changes

1. Prefer small, focused pull requests tied to a ticket or a clear bugfix.
2. CI runs **pytest** and **ruff** on `src/`, `tests/`, and `examples/` (see [.github/workflows/ci.yml](.github/workflows/ci.yml)); ensure they pass locally.
3. After changing a build script, run the matching `qa_*.py` script from the repository root.
4. For Figure 5 (T-010), lineage files live under [docs/lineage/](docs/lineage/); after editing them, run `python scripts/build_figure5_capability_matrix.py` then `python scripts/qa_figure5_capability_matrix.py`.
5. Match existing naming, typing, and documentation style in the files you touch.

## Line endings

The repository uses LF for text files where possible; see [.gitattributes](.gitattributes).

## License

By contributing, you agree that your contributions are licensed under the terms in [LICENSE](LICENSE).
