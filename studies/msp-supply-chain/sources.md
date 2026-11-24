# Sources

Update the pull date and version every time a source is pulled.

| Source | URL | Format | Role | Pull date | Version / commit | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CISA Known Exploited Vulnerabilities | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | CSV | Exploited flaws in management, remote-access, backup, security and identity products | 2026-11-24 | `data/raw/kev_2026-11-24.csv` | Pulled; keyword pool 137 → `kev_keyword_pool.csv`; rules give 95 candidates (JAVS Viewer and N-able MailAssure rules added 2026-11-24) |
| Atlantic Council Breaking Trust | atlanticcouncil.org (Cyber Statecraft Initiative, "Software supply chain security: the dataset"; confirm the URL when re-pulling) | XLSX (SCRM-Database-v.3) | Curated incidents 2021 to 2023 | 2026-11-24 | v3 (last updated 2023) | Pulled; 63 rows first-pass coded. Raw file not committed (download from source) |
| CNCF Catalog of Supply Chain Compromises | https://github.com/cncf/tag-security/tree/main/community/catalog/compromises (moved from supply-chain-security/) | Markdown | Software supply-chain incidents | 2026-11-24 | commit 5fb87f4 (2025-12-08) | Pulled; 31 entries 2021+ → `cncf_candidates.csv`. Catalog has no entries after 2024 |
| MITRE ATT&CK campaigns | https://github.com/mitre-attack/attack-stix-data | STIX JSON | Campaigns using T1195 (supply chain) and T1199 (trusted relationship) | 2026-11-24 | ATT&CK v20.1, commit a8db2f5 (2026-11-05) | Pulled; 2 campaigns 2021+ → `mitre_campaigns.csv` |
| VCDB (VERIS Community Database) | https://github.com/vz-risk/VCDB | JSON | Breaches with a partner route in | 2026-11-24 | commit d2c9c2a (2026-11-23) | Pulled; 35 incidents 2021+ (partner actor, partner vector, or secondary victims) → `vcdb_partner.csv` |
| HHS OCR breach portal | https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf | CSV export | Healthcare breaches with a business associate present | 2026-11-24 | Both tabs, via `scripts/hhs_download.py` | Pulled; 1,512 BA-present breaches 2021+ (1,294 hacking) → `hhs_business_associate.csv`. One row per covered entity, not per BA event; HHS descriptions kept (decision 2026-11-24) |
| SEC EDGAR full-text search | https://www.sec.gov/edgar/search/ (full-text search) | Filings | 8-K Item 1.05 incidents at vendors and providers | | query and date | To pull |
| Government advisories | CISA, NCSC UK, ACSC, CCCS advisory pages | Web | Primary source for incidents and reach | | per item | Ongoing |
| Vendor and incident-response reports | Vendor advisories; Huntress, Sophos, Mandiant, Microsoft and similar | Web | Primary source for capability, reach, behaviours | | per item | Ongoing |
| News outlets (candidate finding only) | See `search_terms.md` | Web | Find candidates; not used for coding | | per search | Ongoing |

## Not used

- Malicious-package feeds (OpenSSF malicious-packages, OSV) as a bulk source: they list every malicious upload and would swamp the set. Package incidents enter only as named campaigns.
- Vendor threat reports whose incident lists are not public: used only to spot missed incidents, not for counts.
