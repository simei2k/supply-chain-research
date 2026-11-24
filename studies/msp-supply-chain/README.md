# MSP supply-chain trust paths

**Question:** Which supplier-compromise paths are both the most common and the most consequential for MSPs, judged by administrative capability and customer reach, and which detectable behaviours follow them?

**Article message:** supply-chain incidents will keep happening and much of the pattern is public. MSPs can rank the trusted connections they run by how often each kind is compromised and how much damage it can do, then switch on the right controls and watch for the matching behaviours.

## Methodology (outline, as of 2026-11-24)

1. **Scope and unit.** Public incidents from 1 January 2021 to the freeze on 30 November 2026. One incident is one supplier event, counted once however many reports cover it. Counting needs a primary source: a government advisory, vendor disclosure, regulatory filing or incident-response report.
2. **Candidate pools.** Candidates come from structured sources and from searches. Versions and pull dates are in `sources.md`.
   - Structured: CISA KEV, filtered to management, remote-access, backup, security and identity products; Atlantic Council Breaking Trust; the CNCF catalogue; MITRE ATT&CK campaigns using T1195 or T1199; VCDB incidents with a partner route in; HHS OCR breaches involving a business associate.
   - Searches: 40 fixed, logged queries across five security outlets and four government agencies, ending at a stated stopping rule (`search_terms.md`, `search_log.csv`).
   - Earlier manual sweeps: the coding Sheet's two tabs.
3. **Inclusion.** An incident counts only when a supplier, service provider or their product was compromised or abused to reach that supplier's customers (`CLAUDE.md`). The following are logged with a reason, not counted:
   - customer-credential abuse on a platform;
   - flaws disclosed but not exploited;
   - packages published by attackers;
   - out-of-period events.
   
   KEV flaws exploited on a provider's own server count only when a report shows downstream reach; otherwise they are tallied as "exploited, no downstream reach reported".
4. **Deduplication.** Every pool row is mapped by hand to one event (`data/dedupe/`). Mass-exploitation campaigns of one product count as one incident. `scripts/build_candidates.py` rebuilds `data/candidates.csv` and stops if any row is left unmapped. HHS rows are grouped by business associate.
5. **Relevance.** Each event is coded:
   - MSP-specific: an MSP or IT service provider is directly involved.
   - MSP-relevant: technology used to manage many customer environments.
   - General: everything else.
   
   The main ranking uses the first two. The all-events ranking is context.
6. **Coding.** Counted incidents are coded from primary sources against `codebook.md`:
   - trust boundary (11 categories);
   - capability as reported (tiers 1 to 4);
   - reach in organisations (exact figure or band);
   - 11 behaviours mapped to ATT&CK;
   - consequences.
   
   Use `NR` unless a source states something did not happen. Code nothing from news alone.
7. **Analysis.** Trust boundaries are ranked by frequency (prevalence) and by the share of "priority cell" incidents: capability tier 3 or 4 with reach of dozens or more (impact). Behaviours seen in 60% or more of priority-cell incidents are reported as detection priorities. Four signals with preset thresholds test whether the data can support the article (`TASK.md` Stage 5).
8. **Reliability.** A second coder codes a random 20% of counted incidents. The target is Cohen's kappa of 0.7 or more on trust boundary and capability tier.

**Known limits.**
- Public reporting under-represents small MSP incidents and over-represents US healthcare (HHS).
- Reach and behaviours are often unreported.
- News searches favour recent years.
- Relevance and trust-boundary coding involve judgement, which the second coder checks.

## Status (2026-11-24)

| Part | Status |
| --- | --- |
| Proposal and decisions | Done (shared doc) |
| KEV and Breaking Trust pulled | Done |
| Pilot coding | 14 counted incidents in `data/coded.csv`; Snowflake moved to `data/logged.csv` |
| Other pools (CNCF, MITRE, VCDB, HHS) | Pulled 2026-11-24 (Stage 1) |
| News searches (Stage 2) | Done 2026-11-24: 40 queries, 65 candidates in `data/candidates/news_candidates.csv` |
| Dedupe (Stage 3) | Done 2026-11-24: 780 events; 210 counted (first pass), 517 to verify, 43 exploited with no downstream reach, 10 logged |
| Full coding | To do |
| Second coder | To do |
| Telemetry visibility | Done internally (see `telemetry/README.md`) |

## Sheet tabs (added 2026-11-24)

Exported from the coding Sheet as CSV into `data/candidates/`:

- "Other candidates" → `sheet_other_candidates.csv` (40 rows)
- "Source sweep" → `sheet_source_sweep.csv` (60 rows)

## Decisions so far

1. Exploiting a flaw in an MSP's own RMM counts, coded as its own access path, when downstream reach is reported.
2. Capability is coded as reported (matrix) and as possible (recommendations only).
3. Rank categories, not vendors; name incidents by the facts in public reporting and credit vendor responses.
4. Data freeze 30 November 2026.
5. Inclusion rules as in `CLAUDE.md`.
6. ConnectWise Cloud Backup reach: use the 162 tenants confirmed by Huntress.
7. HHS business-associate rows keep the HHS web description. A `business_associate` column is filled from the filer (when the BA filed), from names stated in descriptions, and by hand for covered-entity hacking rows of 100,000+ people (`data/hhs_ba_matches.csv`; those rows hold 85% of affected people in covered-entity hacking rows). Smaller rows are left unmatched (2026-11-24).
8. Mass-exploitation campaigns of one product (MOVEit, Accellion, Cleo) are one incident each; providers breached through them are merged in (2026-11-24, to confirm).
9. Packages published by attackers (typosquats, dependency-confusion copycats, malicious uploads) are logged, not counted: no supplier was compromised. Maintainer-account takeovers and maintainer sabotage count (2026-11-24, to confirm).
10. HHS vendor events count (first pass) only when HHS shows more than one customer; the rest are 'To verify' (2026-11-24, to confirm).
11. The main trust-boundary ranking uses MSP-specific and MSP-relevant counted incidents; the all-incidents ranking (HHS included) is reported as context. HHS vendors that are counted or have IT-sounding names were reviewed for relevance (`data/dedupe/hhs_relevance.csv`); the rest default to General supply-chain (2026-11-24).

## Files

See `CLAUDE.md` for the file map, `codebook.md` for fields, `TASK.md` for the collection steps.
