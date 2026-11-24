# Search terms and outlets

Fixed so that searches can be repeated. Add new terms at the bottom with the date added; never silently change a term.

## Date range

1 January 2021 to 30 November 2026.

## Outlets (candidate finding)

- BleepingComputer
- The Record (Recorded Future News)
- SecurityWeek
- Dark Reading
- The Hacker News
- CISA news and advisories; NCSC UK; ACSC; CCCS

Use each outlet's own search or tag pages, or a web search restricted to the site. Do not bulk-scrape.

## Core terms

- "managed service provider" OR MSP
- MSSP
- RMM OR "remote monitoring and management"
- "supply chain attack" OR "supply-chain attack"
- "trusted relationship"
- "downstream customers"
- "third-party" breach "customers"
- "business associate" breach (healthcare data-holding providers)
- "OAuth app" OR "application identity" compromised tenants

## Product terms

ScreenConnect, ConnectWise, Kaseya, VSA, N-able, N-central, SimpleHelp, Atera, NinjaOne, Datto, Syncro, Pulseway, TeamViewer, AnyDesk, BeyondTrust, Splashtop, ManageEngine, Endpoint Central, Ivanti EPM, SolarWinds, Veeam, Commvault, Veritas, Arcserve, Nakivo, SkyKick, Okta, JumpCloud, Entra ID app, GDAP

## Combining

Search each product term with "breach" OR "exploited" OR "compromised" OR "customers". Log every query in `search_log.csv`.

## Added later

| Date added | Term | Why |
| --- | --- | --- |
| 2026-11-24 | Headline listings: BleepingComputer tags supply-chain-attack and managed-service-provider; The Hacker News labels Supply Chain Attack, Supply Chain, Supply Chain Security, Software Supply Chain (titles, links and dates only, via `scripts/harvest_headlines.py`) | Second pass: MSP subset too thin after Stage 3. Each headline screened by hand for a supplier compromise that could involve MSPs; those leads researched individually |
