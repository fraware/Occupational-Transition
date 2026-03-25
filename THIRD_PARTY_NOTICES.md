# Third-party materials bundled in this repository

This project includes small reference files for reproducibility and citation. **Government statistical publications** are generally in the public domain in the United States; **verify** terms on the provider’s site before redistribution in other jurisdictions or for commercial products.

| File | Source / rights | Purpose in repo |
|------|-------------------|-----------------|
| [docs/references/PublicUseDocumentation_final.pdf](docs/references/PublicUseDocumentation_final.pdf) | U.S. Census Bureau / BLS public-use documentation | CPS methodology reference |
| [docs/references/cpsjan24.pdf](docs/references/cpsjan24.pdf) | Census CPS technical documentation (example vintage) | Supplement design reference |
| [raw/Occupation_Codes_Jan2025.pdf](raw/Occupation_Codes_Jan2025.pdf) | BLS/Census occupation coding documentation | Crosswalk validation |
| [raw/table-a1_a2.xlsx](raw/table-a1_a2.xlsx) | Published BLS/Census auxiliary table (check source workbook) | Industry/auxiliary mapping |

Large microdata files (CPS, ACS PUMS, NLSY, etc.) are **not** committed; they are downloaded by scripts under `raw/` per [docs/replication/README.md](docs/replication/README.md). Those datasets have **separate terms of use** from the Census Bureau, BLS, and NLS.

Figures and tables **produced by this repository’s code** from public inputs are covered by the license in [LICENSE](LICENSE) unless they incorporate third-party content under stricter terms.

For Git object database size and removing accidental large blobs from history, see [docs/replication/project_maintenance.md#git-history-size-and-hygiene](docs/replication/project_maintenance.md#git-history-size-and-hygiene).
