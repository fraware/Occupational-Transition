# Contributing

## Scope

This repository is a reproducible research pipeline (Python scripts, frozen CSV outputs, methodology markdown, and visuals). Changes should preserve ticket-by-ticket build and QA contracts described in [README.md](README.md) and [docs/acceptance_matrix.md](docs/acceptance_matrix.md).

## Environment

- Python 3.10 or newer.
- Install dependencies: `pip install -r requirements.txt`.
- Full replication downloads large public microdata into `raw/`; see [docs/replication.md](docs/replication.md) for disk and network expectations.

## Making changes

1. Prefer small, focused pull requests tied to a ticket or a clear bugfix.
2. After changing a build script, run the matching `qa_*.py` script from the repository root.
3. For Figure 5 (T-010), lineage files live under [docs/lineage/](docs/lineage/); after editing them, run `python scripts/build_figure5_capability_matrix.py` then `python scripts/qa_figure5_capability_matrix.py`.
4. Match existing naming, typing, and documentation style in the files you touch.

## Line endings

The repository uses LF for text files where possible; see [.gitattributes](.gitattributes).

## License

By contributing, you agree that your contributions are licensed under the terms in [LICENSE](LICENSE).
