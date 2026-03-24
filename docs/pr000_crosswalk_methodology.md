# PR-000 — Shared occupation and sector crosswalks (methodology)

Last documentation refresh: 2026-03-22.

## Purpose

This project freezes two taxonomies used across the AI-and-labor public-data paper:

1. **22 occupation groups (`occ22`)** — aligned with 2018 SOC major groups excluding military (55-0000), consistent with CPS `PRDTOCC1` and with OEWS/O*NET aggregation.
2. **Six demand-side sectors (`sector6`)** — Manufacturing; Information; Financial activities; Professional and business services; Health care and social assistance; Retail trade — as specified for main-text JOLTS/CES figures.

## Outputs

| File | Description |
| --- | --- |
| `crosswalks/occ22_crosswalk.csv` | Maps CPS `PRDTOCC1`, detailed 2018 Census occupation codes (`PEIO1OCD`), and SOC 2018 detail codes to `occ22_id` / SOC major group. |
| `crosswalks/sector6_crosswalk.csv` | Maps BTOS strata, JOLTS industry codes, CES supersectors/industries, BED industry codes, and NAICS 2-digit sectors (QCEW-aligned) to `sector6_code`. |
| `docs/data_registry.csv` | Provenance: source URL, download URL, file name, snapshot date, version notes. |

## Occupation methodology

- **PRDTOCC1** codes and census occupation code ranges are taken from the U.S. Census Bureau, *Occupation Classification* appendix (Beginning January 2020), including the 23-category recode (codes 1–22 occupational groups; code 23 Armed Forces).
- **2018 Census occupation detail** codes and SOC equivalents are taken from Census Table A2 in the TP-78 file (`table-a1_a2.xlsx`).
- **SOC major groups** follow BLS, *2018 SOC User Guide — Standard Occupational Classification and Coding Structure*.
- **Military**: SOC major group 55-0000 and CPS `PRDTOCC1` code 23 are flagged `is_military_excluded` and do not receive a paper-wide `occ22_id` in the 1–22 civilian taxonomy.

Regenerate: `python scripts/build_crosswalks.py`

## Sector methodology

- **NAICS 2-digit** sectors map to the frozen six sectors when they fall in manufacturing (31–33), information (51), finance or real estate (52–53), professional/management/administrative (54–56), health (62), retail (44–45), or education (61 → Professional and business services). Other NAICS sectors are `is_in_scope=0` for the six-sector comparison.
- **JOLTS** uses published industry aggregates from `jt.industry`; only codes that correspond to the six paper sectors (or their manufacturing sub-aggregates) are `is_in_scope=1`.
- **CES** uses `ce.supersector` and detailed `ce.industry` with `naics_code` prefixes.
- **BED** uses `bd.industry`; 6-digit codes beginning with `300` are interpreted as NAICS via `industry_code - 300000`, consistent with BLS flat-file documentation.
- **BTOS** uses official API strata (`/hfp/btos/api/strata`) for `naics2` and `naics3`.
- **QCEW** industry labels are versioned by BLS; this repository maps **NAICS 2-digit** sectors to `sector6` using the same NAICS prefix logic as CES, consistent with BLS statements that QCEW classifies establishments by NAICS.

Design choice: BED aggregate `200080` (Education and health services) is mapped to **Health care and social assistance** for a single comparable code; detailed BED rows disaggregate education (61) vs health (62) via NAICS-derived rows.

## Reproducibility

- Raw inputs live under `raw/` and should not be hand-edited after download.
- `snapshot_download_date` in `data_registry.csv` records when files were captured in this workspace.
- BLS `www.bls.gov` file downloads may require a browser or approved client; `download.bls.gov` flat files are retrieved over `https` with a standard User-Agent where automated access is permitted.

### Global source-selection policy

- Use pinned official artifacts when an issue requires a fixed reference period.
- Use \"latest available\" only when the issue template explicitly allows it.
- For any \"latest available\" path, metadata must record:
  - selection rule (for example, latest listed year then latest complete period)
  - resolved artifact URL/file name
  - local cached path
  - SHA-256 hash
- If source pages do not publish a release date or last-modified timestamp,
  record `Not reported by source` and `Not observed at build snapshot` in
  `docs/data_registry.csv` instead of leaving blanks.

## QA

Run: `python scripts/qa_crosswalks.py`
