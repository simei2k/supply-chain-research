# Sources

Update the pull date and version every time a source is pulled.

| Source | URL | Format | Role | Pull date | Version / commit | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CISA Known Exploited Vulnerabilities | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | CSV | Exploited flaws in management, remote-access, backup, security and identity products | 2026-11-24 | `data/raw/kev_2026-11-24.csv` | Pulled; filtered to 93 candidates |
| Atlantic Council Breaking Trust | atlanticcouncil.org (Cyber Statecraft Initiative, "Software supply chain security: the dataset"; confirm the URL when re-pulling) | XLSX (SCRM-Database-v.3) | Curated incidents 2021 to 2023 | 2026-11-24 | v3 (last updated 2023) | Pulled; 63 rows first-pass coded. Raw file not committed (download from source) |
| CNCF Catalog of Supply Chain Compromises | https://github.com/cncf/tag-security/tree/main/supply-chain-security/compromises | Markdown | Software supply-chain incidents, 2019 to present | | record commit | To pull |
| MITRE ATT&CK campaigns | https://github.com/mitre-attack/attack-stix-data | STIX JSON | Campaigns using T1195 (supply chain) and T1199 (trusted relationship) | | record release | To pull |
| VCDB (VERIS Community Database) | https://github.com/vz-risk/VCDB | JSON | Breaches with a partner route in | | record commit | To pull |
| HHS OCR breach portal | https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf | CSV export | Healthcare breaches with a business associate present | | export date | To pull |
| SEC EDGAR full-text search | https://www.sec.gov/edgar/search/ (full-text search) | Filings | 8-K Item 1.05 incidents at vendors and providers | | query and date | To pull |
| Government advisories | CISA, NCSC UK, ACSC, CCCS advisory pages | Web | Primary source for incidents and reach | | per item | Ongoing |
| Vendor and incident-response reports | Vendor advisories; Huntress, Sophos, Mandiant, Microsoft and similar | Web | Primary source for capability, reach, behaviours | | per item | Ongoing |
| News outlets (candidate finding only) | See `search_terms.md` | Web | Find candidates; not used for coding | | per search | Ongoing |

## Not used

- Malicious-package feeds (OpenSSF malicious-packages, OSV) as a bulk source: they list every malicious upload and would swamp the set. Package incidents enter only as named campaigns.
- Vendor threat reports whose incident lists are not public: used only to spot missed incidents, not for counts.
