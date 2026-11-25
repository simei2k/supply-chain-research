# Findings: which supplier-compromise paths matter most for MSPs

Written 2026-11-26. Data frozen 30 November 2026. All figures come from `data/coded.csv` (184 counted incidents), `data/candidates.csv` and `signals.md`; recompute with `scripts/signals.py`. This is a research summary, not article copy.

## The question and the answer

**Question.** Which supplier-compromise paths are both the most common and the most consequential for MSPs, judged by administrative capability and customer reach, and which detectable behaviours follow them?

**Short answer.**
- **Most common:** a service provider holding customer data being breached. It is 26 of 63 MSP-relevant incidents (41%). Management platforms (RMM and similar) are second, at 10 (16%).
- **Most consequential:** the same two boundaries lead, but only just. Of the 14 incidents that combine tier 3 or 4 capability with confirmed reach of dozens of organisations or more, these two hold 8 (57%). The other 6 are spread over six different boundaries, one each.
- **Detectable behaviours:** the preset test did not find behaviours common to the whole high-impact group (none reaches 60%). Within individual boundaries there are patterns (below), but those are exploratory.

## What was counted

| Item | Number |
| --- | --- |
| Candidate events after deduplication | 811 |
| Counted incidents (primary source, supplier path, more than one customer) | 184 |
| Of which MSP-specific or MSP-relevant (the main ranking) | 63 (42 specific, 21 relevant) |
| Of which General supply-chain (context ranking) | 121 |
| Logged, not counted | 82 |
| Management or security flaws exploited with no downstream reach reported | 46 |
| Events still unverified | 499 |

Period: 1 January 2021 to 30 November 2026. One incident is one supplier event; mass-exploitation campaigns of one product (MOVEit, Accellion, Cleo, GoAnywhere) count once.

## Main ranking: 63 MSP-specific and MSP-relevant incidents

| Trust boundary | Incidents | Share | Tier 3 or 4 | Reach of dozens or more | Priority cell |
| --- | --- | --- | --- | --- | --- |
| Service provider holding customer data | 26 | 41% | 8 | 15 | 6 |
| RMM or management platform | 10 | 16% | 7 | 5 | 2 |
| API credential or token | 6 | 10% | 2 | 3 | 1 |
| Remote-access tool | 5 | 8% | 4 | 0 | 0 |
| Software update mechanism | 4 | 6% | 4 | 1 | 1 |
| Backup or security-management platform | 3 | 5% | 1 | 2 | 1 |
| Cloud integration | 3 | 5% | 2 | 1 | 1 |
| Identity provider | 2 | 3% | 1 | 1 | 1 |
| Plugin, extension or package | 2 | 3% | 2 | 1 | 1 |
| Vendor or developer account | 2 | 3% | 1 | 0 | 0 |

**Reading the table.**
- **Prevalence and impact are different rankings.** Provider-held data is first on both, but roughly a quarter of its incidents reach the priority cell (6 of 26, 23%). Small boundaries convert at similar or higher rates: software update mechanism 1 of 4, backup platforms 1 of 3, cloud integration 1 of 3.
- **Remote-access tools are capable but show little confirmed reach.** Four of five reached tier 3 or 4, yet none has a confirmed reach of dozens. Reach counts organisations confirmed by a primary source, not how many were exposed to the flaw, so mass exploitation without confirmed downstream victims is not counted. Another 46 exploited flaws in management and security products sit in the "no downstream reach reported" group (21 RMM, 20 backup or security management, 3 remote access, 2 other), which is a different measure of risk than this table.
- **Capability profile of the 63:** tier 4 in 12, tier 3 in 20, tier 2 in 12, tier 1 in 16, not reported in 3. Reach: dozens or more in 29 (46%), several in 10, more than one but uncounted in 23, unknown in 1.
- **Consequences:** data exposed in 59%, service disruption in 46%, ransomware or encryption in 37%. Within provider-held data, 18 of 26 involved ransomware.

### The 14 priority-cell incidents (tier 3 or 4, reach of dozens or more)

Kaseya VSA (2021); Advanced (2022); Okta support system (2023); Capita (2023); Südwestfalen IT (2023); BeyondTrust Remote Support SaaS (2024); IxMetro PowerHost (2024); Indonesia's national data centre (2024); ConnectWise Cloud Backup (2026); MSP Process (2026); IDC Frontier (2026); Beget (2026); cPGuard update channel (2026); the SCKit rogue ScreenConnect clients (2026).

## Context ranking: all 184 counted incidents

| Trust boundary | Incidents |
| --- | --- |
| Service provider holding customer data | 90 |
| Plugin, extension or package | 31 |
| API credential or token | 13 |
| Software update mechanism | 13 |
| RMM or management platform | 11 |
| Build or release pipeline | 8 |
| Remote-access tool | 5 |
| Cloud integration | 5 |
| Vendor or developer account | 3 |
| Backup or security-management platform | 3 |
| Identity provider | 2 |

- 21 of the 184 are in the priority cell; provider-held data holds 7 and package incidents 4.
- 25 of the 90 provider-held-data incidents are US health vendors reported through HHS. That is why this ranking is context only: it over-represents US healthcare.
- Package incidents (31) mostly report downloads, not organisations, so reach is weakly coded for them.

## Behaviours that follow each path (exploratory)

The preset test required a behaviour in 60% or more of priority-cell incidents. Credential access is highest at 57%, then software deployment, lateral movement and ransomware at 50% each. **The test is not met.** Per-boundary rates below are descriptive only, from small groups, and count only behaviours that a source reported.

| Boundary (incidents) | Most often reported |
| --- | --- |
| Service provider holding customer data (26) | Ransomware 69%, exfiltration 42%, credential access 23% |
| RMM or management platform (10) | Remote command 70%, shell or PowerShell 60%, software deployment 60% |
| Remote-access tool (5) | Remote command 100%, software deployment 80%, ransomware 80% |
| API credential or token (6) | Credential access 83%, lateral movement 50% |

## Do the data support the article?

| Signal | Threshold | MSP subset | All incidents |
| --- | --- | --- | --- |
| S1 volume | 60+ total, 30+ MSP, 5+ in top four boundaries | **Strong:** 184, 63, top four 26, 10, 6, 5 | Strong |
| S2 prevalence and impact | top boundaries hold 50% or more of the priority cell | **Strong:** 57% | Strong: 52% |
| S3 reach codability | 40% or fewer unknown reach | **Strong:** 2% unknown (38% if "more than one but uncounted" is added) | 12% unknown (48% with "more than one") |
| S4 behaviour convergence | 3 or 4 behaviours at 60% or more | **Not met:** none | Not met: one |

What this supports: ranking trusted connections by how often and how severely each is compromised (S1 to S3). What it does not support: a single list of behaviours to detect for every high-impact path. The honest framing is by boundary, using the exploratory table above.

## Reliability

A second coder, blind to existing rows, recoded a seeded random 20% of each group.

| Field | MSP sample (13) | General sample (24) |
| --- | --- | --- |
| Trust boundary kappa | 0.78 | 0.93 |
| Capability tier kappa | 0.70 | 0.50, then settled by a tier rule (see below) |
| Reach band kappa | 0.79 | 0.56 |
| Relevance kappa | 0.34 before the rule; 1.00 on a rule-guided re-check of all 37 | not meaningful before the rule (our rows were all General) |

- **Tier rule.** The tier disagreement came from one undefined case (malicious code delivered through a supplier's package, update or installer). A rule was adopted (README decision 17) and a blind re-check agreed on 11 of 12 cases; the twelfth was corrected. That re-check is not independent of how the rule was written.
- **Relevance rule.** The weakest field. Application and data SaaS vendors are General even when they hold many customers' data; MSP-specific is reserved for IT operations suppliers (decision 18). The kappa of 0.34 predates this rule. A blind re-check of all 37 sampled incidents under the written rule agreed on every one, but the rule was written from those same disagreements, so that shows the rule is clear, not that relevance is reliable on unseen incidents.

## Limits to state in any write-up

1. **Public reporting.** Small MSP incidents and incidents that never trigger a notification obligation are under-represented. Health breaches reported to HHS are over-represented in the all-incident set.
2. **Recent years carry more incidents.** 2025 and 2026 hold 28 of the 63 MSP incidents (44%) and 90 of the 184 (49%). Part of this is news search favouring recent events, so no trend is claimed.
3. **Reach and behaviours are often unreported.** Reach is the number of organisations confirmed by a primary source; behaviours are only those observed and reported, not what attackers could do. Where a source could only be read through news excerpts (blocked pages), the coding note says so.
4. **Inclusion rules shape the result.** Provider-held data dominates partly because a provider breach counts when more than one customer's data was exposed, and exploited management-tool flaws without reported downstream reach are not counted (46 of them).
5. **Judgement calls.** Relevance and trust boundary involve judgement. S1 passes on the MSP subset only because Heroku, Vercel and Railway are coded MSP-specific as platform providers; coded General, the fourth boundary would fall below 5. If seven health-data vendors were instead coded MSP-specific the subset would be 70 and the priority cell would not change.
6. **Coders.** Both coders are AI models working from public sources. The second-coder samples are small (13 and 24).
7. **Ransomware on hosting infrastructure** is coded tier 2 when no techniques are reported (decision 12), so tier is partly inferred for those incidents.

## Before this is published

- Confirm the Heroku, Vercel and Railway relevance calls, because S1 depends on them.
- Optionally test the relevance rule on a fresh random sample of incidents not used to write it.
- Resolve any remaining "NR" tiers (3 in the MSP subset) if exact counts are quoted.
- Check each primary link that a news excerpt stood in for, for the incidents named in the article.
- Decide whether the article names incidents; the study ranks categories, and vendors are named only by the facts in public reporting, crediting vendor responses.
