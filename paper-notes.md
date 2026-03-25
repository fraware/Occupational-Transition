
# US Occupational Transition

## 1. What the paper should be
This paper should be framed as the public-data counterpart to private-data and proprietary-usage approaches to AI-and-labor measurement. A good benchmark is Anthropic’s 2026 paper, which combines O*NET tasks, proprietary usage data from the Anthropic Economic Index, and theoretical exposure estimates to study observed exposure and early labor-market signals. A second benchmark is Sam Manning’s 2025 policy brief, which argues for high-frequency AI-adoption data, better job-transition tracking, and targeted monitoring of vulnerable occupations. Your paper would do the public-data version of that agenda: show what federal public data already allow, where the limits are, which incremental changes would generate the highest value, and what the ideal counterfactual data system would make possible. That also makes it directly useful for policy audiences like Senator Warner’s office, because the March 2026 Warner-Hawley letter asks agencies to expand CPS, JOLTS, and NLS-based AI measurement but does not specify, in a granular way, which additions are highest-yield and lowest-burden.
## 2. The core research question
The core question should be: What can the U.S. federal public-data system currently say, credibly and at what level of resolution, about AI’s impact on jobs, occupations, hiring, separation, wages, and worker transitions? Then the paper should answer a second question: What specific low-effort, medium-effort, and large-effort additions would most improve that measurement system? This framing is stronger than a generic “we need more data” argument, because it forces the paper to distinguish between what already exists, what already works, what fails under public-data constraints, and what would materially improve inference without requiring a full administrative redesign. That is also consistent with the spirit of the Warner letter, which explicitly points to CPS, JOLTS, and NLS as expandable instruments, and with BLS’s own recent work incorporating AI into occupational projections while acknowledging that the technology is dynamic and evidence remains uncertain.
## 3. The paper's main structure
I would structure the paper in six sections.
First, a section on what exists now. This should inventory the main public sources. The CPS is a monthly household survey of about 60,000 households, with a 4-8-4 rotation design, occupation data, labor-force status, and a long history of supplements on topics such as worker displacement and job tenure/occupational mobility. The CPS ASEC is an expanded annual supplement based on more than 75,000 households and is much richer on income and annual labor-market circumstances. BTOS is the main high-frequency public business-side source: it covers roughly 1.2 million businesses split into six panels, collects every two weeks, and publishes by sector, state, and the 25 largest metros. JOLTS is the main establishment-side flow survey for openings, hires, quits, layoffs, and separations, but it has a sample of about 21,000 establishments and does not currently collect occupation. NLS follows the same individuals over time and is well suited for long-run career dynamics, while NLSY27 is currently being planned, which makes it a live insertion point for AI questions. OEWS and O*NET are not transition sources, but they are essential public scaffolding: OEWS provides employment and wage estimates for about 830 occupations, and O*NET provides detailed task and worker-requirement descriptions across the occupational system.
Second, a section on what works today. The strongest current worker-side public measurement tool is CPS. Because it is monthly, large, and panel-like over adjacent months, it can support national estimates of occupational transitions at broad occupation levels and can track movements between employment, unemployment, and nonparticipation. The strongest business-side public source is BTOS. Its existing AI supplement already asks whether businesses use AI, in which functions they use it, whether AI performed tasks previously done by employees or supplemented them, whether employment increased or decreased, whether workers used AI or generative AI, what tasks they used it for, and what barriers prevented adoption. Together, CPS and BTOS already allow a serious public-data paper on AI adoption and labor-market outcomes, even before any new survey changes are proposed.
Third, a section on what does not work today. Public LEHD/J2J does not solve the occupation-transition problem, because the public-facing system is designed around worker reallocation across employers rather than a public occupation-to-occupation microdata file. JOLTS does not solve it either, because BLS explicitly states that JOLTS does not collect occupation information. And public data do not provide worker-firm linked records with both firm AI adoption and worker occupation transitions, which is the real reason public analysis cannot reach firm-by-firm causal precision. This negative section matters because it prevents the paper from sounding like a “just analyze what already exists” argument when important missing links are in fact real.
Fourth, a section on what could work with little effort, medium effort, and large effort. This should be the policy-design heart of the paper. I would treat “little effort” as things that fit naturally into existing public instruments and processing systems; “medium effort” as additions that are plausible but operationally nontrivial; and “large effort” as changes that require new infrastructure or data-linkage authority. CPS supplements are a clear low- to medium-effort route because Census explicitly notes that CPS supplements benefit from the survey’s large sample, experienced field staff, and generalized processing systems that can accommodate additional questions. BTOS is another low-effort route because AI questions are already in the field and the average respondent burden is about nine minutes. JOLTS is a medium- to high-effort route because it currently asks count-based flow questions, does not collect occupation, and even its current state estimates require model-based augmentation because the sample alone is too small for direct state estimation.
Fifth, a section on sample sufficiency. This is where you answer the “is each data point actually big enough to be useful?” question. The right answer is not yes or no in general; it depends on the resolution. CPS is sufficient for national analysis at broad occupational groupings, especially when pooling over months or years, but it is not strong enough for highly detailed occupation-by-state-by-month claims. BTOS is designed to publish by sector, state, and the 25 largest metros, so that level is credible for headline business-adoption analysis. JOLTS is already stretched enough at the state level that BLS uses modeled estimates, and BLS explicitly notes that the sample does not directly support sample-based state estimates and that cells with fewer than 30 respondents require heavy augmentation, with cells below five respondents relying entirely on the regional model. That means any proposal to add occupation detail to JOLTS should assume coarse categories, a rotating supplement, or annual rather than monthly outputs. Those sample-sufficiency judgments are partly inferential, but they are grounded in the official sample sizes and modeling rules.
Sixth, a section on the counterfactual ideal system. This is the “if we had the right data, what could we actually estimate?” section. The ideal system would link worker occupation, wages, and employment transitions to firm-level AI adoption and task redesign over time. That would allow estimates at the occupation-by-industry-by-state-by-worker-group level of hiring slowdowns, separations, wage compression, retraining, and occupational switching attributable to AI adoption. Manning’s brief explicitly calls for high-frequency AI-adoption data and enhanced tracking of job transitions, and the Warner letter explicitly calls for cross-agency linking and more detailed reporting. Your paper should make the value of that ideal system concrete, not abstract.
## 4. What the public-data paper can already do
If you want the paper to have an empirical spine rather than only a data-audit function, the best public-data design is a three-part stack.
The first layer is a worker-side outcome layer built from CPS. This gives you employment status, occupation, unemployment, nonparticipation, and broad transition dynamics. It is the right source for “are exposed occupations showing weaker hiring, higher unemployment, or more exits?” The second layer is a business-side adoption layer built from BTOS. This gives you sector-by-state-by-time measures of AI adoption, whether use is substitutive or augmentative, whether employment moved up or down, whether workers used generative AI, and what functions were affected. The third layer is an occupation mapping layer built from O*NET, OEWS, and BLS projections. O*NET provides tasks and worker requirements; OEWS provides employment and wage levels for occupations; and BLS projections now explicitly discuss how AI is being incorporated into occupational case studies. That combination is the public-data analogue of the private-data stack used in papers like Anthropic's.
## 5. Low-effort, medium-effort, and large-effort recommendations
The lowest-effort and highest-value recommendation is not to invent a new survey, but to make better use of what is already being fielded. BTOS already has a sophisticated AI module. The immediate research opportunity is to use the existing public BTOS AI time series as the benchmark business-side adoption series, then link it analytically to CPS worker outcomes at the occupation-group level. That alone would materially improve the public understanding of AI’s labor-market effects. Because BTOS already collects every two weeks, covers roughly 1.2 million businesses through rotating panels, and has an average completion time of about nine minutes, it is the clearest example of a relatively low-burden survey that already yields a lot.
The next best low-effort move is a CPS supplement or short AI module. CPS is already the main worker-side labor-market instrument, and Census explicitly says the supplement framework is designed to accommodate additional questions. This is also more valuable than it may first appear, because the CPS already contains occupation, labor-force status, and panel continuity across months. A small AI module therefore buys much more analytical value than the same question would in a standalone one-off poll. Historically, CPS has already fielded supplements on worker displacement and on job tenure/occupational mobility, which makes an AI-focused labor module institutionally plausible.
The medium-effort option is to use JOLTS, but in a narrower way than the Warner letter suggests. Asking JOLTS to add full occupation and wage detail for all new hires and all separations in the core monthly instrument is probably too burdensome relative to the current survey design. JOLTS currently asks only for counts of openings, hires, quits, layoffs/discharges, and other separations, and BLS states plainly that it does not collect occupation. On top of that, the 21,000-establishment sample is already not enough for direct state estimation and requires a model-based system with augmentation rules at low respondent counts. The more realistic version is an annual or rotating JOLTS supplement with coarse occupation groups and wage bands, not a heavy rewrite of the monthly core. That still has real value because it would add the demand-side flow piece that CPS lacks.
The medium-effort, long-horizon option is NLS. NLS is built to follow the same individuals over time, and the new NLSY27 cohort is currently in planning. That makes it the right place to insert questions on AI use at work, retraining, occupational switching, perceived exposure, and career expectations. This is not the right instrument for near-real-time monitoring, but it is the best public federal vehicle for understanding persistent career effects and intergenerational labor-market adaptation.
The large-effort option is the administrative or linked-data ideal: worker-job-quarter occupation transitions linked to employer AI adoption. That is the true counterfactual system. It is analytically the best, but it is not the right starting point for a public-data paper and it is not where the highest marginal policy value lies today. Manning’s brief is useful here because it argues both for high-frequency adoption data and for better job-transition tracking; your paper can show exactly how much of that agenda can already be approximated with public data, and exactly where the public system still fails.
## 6. What to ask in each survey, and what it would enable
For CPS, the most useful short module would ask workers whether they used AI or generative AI at work in the past week or month, whether AI mostly assisted tasks, replaced tasks, or created new tasks, whether AI changed their hours/pay/workload, whether they received AI-related training, and, for the unemployed or recent job losers, whether AI or automation contributed to their separation or made it harder to find comparable work. Because CPS already has occupation, employment status, hours, demographics, and in some cases earnings, those additions would enable direct worker-level analysis of AI use and labor outcomes by occupation and worker type. This is my recommendation, but it is rooted in the existing CPS design and supplement structure.
For BTOS, the best additions are not many more questions, but more targeted ones. BTOS already asks whether firms use AI, where they use it, whether it replaced or supplemented tasks, whether employment rose or fell, what organizational changes were needed, whether employees use AI or generative AI, what tasks they used it for, and why firms are not adopting it. The highest-value additions would be one or two questions about the share of workers affected and the occupational location of those effects, for example whether the employment effect was concentrated in administrative, technical, customer-facing, or managerial roles. That would enable a much better bridge from business adoption to worker outcomes without turning BTOS into a full occupational survey.
For JOLTS, the right question is not “collect everything by occupation,” but “what is the smallest addition that reveals AI-related labor demand and turnover?” The cleanest ask is probably an annual or rotating supplement that collects coarse occupation groups and wage bands for openings, hires, quits, and layoffs, plus a question on whether some portion of openings, hires, or separations was directly related to AI adoption or AI-enabled process change. That would enable occupation-level demand and turnover analysis. I would not recommend trying to make this part of the monthly core immediately, because the current JOLTS instrument is much lighter and the sample is already thin enough that state estimates rely on heavy modeling. That burden judgment is mine, but it follows directly from the current JOLTS design and sample constraints.
For NLS, the questions should be richer and longitudinal: AI use in the current job, task changes, training received, perceived replacement risk, changes in promotion prospects, changes in occupational aspirations, and whether the respondent switched occupations or accepted lower pay because of technological change. This would enable long-run analysis of AI’s effects on career paths rather than short-run disruption only. Since NLS is already designed for life-course labor-market tracking and NLSY27 is still being planned, this is a real opportunity rather than a theoretical one.
## 7. How to answer the "is the sample enough?" question
I would make this explicit in the paper as a resolution rule.
At the national level, CPS is enough for broad occupational group analysis and for pooled monthly or annual transition estimates. At the state-by-month or detailed-occupation level, CPS becomes much less reliable, so the paper should avoid overclaiming and either pool aggressively or suppress cells. ASEC is better than monthly CPS for richer annual subgroup analysis because it has a larger sample, but it is not the right instrument for high-frequency transition measurement. BTOS is strong enough for sector, state, and large-metro business-adoption monitoring because that is exactly how Census publishes it. JOLTS is adequate for national flow measures, but even state estimates are model-based because the sample is not large enough to support direct state estimation. These are the key sufficiency boundaries the paper should state plainly.
My recommendation is to adopt an internal rule like this: national monthly analysis at broad occupation groups is publishable; national annual analysis can go somewhat finer; state analysis should stay coarse and usually be annual or pooled; anything finer than that should be presented as exploratory rather than definitive. Those thresholds are analytical choices, not federal standards, but they are the right way to keep the paper credible given the official sample sizes and design constraints.
## 8. The concrete contribution to policy
The paper’s policy value is that it would turn vague calls for “better data on AI and work” into a precise measurement roadmap. Warner’s letter identifies CPS, JOLTS, and NLS as candidate vehicles; Manning argues for high-frequency adoption tracking and better job-transition measurement; Anthropic shows what a private-data stack can do. Your paper can connect those dots for the public-data world by answering four concrete questions: what we can already measure, where the data are too thin, which survey additions have the highest payoff per unit of burden, and what the true ideal system would unlock if government later wants to go beyond public data. That is a more useful contribution than either a purely empirical paper with weak data or a purely policy paper with generic recommendations.
A strong title would be something like: “Measuring AI’s Labor-Market Effects with Public Federal Data: What Exists, What Works, and What Small Survey Changes Would Unlock.” That title accurately reflects both the descriptive and design components of the project.

## Policy and briefing artifacts (repository; additive to the paper)

The repo ships **separate** senator- and staff-facing documents and visuals built from the same reproducible `figures/` and `intermediate/*_run_metadata.json` lineage as the empirical stack. They do not replace the paper; they translate measurement limits and Virginia-relevant benchmarks into briefing-ready form. Entry points: `docs/senate_briefing_memo.md` (full narrative, executive summary, visual decision table, federal action matrix, non-claims), `docs/senate_briefing_evidence_baseline_va.md` (frozen headline values), `docs/senate_briefing_lineage_va.md` (metric-to-source appendix), `docs/senate_briefing_script_va.md`, `docs/senate_briefing_qa_va.md`, `docs/senator_handout_1page_va.md`, `docs/senator_packet_order_va.md`. Virginia QCEW-derived tables and `va01`–`va08` stems: `docs/virginia_deep_dive.md`, `docs/figure_catalog.md`. Build/QA: `scripts/run_memo_visuals_build.py` and `scripts/run_memo_visuals_qa.py` (`docs/replication.md`). Claim discipline for testimony: `docs/claim_audit.md` (Senator brief claim ledger). Treat these outputs as **descriptive monitoring** only, not causal AI effect estimates.

## AWES and ALPI (repo monitoring metrics; non-causal)

**AWES.** The Adoption-Weighted Exposure Score (AWES) is an occupation-time descriptive metric defined as the product of the paper’s normalized O*NET/OEWS exposure score and an occupation-specific BTOS adoption mix constructed from OEWS occupation–sector employment weights and BTOS sector-time AI-use shares. AWES complements, but does not replace, the paper’s frozen AI-relevance terciles (`intermediate/ai_relevance_terciles.csv`). Output: `metrics/awes_occ22_monthly.csv`. AWES is not a causal estimate.

**ALPI.** The AI Labor Pressure Index (ALPI) is an occupation-time descriptive pressure metric defined as the equal-weight average of three percentile-scaled components: AWES (as percentile rank), occupation-weighted sector demand stress from JOLTS/CES, and trailing 12-month CPS exit-risk vulnerability. ALPI complements, but does not replace, the paper’s frozen AI-relevance terciles and should be interpreted as a monitoring/prioritization index rather than a causal estimate. Output: `metrics/alpi_occ22_monthly.csv`.

—-----------------



I also do not think your exact review already exists in one place. The closest precursors I found are: the BLS-commissioned report on automation data needs, which is concept-and-gap oriented; the Federal Reserve note summarizing current AI-uptake surveys, which is about survey comparisons rather than the full federal labor-data architecture; Sam Manning’s brief, which is a policy memo rather than a source-by-source audit; and the March 2026 bipartisan Senate letter, which points to CPS, JOLTS, and NLS but does not deeply map each source. I did not find a single public document that systematically walks through the major U.S. public labor datasets one by one, explains exactly what each observes, separates public from restricted boundaries, and rates each source for AI-and-work measurement. That gap is likely real, though I would phrase it carefully in the paper as “we are not aware of a source-by-source public-data audit of this kind,” not as an absolute claim.
The best organizing template for each source is this: unit of observation; universe/coverage; cadence; geography; occupation detail; transition information; AI information; strengths; hard limits; and role in your paper. If you use that template consistently, the paper becomes much clearer and much easier to compare across sources.
1. Current Population Survey (CPS, basic monthly)
The CPS is the core public worker-side dataset. It is a monthly household survey of about 60,000 eligible households, run by Census for BLS, and it provides employment, unemployment, hours, earnings, and not-in-the-labor-force status. It is the single best public source for near-real-time worker outcomes and broad occupational transitions. BLS also notes that periodic CPS supplements cover worker displacement, employee tenure, and occupational mobility.
What you observe publicly is the person. That matters. CPS sees people, not firms and not jobs as administrative objects. Its strength is that it captures labor-force status, demographics, and occupation directly from households. Its weakness is that it does not observe employer-side AI adoption or establishment identifiers in the way a business survey would. So CPS is excellent for “what is happening to workers?” but weak for “which adopting firms caused it?”
For your research, CPS is the best public source for questions like: Are workers in certain occupations showing higher exits to unemployment? Are exposed occupations seeing lower hours or weaker employment? Are broad occupation-to-occupation transitions changing over time? It is not the best source for firm adoption, vacancy detail, or establishment-level demand. In your paper, CPS should be treated as a core source, not a supporting one.
2. CPS Annual Social and Economic Supplement (CPS ASEC)
CPS ASEC is the annual deep-income and work-history layer on top of the CPS. Census describes it as providing annual estimates from a survey of more than 75,000 households, with detailed questions on social and economic characteristics, previous-year income, poverty, work experience, program participation, and related variables.
ASEC is weaker than the monthly CPS for immediate transitions, but much stronger for annual economic well-being. If your question is not only “did an occupation lose jobs?” but also “did affected workers see income losses, poverty changes, or shifts in work experience?”, ASEC is the best public federal survey source. Census also notes that it is not designed to provide county-level direct estimates in most places, which is a reminder that its strength is national and state analysis, not local precision.
In your paper, ASEC should be treated as the best public annual worker-welfare companion to the basic CPS. It deepens the worker side; it does not replace the monthly CPS for transition timing.
3. CPS Displaced Worker / Job Tenure / Occupational Mobility supplements
These supplements are extremely important for your project because they are the closest thing in the public worker-side system to “structured transition” questions. Census lists the Displaced Worker supplement as providing data on workers who lost a job in the last five years due to plant closing, shift elimination, or other work-related reasons, and the Job Tenure/Occupational Mobility supplement as measuring tenure with the current employer and in the current occupation. CPS methodology also notes that supplements are widely used precisely because the CPS has a large sample and broad population coverage.
This matters conceptually. The basic CPS gives you inferred transitions from repeated interviews; these supplements give you direct questions on displacement, tenure, and mobility. That makes them especially valuable for distinguishing normal churn from involuntary loss or occupational change. The drawback is cadence: they are periodic, not monthly core features.
For your paper, these should be treated as high-value special modules, especially if you want to argue that modest additions to CPS could dramatically improve AI-work measurement without building a whole new survey.
4. Survey of Income and Program Participation (SIPP)
SIPP is the best public federal longitudinal household survey for richer monthly life-course dynamics. Census describes it as a nationally representative longitudinal survey that interviews individuals for several years and provides monthly data on changes in employment, household composition, income, and program participation.
Relative to CPS, SIPP is less useful for headline near-real-time labor monitoring, but much better for questions like: how long do workers remain displaced, how do occupational shifts interact with household finances, how does income volatility evolve after a labor-market shock, and what happens to benefit use after occupational change? That makes SIPP especially important if your argument is that AI’s impact cannot be measured purely through payrolls or unemployment counts.
In your paper, SIPP should be a core longitudinal worker-side source, but not the first dataset readers see. CPS should come first, SIPP second.
5. American Community Survey Public Use Microdata Sample (ACS PUMS)
ACS is the largest public household microdata source with occupation and geography, but it is primarily cross-sectional rather than your main transition engine. Census says ACS PUMS gives person and housing-unit records with disclosure protection, and the most detailed geography in public PUMS is the PUMA. Census also explains that occupation in ACS is derived from write-in responses that are autocoded and clerically coded, with a 2018 system of 570 occupation categories arranged into 23 major groups.
ACS is extremely valuable for occupation distributions, local geography, worker characteristics, and subgroup measurement. It is much better than CPS for fine geographic structure and large-sample descriptive work. But it is weaker for short-horizon transitions because public ACS is not the obvious place to recover adjacent-month or adjacent-quarter labor movement. Its role is to describe where workers are and what kinds of workers occupy each occupation, not to give you clean public transition flows.
In your paper, ACS should be treated as a descriptive and calibration source: where exposed occupations live, what demographic groups they contain, how local labor markets differ, and how occupational composition maps geographically.
6. National Longitudinal Surveys (NLS, especially NLSY97 / planned NLSY27)
The NLS system is the best public long-horizon individual panel for studying careers, training, and long-run adjustment. The NLSY97 follows 8,984 respondents first interviewed as youth and now surveyed into adulthood, with topics including job characteristics, training, labor-market status and histories, income, geography, and expectations. Public-use data are available through the NLS Investigator at no cost. BLS is also currently planning a new youth cohort, NLSY27.
This source is not for high-frequency monitoring. It is for deep questions: who adapts, who retrains, who falls behind, how occupations evolve across decades, and whether early AI exposure affects later career trajectories. That is why the March 2026 Senate letter points to NLS as a promising place to add AI questions.
In your paper, NLS should be a strategic medium-effort source: not the best for “what is happening this month,” but probably the best public federal vehicle for “what does AI change over an entire career?”
7. Business Trends and Outlook Survey (BTOS)
BTOS is the best public high-frequency business-side AI dataset currently available. Census says the sample is about 1.2 million businesses split into six panels, with collection every two weeks. The public BTOS data cover business conditions, revenues, employment, hours, demand, and prices. The BTOS AI work shows that the AI supplement added 13 detailed questions beyond two core AI questions, covering AI type, business functions, worker-task effects, employment effects, and barriers to future use.
This is the source closest to “real-time AI adoption.” It is business-side, not worker-side. That means it is excellent for the question “which firms or sectors say they are using AI, in what way, and with what reported employment effect?” It is not good for following specific workers. BTOS is also experimental, and the detailed supplement only ran for a period, while the core AI questions remained.
For your paper, BTOS should be treated as the core public firm-adoption source. If CPS is your core worker-side series, BTOS is its natural business-side counterpart.
8. Annual Business Survey (ABS)
ABS is the best public annual firm-side source for richer technology adoption and workforce impacts. Census says ABS provides economic and demographic characteristics of businesses and owners, covers nonfarm employer businesses filing certain tax forms, and is conducted on a firm basis rather than an establishment basis. Public ABS technology tables include extent of technology use, motivations, workforce impacts, types of workers affected, adverse factors, and technology production.
The key difference from BTOS is cadence and richness. BTOS is fast and high-frequency; ABS is annual and structurally deeper. ABS is therefore better for understanding broader adoption patterns, motivations, and stated workforce effects over longer windows. It is worse for real-time change. Because ABS is firm-based rather than establishment-based, it is also less precise for local labor-demand mechanics than something establishment-centered would be.
In your paper, ABS should be a core annual firm-side source. BTOS tells you what is happening now; ABS tells you more about the structure of adoption and its reported workforce implications.
9. Job Openings and Labor Turnover Survey (JOLTS)
JOLTS is the core public labor-demand flow survey, but it is not occupation-aware. BLS says JOLTS samples about 21,000 establishments and measures total employment, job openings, hires, quits, layoffs/discharges, and other separations. BLS also makes clear that the national sample supports national major-industry estimates and that state estimates rely on model-assisted methods. The March 2026 Senate letter explicitly highlights that JOLTS does not currently provide understanding of labor demand by occupation.
This makes JOLTS analytically important but incomplete. It is the best public federal source for “what is happening to labor demand and turnover flows?” but it cannot directly answer “which occupations are being hired less because of AI?” That is why it sits at the center of the policy discussion: it already captures the right flow objects, but it lacks the occupational layer.
In your paper, JOLTS should be treated as a near-core demand-flow source whose central limitation is exactly what policymakers now want to fix.
10. Quarterly Census of Employment and Wages (QCEW)
QCEW is the highest-coverage public establishment/payroll backbone. BLS says it publishes quarterly counts of employment and wages reported by employers, covering more than 95 percent of U.S. jobs, with county, state, and national detail by detailed industry. It is sourced primarily from state UI programs and includes establishment counts, monthly employment, and quarterly wages.
QCEW is not an occupation dataset and not a worker-transition dataset. It is an establishment-industry-wage-count dataset. That makes it extremely strong for industry geography, local labor-market structure, and benchmarking employment and wages. It is very weak for the specific questions of worker occupation switching or business AI use.
In your paper, QCEW should be a structural benchmark source: the denominator for industry-employment size, local exposure, and payroll geography, not the main source for occupational transitions.
11. Current Employment Statistics (CES)
CES is the monthly payroll survey. BLS says it produces detailed industry estimates of nonfarm employment, hours, and earnings from businesses and government agencies, using worksites drawn from unemployment-insurance tax accounts. It is monthly, industry-based, and establishment-centered.
Relative to QCEW, CES is faster and more survey-based; relative to CPS, it is establishment-side and lacks demographic detail. CES is useful for tracking rapid industry-level employment, hours, and earnings movements, which can matter if your theory is that AI first shows up in payroll patterns before appearing in unemployment or occupational reallocation. But CES does not give occupation, worker transitions, or direct AI measures.
In your paper, CES is a supporting cyclical indicator, not a primary AI source.
12. Business Employment Dynamics (BED)
BED is the public establishment-flow series derived from longitudinal establishment histories. BLS explains that BED calculates gross job gains and losses, openings and closings, using longitudinal histories of establishments. This is valuable because it moves beyond levels and into dynamics.
BED is still establishment-based and private-sector oriented. It can tell you about job creation and destruction dynamics, which is important if AI shifts churn even when net employment looks stable. But it does not provide occupation, worker demographics, or direct AI adoption. So its role is to reveal establishment dynamism, not worker experience.
In your paper, BED is a supporting flow series that can complement JOLTS and CES, especially for establishment openings, closings, and gross job reallocation.
13. LEHD public products (QWI, J2J, LODES, PSEO)
LEHD is crucial conceptually, but the public/restricted boundary matters a lot. Census states that LEHD microdata are available only to approved researchers in the FSRDC network, while public tabular products include QWI, LODES, J2J, and PSEO.
Public LEHD products are extremely useful for worker-employer dynamics in aggregate form, especially job-to-job flows and local employment patterns. But they are not public microdata. That distinction is important for your paper because many people hear “LEHD” and assume they can do worker-level linked analysis publicly; they cannot. For a public-data-only project, LEHD public products are informative but not a substitute for restricted linked microdata.
In your paper, LEHD should be treated as a boundary case: public outputs are useful, but the source also illustrates the line between what the public system can tabulate and what only restricted microdata can reveal.
14. Occupational Employment and Wage Statistics (OEWS)
OEWS is the core public occupation-by-wage dataset. BLS says it produces employment and wage estimates for about 830 occupations, with national, state, metro, nonmetro, and industry-specific estimates. It covers wage-and-salary workers in nonfarm establishments but excludes the self-employed and some other groups.
This is not a transition source and not an AI source. It is the best official public map from occupations to employment and wages. That makes it indispensable for baseline sizing: how many workers are in an occupation, where they are, and how much they earn. It is especially useful when you want to convert “AI exposure” or “AI usage” rankings into labor-market counts or wage distributions.
In your paper, OEWS is a core occupation-structure source. It should sit alongside O*NET, not replace worker or firm surveys.
15. O*NET
O*NET is the core public task-and-skill ontology for occupations. The O*NET database contains rich variables on work and worker characteristics, including skills, work activities, technology, and tasks; it covers U.S. occupations and is updated quarterly, with major annual updates. The current release notes list hundreds of updated occupations and downloadable database formats.
O*NET is not a labor-market outcome dataset. It does not tell you who lost a job, who adopted AI, or what wages changed last month. What it does is give you the task structure needed to operationalize exposure, complementarity, substitutability, and task reallocation hypotheses. This is why so much AI-and-work research uses O*NET.
In your paper, O*NET is a core explanatory scaffold, not an outcome source. It should be used to classify occupations, not to claim realized labor-market effects by itself.
16. Employment Projections / Occupational Outlook Handbook (OOH)
The BLS Employment Projections program publishes 10-year national projections by industry and occupation, using historical and current economic data. BLS has now explicitly incorporated AI-related impacts into some occupational case studies and employment projections discussions.
This source is not a realized-outcomes dataset. It is a model-based forecast and interpretation layer. Its value for your project is that it shows what the federal government currently thinks AI might do to occupation trends, and how much of that thinking is already entering official projections. Its weakness is that it is not evidence of realized impact.
In your paper, Employment Projections and OOH are interpretive benchmark sources: important for policy context, but not substitutes for actual observed worker or firm data.
How I would rank the sources for your project
If the paper is about public measurement of AI’s labor-market effects, the true core stack is: CPS, CPS ASEC / CPS supplements, SIPP, BTOS, ABS, JOLTS, OEWS, and O*NET. QCEW, CES, BED, ACS, NLS, LEHD public products, and Employment Projections are all valuable, but they are either supporting structure, specialized long-horizon sources, or public aggregates that do not solve the main inference problem by themselves.
The deeper point is this. No single public source gives you the full causal object you would ideally want: worker occupation transitions linked to employer AI adoption and wage changes over time. The public system is fragmented across worker surveys, business surveys, establishment flow series, and occupational scaffolds. That fragmentation is exactly why your paper is useful. It can show that the public-data problem is not a lack of data in general; it is a lack of one integrated public architecture. 

—----------------


Below is a first-pass dataset audit sheet you can use in the paper. I grouped it by source type to keep it readable. I am not aware of a single existing paper that already does this exact source-by-source public-data audit for U.S. AI-and-work measurement. The closest things I found are: a BLS gap-analysis report on technology and labor-market measurement, a Federal Reserve note comparing AI-uptake surveys, Sam Manning’s policy brief on AI labor-market monitoring, and the March 2026 Warner-Hawley Senate letter calling for better federal AI workforce data. Those are useful precursors, but none of them appear to provide this exact public-data audit sheet.
Sample sufficiency below is my practical assessment for your use case based on the official sample sizes, coverage, cadence, and level of detail in the source docs.
Worker and household sources
Source
Unit
Frequency
Geography
Occupation detail
Transitions
AI variables
Strengths
Weaknesses
Sample sufficiency
Best use in the paper
CPS (basic monthly)
Person / household
Monthly
National; states via published outputs
Yes, public occupation variables
Yes, via matched-month person panels; also employment/unemployment/NILF flows
No core AI module today
Best public near-real-time worker dataset; strong labor-force status, demographics, occupation, hours, earnings
No employer adoption data; public files are sample-based, not administrative
High for national broad occupation analysis; medium/low for detailed occupation × state × month
Core worker-outcome and public transition source.
CPS ASEC
Person / household
Annual
National and state-level analysis
Yes
Limited direct transition power; strong annual work/income context
No dedicated AI variables
Best public annual worker-welfare layer: income, poverty, work experience
Not designed for high-frequency transitions
High for national annual subgroup analysis; weaker for short-run dynamics
Annual welfare and distributional companion to CPS.
CPS Displaced Worker / Job Tenure / Occupational Mobility supplements
Person
Periodic / supplement schedule
National; some state use possible with pooling
Yes, including former/current occupation in relevant modules
Yes, directly for displacement, tenure, and occupational mobility concepts
No AI variables currently
Closest public worker-side modules to structured displacement/mobility questions
Intermittent, not continuous
High for national episodic analysis; not a continuous monitoring tool
Best precedent for adding an AI module to CPS.
SIPP
Person / household
Panel survey with monthly data over several years
National
Yes
Yes, monthly employment and household changes over time
No dedicated AI module
Richest public longitudinal household survey for earnings volatility, benefit use, family adjustment
Smaller / less timely than CPS for headline monitoring
High for longitudinal national analysis; not ideal for near-real-time monthly monitoring
Best source for medium-run adjustment after occupational shocks.
ACS PUMS
Person / housing unit
Annual (1-year / 5-year PUMS products)
Nation, region, state, PUMA
Yes, coded occupation in public microdata
No clean short-horizon transitions
No
Huge descriptive power; excellent for local occupational composition and subgroup structure
Public geography bottoms out at PUMA; not the right transition engine
High for descriptive levels and subgroup maps; low for short-run transitions
Best descriptive baseline for who is in which occupation and where.
NLSY97 / NLS public-use
Person
Longitudinal; annual then biennial for NLSY97
National
Yes
Yes, over long horizons
No dedicated AI module today
Best public federal source for careers, retraining, life-course dynamics
Too slow/small for real-time monitoring; cohort-specific
High for long-run career analysis; low for current macro monitoring
Best place to study persistent career adaptation and a prime vehicle for future AI questions.

Business, establishment, and payroll sources
Source
Unit
Frequency
Geography
Occupation detail
Transitions
AI variables
Strengths
Weaknesses
Sample sufficiency
Best use in the paper
BTOS
Business
Biweekly collection; panel rotates over year
National, state, sector, large metros
No occupation-by-worker detail
No worker transitions; some employment-change reporting
Yes — core AI questions plus supplement content
Best public high-frequency business-side AI source; large sample; timely
Experimental series; limited occupational granularity
High for sector/state business-adoption monitoring
Core public firm-adoption source and the main business-side counterpart to CPS.
ABS
Firm
Annual
National; many tables by firm characteristics
Limited; not a worker-occupation file
No worker transitions
Yes — innovation/technology modules, workforce impacts
Richer annual structural view of technology adoption and reported workforce effects
Firm-level annual survey, not high-frequency and not establishment/local-flow oriented
High for annual national structural analysis
Best annual business-side source for technology adoption, motivations, and reported workforce effects.
JOLTS
Establishment
Monthly
National; industry; modeled state estimates
No occupation field in core survey
Yes for openings, hires, quits, layoffs, other separations
No direct AI variables
Best public labor-demand flow survey
No occupation in core; sample is modest for detailed state/occupation slicing
High nationally; medium/low for fine state/detail work
Best public demand-flow source and the strongest case for a targeted AI/occupation supplement.
QCEW
Establishment / employer report
Quarterly
County, state, national
No occupation
No worker transitions
No
Near-census employment and wage backbone; >95% of U.S. jobs
Industry/payroll structure only; no occupation, no AI, no worker linking in public use
Very high for industry-geography denominators
Benchmark employment/wage structure and local industry exposure.
CES
Worksite / establishment
Monthly
National, state, metro
No occupation
No direct transitions
No
Fast payroll signal on employment, hours, earnings by industry
No occupation, no worker demographics, no AI
High for industry-cycle monitoring
Supporting cyclical series for payroll/hours/earnings movements.
BED
Establishment / firm histories built from QCEW
Quarterly
National and detailed cross-sections in releases
No occupation
Yes, but establishment job gains/losses, openings/closings — not worker flows
No
Best public establishment dynamism / gross job flow series
No worker-level transitions or occupation
High for establishment-flow analysis
Complement to JOLTS and CES for job creation/destruction dynamics.
LEHD public products (QWI / J2J / LODES / PSEO)
Public aggregates built from linked admin data
Mostly quarterly / periodic by product
National, state, local depending on product
Limited publicly; not a public worker-level occupation file
Yes in aggregate for worker-employer dynamics, especially J2J
No AI variables
Public outputs are powerful for job-to-job and local employment patterns; derived from linked admin data
Underlying microdata are restricted; public products are aggregates, not open worker-level linked files
High for aggregate dynamics; not sufficient for public worker-level occupation transition estimation
Boundary case showing what public tabular admin products can and cannot do.

Occupational scaffolds and interpretation layers
Source
Unit
Frequency
Geography
Occupation detail
Transitions
AI variables
Strengths
Weaknesses
Sample sufficiency
Best use in the paper
OEWS
Occupation × geography / industry estimates
Annual
Nation, state, metro/nonmetro, industry
Very high — ~830 occupations
No
No
Best official public employment-and-wage map for occupations
No transitions; excludes self-employed and some groups
Very high for occupational employment/wage baselines
Core occupation sizing and wage baseline source.
O*NET
Occupation descriptors / task and skill variables
Quarterly updates
National occupational taxonomy
Very high task/skill detail
No realized transitions
No direct outcome AI vars, but strong technology/task descriptors
Best public task/skill ontology for exposure/complementarity hypotheses
Not an outcome dataset; cannot measure realized labor impacts alone
Very high as an explanatory scaffold
Core task/skill layer for exposure mapping and mechanism design.
Employment Projections / OOH
Occupation / industry projections
Annual release cycle; 10-year horizon
National
High
No realized transitions; forecasted change only
No direct AI variable, but BLS now discusses AI in projection context
Best official forward-looking interpretation layer
Model-based projections, not observed effects
High for scenario framing; not for causal measurement
Interpretive benchmark for what official forecasts think AI may change.

Bottom-line ranking for your paper
If you want the shortest, most defensible “core stack,” I would define it this way:
Worker side: CPS, CPS ASEC, CPS supplements, SIPP.
 Business side: BTOS, ABS, JOLTS.
 Occupational structure / mechanism layer: OEWS, O*NET.
 Benchmark / support layer: QCEW, CES, BED, ACS PUMS, LEHD public products, NLS, Employment Projections. 


—---



Below is a scored matrix. The scores are analytical judgments for this specific paper on public federal data and AI/work measurement.
Scale: 1 = weakest, 5 = strongest.
 For implementation burden, 5 = easiest / lowest-burden to use in this project with public data; 1 = hardest / highest-burden.
Scored matrix
Source
Relevance to AI
Transition power
Occupational resolution
Geographic resolution
Timeliness
Implementation burden
CPS (basic monthly)
4
5
4
3
5
4
CPS ASEC
3
2
4
3
2
4
CPS supplements (Displaced Worker / Job Tenure / Occupational Mobility)
4
4
4
2
1
3
SIPP
4
4
4
2
2
2
ACS PUMS
3
1
5
5
2
3
NLSY97 / NLS public-use
4
4
4
2
1
2
BTOS
5
2
1
4
5
4
ABS
4
1
1
3
2
4
JOLTS
4
4
1
3
5
4
QCEW
3
1
1
5
3
5
CES
3
1
1
4
5
5
BED
3
3
1
3
3
4
LEHD public products (QWI/J2J/LODES/PSEO)
4
4
1
4
3
3
OEWS
4
1
5
5
2
5
O*NET
5
1
5
1
3
4
Employment Projections / OOH
3
1
4
1
2
5

How to read the scores
The highest-value worker-side source is CPS: it is monthly, nationally representative, occupation-aware, and has real transition power because the same people can be linked across months in the public files. That is why it scores highest on transition power and timeliness.
The highest-value business-side AI source is BTOS: it is unusually timely, has a very large sample, and already contains explicit AI questions, including detailed supplement questions on use cases, worker-task effects, and employment effects. Its main weakness is that it does not observe worker occupations directly.
The best occupation-structure sources are OEWS and O*NET. OEWS gives the cleanest public map of employment and wages by occupation and geography, while O*NET gives the richest public map of tasks, skills, and work activities. Neither one has real transition power, which is why they score 1 there.
The best demand-flow source is JOLTS, because it directly measures openings, hires, quits, layoffs, and other separations. But it scores very low on occupational resolution because the public JOLTS system does not provide occupation-level demand data.
The largest gap in the public system is visible in the combination of these scores: no single public dataset scores highly on AI relevance + transition power + occupational resolution at the same time. CPS is strong on transitions and occupations but weak on direct AI. BTOS is strong on AI but weak on worker occupation. JOLTS is strong on labor-demand flows but weak on occupation. OEWS and O*NET are strong scaffolds but not outcome datasets.
My practical ranking for the paper
If you want a core empirical stack, I would rank it:
CPS


BTOS


JOLTS


OEWS


O*NET


SIPP


CPS supplements / ASEC


That stack gets you the closest possible public-data approximation to: worker outcomes, business AI adoption, labor-demand flows, occupational structure, and task exposure.

—----------------


A dataset-to-claim matrix is the better choice for the paper. It is more explicit than a heatmap and makes the overclaim boundaries visible.
Legend
 ✓ = can directly support this claim with public data
 △ = can support it only indirectly, partially, or with important caveats
 ✗ = cannot support this claim with public data
Dataset-to-claim matrix
Source
Worker outcomes
Worker occupational transitions
Firm AI adoption
Labor demand / turnover
Occupational structure / wages
Task exposure / mechanism
Local geographic exposure
Worker–firm AI causal claims
CPS (basic monthly)
✓
✓
✗
△
△
✗
△
✗
CPS ASEC
✓
△
✗
✗
△
✗
△
✗
CPS supplements
✓
✓
✗
✗
△
✗
✗
✗
SIPP
✓
✓
✗
✗
△
✗
△
✗
ACS PUMS
✓
✗
✗
✗
✓
✗
✓
✗
NLSY / NLS public-use
✓
✓
✗
✗
△
✗
△
✗
BTOS
△
✗
✓
△
✗
△
✓
✗
ABS
△
✗
✓
✗
✗
△
△
✗
JOLTS
✗
✗
✗
✓
✗
✗
△
✗
QCEW
△
✗
✗
✗
✗
✗
✓
✗
CES
△
✗
✗
✗
✗
✗
✓
✗
BED
✗
✗
✗
✓
✗
✗
△
✗
LEHD public products (QWI/J2J/LODES/PSEO)
△
△
✗
✓
✗
✗
✓
✗
OEWS
✗
✗
✗
✗
✓
✗
✓
✗
O*NET
✗
✗
✗
✗
△
✓
✗
✗
Employment Projections / OOH
✗
✗
✗
✗
△
△
✗
✗

Exact reading of the matrix
CPS
CPS can directly support claims about employment, unemployment, hours, earnings, and broad occupational transitions because it is a monthly household survey with occupation and labor-force-status information, and the public files allow matched-month analysis. It cannot support direct claims about firm AI adoption or worker–firm causal effects, because it does not observe employer AI behavior. It only partially supports local analysis because its public-use structure is much stronger nationally than at detailed local-by-occupation resolution.
CPS ASEC
ASEC can directly support claims about annual worker outcomes and income-related consequences, and it can partially support occupational mobility and structure questions, but it is not the right source for high-frequency transitions or labor-demand flows. It also has no direct AI adoption variable.
CPS supplements
The Displaced Worker and Job Tenure / Occupational Mobility supplements can directly support claims about displacement, tenure, and occupational mobility because they ask those questions explicitly. They do not support firm-side AI or demand-flow claims unless new AI questions are added.
SIPP
SIPP can directly support claims about worker outcomes and longer-run worker transitions, because it is a longitudinal survey with monthly data on employment and economic circumstances over several years. It cannot support direct firm-adoption or labor-demand claims.
ACS PUMS
ACS PUMS is very strong for occupational structure, worker composition, and geography, because it provides public microdata with state and PUMA geography. It is not the right source for short-horizon occupational transitions or firm AI adoption.
NLSY / NLS
The NLS public-use data can support claims about career trajectories, training, and long-run worker transitions, because they follow the same individuals over time and include job characteristics, training, and labor-market histories. They are not suited to current macro monitoring or direct employer AI adoption.
BTOS
BTOS is the strongest public source for firm AI adoption and can partially support claims about employment effects and organizational change, because the AI supplement asks businesses about AI use, the functions where AI is used, and employment/task effects. It cannot support worker occupational transitions directly because the unit is the business, not the worker.
ABS
ABS can directly support annual claims about firm technology adoption and reported workforce impacts, including technology use and impacts on workers or worker types. It cannot support worker transitions or real-time labor-demand flows.
JOLTS
JOLTS can directly support claims about labor demand and turnover because it measures job openings, hires, quits, layoffs and discharges, and other separations. It cannot directly support occupational claims because the public JOLTS system does not provide occupation detail in the core data.
QCEW
QCEW is excellent for local geographic employment and wage structure by industry, because it covers more than 95 percent of U.S. jobs at county, state, and national levels. It does not support worker transitions, occupation, or AI adoption directly.
CES
CES can partially support worker-outcome claims only in the narrow sense of industry payroll employment, hours, and earnings trends. It does not support worker-level occupation, transitions, or AI adoption.
BED
BED can directly support claims about gross job gains, gross job losses, openings, and closings at the establishment level. It cannot support worker occupational transitions or AI claims.
LEHD public products
The public LEHD products can directly support aggregate labor-demand and worker-flow claims, especially through J2J and related outputs, and they are strong for geography. But they only partially support worker transition claims in your paper because the underlying linked microdata are restricted and the public products are aggregates, not open worker-level occupation histories.
OEWS
OEWS directly supports claims about occupational employment and wages, with national, state, metro, and industry-specific estimates. It does not support transitions, AI adoption, or labor-demand flows.
O*NET
O*NET directly supports claims about task exposure, work activities, skills, and occupational mechanism hypotheses. It does not support realized labor-market effects by itself.
Employment Projections / OOH
These sources can partially support claims about expected occupational change and interpretive mechanisms, because they provide 10-year projections and official narrative context. They do not support realized worker transitions, firm adoption, or causal claims about current AI effects.
The three most important “cannot claim” boundaries
You should make these explicit in the paper.
First, no public source in this stack can directly support a claim like:
 “Workers at AI-adopting firms in occupation X saw outcome Y.”
 That requires a worker–firm linked public dataset with both employer AI adoption and worker outcomes, which you do not have.
Second, no public source here gives you a clean national administrative file of worker-level occupation-to-occupation transitions linked to firms. CPS and SIPP can estimate transitions from surveys; LEHD public products can show aggregate flows; but the ideal linked worker-firm occupation panel is not public.
Third, no single public source simultaneously gives you AI adoption + worker transitions + detailed occupation + local geography. That is why the paper needs a multi-source architecture rather than a “one perfect dataset” framing.
The positive claim architecture for the paper
The cleanest way to position the empirical core is:
CPS/SIPP/NLS for worker outcomes and transitions,
 BTOS/ABS for firm-side AI adoption and self-reported workforce effects,
 JOLTS/BED/CES/QCEW for labor-demand and establishment dynamics,
 OEWS/O*NET/ACS for occupational structure, wages, tasks, and geography.


—----


Main text: condensed figure
I would put a single compact matrix in the main text with only the core datasets and only the core claim families. That keeps the figure readable and makes the central point obvious: no single public dataset covers AI adoption, worker transitions, labor demand, and occupational structure at once. That conclusion follows directly from the official scope of CPS, BTOS, JOLTS, OEWS, O*NET, SIPP, ABS, and LEHD public products.
Figure 1. What the main public datasets can and cannot identify for AI-and-work research
Legend:
 ● = directly supports the claim
 ◐ = supports the claim only partially or indirectly
 ○ = cannot support the claim with public data
Dataset
Worker outcomes
Occupational transitions
Firm AI adoption
Labor demand / turnover
Occupational structure / wages
Task exposure / mechanism
CPS
●
●
○
◐
◐
○
SIPP
●
●
○
○
◐
○
BTOS
◐
○
●
◐
○
◐
ABS
◐
○
●
○
○
◐
JOLTS
○
○
○
●
○
○
LEHD public products
◐
◐
○
●
○
○
OEWS
○
○
○
○
●
○
O*NET
○
○
○
○
◐
●

Suggested figure note
Notes: This figure summarizes the identification frontier of the main U.S. public datasets relevant to AI-and-work measurement. CPS is the core public worker-side source because it is monthly, occupation-aware, and supports matched-month transition analysis; SIPP adds richer longitudinal worker dynamics; BTOS and ABS are the core public business-side AI adoption sources; JOLTS is the core public labor-demand flow source; LEHD public products provide aggregate worker-employer flow statistics but not open worker-level linked microdata; OEWS provides occupational employment and wage structure; and O*NET provides the task and skill layer used to operationalize exposure and mechanism hypotheses. Symbols reflect what each source can support with public data alone, not what would be possible in restricted-access environments.
Why this works in the main text
This version is compact enough for a journal article or policy paper and makes the core argument legible in a few seconds: the public-data system is modular and fragmented. Worker outcomes live mainly in CPS/SIPP, firm adoption lives mainly in BTOS/ABS, labor demand lives mainly in JOLTS/LEHD public products, and occupational structure/mechanism lives mainly in OEWS/O*NET.
Appendix: fuller version
In the appendix, I would include a fuller table with all major public sources and more granular claim categories. This is where you can be explicit about local geography, welfare outcomes, and the public/restricted boundary.
Table A1. Dataset-to-claim matrix for U.S. public data on AI and labor markets
Legend:
 ✓ = directly supports the claim with public data
 △ = supports the claim only partially, indirectly, or with important caveats
 ✗ = cannot support the claim with public data
Source
Worker outcomes
Worker occupational transitions
Firm AI adoption
Labor demand / turnover
Occupational structure / wages
Task exposure / mechanism
Local geographic exposure
Worker–firm AI causal claims
CPS (basic monthly)
✓
✓
✗
△
△
✗
△
✗
CPS ASEC
✓
△
✗
✗
△
✗
△
✗
CPS supplements
✓
✓
✗
✗
△
✗
✗
✗
SIPP
✓
✓
✗
✗
△
✗
△
✗
ACS PUMS
✓
✗
✗
✗
✓
✗
✓
✗
NLS public-use
✓
✓
✗
✗
△
✗
△
✗
BTOS
△
✗
✓
△
✗
△
✓
✗
ABS
△
✗
✓
✗
✗
△
△
✗
JOLTS
✗
✗
✗
✓
✗
✗
△
✗
QCEW
△
✗
✗
✗
✗
✗
✓
✗
CES
△
✗
✗
✗
✗
✗
✓
✗
BED
✗
✗
✗
✓
✗
✗
△
✗
LEHD public products
△
△
✗
✓
✗
✗
✓
✗
OEWS
✗
✗
✗
✗
✓
✗
✓
✗
O*NET
✗
✗
✗
✗
△
✓
✗
✗
Employment Projections / OOH
✗
✗
✗
✗
△
△
✗
✗

Suggested appendix note
Notes: “Worker outcomes” includes employment, unemployment, hours, earnings, poverty, and related household outcomes. “Worker occupational transitions” means movement between occupations or between occupation, unemployment, and nonparticipation. “Firm AI adoption” refers to direct measures of business use of AI or related advanced technologies. “Labor demand / turnover” refers to openings, hires, quits, layoffs, separations, or establishment-level job creation/destruction. “Occupational structure / wages” refers to occupation counts, distributions, and wage levels. “Task exposure / mechanism” refers to task, skill, work-activity, and technology descriptors used to infer how AI may affect occupations. “Worker–firm AI causal claims” are claims of the form: workers at AI-adopting firms in occupation X experienced outcome Y. No dataset in the public stack directly identifies that object. The coding is based on official documentation for CPS, SIPP, ACS PUMS, NLS, BTOS, ABS, JOLTS, QCEW, CES, BED, LEHD public products, OEWS, O*NET, and Employment Projections.
Formatting guidance
For the main-text figure, I would use three colors only: dark fill for direct support, medium fill for partial support, and light fill for no support. Do not use numbers in the main text; symbols read faster. In the appendix, keep the checkmark matrix and add short notes under the table. That split gives you a clean narrative figure in the paper and a defensible audit trail in the back. The design choice matters because these sources differ not just in topic, but in unit of observation, cadence, and public-access boundary.
One-sentence caption options
For the main text:
 Figure 1. The U.S. public data system for AI-and-work measurement is complementary rather than integrated: worker outcomes, firm adoption, labor demand, and occupational structure are observed in different datasets.
For the appendix:
 Table A1. No public U.S. dataset simultaneously identifies worker outcomes, occupational transitions, firm AI adoption, and worker–firm linkage; credible analysis therefore requires a multi-source design.


—------------




Dataset-to-figure map
Section 1 — Baseline: where are the occupations, tasks, and workers?
Empirical question: Which occupations matter most for AI-and-work analysis, where are they located, and how large are they in employment and wage terms?
Main figure:
 Figure 1. Occupational baseline map of the U.S. labor market
 Use OEWS for occupation-level employment and wage counts, O*NET for task and skill structure, and ACS PUMS for demographic and local geographic composition. OEWS gives annual employment and wage estimates for roughly 830 occupations across national, state, metro, and industry views; O*NET provides the task, skill, and work-activity descriptors; ACS PUMS gives public person-level microdata with geography down to the PUMA level. This figure should establish the occupational universe before any AI or transition analysis begins.
What this section can claim: the scale, wage profile, task profile, and geographic distribution of occupations.
 What it cannot claim: realized AI impacts or causal effects. Those require outcome or adoption data that these sources do not contain.

Section 2 — Worker-side outcomes: are exposed occupations already showing different labor-market patterns?
Empirical question: Do workers in more AI-relevant occupations show different employment, unemployment, hours, or earnings patterns?
Main figure:
 Figure 2. Worker outcomes by occupation and AI-related task profile
 Use CPS as the main source, optionally complemented by CPS ASEC for annual income and welfare outcomes. CPS is monthly, household-based, and provides employment, unemployment, hours, earnings, and labor-force status for the civilian noninstitutional population, with broad labor-force and occupational information. ASEC extends the CPS with richer annual income and work-history context.
Supporting appendix figure:
 Figure A1. Annual income and welfare consequences in exposed occupations
 Use CPS ASEC to look at income, poverty, or annual work experience by occupation group, especially if the paper wants a welfare distribution angle rather than only employment rates.
What this section can claim: worker-side labor-market differences across occupations and over time.
 What it cannot claim: that those differences are caused by firm-level AI adoption, because CPS does not observe employer adoption behavior.

Section 3 — Occupational mobility: are workers moving across occupations, unemployment, or nonparticipation?
Empirical question: Are workers in certain occupations more likely to switch occupations, exit employment, or re-enter through different occupations?
Main figure:
 Figure 3. Occupation-to-occupation and occupation-to-nonemployment transitions
 Use matched monthly CPS as the primary public transition engine. CPS is the only core public monthly worker survey in this stack that is both occupation-aware and usable for matched-month labor-force flow analysis. You can also use CPS supplements on displaced workers or job tenure/occupational mobility when they are available, and SIPP as the richer longitudinal complement for medium-run adjustment.
Supporting appendix figure:
 Figure A2. Medium-run post-shock adjustment paths
 Use SIPP to show that beyond immediate transitions, the public system can also track changes in employment, income, household composition, and program participation over several years.
What this section can claim: estimated public-data worker transitions across occupations and labor-force states.
 What it cannot claim: firm-linked occupational transitions or administrative ground truth for worker-job spells. That would require linked administrative microdata not available publicly.

Section 4 — Firm-side AI adoption: who is adopting AI, where, and with what reported employment effects?
Empirical question: Which firms report using AI, in what functions, and with what stated employment or task effects?
Main figure:
 Figure 4. Public business-side AI adoption and reported workforce effects
 Use BTOS as the main source and ABS as the annual structural complement. BTOS is a high-frequency Census survey of employer businesses and has a dedicated AI supplement/question set covering AI use, business functions, and workforce/task effects. ABS is annual, samples employer businesses, and has technology modules and technology-focused products that include AI and related technologies. BTOS is the best source for near-real-time adoption; ABS is better for annual structural adoption patterns.
Supporting appendix figure:
 Figure A3. Firm adoption heterogeneity by industry, size, and business characteristics
 Use ABS to go deeper on cross-sectional differences in adoption, especially where you want more business-structure detail than BTOS provides.
What this section can claim: direct public evidence on business adoption and self-reported employment/task effects.
 What it cannot claim: worker-level realized effects inside adopting firms, because BTOS and ABS observe businesses, not linked workers.

Section 5 — Labor demand and turnover: are openings, hires, quits, and layoffs changing in relevant sectors?
Empirical question: Is labor demand shifting in ways consistent with AI adoption, even when worker-level occupation outcomes are still ambiguous?
Main figure:
 Figure 5. Labor-demand and turnover patterns in AI-relevant sectors
 Use JOLTS as the core public demand-flow source, with CES, BED, and QCEW as supporting establishment/payroll context. JOLTS directly measures openings, hires, quits, layoffs/discharges, and other separations. CES provides monthly establishment employment, hours, and earnings by industry. BED adds gross job gains, losses, openings, and closings. QCEW gives the high-coverage quarterly industry-geography backbone, covering more than 95 percent of U.S. jobs.
Supporting appendix figure:
 Figure A4. Sectoral payroll and churn context
 Use CES + BED + QCEW to show whether a sector’s apparent AI story is actually a broader cyclical or structural labor-market story.
What this section can claim: changes in labor demand and turnover at the establishment/industry level.
 What it cannot claim: occupation-specific labor demand in public JOLTS, because JOLTS does not provide occupation detail in the public core series.

Section 6 — Aggregate worker-employer dynamics: what public linked-admin products can add
Empirical question: What do public linked administrative products add beyond household and business surveys?
Main figure:
 Figure 6. Public linked-admin benchmarks for worker-employer dynamics
 Use LEHD public products, especially J2J/QWI/LODES/PSEO, as aggregate benchmarks for worker-employer dynamics and local employment structure. LEHD is a quarterly linked employer-employee database at Census, but the underlying microdata are restricted; the public-facing products are aggregates and applications rather than open worker-level linked files. J2J in particular is built from job-level data from state UI programs merged to business and household data.
What this section can claim: aggregate public worker-employer dynamics and local labor-market structure.
 What it cannot claim: open public worker-level occupation histories or public worker–firm AI linkages.

Section 7 — Long-run adaptation and career paths
Empirical question: If AI changes work gradually rather than immediately, which public data can capture long-run adaptation?
Main figure:
 Figure 7. Long-run adjustment channels: careers, retraining, and persistent occupational change
 Use NLSY97 / NLS public-use and SIPP. NLS public-use data are designed for long-run study of labor-market activity, schooling, and related life-course outcomes, and NLSY97 specifically follows a cohort from school-to-work transition into adulthood. SIPP complements that by providing monthly longitudinal data on employment, income, and household conditions. This section is where you show that public data are stronger on adaptation over time than many people realize.
What this section can claim: persistent career effects, retraining, and medium- to long-run adjustment.
 What it cannot claim: near-real-time AI shocks or direct employer adoption effects.

Section 8 — The identification frontier: what no public dataset can do alone
Empirical question: What remains unobservable in the public federal data system?
Main figure:
 Figure 8. The missing public link: no worker–firm AI panel
 This is a synthesis figure, not a data figure. It should rest on the documented scope of the earlier sources: CPS and SIPP observe workers; BTOS and ABS observe businesses; JOLTS/CES/QCEW/BED observe establishments and demand/payroll dynamics; OEWS and O*NET observe occupational structure and task content; LEHD public products expose only aggregate linked-admin outputs. The figure should make the paper’s central point visually: no public dataset simultaneously identifies worker occupation, worker transition, firm AI adoption, and worker–firm linkage.
A compact version you can drop into the paper outline
You could summarize the full map like this:
Paper section
Core figure
Primary datasets
What the figure does
Baseline structure
Fig. 1
OEWS + O*NET + ACS PUMS
Maps occupations, tasks, wages, and geography
Worker outcomes
Fig. 2
CPS (+ ASEC)
Shows worker-side employment, hours, earnings, unemployment patterns
Occupational mobility
Fig. 3
Matched CPS (+ SIPP, CPS supplements)
Estimates occupation and labor-force transitions
Firm AI adoption
Fig. 4
BTOS + ABS
Measures adoption, functions, and reported workforce effects
Labor demand
Fig. 5
JOLTS + CES + BED + QCEW
Shows openings, hires, separations, payroll context
Linked-admin benchmark
Fig. 6
LEHD public products
Benchmarks aggregate worker-employer dynamics
Long-run adaptation
Fig. 7
NLS + SIPP
Tracks career adjustment and medium-run adaptation
Identification frontier
Fig. 8
Synthesis of all above
Shows what the public system still cannot identify

The best way to use this in writing is to make each section begin with a one-line sentence of the form:
 “This section uses [datasets] because they are the only public sources in our stack that can identify [specific empirical object].”
 That keeps the paper disciplined and prevents readers from expecting a source to answer questions it was never designed to answer. 


—-------------



Dataset-to-figure map
Section 1 — Baseline: where are the occupations, tasks, and workers?
Empirical question: Which occupations matter most for AI-and-work analysis, where are they located, and how large are they in employment and wage terms?
Main figure:
Figure 1. Occupational baseline map of the U.S. labor market
Use OEWS for occupation-level employment and wage counts, O*NET for task and skill structure, and ACS PUMS for demographic and local geographic composition. OEWS gives annual employment and wage estimates for roughly 830 occupations across national, state, metro, and industry views; O*NET provides the task, skill, and work-activity descriptors; ACS PUMS gives public person-level microdata with geography down to the PUMA level. This figure should establish the occupational universe before any AI or transition analysis begins.
What this section can claim: the scale, wage profile, task profile, and geographic distribution of occupations.
What it cannot claim: realized AI impacts or causal effects. Those require outcome or adoption data that these sources do not contain.

Section 2 — Worker-side outcomes: are exposed occupations already showing different labor-market patterns?
Empirical question: Do workers in more AI-relevant occupations show different employment, unemployment, hours, or earnings patterns?
Main figure:
Figure 2. Worker outcomes by occupation and AI-related task profile
Use CPS as the main source, optionally complemented by CPS ASEC for annual income and welfare outcomes. CPS is monthly, household-based, and provides employment, unemployment, hours, earnings, and labor-force status for the civilian noninstitutional population, with broad labor-force and occupational information. ASEC extends the CPS with richer annual income and work-history context.
Supporting appendix figure:
Figure A1. Annual income and welfare consequences in exposed occupations
Use CPS ASEC to look at income, poverty, or annual work experience by occupation group, especially if the paper wants a welfare distribution angle rather than only employment rates.
What this section can claim: worker-side labor-market differences across occupations and over time.
What it cannot claim: that those differences are caused by firm-level AI adoption, because CPS does not observe employer adoption behavior.

Section 3 — Occupational mobility: are workers moving across occupations, unemployment, or nonparticipation?
Empirical question: Are workers in certain occupations more likely to switch occupations, exit employment, or re-enter through different occupations?
Main figure:
Figure 3. Occupation-to-occupation and occupation-to-nonemployment transitions
Use matched monthly CPS as the primary public transition engine. CPS is the only core public monthly worker survey in this stack that is both occupation-aware and usable for matched-month labor-force flow analysis. You can also use CPS supplements on displaced workers or job tenure/occupational mobility when they are available, and SIPP as the richer longitudinal complement for medium-run adjustment.
Supporting appendix figure:
Figure A2. Medium-run post-shock adjustment paths
Use SIPP to show that beyond immediate transitions, the public system can also track changes in employment, income, household composition, and program participation over several years.
What this section can claim: estimated public-data worker transitions across occupations and labor-force states.
What it cannot claim: firm-linked occupational transitions or administrative ground truth for worker-job spells. That would require linked administrative microdata not available publicly.

Section 4 — Firm-side AI adoption: who is adopting AI, where, and with what reported employment effects?
Empirical question: Which firms report using AI, in what functions, and with what stated employment or task effects?
Main figure:
Figure 4. Public business-side AI adoption and reported workforce effects
Use BTOS as the main source and ABS as the annual structural complement. BTOS is a high-frequency Census survey of employer businesses and has a dedicated AI supplement/question set covering AI use, business functions, and workforce/task effects. ABS is annual, samples employer businesses, and has technology modules and technology-focused products that include AI and related technologies. BTOS is the best source for near-real-time adoption; ABS is better for annual structural adoption patterns.
Supporting appendix figure:
Figure A3. Firm adoption heterogeneity by industry, size, and business characteristics
Use ABS to go deeper on cross-sectional differences in adoption, especially where you want more business-structure detail than BTOS provides.
What this section can claim: direct public evidence on business adoption and self-reported employment/task effects.
What it cannot claim: worker-level realized effects inside adopting firms, because BTOS and ABS observe businesses, not linked workers.

Section 5 — Labor demand and turnover: are openings, hires, quits, and layoffs changing in relevant sectors?
Empirical question: Is labor demand shifting in ways consistent with AI adoption, even when worker-level occupation outcomes are still ambiguous?
Main figure:
Figure 5. Labor-demand and turnover patterns in AI-relevant sectors
Use JOLTS as the core public demand-flow source, with CES, BED, and QCEW as supporting establishment/payroll context. JOLTS directly measures openings, hires, quits, layoffs/discharges, and other separations. CES provides monthly establishment employment, hours, and earnings by industry. BED adds gross job gains, losses, openings, and closings. QCEW gives the high-coverage quarterly industry-geography backbone, covering more than 95 percent of U.S. jobs.
Supporting appendix figure:
Figure A4. Sectoral payroll and churn context
Use CES + BED + QCEW to show whether a sector’s apparent AI story is actually a broader cyclical or structural labor-market story.
What this section can claim: changes in labor demand and turnover at the establishment/industry level.
What it cannot claim: occupation-specific labor demand in public JOLTS, because JOLTS does not provide occupation detail in the public core series.

Section 6 — Aggregate worker-employer dynamics: what public linked-admin products can add
Empirical question: What do public linked administrative products add beyond household and business surveys?
Main figure:
Figure 6. Public linked-admin benchmarks for worker-employer dynamics
Use LEHD public products, especially J2J/QWI/LODES/PSEO, as aggregate benchmarks for worker-employer dynamics and local employment structure. LEHD is a quarterly linked employer-employee database at Census, but the underlying microdata are restricted; the public-facing products are aggregates and applications rather than open worker-level linked files. J2J in particular is built from job-level data from state UI programs merged to business and household data.
What this section can claim: aggregate public worker-employer dynamics and local labor-market structure.
What it cannot claim: open public worker-level occupation histories or public worker–firm AI linkages.

Section 7 — Long-run adaptation and career paths
Empirical question: If AI changes work gradually rather than immediately, which public data can capture long-run adaptation?
Main figure:
Figure 7. Long-run adjustment channels: careers, retraining, and persistent occupational change
Use NLSY97 / NLS public-use and SIPP. NLS public-use data are designed for long-run study of labor-market activity, schooling, and related life-course outcomes, and NLSY97 specifically follows a cohort from school-to-work transition into adulthood. SIPP complements that by providing monthly longitudinal data on employment, income, and household conditions. This section is where you show that public data are stronger on adaptation over time than many people realize.
What this section can claim: persistent career effects, retraining, and medium- to long-run adjustment.
What it cannot claim: near-real-time AI shocks or direct employer adoption effects.

Section 8 — The identification frontier: what no public dataset can do alone
Empirical question: What remains unobservable in the public federal data system?
Main figure:
Figure 8. The missing public link: no worker–firm AI panel
This is a synthesis figure, not a data figure. It should rest on the documented scope of the earlier sources: CPS and SIPP observe workers; BTOS and ABS observe businesses; JOLTS/CES/QCEW/BED observe establishments and demand/payroll dynamics; OEWS and O*NET observe occupational structure and task content; LEHD public products expose only aggregate linked-admin outputs. The figure should make the paper’s central point visually: no public dataset simultaneously identifies worker occupation, worker transition, firm AI adoption, and worker–firm linkage.
A compact version you can drop into the paper outline
You could summarize the full map like this:
Paper section
Core figure
Primary datasets
What the figure does
Baseline structure
Fig. 1
OEWS + O*NET + ACS PUMS
Maps occupations, tasks, wages, and geography
Worker outcomes
Fig. 2
CPS (+ ASEC)
Shows worker-side employment, hours, earnings, unemployment patterns
Occupational mobility
Fig. 3
Matched CPS (+ SIPP, CPS supplements)
Estimates occupation and labor-force transitions
Firm AI adoption
Fig. 4
BTOS + ABS
Measures adoption, functions, and reported workforce effects
Labor demand
Fig. 5
JOLTS + CES + BED + QCEW
Shows openings, hires, separations, payroll context
Linked-admin benchmark
Fig. 6
LEHD public products
Benchmarks aggregate worker-employer dynamics
Long-run adaptation
Fig. 7
NLS + SIPP
Tracks career adjustment and medium-run adaptation
Identification frontier
Fig. 8
Synthesis of all above
Shows what the public system still cannot identify

The best way to use this in writing is to make each section begin with a one-line sentence of the form:
“This section uses [datasets] because they are the only public sources in our stack that can identify [specific empirical object].”
That keeps the paper disciplined and prevents readers from expecting a source to answer questions it was never designed to answer.
I can next turn this into a section-by-section writing outline with thesis sentence, dataset sentence, and candidate chart type for each figure.
turn this into a section-by-section writing outline with thesis sentence, dataset sentence, and candidate chart type for each figure.
I’m translating the figure map into a writing architecture now: each section will have one core claim, one explicit identification sentence, and one figure form that matches what the data can actually show. I’m refreshing the official source base so the outline stays citation-ready.
Thought for 1m 23s
Below is a section-by-section writing outline you can use as a draft backbone.
1. Occupational baseline: what the U.S. labor market looks like before we ask any AI question
Thesis sentence:
Before estimating any effect of AI, we need to establish the occupational baseline: which occupations are large, where they are located, how much they pay, and what tasks they involve.
Dataset sentence:
This section uses OEWS to measure occupation-level employment and wages, ACS PUMS to describe worker composition and geography down to the PUMA level, and O*NET to characterize task, skill, and work-activity content.
Candidate chart type:
A ranked horizontal bar chart of employment by occupation group, paired with a dot plot of median or mean wages, plus a heatmap of selected O*NET task dimensions by occupation cluster.

2. Worker-side outcomes: are some occupations already diverging in employment, unemployment, hours, or earnings?
Thesis sentence:
The first empirical question is whether workers in occupations that appear more exposed to AI-related task change already show different labor-market outcomes, such as employment rates, unemployment rates, hours, or earnings.
Dataset sentence:
This section uses the monthly CPS as the core worker-side source because it is a monthly household survey that measures employment, unemployment, hours, earnings, and labor-force status, and it uses CPS ASEC as the annual companion when the analysis needs income, poverty, or broader socioeconomic outcomes.
Candidate chart type:
A line chart showing employment or unemployment trends for high- versus low-exposure occupation groups, with a companion coefficient plot or dot plot for hours and earnings gaps.

3. Occupational mobility: are workers moving across occupations, into unemployment, or out of the labor force?
Thesis sentence:
A key public-data test of labor-market disruption is whether workers in certain occupations are more likely to switch occupations, become unemployed, or leave the labor force altogether.
Dataset sentence:
This section uses matched monthly CPS as the core public transition source, because CPS is monthly and occupation-aware, and it uses SIPP as the richer longitudinal complement when the analysis needs medium-run adjustment paths rather than adjacent-month flows.
Candidate chart type:
A Sankey diagram or transition heatmap showing flows from occupation groups to other occupation groups, unemployment, and nonparticipation; in the appendix, add a small-multiples line chart for longer-run post-transition outcomes from SIPP.

4. Worker displacement and tenure: can public surveys distinguish normal churn from adverse disruption?
Thesis sentence:
Not all labor-market mobility is evidence of disruption, so the paper should separately identify displacement, tenure loss, and occupational mobility using the public CPS supplement architecture.
Dataset sentence:
This section uses the CPS Displaced Worker / Employee Tenure / Occupational Mobility supplements, which directly collect information on recent job loss due to work-related reasons and on tenure and occupational mobility, making them the closest public worker-side modules to structured displacement measurement.
Candidate chart type:
A grouped bar chart comparing displacement, tenure, and occupational mobility rates across broad occupation groups, ideally with a pre/post or high-/low-exposure split.

5. Firm-side AI adoption: who reports using AI, and what do they say it is doing inside the business?
Thesis sentence:
Any serious public-data paper on AI and work needs a direct business-side adoption measure, not just worker-side outcomes inferred from occupations.
Dataset sentence:
This section uses BTOS as the high-frequency business-side AI source because it provides near-real-time data on employer businesses and includes AI questions on use, functions, and reported workforce effects, and it uses ABS as the annual structural complement because ABS measures business characteristics, innovation, and technology adoption at the firm level.
Candidate chart type:
A state-by-sector heatmap of AI adoption rates from BTOS, paired with a stacked bar chart showing reported effects on tasks, employment, or business functions; for ABS, use an annual cross-sectional bar or dot plot by firm size or industry.

6. Labor demand and turnover: are openings, hires, quits, and layoffs shifting in AI-relevant sectors?
Thesis sentence:
Even when worker-level changes are still ambiguous, shifts in openings, hires, quits, and layoffs can reveal whether labor demand is weakening, rebalancing, or accelerating in sectors most exposed to AI adoption.
Dataset sentence:
This section uses JOLTS as the core public demand-flow source because it publishes monthly estimates of job openings, hires, and separations, and it uses CES, BED, and QCEW as supporting establishment and payroll context for employment, hours, earnings, job creation/destruction, and local industry structure.
Candidate chart type:
A multi-line chart of openings, hires, quits, and layoffs for AI-relevant sectors, with an appendix panel using CES or QCEW to show whether the same sectors are also changing in payroll employment or wages.

7. Aggregate worker-employer dynamics: what public linked-admin products add beyond surveys
Thesis sentence:
Public linked-administrative products can add an important aggregate benchmark on worker-employer dynamics, but they do not eliminate the identification limits of the public system.
Dataset sentence:
This section uses LEHD public products such as QWI, J2J, LODES, and PSEO to benchmark aggregate worker-employer dynamics and local employment structure, while making explicit that the underlying linked microdata remain restricted and that the public outputs are aggregate products rather than open worker-level linked files.
Candidate chart type:
A benchmark line chart or panel chart comparing public survey-based transition signals with aggregate J2J or QWI patterns, plus a simple schematic showing the boundary between public tabulations and restricted linked microdata.

8. Long-run adaptation: do public panel data capture career adjustment, retraining, and persistence?
Thesis sentence:
If AI changes careers gradually rather than immediately, the right public-data question is not only whether workers are displaced, but whether they retrain, switch occupations, or recover over the medium and long run.
Dataset sentence:
This section uses NLSY97 / NLS public-use for long-run career histories, job characteristics, and training, and it uses SIPP for medium-run monthly adjustment in employment, income, and household circumstances.
Candidate chart type:
An event-study line chart showing outcomes before and after occupational change or displacement, or a cohort-path chart showing retraining, occupation switching, and earnings recovery over time.

9. Identification frontier: what no public dataset can do alone
Thesis sentence:
The public U.S. data system is informative but not integrated: no public dataset simultaneously identifies worker occupation, worker transition, employer AI adoption, and worker–firm linkage.
Dataset sentence:
This final synthesis section draws on the documented scope of CPS, SIPP, BTOS, ABS, JOLTS, LEHD public products, OEWS, O*NET, ACS, and NLS to show that the public architecture is modular—worker outcomes live mainly in household surveys, AI adoption lives mainly in business surveys, labor demand lives mainly in establishment surveys, and task structure lives mainly in occupational databases.
Candidate chart type:
A publication-ready matrix or block diagram showing which empirical objects are observed by which public sources, with the missing worker–firm AI link visually highlighted.
A compact drafting formula for each section
For each empirical section, you can write the first paragraph in the same three-step structure:
Thesis sentence: what the section is trying to identify.
Dataset sentence: why these datasets are the right public sources for that object.
Boundary sentence: what the section still cannot identify, even after combining those sources.



—-----------



The next steps are:
Freeze the paper’s exact question.
 Use one sentence and do not change it again. For example:
 “What can U.S. public federal data already tell us about AI’s labor-market effects, what are the hard limits, and which incremental survey changes would unlock the most value?”


Freeze the dataset perimeter.
 Lock the core stack now:
 CPS, CPS ASEC, CPS supplements, SIPP, BTOS, ABS, JOLTS, OEWS, O*NET
 and treat ACS, QCEW, CES, BED, LEHD public products, NLS, Employment Projections as supporting sources.


Turn the audit into a master appendix table.
 Make one final table with:
 dataset, unit, frequency, geography, occupation detail, transition power, AI variables, strengths, weaknesses, sample sufficiency, best use, and key citation.
 This becomes the paper’s source-of-truth.


Choose the empirical spine.
 Do not try to use every dataset equally. The paper needs one central empirical backbone.
 The best one is:


CPS for worker outcomes and occupational transitions


BTOS for firm-side AI adoption


JOLTS for labor-demand flows


OEWS + O*NET for occupation/task structure


Decide the main claims the paper will actually make.
 I would limit it to 4:


what public data already measure well


what public data measure only imperfectly


what public data cannot identify at all


which low/medium/high-effort additions would most improve the system


Build the figure list now.
 Lock the figures before writing full prose. For example:


Fig. 1: public-data architecture / dataset-to-claim matrix


Fig. 2: occupational baseline from OEWS + O*NET


Fig. 3: worker outcomes from CPS


Fig. 4: occupational transitions from matched CPS


Fig. 5: firm AI adoption from BTOS/ABS


Fig. 6: labor-demand flows from JOLTS


Fig. 7: identification frontier / missing worker–firm AI link


Do one pilot empirical pass.
 Before drafting heavily, test whether the data actually support the figures. Start with:


one CPS transition table at broad occupation level


one BTOS AI-adoption cross-tab by sector/state


one JOLTS sector trend chart
 This will tell you quickly where the paper is strong and where sample or design issues bite.


Write the “what works / what doesn’t” section early.
 That section is already mostly conceptually done and will stabilize the rest of the paper. It should clearly separate:


works now


works partially


does not work with public data


would work with small survey changes


Write the policy-design section after the empirical pilot.
 Only recommend survey additions once you have seen where the public system actually breaks. That section should be organized by:


little effort


medium effort


large effort


Write the introduction and abstract last.
 Those will be much sharper once the empirical spine and limits are fixed.


The single most important next step is to run the pilot empirical pass. Until that is done, everything else is still architecture rather than evidence.


—-----------




1) Exact paper question
Recommended final question
What can U.S. public federal data credibly tell us about AI’s effects on workers, occupations, labor demand, and business adoption, what are the hard identification limits, and which incremental changes to existing surveys would generate the largest measurement gains?
This is better than the earlier wording for three reasons. First, it makes clear that the paper is about public federal data, not all possible data. Second, it names the four empirical objects that actually exist across the current public system: workers, occupations, labor demand, and business adoption. Third, it makes the paper’s contribution explicit: not just inventorying data, but identifying the hard limits and the highest-value incremental fixes. That framing matches the documented scope of the main public sources: CPS measures worker labor-force outcomes, BTOS measures business-side AI use, JOLTS measures openings/hires/separations, OEWS measures occupational employment and wages, O*NET provides task and skill structure, SIPP provides longitudinal worker dynamics, ABS provides annual business technology/adoption information, and CPS supplements are designed to accommodate added questions.
If you want a slightly sharper, more academic version, I would use this instead:
How far can the current U.S. public federal data system go in measuring AI’s labor-market effects, where does it fail, and which low-burden extensions to existing surveys would most improve inference?
This version is a bit more elegant, but the first version is clearer for policymakers.
2) Dataset perimeter
I would not keep all nine datasets on the same level. That makes the paper feel like a catalog rather than a designed empirical argument.
I recommend freezing the perimeter in three tiers.
Tier 1: primary empirical core
These are the datasets the paper should rely on most heavily.
CPS, BTOS, JOLTS, OEWS, O*NET
Why these five?
CPS is the main public worker-side source: it is monthly and measures employment, unemployment, hours, earnings, and labor-force status. BTOS is the main public high-frequency business-side AI source: it provides near-real-time data on employer businesses and includes AI-use questions. JOLTS is the main public labor-demand flow source: openings, hires, and separations. OEWS is the main public occupation-and-wage structure source. O*NET is the main public task-and-skill mechanism source. Together, these five already span the core public architecture of the paper.
Tier 2: extended core
These are important, but they should deepen the argument rather than define it.
CPS ASEC, CPS supplements, SIPP, ABS
Why move them here rather than keep them in the top tier?
CPS ASEC is excellent for annual income and welfare context, but not the main high-frequency engine. CPS supplements are highly valuable for displacement, tenure, and mobility, and Census explicitly notes that supplements are well suited to added questions, but they are episodic rather than continuous. SIPP is the best public longitudinal worker survey for medium-run adjustment, but it is not the main near-real-time monitoring source. ABS is the best annual structural business-side source for technology and innovation, but BTOS is the stronger real-time AI adoption source.
Tier 3: supporting sources
These should stay in the paper, but mainly as benchmarks, context, or appendix material.
ACS PUMS, QCEW, CES, BED, LEHD public products, NLS, Employment Projections
This tier is still important. ACS is great for local occupational composition; QCEW and CES give industry/payroll structure and timing; BED gives establishment dynamism; LEHD public products give aggregate linked-admin benchmarks; NLS is powerful for long-run career dynamics; Employment Projections gives the official forecast layer. But none of these should define the paper’s core empirical spine.
3) My recommendation in one line
So I would freeze the design like this:
Primary empirical core: CPS, BTOS, JOLTS, OEWS, O*NET
 Extended core: CPS ASEC, CPS supplements, SIPP, ABS
 Supporting: ACS, QCEW, CES, BED, LEHD public products, NLS, Employment Projections
That is tighter than your original perimeter and, in my view, stronger.
4) The exact wording I would put in the draft
You could write this in the paper notes:
Research question.
 What can U.S. public federal data credibly tell us about AI’s effects on workers, occupations, labor demand, and business adoption, what are the hard identification limits, and which incremental changes to existing surveys would generate the largest measurement gains?
Dataset perimeter.
 The paper’s primary empirical core consists of CPS, BTOS, JOLTS, OEWS, and ONET. CPS ASEC, CPS supplements, SIPP, and ABS are treated as extended-core sources that deepen worker-side and business-side analysis. ACS PUMS, QCEW, CES, BED, LEHD public products, NLS, and Employment Projections are treated as supporting sources used for context, benchmarking, and appendix analysis.*
That is the version I would lock.

—------


Recommended final set of 5 core claims
Claim 1
U.S. public federal data already allow a precise baseline description of the occupations most relevant to AI: their employment levels, wage structure, geographic distribution, and task content.
 This claim is anchored in OEWS for occupational employment and wages, O*NET for tasks, skills, and work activities, and optionally ACS PUMS for worker composition and local geography. OEWS publishes annual employment and wage estimates for roughly 830 occupations across the nation, states, metros, and industries, while O*NET provides the task-and-skill architecture needed to interpret exposure and mechanism.
Why this should be frozen: it gives the paper a clean starting point and uses sources that are strong exactly where they claim strength. It does not imply realized AI effects.

Claim 2
U.S. public federal data can credibly measure worker-side labor-market outcomes and broad occupational mobility, but mainly through survey-based inference rather than public linked administrative microdata.
 This claim is anchored in CPS as the core monthly worker-side source, with CPS ASEC, CPS supplements, and SIPP as extensions. CPS directly measures employment, unemployment, hours, earnings, and people not in the labor force; SIPP is a nationally representative longitudinal survey with monthly data on employment and economic circumstances over time; and the CPS displaced worker / tenure / occupational mobility supplements directly ask about displacement, tenure, and mobility.
Why this should be frozen: it makes a strong positive claim without pretending you have a public worker-level administrative occupation-transition file.

Claim 3
U.S. public federal data already provide direct measurement of business-side AI adoption and self-reported workforce effects, but from business surveys rather than worker-linked data.
 This claim is anchored in BTOS and ABS. Census states that the BTOS AI supplement was designed to measure how widespread AI use is among businesses, what kinds of AI they use, how that use affects employment, and how it changes business organization. ABS provides annual information on business characteristics and explicitly measures innovation and technology topics.
Why this should be frozen: it gives the paper a direct adoption leg, which is essential if you want to avoid making the whole project purely occupation-exposure based.

Claim 4
U.S. public federal data can track labor-demand and turnover dynamics in AI-relevant sectors, but the core public demand-flow system does not yet provide occupation-level demand measurement.
 This claim is anchored in JOLTS as the core labor-demand flow source, with CES, QCEW, BED, and LEHD public products as supporting context and benchmarks. JOLTS publishes job openings, hires, and separations, but its public system is establishment-based and not occupation-resolved in the way your project would ideally want.
Why this should be frozen: it makes JOLTS central without overselling it as an occupation dataset.

Claim 5
The main limitation of the current public federal data system is not the absence of data altogether, but the absence of a public integrated worker–firm AI panel; therefore, the highest-value policy response is to extend existing surveys rather than build an entirely new data system from scratch.
 This is the synthesis claim. It follows from the documented structure of the sources above: CPS and SIPP observe workers; BTOS and ABS observe firms; JOLTS observes labor demand and turnover; OEWS and O*NET observe occupational structure and task content. No public source jointly identifies worker occupation, worker transition, employer AI adoption, and worker–firm linkage.
Why this should be frozen: this is the paper’s real contribution. It turns a dataset inventory into a measurement-architecture argument.
How these claims line up with the dataset perimeter
Your primary empirical core maps cleanly now:
CPS → Claim 2


BTOS → Claim 3


JOLTS → Claim 4


OEWS → Claim 1


O*NET → Claim 1 and part of Claim 5


Your extended core deepens, rather than changes, the claims:
CPS ASEC → Claim 2


CPS supplements → Claim 2


SIPP → Claim 2 and part of Claim 5


ABS → Claim 3


Your supporting sources become exactly that:
ACS PUMS → supports Claim 1


QCEW / CES / BED / LEHD public products → support Claim 4


NLS → future-facing extension of Claim 2 / Claim 5


Employment Projections → interpretive context, not a core claim carrier


The exact wording I would lock into your notes
You can literally paste this into your working doc:
Core claims.
U.S. public federal data already allow a precise baseline description of the occupations most relevant to AI: their employment levels, wage structure, geographic distribution, and task content.


U.S. public federal data can credibly measure worker-side labor-market outcomes and broad occupational mobility, but mainly through survey-based inference rather than public linked administrative microdata.


U.S. public federal data already provide direct measurement of business-side AI adoption and self-reported workforce effects, but from business surveys rather than worker-linked data.


U.S. public federal data can track labor-demand and turnover dynamics in AI-relevant sectors, but the core public demand-flow system does not yet provide occupation-level demand measurement.


The main limitation of the current public federal data system is the absence of a public integrated worker–firm AI panel; therefore, the highest-value policy response is to extend existing surveys rather than build an entirely new system from scratch.


This is the set I would freeze.
The next best step is to freeze the paper structure around these five claims so every section and every figure maps one-to-one onto them.



—--------------


Frozen paper structure
Introduction
Purpose: State the question, contribution, and boundary conditions.
 Job of this section: Explain that the paper is about public federal data, not private platform data or restricted administrative microdata; define the problem as one of measurement architecture rather than one of “no data exists.” CPS measures worker outcomes, BTOS measures business-side AI adoption, JOLTS measures labor-demand flows, OEWS measures occupational employment and wages, and O*NET provides task content, but these pieces live in different public systems.
No main figure here.

Section 1 — Occupational baseline
Maps to Claim 1:
 U.S. public federal data already allow a precise baseline description of the occupations most relevant to AI: their employment levels, wage structure, geographic distribution, and task content.
Main datasets: OEWS + O*NET
 Supporting datasets: ACS PUMS
Main figure:
 Figure 1. Occupational baseline for AI-and-work analysis
 A two-panel figure: occupation employment/wage ranking from OEWS, plus a task-profile heatmap from ONET. OEWS provides annual employment and wage estimates for about 830 occupations across national, state, metro, and industry views; ONET provides the task and skill descriptors used to characterize occupational content.
What this section is allowed to claim:
 What occupations are large, high-wage, geographically concentrated, and task-structured in ways plausibly relevant to AI.
What it is not allowed to claim:
 Any realized AI effect.

Section 2 — Worker outcomes and occupational mobility
Maps to Claim 2:
 U.S. public federal data can credibly measure worker-side labor-market outcomes and broad occupational mobility, but mainly through survey-based inference rather than public linked administrative microdata.
Main datasets: CPS
 Extended-core datasets: CPS ASEC, CPS supplements, SIPP
Main figure:
 Figure 2. Worker outcomes and broad occupational transitions
 A two-part figure: line chart or event-style panel for employment/unemployment/hours by occupation group from CPS, plus a transition heatmap or Sankey for occupation-to-occupation / occupation-to-nonemployment flows using matched CPS. CPS is a monthly household survey that provides employment, unemployment, hours, earnings, and labor-force status; public-use microdata are available for researchers.
Appendix figures:
 Figure A1: annual welfare and income consequences from CPS ASEC.
 Figure A2: medium-run adjustment paths from SIPP.
 CPS supplements and SIPP deepen this section because supplements can capture displacement/tenure/mobility directly, while SIPP adds richer longitudinal household dynamics.
What this section is allowed to claim:
 Worker-side differences and broad mobility patterns by occupation group.
What it is not allowed to claim:
 That those worker outcomes are caused by observed firm-level AI adoption.

Section 3 — Business-side AI adoption
Maps to Claim 3:
 U.S. public federal data already provide direct measurement of business-side AI adoption and self-reported workforce effects, but from business surveys rather than worker-linked data.
Main datasets: BTOS
 Extended-core dataset: ABS
Main figure:
 Figure 3. Business-side AI adoption and reported workforce effects
 A state-by-sector heatmap or grouped bar chart from BTOS showing AI use, functions of use, and reported employment/task effects; an annual ABS companion can appear in the appendix or in a second panel. Census states that BTOS includes AI questions designed to show how widespread AI use is, the types of AI businesses use, how that use impacts employment, and how AI changes business organization. BTOS is collected every two weeks from a sample of about 1.2 million businesses split into six panels.
Appendix figure:
 Figure A3: ABS cross-sectional adoption differences by industry, firm size, or business characteristics.
What this section is allowed to claim:
 Direct public evidence on business adoption and self-reported workforce/task effects.
What it is not allowed to claim:
 Worker-level effects inside adopting firms.

Section 4 — Labor demand and turnover
Maps to Claim 4:
 U.S. public federal data can track labor-demand and turnover dynamics in AI-relevant sectors, but the core public demand-flow system does not yet provide occupation-level demand measurement.
Main dataset: JOLTS
 Supporting datasets: CES, QCEW, BED, LEHD public products
Main figure:
 Figure 4. Openings, hires, quits, and layoffs in AI-relevant sectors
 A multi-line trend figure using JOLTS, possibly normalized to pre-period levels, with CES/QCEW/BED context in the appendix. JOLTS is a monthly survey that produces estimates of job openings, hires, and separations.
Appendix figures:
 Figure A4: payroll employment and hours context from CES.
 Figure A5: establishment churn from BED.
 Figure A6: local industry size and payroll structure from QCEW.
What this section is allowed to claim:
 Sector-level labor-demand and turnover dynamics.
What it is not allowed to claim:
 Occupation-specific labor-demand shifts from JOLTS itself.

Section 5 — The identification frontier and the measurement agenda
Maps to Claim 5:
 The main limitation of the current public federal data system is the absence of a public integrated worker–firm AI panel; therefore, the highest-value policy response is to extend existing surveys rather than build an entirely new system from scratch.
Main datasets: synthesis of CPS, BTOS, JOLTS, OEWS, O*NET
 Supporting datasets: SIPP, ABS, LEHD public products, ACS, NLS, QCEW/CES/BED
Main figure:
 Figure 5. Public-data identification frontier for AI-and-work research
 This should be the condensed dataset-to-claim matrix or block diagram: worker outcomes in CPS/SIPP, business adoption in BTOS/ABS, labor demand in JOLTS, occupation/wage structure in OEWS, task mechanism in ONET, with the missing worker–firm AI linkage highlighted. BTOS is business-side, CPS is worker-side, JOLTS is demand-side, and OEWS/ONET are occupational scaffolds; no public source combines all of them in one linked panel.
What this section is allowed to claim:
 That the public system is modular rather than integrated, and that the highest-return fixes are survey extensions rather than a total rebuild.
What it is not allowed to claim:
 That a public integrated worker–firm AI panel already exists.

Conclusion / policy implications
Purpose: Summarize what works, what does not, and what low-burden additions would unlock the most value.
 This section should flow directly from Section 5 and argue for extensions to existing surveys because the main public sources already cover the relevant objects separately: worker outcomes in CPS, business adoption in BTOS/ABS, and demand flows in JOLTS.
No new main figure.
Frozen figure map
Figure 1 → Claim 1 → OEWS + O*NET


Figure 2 → Claim 2 → CPS


Figure 3 → Claim 3 → BTOS


Figure 4 → Claim 4 → JOLTS


Figure 5 → Claim 5 → synthesis of all core datasets


That is the cleanest one-to-one mapping.
Exact wording to lock into your notes
Paper structure.
 The paper is organized around five core claims. Section 1 establishes the occupational baseline using OEWS and ONET. Section 2 evaluates worker-side outcomes and broad occupational mobility using CPS, with CPS ASEC, CPS supplements, and SIPP as extensions. Section 3 measures business-side AI adoption and reported workforce effects using BTOS, with ABS as the annual structural complement. Section 4 analyzes labor-demand and turnover dynamics using JOLTS, with CES, QCEW, BED, and LEHD public products as supporting context. Section 5 synthesizes these results to show that the main public-data limitation is the absence of an integrated worker–firm AI panel and uses that result to motivate extensions to existing surveys rather than a wholesale redesign of the federal data system.* 



—-------



The key design choice is to keep the same occupational grouping throughout the paper whenever worker or occupation comparisons appear. I would freeze that grouping at the level of broad occupation groups harmonized across OEWS and O*NET using SOC-based occupational categories, and then use the closest compatible CPS broad occupation grouping for the worker-side sections. That keeps the paper readable and avoids pretending the public system can support very fine occupation-by-state-by-month inference everywhere. OEWS produces annual estimates for roughly 830 occupations, O*NET is updated quarterly and provides detailed task content, and BLS has published work on mapping occupation information across federal systems using the SOC framework.
Figure 1 — Occupational baseline for AI-and-work analysis
Purpose: establish the occupational universe before any AI or outcome claim.
Chart type: two-panel figure.
Panel A
Type: horizontal bar chart


Y-axis: broad occupation groups


X-axis: total employment


Source: OEWS


Sorting: descending by employment


Comparison: largest vs smallest occupation groups in employment terms


Panel B
Type: heatmap


Y-axis: same broad occupation groups as Panel A


X-axis: a small fixed set of O*NET-derived task dimensions relevant to AI, for example: information processing, writing/documentation, analytical reasoning, customer interaction, physical/manual activity, and routine administrative work


Cell value: standardized task-intensity score


Comparison: which large occupations are task-exposed in ways plausibly relevant to AI


What this figure should show: the occupations that matter most, how large they are, and what kinds of tasks they involve. OEWS is the right employment-and-wage backbone because it provides occupation-level employment and wage estimates nationally and by geography, while O*NET is the right task scaffold because it is the federal occupation database built around task, skill, and work-activity descriptors and is updated quarterly.
Figure 2 — Worker outcomes and broad occupational transitions
Purpose: show what public worker-side data can say about labor-market outcomes and mobility.
Chart type: two-panel figure.
Panel A
Type: line chart


X-axis: time, monthly


Y-axis: worker outcome rate


Main outcome: unemployment rate


Optional second version for appendix: employment-population ratio or average weekly hours


Grouping: occupation groups split into high, middle, and low AI-relevance bins, where the bins are constructed from the Figure 1 task profile


Comparison: whether high-AI-relevance occupation groups are diverging from low-AI-relevance groups over time


Panel B
Type: transition heatmap


Rows: origin state in month ttt


Columns: destination state in month t+1t+1t+1


States: broad occupation groups plus unemployed plus not in labor force


Cell value: weighted transition probability from matched monthly CPS


Comparison: which occupation groups have the highest transition intensity into other occupations, unemployment, or nonparticipation


What this figure should show: first, whether worker outcomes differ systematically across occupation groups; second, whether the public CPS can recover broad occupational mobility and labor-force transitions. CPS is the correct worker-side source because it is a monthly survey of U.S. households that provides employment, unemployment, hours, earnings, and people not in the labor force; the public-use files are monthly person-level records, and Census documents how to link CPS public-use files across months.
Figure 3 — Business-side AI adoption and reported workforce effects
Purpose: show direct public evidence on firm-side AI adoption.
Chart type: two-panel figure.
Panel A
Type: heatmap


Y-axis: industry sector


X-axis: state


Cell value: share of businesses reporting AI use


Source: BTOS


Comparison: where public business-side AI adoption is highest and lowest


Panel B
Type: grouped bar chart


X-axis: selected AI-use consequences


Bars: share of AI-using businesses reporting each consequence


Categories: supplementing employee tasks, performing tasks previously done by employees, introducing new tasks, increasing employment, decreasing employment, no employment change


Comparison: augmentation versus substitution versus no reported employment effect


What this figure should show: AI adoption is directly measurable on the business side with public data, and BTOS is the right source because Census designed the AI supplement to measure how widespread AI use is, what business functions use it, whether it performs or supplements employee tasks, and how firms say it affects employment. BTOS is also timely enough for this to be a real monitoring figure, since Census fields it every two weeks from a sample of about 1.2 million businesses split into six panels.
Figure 4 — Labor demand and turnover in AI-relevant sectors
Purpose: show what public demand-side data can say, separate from worker surveys.
Chart type: two-panel figure.
Panel A
Type: multi-line chart


X-axis: time, monthly


Y-axis: rate or level


Series: job openings rate, hires rate, quits rate, layoffs and discharges rate


Grouping: a fixed set of sectors chosen for AI relevance and contrast, for example information, professional and business services, finance and insurance, manufacturing, and health care/social assistance


Source: JOLTS


Comparison: whether AI-relevant sectors show distinct demand or turnover patterns


Panel B
Type: indexed line chart


X-axis: time, monthly or quarterly


Y-axis: index with common base period = 100


Series: payroll employment or average weekly hours by the same sectors


Sources: CES for monthly payroll/hours, optional QCEW in appendix for quarterly benchmark levels


Comparison: whether turnover changes line up with broader payroll and hours changes


What this figure should show: public data can track labor-demand and turnover dynamics well at the sector level, but not yet at the occupation level in the core demand-flow system. JOLTS publishes monthly estimates of job openings, hires, and separations, while CES and QCEW provide establishment-based employment, hours, earnings, and payroll context.
Figure 5 — The public-data identification frontier
Purpose: make the paper’s main architecture claim visually undeniable.
Chart type: condensed capability matrix.
Rows: core datasets
 CPS, BTOS, JOLTS, OEWS, O*NET
Columns: empirical objects
 worker outcomes, occupational transitions, firm AI adoption, labor demand/turnover, occupational structure/wages, task mechanism, worker–firm AI linkage
Cell coding:
 filled = directly observed
 half-filled = partially or indirectly observed
 empty = not observed
Comparison: not across time, but across measurement capability
What this figure should show: the public system is modular rather than integrated. CPS directly observes worker outcomes and broad transitions; BTOS directly observes business-side AI adoption; JOLTS directly observes labor-demand flows; OEWS directly observes occupational employment and wages; ONET directly observes task content. No public source in the core stack directly observes the combined object “workers in occupation X at AI-adopting firms experience outcome Y.” CPS is a worker survey, BTOS is a business survey, JOLTS is an establishment flow survey, OEWS is an occupation-wage system, and ONET is a task/skill database.
Final frozen comparison logic across all five figures
To keep the paper coherent, I would freeze these cross-figure conventions:
Occupation comparisons always use the same broad occupation grouping.


AI relevance is always derived from the same O*NET-based task profile from Figure 1.


Worker-side outcomes always come from CPS-based measures unless explicitly moved to appendix extensions.


Firm-side AI adoption always comes from BTOS in the main text; ABS can deepen it in the appendix.


Demand-side dynamics always come from JOLTS in the main text, with CES/QCEW/BED only as context.


Figure 5 is the synthesis figure and should use only the core stack, not the supporting datasets.


That gives you a fully locked five-figure spine: baseline, workers, firms, demand, and identification frontier.




—--------------



Rule for what moves out of the main text
The main text keeps only figures that are necessary to prove the five core claims. Anything that does one of these four things moves to the appendix:
validates a main-text result,


adds welfare or subgroup detail,


provides establishment/payroll context, or


deepens a source that is important but not central to the claim.


That keeps the paper lean while preserving rigor.
Final main-text figures
These stay in the main text:
Figure 1 — Occupational baseline for AI-and-work analysis
 OEWS + O*NET


Figure 2 — Worker outcomes and broad occupational transitions
 CPS


Figure 3 — Business-side AI adoption and reported workforce effects
 BTOS


Figure 4 — Labor demand and turnover in AI-relevant sectors
 JOLTS


Figure 5 — The public-data identification frontier
 Synthesis of CPS, BTOS, JOLTS, OEWS, O*NET


This keeps the main text anchored on the primary empirical core: CPS, BTOS, JOLTS, OEWS, and ONET. CPS is the main monthly worker-side source, BTOS is the main public high-frequency business-side AI source, JOLTS is the main public labor-demand flow source, OEWS is the core occupation/wage structure source, and ONET is the core task/skill mechanism source.
Frozen appendix figure list
Figure A1 — Annual worker welfare and income context
Dataset: CPS ASEC
 What it shows: annual income, poverty, or work-experience differences across the same broad occupation groupings used in the main text.
 Why it moves out of the main text: it deepens Claim 2, but the main worker-side claim can already be made with monthly CPS. ASEC is the right extension because it adds annual socioeconomic detail rather than high-frequency labor-market movement. The CPS/ASEC documentation makes clear that the monthly CPS is the basis for employment/unemployment measurement, while ASEC adds annual context.
Figure A2 — Medium-run adjustment after occupational change
Dataset: SIPP
 What it shows: how employment, income, and household conditions evolve after occupational transitions or labor-market shocks.
 Why it moves out of the main text: SIPP is extremely valuable for richer longitudinal adjustment, but it is not the core near-real-time empirical engine of the paper. It should deepen the worker-transition section rather than compete with CPS in the main narrative. Census describes SIPP as a nationally representative longitudinal survey with monthly data on changes in employment, household composition, income, and program participation.
Figure A3 — Displacement, tenure, and mobility validation
Dataset: CPS supplements
 What it shows: direct displacement or tenure patterns where the supplement schedule allows it.
 Why it moves out of the main text: it is the best validation or enrichment for Claim 2, but the supplements are episodic, not continuous. The main paper should not rely on an intermittent source for its core transition result. CPS supplements exist specifically to add topical questions such as displacement and mobility to the CPS platform.
Figure A4 — Annual structural heterogeneity in firm AI adoption
Dataset: ABS
 What it shows: adoption differences by industry, firm size, age, or business characteristics.
 Why it moves out of the main text: BTOS already carries the main firm-side adoption claim because it is higher-frequency and specifically designed for current business conditions. ABS is ideal for annual structural depth, but that is secondary to the core adoption result. Census research and ABS documentation make clear that BTOS and ABS are complementary, with BTOS providing high-frequency signals and ABS offering deeper annual structure.
Figure A5 — Payroll employment and hours context
Dataset: CES
 What it shows: monthly payroll employment and average weekly hours in the same sectors used in Figure 4.
 Why it moves out of the main text: CES is useful context for whether JOLTS demand-flow changes coincide with broader payroll changes, but it is not itself the labor-demand flow source. BLS explicitly distinguishes CPS as the household survey and CES as the payroll or establishment survey.
Figure A6 — Establishment churn and job creation/destruction context
Dataset: BED
 What it shows: gross job gains, gross job losses, establishment openings, and closings in sectors relevant to the JOLTS discussion.
 Why it moves out of the main text: BED is an excellent context series, but the main demand-flow claim should remain centered on JOLTS. BLS notes that JOLTS measures hires and separations and BED provides quarterly business employment dynamics derived from QCEW longitudinal histories.
Figure A7 — Local industry size and payroll benchmark
Dataset: QCEW
 What it shows: county/state/metro industry employment and wage structure for sectors discussed in Figures 3–4.
 Why it moves out of the main text: QCEW is essential as a benchmark and denominator, but it does not directly identify AI adoption, worker transitions, or labor-demand flows. BLS describes QCEW as a quarterly count of employment and wages reported by employers covering more than 95 percent of U.S. jobs.
Figure A8 — Aggregate linked-admin benchmark
Dataset: LEHD public products
 What it shows: aggregate worker-employer dynamics from public tabulations such as J2J/QWI/LODES/PSEO.
 Why it moves out of the main text: LEHD public products are powerful benchmarks, but the main paper should not depend on a public/restricted boundary case to make its central argument. Census explicitly distinguishes the public LEHD products from the underlying restricted linked microdata.
Figure A9 — Local occupational composition
Dataset: ACS PUMS
 What it shows: local demographic and geographic composition of the broad occupation groups used in Figure 1.
 Why it moves out of the main text: ACS is ideal for descriptive local structure, but it does not drive the paper’s main identification claims. It should support the baseline rather than sit at the center of it. Census’ public-use microdata program is designed for descriptive microdata analysis with disclosure protection.
Figure A10 — Long-run career adaptation
Dataset: NLSY97 / NLS public-use
 What it shows: long-run career, retraining, or occupational persistence paths.
 Why it moves out of the main text: this is valuable for future-facing or long-horizon interpretation, but it is not necessary to establish the paper’s main public-data architecture claims. NLS is the right place for long-run career dynamics, not current macro monitoring.
What is now explicitly out of the main text
To keep the paper lean, these pieces should not appear as main-text figures:
annual welfare detail from CPS ASEC


longitudinal household adjustment from SIPP


episodic validation from CPS supplements


annual firm heterogeneity from ABS


payroll context from CES


establishment churn from BED


local industry denominators from QCEW


public linked-admin benchmarking from LEHD public products


local descriptive composition from ACS


long-run careers from NLS


Those all still matter; they just matter as validation, depth, and context, not as the core narrative.
Final frozen structure in one line
Main text = one figure per core claim.
 Appendix = validation, welfare detail, longitudinal depth, establishment/payroll context, local descriptive structure, and public/restricted boundary benchmarks.
That is the cleanest split.



—------------


Below is the frozen variable spec sheet for the main paper. I am treating anything labeled “design choice” as a decision we are locking now, not something claimed by the source itself.
Common conventions across the whole paper
1) Common occupation grouping
 Use 22 broad occupation groups as the paper-wide occupation taxonomy. Concretely, the worker-side implementation uses CPS PRDTOCC1, which Census documents as a 22-category occupation recode for the main job. On the occupational-structure side, map OEWS and O*NET detailed SOC occupations into the same 22-group system by aggregating to the 2018 SOC major groups excluding military. This is the cleanest harmonization because the 2018 SOC has 23 major groups, while OEWS explicitly covers 22 of the 23 because it excludes military occupations, and the CPS public-use occupation recode also has 22 categories.
2) Common AI-relevance measure
 Use a single author-constructed AI Task Index for all occupation comparisons. For each occupation, compute the average of the standardized ONET ratings for:
 Analyzing Data or Information, Processing Information, Documenting/Recording Information, and Working with Computers. These are all standard ONET work-activity descriptors. Keep two additional ONET descriptors only as contrast variables, not part of the index: Assisting and Caring for Others and Handling and Moving Objects. The first four define the main “AI-relevance” score; the last two help distinguish cognitive-digital work from interpersonal-care and physical-manual work. Then sort the 22 occupation groups into high / middle / low AI-relevance terciles using the employment-weighted distribution from OEWS. This is a design choice, but it is built from official ONET descriptors and official OEWS employment weights.
3) Common time convention
 Use two time conventions, fixed now. For structural cross-sections, use the latest available snapshot at implementation time: latest OEWS year and latest O*NET release. For time-series figures, use January 2019 to the latest available observation, but mark August 28, 2023 as the start of the public BTOS AI-core monitoring window and treat the post-August-2023 period as the main AI-monitoring window in the text. This keeps the paper comparable across CPS, BTOS, JOLTS, and CES while still acknowledging that direct public business-side AI measurement begins later than the labor-market series.
4) Common sector grouping for business/demand sections
 Freeze a six-sector comparison set for Figures 3 and 4:
 Manufacturing, Information, Financial activities, Professional and business services, Health care and social assistance, and Retail trade.
 For JOLTS and CES, use the published industry categories directly. For BTOS, aggregate published business-sector categories to the nearest comparable grouping where needed. This is a design choice, but it is grounded in the fact that JOLTS publishes industry estimates and BTOS is designed to support detailed subsector analysis.
5) Common geography rule
 Keep the main text national. State and local geography move to the appendix. This is a design choice to keep the paper lean and avoid thin-cell interpretation in the main results. It also aligns with the strengths of the data: CPS and JOLTS are strongest nationally, BTOS supports geographic detail, OEWS supports extensive geography, and QCEW/ACS are stronger for local descriptive context than for the paper’s central causal-architecture argument.

Figure 1 — Occupational baseline for AI-and-work analysis
Outcome variable
 Panel A:
OEWS employment share = occupation-group employment divided by total OEWS employment


OEWS median annual wage for the same occupation group


Panel B:
Employment-weighted mean O*NET scores for the six fixed task dimensions:


Analyzing Data or Information


Processing Information


Documenting/Recording Information


Working with Computers


Assisting and Caring for Others


Handling and Moving Objects


Grouping variable
 The common 22 occupation groups defined above. OEWS and O*NET detailed occupations are crosswalked into these 22 groups using SOC.
Comparison
 Panel A compares occupation groups by size and pay.
 Panel B compares occupation groups by task profile and supplies the AI-relevance terciles used later.
Source
 OEWS + ONET. OEWS provides annual occupation employment and wage estimates; ONET provides occupational task and work-activity descriptors.
Time window
 Latest available OEWS year and latest available O*NET release at implementation time.
Geography
 National only.
Weighting / normalization
Panel A employment uses OEWS national occupation employment totals; employment share is normalized by total OEWS employment.


Panel B O*NET values are aggregated to the 22 occupation groups using OEWS employment weights, then standardized as z-scores across the 22 groups.


The AI Task Index is the mean of the four digital-information O*NET z-scores; terciles are formed from that index.


One-sentence interpretation rule
 Figure 1 is the paper’s occupational map: it identifies which occupations are large, high- or low-wage, and structured around task profiles that are more or less aligned with current AI capabilities.

Figure 2 — Worker outcomes and broad occupational transitions
Outcome variable
 Panel A:
Mean usual weekly hours worked on the main job = CPS PEHRUSL1, among employed civilian noninstitutional persons age 16+


Panel B:
One-month transition probabilities across states defined as


the 22 occupation groups when employed, using PRDTOCC1


Unemployed when 3 <= PEMLR <= 4


Not in labor force otherwise within the civilian noninstitutional population age 16+


Grouping variable
 High / middle / low AI-relevance terciles from Figure 1 for Panel A.
 For Panel B, the full state space is the 22 occupation groups + unemployed + NILF.
Comparison
 Panel A compares the intensive-margin worker outcome—usual hours—across the three AI-relevance bins over time.
 Panel B compares where workers go next month: stay in the same occupation group, move to another occupation group, become unemployed, or leave the labor force.
Source
 Monthly CPS public-use microdata. CPS is the monthly household survey that provides employment, unemployment, hours, earnings, and people not in the labor force, and Census documents the key identifiers, occupation recodes, and weights on the public files.
Time window
 January 2019 through latest available month, with August 2023 marked as the beginning of the BTOS AI-core monitoring window for cross-figure comparison.
Geography
 National only.
Weighting / normalization
Use PWCMPWGT / 10,000 for all CPS estimates.


Panel A universe: civilian noninstitutional population age 16+, employed (1 <= PEMLR <= 2), with valid PRDTOCC1 and PEHRUSL1.


Panel B matching uses HRHHID + HRHHID2 + PULINENO, as Census instructs for linking the same individuals across months.


Transition probabilities are row-normalized using the month-ttt CPS weight.


One-sentence interpretation rule
 Figure 2 shows what public worker-side data can identify directly: changes in hours among employed workers and broad one-month transitions across occupations, unemployment, and nonparticipation.

Figure 3 — Business-side AI adoption and reported workforce effects
Outcome variable
 Panel A:
Current AI use rate = firm-weighted share of businesses answering Yes to BTOS core AI question 23 (“did this business use AI in any of its business functions?”)


Expected AI use rate = firm-weighted share answering Yes to BTOS forward AI question 33 (“during the next six months, do you think this business will be using AI in any of its business functions?”)


Panel B:
Among AI-using businesses in the pooled AI supplement window, share reporting:


Perform a task previously done by an employee


Supplement or enhance a task performed by an employee


Introduce a new task not previously done by an employee


Employment increased


Employment decreased


Employment did not change


Grouping variable
 Panel A: none beyond the two national series, current vs expected use.
 Panel B: workforce-effect categories listed above.
 The fixed six-sector grouping is reserved for appendix Figure A4, not the main figure, to keep Figure 3 lean.
Comparison
 Panel A compares current versus expected AI use over time.
 Panel B compares augmentation, substitution, new-task creation, and reported total-employment effects.
Source
 BTOS AI core questions plus BTOS AI supplement. Census states that BTOS provides timely data on business conditions, that AI content was added to measure how widespread AI use is and how it affects employment and business organization, and that the detailed AI supplement asked about types of AI, business functions, impact on worker tasks and equipment, and employment effects.
Time window
 Panel A: August 28, 2023 through latest available BTOS AI-core collection.
 Panel B: pooled supplement window December 4, 2023 through February 25, 2024.
Geography
 National only in the main text.
 State totals for overall AI use, if included at all, move to the appendix.
Weighting / normalization
 Use the published BTOS firm-weighted shares.
 For Panel B, report category shares among the relevant respondent universe:
task-effect items among AI users asked the supplement question


employment-effect item among the same supplement universe.


One-sentence interpretation rule
 Figure 3 is the direct public adoption figure: it shows that AI use is measurable on the business side and that businesses publicly report whether AI is supplementing workers, replacing tasks, creating new tasks, or changing total employment.

Figure 4 — Labor demand and turnover in AI-relevant sectors
Outcome variable
 Panel A:
 Use seasonally adjusted JOLTS rates for:
Job openings rate


Hires rate


Quits rate


Layoffs and discharges rate


Panel B:
 Use CES payroll employment index for the same sector set.
 Base period = August 2023 = 100. CES publishes monthly employment, hours, and earnings by industry.
Grouping variable
 The fixed six-sector comparison set:
Manufacturing


Information


Financial activities


Professional and business services


Health care and social assistance


Retail trade


Comparison
 Panel A compares labor-demand and turnover rates across the six sectors over time.
 Panel B compares payroll employment trajectories across the same sectors to show whether turnover changes line up with broader employment changes.
Source
 JOLTS for demand/turnover; CES for payroll employment context. JOLTS publishes monthly and annual estimates of job openings, hires, and separations, including industry estimates; CES publishes detailed monthly industry estimates of nonfarm employment, hours, and earnings.
Time window
 January 2019 through latest available month.
Geography
 National only.
Weighting / normalization
Panel A uses published seasonally adjusted JOLTS rates, not levels.


Panel B uses CES sector employment indexed to August 2023 = 100.


QCEW does not enter the main figure; it remains an appendix benchmark because it is quarterly and establishment/payroll-structural rather than a direct demand-flow series.


One-sentence interpretation rule
 Figure 4 shows what the public demand-side system can identify: sector-level shifts in openings, hiring, quits, layoffs, and payroll employment, but not occupation-specific labor demand.

Figure 5 — The public-data identification frontier
Outcome variable
 None in the usual statistical sense. This is a capability matrix.
Grouping variable
 Rows = the five core datasets only:
CPS


BTOS


JOLTS


OEWS


O*NET


Columns = the seven fixed empirical objects:
Worker outcomes


Occupational transitions


Firm AI adoption


Labor demand / turnover


Occupational structure / wages


Task mechanism


Worker–firm AI linkage


Comparison
 Cell coding only:
Filled = directly observed


Half-filled = partially or indirectly observed


Empty = not observed with public data


Source
 This is a synthesis figure built from the official scope of the five core sources: CPS is the worker-side monthly survey; BTOS is the business-side high-frequency survey with AI questions; JOLTS is the labor-demand and turnover survey; OEWS is the occupation employment/wage structure program; O*NET is the occupational task/skill database.
Time window
 Not applicable.
Geography
 Not applicable.
Weighting / normalization
 Not applicable.
One-sentence interpretation rule
 Figure 5 is the architecture figure: it makes explicit that the public system is modular rather than integrated, because no public source jointly observes workers, occupations, firm AI adoption, and worker–firm linkage in one panel.

What is now locked
The following decisions should now be treated as frozen:
Occupation taxonomy: 22 broad groups


AI-relevance measure: four-variable O*NET AI Task Index + two contrast dimensions


Main-text geography: national only


Main-text business/demand sectors: fixed six-sector set


Trend convention: Jan 2019–latest, with Aug 2023 marked as the start of the BTOS AI-monitoring window


Figure 1–5 contents: fixed as specified above


—--------------

For the appendix, I am freezing the measurement concepts and comparisons, not every literal public-use variable code, because several appendix sources are versioned by year or by instrument release. For implementation, the exact code names should be pulled from the current-year public-use codebooks or APIs, but the substantive objects, universes, comparisons, and normalization rules are now fixed. That is the honest way to lock the appendix without pretending every source uses stable variable names across years. The roles of these sources are also fixed: CPS ASEC adds annual worker welfare context; SIPP adds medium-run longitudinal adjustment; CPS supplements validate displacement, tenure, and mobility; ABS adds annual structural business heterogeneity; CES, BED, and QCEW add establishment/payroll context; LEHD public products add aggregate linked-admin benchmarks; ACS adds local descriptive composition; and NLS adds long-run career dynamics.
Appendix-wide rules
Common occupation grouping
 Keep the same 22 broad occupation groups used in the main text whenever an appendix source has occupation data. If a source does not naturally support that mapping, do not force detailed occupation analysis; instead use the fixed sector grouping or the AI-relevance terciles inherited from Figure 1.
Common AI-relevance measure
 Do not invent a second exposure metric in the appendix. Use the same high / middle / low AI-relevance terciles built from the Figure 1 O*NET-based AI Task Index whenever a worker-side appendix figure needs an exposure grouping.
Common time convention
 Main appendix comparisons use the same broad window as the main text—2019 to latest available—except where a source is inherently annual or irregular. In those cases, use the latest available annual series or supplement cycle and state clearly that the figure is structural or validation-oriented, not a high-frequency trend.
Common role rule
 Every appendix figure must answer one of four subordinate functions only: validation, welfare depth, structural heterogeneity, or contextual benchmarking. If a figure starts making a new main claim, it does not belong in the appendix.

Figure A1 — Annual worker welfare and income context
Outcome variable
 Annual worker welfare outcomes by occupation group:
annual wage and salary income


annual personal income


poverty status


weeks worked in the prior calendar year


any unemployment experienced during the prior calendar year


Grouping variable
 Same 22 broad occupation groups, collapsed to the same high / middle / low AI-relevance terciles used in Figure 2 for the main comparison.
Comparison
 Compare annual income and poverty outcomes across the three AI-relevance terciles, with a secondary split for workers who remained employed all year versus those with any unemployment during the prior calendar year.
Source
 CPS ASEC. The ASEC is the annual supplement to CPS and collects information on employment and unemployment experienced during the prior calendar year as well as income and related social and economic characteristics.
Time window
 Annual observations, 2019 through latest available ASEC.
Geography
 National only.
Weighting / normalization
 Use the ASEC person weight from the relevant public-use file; report weighted means or shares. Keep all outcomes annual and do not mix them with monthly CPS outcomes.
One-sentence interpretation rule
 A1 is not a new labor-market figure; it shows whether the worker-side differences in Figure 2 also appear in annual income and poverty terms.

Figure A2 — Medium-run adjustment after occupational change
Outcome variable
 Monthly post-shock or post-transition outcomes:
employment indicator


monthly earnings / total monthly income


household income


participation in major government programs


Grouping variable
 Workers experiencing an occupation change or movement into nonemployment, grouped by the AI-relevance tercile of the origin occupation.
Comparison
 Event-time comparison from several months before to several months after the transition, showing how employment and income evolve.
Source
 SIPP. SIPP is a nationally representative longitudinal survey with monthly data on employment, income, household composition, and government program participation over time.
Time window
 Use the latest SIPP panels that cover the post-2019 period.
Geography
 National only.
Weighting / normalization
 Use the relevant SIPP person longitudinal or monthly weight for the selected panel; normalize event time so month 0 is the occupation-change or labor-force transition month.
One-sentence interpretation rule
 A2 extends Figure 2 by showing whether transitions linked to more AI-relevant occupations are associated with more persistent income or employment adjustment.

Figure A3 — Displacement, tenure, and mobility validation
Outcome variable
displaced-worker indicator


current job tenure


current occupation tenure / occupational mobility measure, where available in the supplement cycle


Grouping variable
 The same 22 occupation groups or the corresponding AI-relevance terciles.
Comparison
 Compare displacement incidence and tenure across AI-relevance terciles.
Source
 CPS Displaced Worker / Employee Tenure / Occupational Mobility supplements. Census documents that these supplements provide data on workers who lost a job in the last five years due to plant closing, shift elimination, or other work-related reason, and that the employee tenure and occupational mobility questions are asked in the January supplement cycles.
Time window
 Use the most recent available January supplement cycle that includes the needed topics; if multiple cycles are used, keep them separate or harmonize only at broad occupation level.
Geography
 National only.
Weighting / normalization
 Use the supplement-specific person weights from the public-use file.
One-sentence interpretation rule
 A3 validates the worker-transition story by asking whether the same occupations also show higher direct displacement or weaker tenure in the dedicated CPS supplement system.

Figure A4 — Annual structural heterogeneity in firm AI adoption
Outcome variable
business use of AI or other advanced technology


reported impact on number of workers employed


reported impact on the types or skill levels of workers employed


Grouping variable
 Industry sector and firm size class.
Comparison
 Compare adoption and reported workforce impacts across industries and size classes.
Source
 ABS. Census states that ABS measures selected business characteristics including innovation and technology, and its technology tables include AI, motivations for technology use, impacts on the workforce, and effects on worker types.
Time window
 Use the latest available ABS technology/innovation module that contains AI or advanced technology workforce-impact items.
Geography
 National only in the main appendix version; state cuts only if they remain stable and add real value.
Weighting / normalization
 Use the published ABS weighted shares or API/tabulated outputs rather than rebuilding from raw internal records.
One-sentence interpretation rule
 A4 does not replace Figure 3; it adds annual structural depth by showing which kinds of firms and sectors report AI or advanced-technology use and what workforce effects they report.

Figure A5 — Payroll employment and hours context
Outcome variable
payroll employment index


average weekly hours index


Grouping variable
 The same six sectors used in Figure 4:
 manufacturing, information, financial activities, professional and business services, health care and social assistance, and retail trade.
Comparison
 Compare sector payroll employment and hours trends to see whether the JOLTS demand-flow story is mirrored in broader payroll conditions.
Source
 CES. CES produces monthly industry estimates of nonfarm employment, hours, and earnings on payrolls.
Time window
 January 2019 through latest available month.
Geography
 National only.
Weighting / normalization
 Use published seasonally adjusted CES series, indexed to August 2023 = 100 to align visually with the BTOS AI-monitoring window.
One-sentence interpretation rule
 A5 is pure context: it shows whether sectors with unusual openings or quits in Figure 4 also experienced broader payroll employment or hours changes.

Figure A6 — Establishment churn and job creation/destruction context
Outcome variable
gross job gains rate


gross job losses rate


openings share


closings share, where useful


Grouping variable
 Same six sectors as Figure 4, at the broadest BED industry grouping that is consistently available.
Comparison
 Compare whether sectors with AI-relevant demand changes also exhibit unusual establishment churn.
Source
 BED. BLS states that BED tracks gross job gains and gross job losses from establishment openings/expansions and closings/contractions using longitudinal establishment histories.
Time window
 Quarterly, 2019 through latest available quarter.
Geography
 National only.
Weighting / normalization
 Use published BED rates where available; otherwise compute simple indexes from published levels only if needed.
One-sentence interpretation rule
 A6 checks whether the labor-demand patterns in Figure 4 reflect broader establishment creation/destruction dynamics rather than only vacancy or hiring behavior.

Figure A7 — Local industry size and payroll benchmark
Outcome variable
employment share by sector


average weekly wage by sector


Grouping variable
 State or county, depending on stability, for the same six sectors used in Figures 3 and 4.
Comparison
 Compare how exposed sectors differ in local economic weight and pay structure across places.
Source
 QCEW. BLS states that QCEW publishes quarterly counts of employment and wages reported by employers covering more than 95 percent of U.S. jobs at county, state, and national levels by detailed industry.
Time window
 Latest available annualized quarter or latest full year.
Geography
 State by default; county only for selected illustrations if the paper needs a local benchmark panel.
Weighting / normalization
 Employment shares normalized by total QCEW-covered employment in the geography; wages reported as published average weekly wage.
One-sentence interpretation rule
 A7 is the denominator figure: it shows where the sectors discussed in Figures 3 and 4 actually matter most in local employment and wage terms.

Figure A8 — Aggregate linked-admin benchmark
Outcome variable
 Choose one national linked-admin benchmark series only:
J2J job-to-job flow rate as the default
 Optional secondary series:


hires from nonemployment


Grouping variable
 National aggregate; if a sector split is feasible from public J2J outputs, use the same broad six-sector set, otherwise keep the series aggregate.
Comparison
 Compare aggregate worker reallocation over time with the survey-based transition patterns from Figure 2.
Source
 LEHD public products, specifically J2J as part of the public LEHD/LED suite. Census states that the LEHD program produces public-use information combining federal, state, and Census data, and that the public data products include QWI, J2J, LODES, and PSEO.
Time window
 Quarterly, 2019 through latest available quarter.
Geography
 National only.
Weighting / normalization
 Use the published J2J rate or public aggregate directly; do not attempt to reconstruct linked microdata behavior from the public tables.
One-sentence interpretation rule
 A8 is a benchmark-only figure showing what aggregate linked administrative products add beyond surveys, without implying that public worker-level linked occupation histories are available.

Figure A9 — Local occupational composition
Outcome variable
share of workers in each of the 22 occupation groups


share of workers in high / middle / low AI-relevance terciles


selected demographic composition measures, preferably education and age


Grouping variable
 PUMA.
Comparison
 Compare the geographic concentration of AI-relevant occupation groups across places.
Source
 ACS PUMS. Census states that ACS PUMS enables users to create custom estimates and tables from person and housing-unit records, and PUMAs are the public geography used for ACS PUMS dissemination.
Time window
 Latest 1-year or 5-year PUMS file, depending on the desired stability and geography.
Geography
 PUMA only.
Weighting / normalization
 Use the ACS person weight and report weighted shares.
One-sentence interpretation rule
 A9 supports Figure 1 by showing where high-AI-relevance occupations are concentrated geographically and what kinds of workers occupy those places.

Figure A10 — Long-run career adaptation
Outcome variable
occupation-switch indicator


labor-force status


annual earnings or income measure


training or schooling participation, where consistently available


Grouping variable
 Respondents classified by the AI-relevance tercile of a baseline or prior occupation.
Comparison
 Compare long-run career paths and earnings trajectories for workers starting in higher- versus lower-AI-relevance occupations.
Source
 NLSY97 / NLS public-use. NLS public-use data are available at no cost through the Investigator, and the NLS system is designed to track labor-market and other life experiences of individuals over time.
Time window
 Use the latest public NLSY97 rounds available at implementation time.
Geography
 National only in public-use form.
Weighting / normalization
 Use the round-appropriate public-use NLS weight; if multiple rounds are stacked, use the NLS custom weighting guidance available through Investigator.
One-sentence interpretation rule
 A10 is the long-horizon extension: it asks whether occupations that look more AI-relevant at baseline are associated with different long-run career switching, training, or earnings paths.
What is now fully locked
The appendix is now strictly subordinate:
A1–A3 deepen Figure 2 on workers and mobility.


A4 deepens Figure 3 on firm adoption.


A5–A8 deepen Figure 4 on demand, payroll, churn, and aggregate worker-employer dynamics.


A9 deepens Figure 1 on local occupational composition.


A10 extends the paper forward in time, but only as a long-run interpretation layer, not a competing empirical spine.


—------------



Below is the data assembly checklist for implementation. It is ordered so you can build the paper figure by figure, while reusing shared inputs across figures.
Phase 0 — shared setup for the whole paper
Create one project folder with these subfolders: raw, intermediate, crosswalks, figures, and docs. Put all raw downloads there and never edit them in place. This matters because the paper uses multiple public systems with different cadences: CPS is monthly, BTOS is biweekly, JOLTS and CES are monthly, QCEW and BED are quarterly, OEWS and ABS are annual, and O*NET is versioned by release.
Then build three shared reference files before touching any figure. First, a 22-group occupation crosswalk linking CPS PRDTOCC1 to the 2018 SOC major-group structure excluding military, because CPS public-use files expose a 22-category occupation recode and OEWS also uses 22 of the 23 SOC major groups, excluding military occupations. Second, an O*NET-to-SOC lookup so the same occupation grouping can feed both the baseline and worker-side sections. Third, a sector crosswalk mapping BTOS sectors, JOLTS industries, CES industries, BED industries, and QCEW industries into the fixed six-sector set you already froze.
Finally, create one shared metadata file recording the exact release date, download URL, and snapshot date for every dataset. That avoids later confusion when public series revise or when annual programs roll to a new year. JOLTS and CPS are revised regularly, BTOS changes by collection window, and OEWS is an annual release.
Figure 1 — Occupational baseline
Download the latest OEWS national occupation employment and wage estimates and the latest O*NET database release. You need OEWS employment and wage estimates because OEWS is the official program producing annual employment and wage estimates for about 830 occupations, and you need O*NET because it is the public task-and-skill descriptor source for occupations.
Build one intermediate table at the detailed occupation level with these fields: detailed SOC code, occupation title, employment, median annual wage, and the six O*NET work-activity dimensions you froze earlier. Then aggregate that table to the common 22 occupation groups using employment weights from OEWS. Use that aggregated table to compute the AI Task Index and the high/middle/low terciles that will be reused in Figure 2 and the appendix. OEWS is aligned to the 2018 SOC and excludes military occupations, which is exactly why it is the right anchor for this aggregation.
Before making the figure, validate three things: the occupation groups sum to total OEWS employment, the wage aggregation rule is documented and consistent, and the tercile cutoffs are saved to a small lookup file for reuse later. The output of this phase should be:
figure1_panelA_occ_baseline.csv


figure1_panelB_task_heatmap.csv


ai_relevance_terciles.csv


Figure 2 — Worker outcomes and broad occupational transitions
Download all monthly CPS public-use microdata files from January 2019 to the latest month. Census states that the monthly CPS public-use files contain one record per household member and do not include personally identifiable information, and BLS confirms CPS is the monthly household survey for employment, unemployment, hours, earnings, and people not in the labor force.
Build two CPS extracts.
The first is the worker-outcome extract. Keep civilian noninstitutional persons age 16 and over. Pull the variables needed for:
labor-force status from PEMLR


broad occupation from PRDTOCC1


usual weekly hours on the main job from PEHRUSL1


person weight from PWCMPWGT


the public person-linking identifiers used across months
 Census documents the CPS public-use variables and the monthly file structure in the public-use documentation.


The second is the matched-month transition extract. Match adjacent months using the public CPS identifiers you froze earlier and compute month-ttt to month-t+1t+1t+1 transitions across the 22 occupation groups plus unemployed and not in labor force. Use PWCMPWGT/10,000 as the weight scaling consistent with the public-use documentation. Save both the raw transition counts and the row-normalized transition probabilities.
Then merge the CPS occupation groups to the AI-relevance terciles from Figure 1. That lets Panel A compare average hours across high/middle/low AI-relevance bins and Panel B show the transition matrix.
Validate four things before plotting:
weighted hours series look plausible month to month


unmatched or duplicate person links are logged


occupation groups map cleanly to the 22-group system


transition rows sum to one after normalization


The output of this phase should be:
figure2_panelA_hours_by_ai_tercile.csv


figure2_panelB_transition_counts.csv


figure2_panelB_transition_probs.csv


Figure 3 — Business-side AI adoption and reported workforce effects
Download the BTOS public data for the AI core questions over the full public AI-monitoring window and the AI supplement outputs for the pooled supplement period. Census says BTOS data collection occurs every two weeks, the sample is about 1.2 million businesses in six panels, and the BTOS core and AI content documentation explicitly includes the AI-use questions and supplement questions on workforce effects.
Build two BTOS extracts.
The first is the core AI trend extract with:
collection date


current AI use rate


expected future AI use rate


The second is the supplement workforce-effect extract with the shares of AI-using businesses reporting:
task previously done by an employee


supplement or enhance a task performed by an employee


introduce a new task


employment increased


employment decreased


employment did not change


Do not overcomplicate this figure with state or sector detail in the main text. Keep the main figure national, and push structural heterogeneity to ABS in the appendix. BTOS is already the direct public business-side AI source, and its documented purpose is to measure how widespread AI use is and how it affects employment and business organization.
Validate three things:
the AI trend series uses consistent question definitions through time


the supplement categories are drawn from the correct respondent universe


published percentages are used as published, not recomputed from incompatible files


The output of this phase should be:
figure3_panelA_btos_ai_trends.csv


figure3_panelB_btos_workforce_effects.csv


Figure 4 — Labor demand and turnover in AI-relevant sectors
Download JOLTS monthly industry rates from January 2019 to the latest month and CES monthly industry employment for the same period. BLS states that JOLTS produces monthly estimates of job openings, hires, and separations, and CES produces monthly industry estimates of employment, hours, and earnings.
Build one JOLTS panel and one CES panel for the fixed six-sector set:
manufacturing


information


financial activities


professional and business services


health care and social assistance


retail trade


For JOLTS, pull the seasonally adjusted:
job openings rate


hires rate


quits rate


layoffs and discharges rate


For CES, pull payroll employment and index it to August 2023 = 100. That keeps the visual comparison aligned with the BTOS public AI-monitoring window. BLS technical notes explain how JOLTS annual average rates are constructed from published monthly levels and CES employment, but for the figure you should stay with published monthly seasonally adjusted rates and a simple CES employment index.
Validate four things:
the sector labels are consistent across JOLTS and CES


all JOLTS series are seasonally adjusted


the CES index base month is correctly applied


no sector is missing observations in the chosen window


The output of this phase should be:
figure4_panelA_jolts_sector_rates.csv


figure4_panelB_ces_sector_index.csv


Figure 5 — Identification frontier
This figure is a hand-built synthesis matrix, not a statistical extraction. Use the five core datasets only:
CPS


BTOS


JOLTS


OEWS


O*NET


And the seven fixed empirical objects:
worker outcomes


occupational transitions


firm AI adoption


labor demand / turnover


occupational structure / wages


task mechanism


worker–firm AI linkage


Populate the matrix using the capability rules already frozen: filled for directly observed, half-filled for partial or indirect support, empty for not observed. The coding must be justified by the official scope of the sources: CPS is the household survey for worker outcomes, BTOS is the business survey with AI questions, JOLTS is the demand-flow survey, OEWS is the occupation employment/wage program, and O*NET is the occupation task/skill database.
The output of this phase should be:
figure5_capability_matrix.csv


Appendix build order
Do not start all appendix figures at once. Build them only after Figures 1–5 are assembled.
Start with A1–A3 because they are closest to Figure 2 and validate the worker-side story. CPS ASEC adds annual worker welfare context, SIPP adds medium-run longitudinal adjustment, and CPS supplements add direct displacement/tenure/mobility validation. CPS and SIPP are documented public worker-side sources, and the CPS supplement system is explicitly designed for topical modules.
Then build A4 from ABS as the annual structural business-side extension of Figure 3. ABS is the annual firm-side technology and business-characteristics complement, while BTOS remains the main-text real-time AI source.
Then build A5–A8 as pure context for Figure 4:
CES payroll/hours


BED establishment churn


QCEW local industry size and wages


LEHD public product benchmark
 QCEW covers more than 95 percent of U.S. jobs and is your denominator source, while LEHD public products are aggregate linked-admin benchmarks rather than open worker-level files.


Finally build A9–A10 only if needed for the final draft:
ACS PUMS for local occupational composition


NLSY for long-run career adaptation


QA checklist before plotting anything
Before producing any figure, run this same short QA pass:
verify the time window matches the frozen design


verify the geography is national unless the figure is explicitly appendix-local


verify the grouping variable matches the frozen 22-group occupation or six-sector system


verify the weight or normalization rule is written in the codebook or source note


save one tidy CSV per panel, not a mixed notebook object


write one plain-English interpretation sentence in the output metadata


Immediate implementation order
Build in this exact order:
ai_relevance_terciles.csv


figure1_panelA_occ_baseline.csv


figure1_panelB_task_heatmap.csv


figure2_panelA_hours_by_ai_tercile.csv


figure2_panelB_transition_probs.csv


figure3_panelA_btos_ai_trends.csv


figure3_panelB_btos_workforce_effects.csv


figure4_panelA_jolts_sector_rates.csv


figure4_panelB_ces_sector_index.csv


figure5_capability_matrix.csv


That sequence is important because Figure 1 defines the AI-relevance grouping used later, and Figures 2–4 depend on it. OEWS and O*NET define the occupation/task baseline, CPS carries the worker-side outcomes and transitions, BTOS carries the business-side AI adoption, and JOLTS/CES carry the demand-side context.


—------


Below is a repo-style task board you can drop into GitHub Issues, Linear, or a project README.
The board assumes the frozen design is already fixed: CPS for worker outcomes and transitions, BTOS for business-side AI adoption, JOLTS for labor-demand flows, OEWS for occupational employment/wages, and O*NET for task content; the appendix extends those figures with ASEC, SIPP, CPS supplements, ABS, CES, BED, QCEW, LEHD public products, ACS PUMS, and NLS.
PR-000 — Shared setup and crosswalks
Goal
 Create the common infrastructure used by all figures.
Dependencies
 None.
Outputs
crosswalks/occ22_crosswalk.csv


crosswalks/sector6_crosswalk.csv


docs/data_registry.csv


Tasks
 Create the 22-group occupation crosswalk.
 Create the fixed six-sector crosswalk.
 Create the dataset registry with source URL, release date, download date, and file hash.
Acceptance criteria
occ22_crosswalk.csv: every source occupation code used in the paper maps to exactly one paper-wide 22-group occupation.


sector6_crosswalk.csv: every sector used in BTOS, JOLTS, CES, BED, and QCEW maps to exactly one fixed six-sector group.


data_registry.csv: every raw data file used later has a recorded source, release date, and snapshot date.



T-001 — Figure 1, Panel A: occupational baseline
Goal
 Build employment share and median wage by the 22 occupation groups.
Dependencies
 PR-000.
Outputs
figures/figure1_panelA_occ_baseline.csv


Tasks
 Download latest OEWS national occupation data.
 Map detailed occupations to the 22-group system.
 Compute employment share and attach median annual wage.
Acceptance criterion
figure1_panelA_occ_baseline.csv: contains exactly 22 rows, one per occupation group, with columns for occupation group, employment, employment share, and median annual wage; employment shares sum to 1 within rounding.



T-002 — Figure 1, Panel B: task heatmap and AI index
Goal
 Build the O*NET task-profile matrix and AI Task Index.
Dependencies
 PR-000, T-001.
Outputs
figures/figure1_panelB_task_heatmap.csv


intermediate/ai_relevance_terciles.csv


Tasks
 Download latest O*NET data.
 Extract the six frozen task dimensions.
 Aggregate to the 22-group occupation system using OEWS employment weights.
 Standardize dimensions and compute the AI Task Index.
 Assign high/middle/low AI-relevance terciles.
Acceptance criteria
figure1_panelB_task_heatmap.csv: contains exactly 22 rows and the six frozen task-dimension scores as z-scores.


ai_relevance_terciles.csv: contains exactly 22 rows, one tercile per occupation group, and every occupation group is assigned to exactly one tercile.



T-003 — Figure 2, Panel A: worker hours by AI-relevance tercile
Goal
 Build the monthly CPS series for usual weekly hours by AI-relevance tercile.
Dependencies
 PR-000, T-002.
Outputs
figures/figure2_panelA_hours_by_ai_tercile.csv


Tasks
 Download monthly CPS public-use files from January 2019 onward.
 Restrict to civilian noninstitutional population age 16+.
 Keep employed respondents with valid occupation and usual-hours data.
 Map CPS occupation groups to AI-relevance terciles.
 Compute weighted mean usual weekly hours by month and tercile.
Acceptance criterion
figure2_panelA_hours_by_ai_tercile.csv: contains one row per month × tercile, uses the frozen CPS weight convention, and has no missing tercile-month combinations after the chosen start date.



T-004 — Figure 2, Panel B: occupational transition counts
Goal
 Build raw matched-month CPS transition counts.
Dependencies
 PR-000, T-002.
Outputs
figures/figure2_panelB_transition_counts.csv


Tasks
 Match CPS respondents across adjacent months using the frozen public identifiers.
 Define destination states as the 22 occupation groups plus unemployed plus NILF.
 Compute weighted transition counts from month ttt to month t+1t+1t+1.
Acceptance criterion
figure2_panelB_transition_counts.csv: contains one row per origin × destination × month pair, and every origin state has positive total weighted mass for months retained in the analysis.



T-005 — Figure 2, Panel B: transition probabilities
Goal
 Convert matched CPS transition counts into row-normalized probabilities.
Dependencies
 T-004.
Outputs
figures/figure2_panelB_transition_probs.csv


Tasks
 Row-normalize transition counts by origin state and month.
 Add summary fields for same-occupation retention, occupation switching, unemployment entry, and NILF entry.
Acceptance criterion
figure2_panelB_transition_probs.csv: for every month × origin state, destination probabilities sum to 1 within numerical tolerance.



T-006 — Figure 3, Panel A: BTOS AI-use trends
Goal
 Build national BTOS trends for current and expected AI use.
Dependencies
 PR-000.
Outputs
figures/figure3_panelA_btos_ai_trends.csv


Tasks
 Download BTOS core AI question outputs.
 Extract current AI use and expected next-6-month AI use.
 Build a time series starting at the first public AI-core wave.
Acceptance criterion
figure3_panelA_btos_ai_trends.csv: contains one row per BTOS collection period with columns for date, current AI use rate, and expected AI use rate, all as published weighted shares.



T-007 — Figure 3, Panel B: BTOS workforce effects
Goal
 Build national BTOS supplement shares for task and employment effects.
Dependencies
 PR-000.
Outputs
figures/figure3_panelB_btos_workforce_effects.csv


Tasks
 Download BTOS AI supplement outputs.
 Extract the six frozen workforce-effect categories.
 Pool over the frozen supplement window only.
Acceptance criterion
figure3_panelB_btos_workforce_effects.csv: contains exactly the six frozen categories, each as a published weighted share from the supplement universe.



T-008 — Figure 4, Panel A: JOLTS sector rates
Goal
 Build monthly JOLTS openings, hires, quits, and layoffs/discharges rates for the fixed six sectors.
Dependencies
 PR-000.
Outputs
figures/figure4_panelA_jolts_sector_rates.csv


Tasks
 Download seasonally adjusted JOLTS series from January 2019 onward.
 Map industries to the frozen six-sector set.
 Keep the four frozen rates only.
Acceptance criterion
figure4_panelA_jolts_sector_rates.csv: contains one row per month × sector × rate, and all rates are seasonally adjusted published series.



T-009 — Figure 4, Panel B: CES payroll employment index
Goal
 Build sector payroll employment indexes aligned to the BTOS AI window.
Dependencies
 PR-000.
Outputs
figures/figure4_panelB_ces_sector_index.csv


Tasks
 Download CES monthly sector employment series.
 Map to the six-sector set.
 Index each sector to August 2023 = 100.
Acceptance criterion
figure4_panelB_ces_sector_index.csv: contains one row per month × sector, and every sector equals 100 in August 2023.



T-010 — Figure 5: capability matrix
Goal
 Build the fixed synthesis matrix for the five core datasets.
Dependencies
 T-001 through T-009 conceptually complete.
Outputs
figures/figure5_capability_matrix.csv


Tasks
 Create rows for CPS, BTOS, JOLTS, OEWS, O*NET.
 Create columns for the seven frozen empirical objects.
 Populate each cell with direct, partial, or none according to the locked rules.
Acceptance criterion
figure5_capability_matrix.csv: contains exactly 5 rows × 7 columns of capability values plus a legend key, with no extra datasets or empirical objects.



T-011 — Figure A1: annual welfare and income context
Goal
 Build annual worker welfare outcomes by AI-relevance tercile from CPS ASEC.
Dependencies
 PR-000, T-002.
Outputs
figures/figureA1_asec_welfare_by_ai_tercile.csv


Tasks
 Download ASEC files for 2019 onward.
 Map occupations to the common 22-group system and terciles.
 Compute annual income, poverty, weeks worked, and unemployment incidence.
Acceptance criterion
figureA1_asec_welfare_by_ai_tercile.csv: contains one row per year × tercile with weighted values for all frozen welfare outcomes.



T-012 — Figure A2: medium-run adjustment
Goal
 Build event-time outcomes around occupational change or nonemployment transition using SIPP.
Dependencies
 PR-000, T-002.
Outputs
figures/figureA2_sipp_event_study.csv


Tasks
 Download the selected SIPP panel(s).
 Define transition events.
 Compute event-time means for employment, income, and program participation.
Acceptance criterion
figureA2_sipp_event_study.csv: contains one row per event time × AI tercile with weighted means for the frozen outcomes.



T-013 — Figure A3: displacement, tenure, and mobility validation
Goal
 Build CPS supplement validation measures.
Dependencies
 PR-000, T-002.
Outputs
figures/figureA3_cps_supp_validation.csv


Tasks
 Download the latest relevant CPS supplement files.
 Map occupations to the paper-wide grouping.
 Compute displacement, tenure, and mobility measures.
Acceptance criterion
figureA3_cps_supp_validation.csv: contains one row per occupation group or AI tercile with the frozen supplement-based measures and the correct supplement weight applied.



T-014 — Figure A4: ABS structural heterogeneity
Goal
 Build annual structural comparisons in firm AI or advanced-technology use.
Dependencies
 PR-000.
Outputs
figures/figureA4_abs_structural_adoption.csv


Tasks
 Download ABS technology/innovation tables with workforce-impact content.
 Keep industry and firm-size cuts only.
 Extract adoption and workforce-effect measures.
Acceptance criterion
figureA4_abs_structural_adoption.csv: contains one row per industry × firm-size group with the frozen ABS adoption and workforce-effect measures.



T-015 — Figure A5: CES payroll and hours context
Goal
 Build appendix payroll-employment and hours series for the six sectors.
Dependencies
 PR-000.
Outputs
figures/figureA5_ces_payroll_hours.csv


Tasks
 Download CES sector employment and average weekly hours series.
 Map to six sectors.
 Index both to August 2023 = 100.
Acceptance criterion
figureA5_ces_payroll_hours.csv: contains one row per month × sector with both indexed employment and indexed hours.



T-016 — Figure A6: BED establishment churn
Goal
 Build sector-level establishment churn context.
Dependencies
 PR-000.
Outputs
figures/figureA6_bed_churn.csv


Tasks
 Download BED quarterly series.
 Map industries to the six-sector set.
 Keep gross job gains, gross job losses, openings, and closings.
Acceptance criterion
figureA6_bed_churn.csv: contains one row per quarter × sector with all frozen BED measures present.



T-017 — Figure A7: QCEW local benchmark
Goal
 Build state-level sector employment shares and wages.
Dependencies
 PR-000.
Outputs
figures/figureA7_qcew_state_benchmark.csv


Tasks
 Download latest QCEW state-sector employment and wage data.
 Map to six sectors.
 Compute employment shares and keep average weekly wage.
Acceptance criterion
figureA7_qcew_state_benchmark.csv: contains one row per state × sector with employment share and average weekly wage, and state shares sum to 1 across the retained sectors only if explicitly normalized that way.



T-018 — Figure A8: LEHD public benchmark
Goal
 Build an aggregate linked-admin benchmark series.
Dependencies
 PR-000.
Outputs
figures/figureA8_lehd_benchmark.csv


Tasks
 Download the chosen public LEHD/J2J benchmark series.
 Keep the national aggregate only unless a sector split is stable and straightforward.
 Align time frequency to quarter.
Acceptance criterion
figureA8_lehd_benchmark.csv: contains one row per quarter for the chosen benchmark rate with source metadata attached.



T-019 — Figure A9: ACS local occupational composition
Goal
 Build local composition measures for occupation groups and AI terciles.
Dependencies
 PR-000, T-002.
Outputs
figures/figureA9_acs_local_composition.csv


Tasks
 Download latest ACS PUMS.
 Map occupations to the 22-group system and AI terciles.
 Compute PUMA-level occupation and tercile shares plus selected demographics.
Acceptance criterion
figureA9_acs_local_composition.csv: contains one row per PUMA with weighted shares for the 22 groups and the three AI terciles.



T-020 — Figure A10: long-run career adaptation
Goal
 Build long-run occupation-switching and earnings trajectories from NLS.
Dependencies
 PR-000, T-002.
Outputs
figures/figureA10_nls_longrun.csv


Tasks
 Download the chosen NLS public-use cohort data.
 Define baseline occupation and AI tercile.
 Compute longitudinal outcomes for occupation switching, earnings, and training.
Acceptance criterion
figureA10_nls_longrun.csv: contains one row per survey round × baseline AI tercile with weighted longitudinal outcomes.



Suggested status flow
Use the same labels for every ticket:
Backlog


Ready


In progress


Blocked


QA


Done


Suggested milestone order
Use three milestones:
M1 Core crosswalks + Figures 1–2


M2 Figures 3–5


M3 Appendix A1–A10



—-----



Once the repo is implemented, the next steps should be this exact sequence:
Run a full build from raw data to final figure CSVs.
 Make sure a fresh clone of the repo can reproduce every output file from raw/ through figures/ with one documented command or one ordered script chain.


Do a file-by-file acceptance review.
 For every output listed in the issue board, check the exact acceptance criterion and mark each ticket either:


pass,


pass with note,


fail.
 Do not move on until every main-text file passes:


figure1_panelA_occ_baseline.csv


figure1_panelB_task_heatmap.csv


ai_relevance_terciles.csv


figure2_panelA_hours_by_ai_tercile.csv


figure2_panelB_transition_probs.csv


figure3_panelA_btos_ai_trends.csv


figure3_panelB_btos_workforce_effects.csv


figure4_panelA_jolts_sector_rates.csv


figure4_panelB_ces_sector_index.csv


figure5_capability_matrix.csv


Generate the actual figures, not just the data tables.
 Create the final plotting scripts and export:


publication PNGs,


vector PDFs or SVGs,


one caption file per figure,


one source note per figure.
 At this stage, lock the visual style so all figures use the same fonts, axis formatting, date formatting, and color logic.


Write a one-page figure memo for each main-text figure.
 Each memo should contain:


the exact question the figure answers,


the dataset(s) used,


the construction logic,


the main empirical takeaway,


what the figure does not identify,


possible reviewer objections.
 This step is crucial because it turns code outputs into paper-ready arguments.


Run a claim audit against the five frozen claims.
 For each claim, verify that the implemented figure really supports it and does not overreach.

 Use this mapping:


Claim 1 ↔ Figure 1


Claim 2 ↔ Figure 2


Claim 3 ↔ Figure 3


Claim 4 ↔ Figure 4


Claim 5 ↔ Figure 5


For each one, write:


supported directly,


supported partially,


not yet supported.


Run robustness and sanity checks before drafting prose.
 These should be explicit scripts, not ad hoc inspection.

 For Figure 1:


test whether the AI-relevance terciles change materially under alternative O*NET weighting choices.


For Figure 2:


test alternative worker outcomes besides hours,


verify CPS matching rates,


verify transition probabilities are stable when pooling differently.


For Figure 3:


verify the BTOS trend does not mix incompatible question definitions,


confirm supplement shares are computed on the correct universe.


For Figure 4:


verify sector mappings,


compare rates versus levels where relevant,


check whether the patterns are driven by one unusual period.


For Figure 5:


confirm every cell is justified by documentation, not intuition.


Write the Methods / Data section immediately after validation.
 Do not wait until the full paper draft.
 This section should already be straightforward because the repo structure forced you to define:


source,


universe,


time window,


geography,


grouping,


weighting,


normalization,


limitations.


Draft the paper in the same order as the figures.
 Use the frozen structure:


Introduction


Section 1: occupational baseline


Section 2: worker outcomes and mobility


Section 3: business-side AI adoption


Section 4: labor demand and turnover


Section 5: identification frontier and measurement agenda


Conclusion


For each section, write in this order:


thesis sentence,


dataset sentence,


figure discussion,


identification boundary,


implication.


Only after the main text is stable, build the appendix figures.
 Do not let the appendix expand the project prematurely.
 Appendix order should be:


A1–A3 first,


then A4,


then A5–A8,


then A9–A10 last.


Create a “results freeze” commit.
 Once the main figures and paper draft are aligned, create one tagged commit that freezes:


raw data snapshot references,


intermediate outputs,


final figure data,


plotting scripts,


manuscript draft version.
 That gives you one stable research state you can cite internally.


Do an internal replication pass by a second person.
 Someone other than the implementer should:


clone the repo,


run the full pipeline,


reproduce the main figures,


check a sample of source-to-output mappings.
 If they cannot do it cleanly, the repo is not ready.


Then move into paper-polish mode.
 At that point the remaining tasks are:


tighten captions,


shorten figure notes,


align terminology across sections,


make the introduction and conclusion sharper,


trim anything that sounds broader than the evidence.


The exact milestone sequence after implementation is therefore:
Build check → acceptance review → figure generation → figure memos → claim audit → robustness checks → methods section → main draft → appendix → results freeze → independent replication → final polish
The single most important next step, right after implementation, is not writing. It is the claim audit plus robustness review, because that is where you find out whether the repo actually proves the paper you planned.
