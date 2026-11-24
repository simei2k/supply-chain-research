# MSP supply-chain trust paths

**Question:** Which supplier-compromise paths are both the most common and the most consequential for MSPs, judged by administrative capability and customer reach, and which detectable behaviours follow them?

**Article message:** supply-chain incidents will keep happening and much of the pattern is public. MSPs can rank the trusted connections they run by how often each kind is compromised and how much damage it can do, then switch on the right controls and watch for the matching behaviours.

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
