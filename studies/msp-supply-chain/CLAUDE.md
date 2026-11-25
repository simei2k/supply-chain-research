# Study: MSP supply-chain trust paths

@codebook.md

## Research question

Which supplier-compromise paths are both the most common and the most consequential for MSPs, judged by administrative capability and customer reach, and which detectable behaviours follow them?

The article ranks **categories of trust boundary**, never individual vendors. Incidents and vendors may be named by the facts in public reporting, crediting vendor responses where true.

## Period and unit

- Period: 1 January 2021 to the data freeze, **30 November 2026**.
- One incident = one supplier event, deduplicated across every report that covers it.
- An incident needs a **primary source** (government advisory, vendor disclosure, filing, or incident-response report). Secondary reporting alone is logged, not counted.

## Inclusion rules

An incident **counts** only when a supplier, a service provider or their product was compromised or abused to reach that supplier's customers.

| Case | Decision |
| --- | --- |
| Customer credential abuse on a platform: each customer's own stolen credentials were used and the supplier itself was not compromised (Snowflake 2024) | Logged, not counted |
| A KEV flaw exploited on a provider's own server, with a report showing the attacker went on to reach that provider's customers (SimpleHelp and DragonForce 2025) | Counted |
| The same, with no report of downstream reach | Logged, and tallied by trust boundary as "exploited, no downstream reach reported". Never assign guessed actions |
| A service provider that holds customer data was itself breached and data of more than one customer was exposed (Conduent, TriZetto) | Counted, trust boundary "Service provider holding customer data" |
| Each victim ran the software on its own server and lost its own data | KEV rule above applies |
| Flaws disclosed but not exploited | Out of scope |

Every excluded case goes to `data/logged.csv` with its reason and rule.

## Files

| File | What it is |
| --- | --- |
| `codebook.md` | Fields, allowed values, tiers, reach bands |
| `TASK.md` | The collection task for a Claude Code session |
| `sources.md` | Every source with URL and pull date |
| `search_terms.md` | Fixed search terms and outlets |
| `search_log.csv` | One row per search run |
| `data/raw/` | Small public pulls, dated (KEV CSV) |
| `data/candidates/` | Candidate pools before deduplication |
| `data/candidates.csv` | All pools, deduplicated: one row per supplier event with status (built by `scripts/build_candidates.py`) |
| `data/dedupe/` | Hand dedupe decisions: `events.csv` (one row per event), `event_map.csv` (pool row to event) and `hhs_relevance.csv` (relevance review of HHS vendors) |
| `data/coded.csv` | Counted incidents, coded |
| `data/coder2.csv` | Blind second-coder rows for the reliability sample (same columns as `coded.csv`) |
| `data/logged.csv` | Excluded cases, with reasons |
| `signals.md` | Stage 5 signals and reliability results (`scripts/signals.py`) |
| `data/hhs_ba_matches.csv` | Hand matches of HHS covered-entity rows to their business associate, with source |
| `scripts/` | KEV filters and any collection or dedupe scripts |
| `telemetry/README.md` | Plain-language note only; no internal data |

## Rules specific to this study

- Code **capability as reported** for the matrix. "Capability as possible" is coded once per product, in a separate file, for recommendations only.
- Reach: record the exact count and its source where given; otherwise use the band. Prefer the confirmed figure over larger unconfirmed ones (ConnectWise Cloud Backup: 162 tenants confirmed by Huntress; other reports say 173 or over 300).
- Use `NR` (not reported) rather than `N` unless a source explicitly says something did not happen.
- Each coded row carries its primary source links and a short coding note. Flag anything uncertain in the note.
