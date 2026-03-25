# Senate Briefing Memo

## Subject
What U.S. public federal data can and cannot say about AI and labor: immediate actions, expected payoff, and guardrails.

## One-page executive summary (Virginia-first)

### Core statement

Public federal data already supports a credible, reproducible, and policy-usable
Virginia readout on AI-and-work conditions. The near-term strategy should focus
on upgrading existing surveys (CPS, BTOS, scoped JOLTS supplement) rather than
waiting for a greenfield data architecture.

### Three headline findings

1. **Virginia's labor structure in the six-sector benchmark is concentrated in
   HCS and manufacturing.**
   In the retained 2025 Q3 benchmark frame, HCS is 37.62% and manufacturing is
   28.69% of Virginia's six-sector employment denominator.

2. **Virginia differs from peers in ways that matter for federal oversight.**
   Virginia is rank 1 of 31 in retail share and rank 4 of 31 in manufacturing
   share in the retained benchmark set, indicating distinct compositional
   exposure relative to the peer region.

3. **A defensible near-term signal stack exists now.**
   The Virginia KPI dashboard combines structural sector shares/ranks and
   business-side adoption context (including BTOS state signal where published),
   which is sufficient for oversight monitoring but not causal attribution.

### Three federal asks

1. **CPS AI worker module (0-3 months to scope; 3-9 months to field).**
2. **BTOS AI question stability and publication continuity (0-3 and 3-9 months).**
3. **Scoped JOLTS supplement pilot for occupation-aware demand context (9-18 months).**

### Guardrails paragraph (non-claims)

This brief is a descriptive monitoring package, not a causal estimator. It does
not identify worker-firm linked treatment effects and does not support
fine-grained local monthly causal attribution. All senator-facing values are
traceable to versioned pipeline outputs and metadata under `figures/` and
`intermediate/*_run_metadata.json` (see `docs/senate_briefing_evidence_baseline_va.md`).

## Opening
Federal policymakers do not need to wait for a new national data system to begin credible AI-and-work monitoring. Existing public instruments already support a practical measurement stack when used together: worker-side outcomes (CPS), business-side AI adoption and directly published employment-effect rows (BTOS), labor-demand context for selected comparison sectors (JOLTS/CES), and occupational and task structure (OEWS/O*NET).

The core policy message is straightforward: make targeted, low-burden upgrades to existing surveys now, while planning a longer-run linked architecture for causal precision.

## Three asks

1. **Add a short AI worker module to CPS (highest near-term worker-side leverage).**
   Request a compact, repeatable CPS module on AI use at work, task substitution/augmentation, training, and perceived labor impacts.
   Why this matters: CPS already supports national worker-outcome monitoring at useful frequency and scale.

2. **Stabilize and refine BTOS AI items (highest near-term firm-side leverage).**
   Preserve a consistent core AI question set in BTOS and add minimal role and occupation-impact detail where feasible.
   Why this matters: BTOS is already the strongest public high-frequency business-side AI source, and public rows directly identify adoption plus employment-effect categories; task-effect interpretation is only partial when item-25 rows are not publicly tabulated.

3. **Pilot a scoped JOLTS supplement, not a full core redesign.**
   Test coarse occupation and wage-band demand-flow items in a rotating or annual supplement.
   Why this matters: JOLTS is central for openings/hires/separations but is not occupation-resolved in public release; it supports selected-sector comparison context, and scoped expansion is operationally more realistic than immediate full redesign.

## Expected payoff

- **Near-term (months):** National monitoring of AI-related worker outcomes and business adoption using transparent public series.
- **Medium-term (1-2 years):** Better occupation-aware demand signals and clearer cross-source interpretation for labor-policy decisions.
- **System-level:** Higher-quality public evidence for hearings, oversight, and agency coordination without overpromising causal attribution.

## Implementation timeline

- **0-3 months:** Interagency scoping of CPS and BTOS question language; define stable publication outputs and metadata standards.
- **3-9 months:** Field CPS module and BTOS refinements; publish regular dashboard-style public outputs with methods notes.
- **9-18 months:** Launch and evaluate scoped JOLTS supplement pilot; publish validation and response-burden findings.
- **18+ months:** Use pilot evidence to decide whether to scale occupation-linked demand measurement; continue planning for long-run worker-firm linked architecture.

## Guardrails against overclaiming

1. **State what is descriptive vs causal.**
   Public survey outputs support credible monitoring, not firm-level causal identification of AI effects.

2. **Keep resolution claims realistic.**
   National/coarse group estimates are strongest; highly granular occupation-by-state-by-month claims require caution and pooling.

3. **Do not treat synthesis matrices as estimators.**
   Capability classifications are decision tools, not empirical effect sizes.

4. **Split empirical diagnosis from policy recommendation.**
   The missing integrated worker-firm AI panel is a direct empirical diagnosis; prioritizing survey extensions over greenfield systems is a policy design judgment.

5. **Require reproducibility and provenance for policy-facing outputs.**
   Every released metric should carry source, method, and metadata lineage.

## Virginia deep-dive section (for senator briefing)

### Why Virginia needs a dedicated readout

Virginia combines a relatively high share of employment in manufacturing and
health care/social assistance within the project's six-sector benchmark frame,
with meaningful concentration in professional/business services and retail. For
oversight and appropriations decisions, this composition implies that federal
AI-and-work monitoring should be interpreted through a state lens rather than
national averages alone.

### Current Virginia structural profile (QCEW benchmark frame)

Using the retained period in the state benchmark pipeline (2025 Q3), Virginia's
six-sector composition is:

- Health care and social assistance: 37.62%
- Manufacturing: 28.69%
- Retail trade: 16.00%
- Professional and business services: 15.95%
- Financial activities: 1.41%
- Information: 0.32%

Selected rank context within the retained-state set:

- Retail share rank: 1 of 31
- Manufacturing share rank: 4 of 31
- Information weekly-wage rank: 5 of 31
- Financial-activities weekly-wage rank: 4 of 31

Policy interpretation: Virginia's observed mix suggests that near-term federal
measurement value is highest when worker-side signals (CPS module), firm-side
adoption signals (BTOS stability/refinement), and selected-sector demand
context (JOLTS/CES) are read jointly against this state structure.

### Virginia-focused implementation asks (federal, not state-run redesign)

1. **CPS AI worker module with stable subgroup outputs relevant to Virginia.**
   Preserve national comparability while ensuring release tables can support
   state-relevant subgroup diagnostics with pooled windows where needed.

2. **BTOS publication stability with state-facing continuity.**
   Maintain a consistent AI core item set and publication cadence so Virginia's
   trend interpretation does not depend on shifting question definitions.

3. **Scoped JOLTS supplement pilot for occupation-aware demand context.**
   Prioritize a low-burden supplement design that can improve interpretation of
   sector-level demand movements affecting Virginia's dominant sectors.

### Limits for testimony language

- The Virginia deep dive is **descriptive structural benchmarking** from public
  QCEW aggregates mapped to the frozen six-sector system.
- It is **not** a direct estimate of AI causality, treatment effects, or
  worker-firm linked dynamics.
- The denominator is employment inside the six in-scope sectors, not all-state
  employment across all industries.
- State comparisons reflect the retained benchmark set and period used by the
  reproducible pipeline.

### Virginia visual spine: decision and limitation sentences

| Visual stem | Decision sentence | Limitation sentence |
|-------------|-------------------|---------------------|
| `va01_virginia_sector_composition` | Given Virginia's concentration in HCS and manufacturing, prioritize worker-side and sector-sensitive monitoring resources in those domains first. | Composition is based on the six-sector QCEW benchmark denominator, not all-industry statewide employment. |
| `va02_virginia_sector_wages` | Use wage dispersion across sectors to target where adjustment risk may be more or less buffered by earnings levels. | Sector wage aggregates are descriptive and do not identify AI-specific wage effects. |
| `va03_virginia_peers_sector_shares` | Use peer share deviations to prioritize regionally tailored oversight and appropriations questions rather than national-average assumptions. | Peer comparisons are conditional on the retained benchmark set and period. |
| `va04_virginia_peers_sector_wages` | Use peer wage gaps to frame competitiveness and resilience discussions in hearings and interagency planning. | Wage differences across peers do not isolate policy or AI causal channels. |
| `va05_virginia_sector_ranks` | Translate rank positions into explicit oversight priorities (for example, where to scrutinize transition pathways and workforce supports). | Ranks summarize relative position only; they are not impact magnitudes. |
| `va06_virginia_kpi_dashboard` | Use the dashboard as a near-term accountability board for whether federal measurement upgrades are producing actionable signals. | KPI values combine descriptive constructs and must not be interpreted as causal estimates. |

### Federal action matrix (three horizons)

| Horizon | Federal action | Evidence anchor | Expected payoff | Implementation risk |
|---------|----------------|-----------------|-----------------|---------------------|
| 0-3 months | Finalize CPS AI module wording, BTOS core-item stability language, and publication metadata standards. | `va01`-`va06`; `figures/virginia_memo_kpis.csv`; `docs/memo_visual_precision.md` | Immediate improvement in comparability and transparency of public monitoring outputs. | Interagency coordination lag and scope creep in module design. |
| 3-9 months | Field CPS module and stable BTOS outputs; publish recurring Virginia-relevant dashboard tables with methods notes. | `figures/memo_dashboard_kpis.csv`; `figures/memo_btos_state_ai_use_latest.csv`; Virginia KPI lineage | Routine, policy-facing monitoring cadence usable for oversight and committee briefings. | Release timing mismatches and data-quality heterogeneity across instruments. |
| 9-18 months | Run scoped JOLTS supplement pilot with coarse occupation/wage-band demand-flow items and publish pilot evaluation. | `figures/figure4_panelA_jolts_sector_rates.csv`; `figures/figure4_panelB_ces_sector_index.csv`; methods guardrails | Better occupation-aware demand context without immediate core-system redesign burden. | Response burden constraints and limits in public-tab granularity. |

### What this brief does NOT claim

- It does **not** estimate causal impacts of AI on Virginia workers or firms.
- It does **not** infer worker-firm matched micro effects from public files.
- It does **not** support highly granular local monthly causal statements.
- It does **not** replace the need for longer-run linked data architecture.

## Bottom line for legislative action
The highest-value federal strategy is to **upgrade existing surveys** (CPS + BTOS first, scoped JOLTS next), publish transparent and reproducible indicators, and avoid claims that exceed the identification limits of available public data.

