# Codebook

Columns of `data/coded.csv`, in order. Values: `Y` yes, `N` no (only when a source says so), `NR` not reported.

| Column | Allowed values / format | Notes |
| --- | --- | --- |
| ID | `P01`... for pilot, `I001`... for new rows | Unique |
| Incident | Short name | Name the event, not just the vendor |
| Year | YYYY | Year the compromise was disclosed |
| Relevance | MSP-specific; MSP-relevant; General supply-chain | MSP-specific: customers were reached through an MSP, MSSP, IT outsourcer, hosting or cloud-infrastructure provider (including government shared IT providers), or through a product sold mainly to MSPs (e.g. Kaseya VSA, N-central, SkyKick). MSP-relevant: the compromised product is one MSPs use to administer or secure customer environments: RMM, remote access or support, PAM or password vaults, backup, identity, MFA or directory, email security, device management, hosting control panels, MSP-facing distribution or licensing. General: everything else, including business-process outsourcers and products not used for IT administration (tightened 2026-11-25). Application and data vendors are General even when they host customer data for many organisations: EHR, practice-management, billing, benefits, mailing, analytics, AI and other SaaS applications. MSP-specific covers IT operations suppliers: MSPs and MSSPs, IT outsourcers, managed hosting, colocation, IaaS and PaaS providers, and government shared IT providers (clarified 2026-11-26) |
| Trust boundary | One of the eleven below | The compromised component |
| Access path | Free text | How the attacker got in, e.g. "Exploited flaw (CVE-...)", "Stolen app secret" |
| Read data | Y / N / NR | Capability as reported |
| Access credentials | Y / N / NR | Credentials or tokens |
| Execute commands | Y / N / NR | |
| Deploy software | Y / N / NR | |
| Create/modify accounts | Y / N / NR | |
| Change security settings | Y / N / NR | |
| Disable protection | Y / N / NR | |
| Alter backup | Y / N / NR | Alter backup or recovery |
| Multiple tenants | Y / N / NR | Feeds reach, not tier |
| Lateral movement | Y / N / NR | Across endpoints |
| Capability tier (reported) | `1 Data access`; `2 Endpoint action`; `3 Software deployment`; `4 Security controls` | Highest tier reached |
| Orgs reached (as reported) | Free text with the figure and who reported it | |
| Reach band | Single organisation; Several; Dozens; Hundreds or more; Unknown; Unknown (more than one) | Several = 2 to 9, Dozens = 10 to 99 |
| Crossed customer boundary | Y / N / NR | |
| Shell/PowerShell | Y / N / NR | Behaviour |
| Remote command | Y / N / NR | Behaviour |
| Software deployment | Y / N / NR | Behaviour |
| Services/tasks | Y / N / NR | New services or scheduled tasks |
| Credential access | Y / N / NR | Behaviour |
| Security-tool interference | Y / N / NR | Exclusions, protection turned off, services stopped |
| Backup disruption | Y / N / NR | Behaviour |
| Lateral movement (beh.) | Y / N / NR | Behaviour |
| Archive creation | Y / N / NR | Behaviour |
| Exfiltration | Y / N / NR | Behaviour |
| Ransomware | Y / N / NR | Behaviour |
| Primary source | URLs separated by ` ; ` | At least one primary source |
| Coding notes | Free text | Uncertainty, conflicting figures, dedupe decisions |
| Data exposed | Y / N / NR | Consequence |
| People or orgs exposed | Number and unit, with date of the figure | Latest primary figure |
| Service disruption | Y / N / NR | Consequence |
| Ransomware or encryption | Y / N / NR | Consequence |
| Coder | Name or `claude-<session>` | |
| Coded on | YYYY-MM-DD | |

## Trust boundaries (eleven)

1. Software update mechanism
2. Build or release pipeline
3. Vendor or developer account
4. RMM or management platform
5. Remote-access tool
6. Cloud integration
7. API credential or token
8. Plugin, extension or package
9. Backup or security-management platform
10. Identity provider
11. Service provider holding customer data

## Capability tiers

| Tier | Includes |
| --- | --- |
| 1 Data access | Read data, access credentials or tokens |
| 2 Endpoint action | Execute commands, lateral movement |
| 3 Software deployment | Deploy software, create or modify accounts |
| 4 Security controls | Change security settings, disable protection, alter backup |

**Tier rule for software-supply delivery (2026-11-26):** when malicious code reaches customers' endpoints through the supplier's own package, update, installer or release channel, the capability reported is tier 3 (Software deployment). Tier 2 applies when an attacker runs commands through a provider's access (hosting ransomware, remote tools). Platform incidents where only the customers' secrets were stolen (e.g. CircleCI) stay tier 1.

**Priority cell:** tier 3 or 4 with reach of Dozens or Hundreds or more.

## Behaviours mapped to MITRE ATT&CK

| Behaviour | Technique (starting point) |
| --- | --- |
| Shell/PowerShell | T1059 |
| Remote command | T1219, T1072 |
| Software deployment | T1072, T1105 |
| Services/tasks | T1543, T1053 |
| Credential access | T1003, T1552 |
| Security-tool interference | T1562.001 |
| Backup disruption | T1490 |
| Lateral movement | T1021, T1550 |
| Archive creation | T1560 |
| Exfiltration | T1041, T1567 |
| Ransomware | T1486 |

## Reliability

A second coder codes a random 20% of counted incidents. Target Cohen's kappa of 0.7 or more on trust boundary and capability tier.
