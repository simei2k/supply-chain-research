# Task: build the full incident set

Paste the line below into a Claude Code session opened in this folder, or say "do TASK.md".

> Read CLAUDE.md, codebook.md, sources.md and search_terms.md, then carry out TASK.md stage by stage. Stop after each stage, show me the counts, and wait for my go-ahead.

## Stage 1: pull the structured sources

1. Re-download the KEV CSV to `data/raw/kev_<YYYY-MM-DD>.csv`. Run:
   - `python scripts/kev_filter.py data/raw/kev_<date>.csv data/candidates/kev_keyword_pool.csv`
   - `python scripts/kev_clean.py data/raw/kev_<date>.csv data/candidates/kev_candidates.csv`
   Then review entries the keyword pool caught but the rules missed, and add rules for any management, remote-access, backup, security or identity product.
2. Clone or download the CNCF catalog, MITRE ATT&CK STIX data and VCDB **outside the repo** (for example `~/research-data/`). Record each commit or release in `sources.md`.
3. Extract candidates 2021 to the freeze into `data/candidates/`:
   - `cncf_candidates.csv` from the catalog entries;
   - `mitre_campaigns.csv` for campaigns using T1195 or T1199;
   - `vcdb_partner.csv` for incidents with a partner route in;
   - `hhs_business_associate.csv` from the HHS export (the user downloads it if the portal blocks scripts).
4. Report row counts per file.

## Stage 2: targeted news search

1. Run the searches in `search_terms.md` against each outlet, for the full date range.
2. Log every query in `search_log.csv` (one row per query).
3. Add new candidates to `data/candidates/news_candidates.csv`: incident name, date, outlet link, why it may qualify. Links and facts only.
4. Stopping rule: stop when a further outlet or term adds fewer than two new MSP-specific or MSP-relevant candidates. Record when and why you stopped in `search_log.csv`.

## Stage 3: deduplicate

1. Merge every file in `data/candidates/` (plus any exported Sheet tabs the user adds) into `data/candidates.csv`, one row per supplier event.
2. Start with the key vendor + product + year, then check by hand: one campaign can span several CVEs; one CVE can be used in several separate incidents.
3. Keep a `sources_merged` column listing every pool the event came from.
4. Apply the inclusion rules in CLAUDE.md. Excluded cases go to `data/logged.csv` with reason and rule. Keep the tally of "exploited, no downstream reach reported" by trust boundary.
5. Report: candidates in, events after dedupe, counted, logged, by relevance class.

## Stage 4: code each counted incident

1. For each counted event, find primary sources (advisory, vendor post, filing, incident-response report) and fill every column of `data/coded.csv` per `codebook.md`.
2. Do not code from news alone. If no primary source exists, log the case instead.
3. Put uncertainty in Coding notes. Never guess capability or behaviours.
4. Work in batches of 10; after each batch show the rows for review.

## Stage 5: signals

Compute and report:

- **S1 Volume:** counted incidents; MSP-specific plus MSP-relevant; incidents in each of the top four trust boundaries. Strong: 60+ total, 30+ MSP-specific or MSP-relevant, 5+ in each top-four boundary.
- **S2 Prevalence x impact:** share of priority-cell incidents (tier 3 or 4, reach Dozens or more) held by the top two or three trust boundaries. Strong: 50% or more.
- **S3 Reach codability:** share of MSP-specific and MSP-relevant incidents with reach Unknown. Strong: 40% or less.
- **S4 Behaviour convergence:** behaviours present in 60% or more of priority-cell incidents that report behaviours. Strong: three or four behaviours.

Write the results to `signals.md` with the date and the commit of `data/coded.csv` they were computed from.

## Never

- Copy article text into the repo.
- Commit company or internal data of any kind.
- Change a search term without logging it.
