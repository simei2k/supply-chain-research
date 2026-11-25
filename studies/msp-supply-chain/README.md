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
| Dedupe (Stage 3) | Done 2026-11-24; as of 2026-11-25: 811 events; 184 counted (all coded), 499 to verify, 46 exploited with no downstream reach, 82 logged |
| Full coding (Stage 4B) | Done 2026-11-25: 184 counted incidents coded in `data/coded.csv` (63 MSP-specific or MSP-relevant, 121 General). 499 HHS and other events remain "To verify" and are not part of the counted set |
| Second coder | Done 2026-11-26: MSP sample (13): trust boundary 0.78, tier 0.70, relevance 0.34 (`data/coder2.csv`). General sample (24): trust boundary 0.93, tier 0.50 before decision 17 (software-supply agreement 36%), 24 of 24 after a rule-guided re-check; reach 0.56; relevance degenerate (`data/coder2_general.csv`). Relevance re-check under the written rule: 37 of 37 agree (`data/relevance_recheck.csv`) |
| Signals (Stage 5) | Provisional 2026-11-25 in `signals.md`: MSP subset S1, S2, S3 strong, S4 not met |
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
8. Mass-exploitation campaigns of one product (MOVEit, Accellion, Cleo, GoAnywhere) are one incident each; providers breached through them are merged in (confirmed 2026-11-24).
9. Packages published by attackers (typosquats, dependency-confusion copycats, malicious uploads) are logged, not counted: no supplier was compromised. Maintainer-account takeovers and maintainer sabotage count (2026-11-24, to confirm).
10. HHS vendor events count (first pass) only when HHS shows more than one customer; the rest are 'To verify' (2026-11-24, to confirm).
11. The main trust-boundary ranking uses MSP-specific and MSP-relevant counted incidents; the all-incidents ranking (HHS included) is reported as context. HHS vendors that are counted or have IT-sounding names were reviewed for relevance (`data/dedupe/hhs_relevance.csv`); the rest default to General supply-chain (2026-11-24).

12. Ransomware on a provider's shared hosting infrastructure is coded tier 2 (Endpoint action) when no attacker techniques are reported; the inference is stated in the coding note (2026-11-25).
13. A multi-customer outage of a provider's hosted service counts as "services exposed" even without customer data exposure (Ingram Micro, Rackspace). A single customer reached through a provider path is logged, not counted (M&S/Co-op, Play/Adlumin) (2026-11-25).
14. Year is the first public disclosure; events first disclosed in 2020 are logged as out of period even when 2021 notices followed (Netgain) (2026-11-25).
15. Coding values: `N` only on an explicit statement; behaviours inferred from a CVE description or malware capability (not observed) are `NR`; "crossed customer boundary" is `Y` when data of more than one customer held by the provider was exposed (2026-11-25).

16. Relevance definitions tightened after the second coder (relevance kappa 0.34); see `codebook.md`. Recoded: Atento and Verkada to General, Okta/Sitel and SimpleHelp utility-billing provider to MSP-relevant. Mimecast boundary set to Cloud integration (2026-11-25).

17. Tier rule for software-supply delivery: malicious code delivered to customers' endpoints through the supplier's own package, update, installer or release channel is tier 3 (Software deployment). Adopted after the General second-coder check (tier kappa 0.50, software-supply agreement 36%); 21 rows recoded, then Accellion corrected to tier 2 after a blind re-check (2026-11-26).

18. Relevance line for data-holding vendors: application and data SaaS vendors (EHR, billing, benefits, mailing, analytics, AI) are General even when they host many customers' data; MSP-specific is reserved for IT operations suppliers (MSPs, IT outsourcers, managed hosting, IaaS and PaaS, government shared IT). The rule matches the existing coding, so no rows changed. Heroku, Vercel and Railway stay MSP-specific as PaaS (2026-11-26).

## Files

See `CLAUDE.md` for the file map, `codebook.md` for fields, `TASK.md` for the collection steps.
