# Figures documentation

**Audience:** Anyone connecting CSV outputs, static visuals, captions, and source notes.

## How the pieces fit

- **[figure_catalog.md](figure_catalog.md)** — authoritative map from paper or memo stems to CSV paths, caption files, and source notes. Other docs and QA scripts treat it as the contract.
- **[captions/](captions/)** — one file per figure stem with final caption text.
- **[source_notes/](source_notes/)** — provenance and limitation notes per stem.
- **[memos/](memos/)** — build or design notes for visuals where needed.

The catalog paths are stable interfaces: if you move or rename caption or source-note files, update the catalog and any consumers in the same change.

## Related

- [quality README](../quality/README.md) — visual style lock and memo precision rules
- [replication README](../replication/README.md) — how CSVs and visuals are produced
- [Documentation hub](../README.md) — full map of `docs/`
