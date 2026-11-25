# Signals (Stage 5)

Computed 2026-11-25 by `scripts/signals.py` from `data/coded.csv` (184 counted incidents, all coded) and `data/candidates.csv`. Recompute after committing and note the commit here. Second-coder checks cover both samples (see Reliability). The tier rule in README decision 17 was applied after the General check.

# Scope A: main ranking

### Scope: MSP-specific + MSP-relevant (63 coded incidents)

### S1 Volume

- Counted incidents (all relevance): 184 (threshold 60+)
- Counted MSP-specific + MSP-relevant: 63 (threshold 30+); coded: 63
- Coded rows in scope by trust boundary (top four need 5+ each):

| Trust boundary | Incidents | Priority cell |
| --- | --- | --- |
| Service provider holding customer data | 26 | 6 |
| RMM or management platform | 10 | 2 |
| API credential or token | 6 | 1 |
| Remote-access tool | 5 | 0 |
| Software update mechanism | 4 | 1 |
| Cloud integration | 3 | 1 |
| Backup or security-management platform | 3 | 1 |
| Plugin, extension or package | 2 | 1 |
| Identity provider | 2 | 1 |
| Vendor or developer account | 2 | 0 |

S1: strong (top four: Service provider holding customer data 26, RMM or management platform 10, API credential or token 6, Remote-access tool 5)

### S2 Prevalence x impact

- Priority-cell incidents (tier 3-4, reach Dozens or more): 14 of 63
- Share held by the top 2 boundaries by prevalence: 57%
- Share held by the top 3 boundaries by prevalence: 64%

S2: strong (threshold 50%)

### S3 Reach codability

- Reach band Unknown: 2%
- Unknown or Unknown (more than one): 38% (no count, but more than one organisation confirmed)

S3: strong on Unknown alone; strong counting both (threshold 40% or less)

### S4 Behaviour convergence

- Priority-cell incidents reporting any behaviour: 14 of 14

| Behaviour | Share of those incidents |
| --- | --- |
| Credential access | 57% |
| Software deployment | 50% |
| Lateral movement (beh.) | 50% |
| Ransomware | 50% |
| Shell/PowerShell | 36% |
| Remote command | 36% |
| Security-tool interference | 36% |
| Exfiltration | 36% |
| Backup disruption | 21% |
| Services/tasks | 14% |
| Archive creation | 7% |

S4: not met (0 behaviours at 60%+: none; threshold three or four)


# Scope B: context ranking

### Scope: all coded (184 coded incidents)

### S1 Volume

- Counted incidents (all relevance): 184 (threshold 60+)
- Counted MSP-specific + MSP-relevant: 63 (threshold 30+); coded: 63
- Coded rows in scope by trust boundary (top four need 5+ each):

| Trust boundary | Incidents | Priority cell |
| --- | --- | --- |
| Service provider holding customer data | 90 | 7 |
| Plugin, extension or package | 31 | 4 |
| API credential or token | 13 | 2 |
| Software update mechanism | 13 | 1 |
| RMM or management platform | 11 | 2 |
| Build or release pipeline | 8 | 1 |
| Remote-access tool | 5 | 0 |
| Cloud integration | 5 | 1 |
| Vendor or developer account | 3 | 1 |
| Backup or security-management platform | 3 | 1 |
| Identity provider | 2 | 1 |

S1: strong (top four: Service provider holding customer data 90, Plugin, extension or package 31, API credential or token 13, Software update mechanism 13)

### S2 Prevalence x impact

- Priority-cell incidents (tier 3-4, reach Dozens or more): 21 of 184
- Share held by the top 2 boundaries by prevalence: 52%
- Share held by the top 3 boundaries by prevalence: 62%

S2: strong (threshold 50%)

### S3 Reach codability

- Reach band Unknown: 12%
- Unknown or Unknown (more than one): 48% (no count, but more than one organisation confirmed)

S3: strong on Unknown alone; not met counting both (threshold 40% or less)

### S4 Behaviour convergence

- Priority-cell incidents reporting any behaviour: 19 of 21

| Behaviour | Share of those incidents |
| --- | --- |
| Credential access | 63% |
| Software deployment | 53% |
| Exfiltration | 47% |
| Shell/PowerShell | 42% |
| Lateral movement (beh.) | 37% |
| Ransomware | 37% |
| Remote command | 32% |
| Security-tool interference | 26% |
| Services/tasks | 21% |
| Backup disruption | 16% |
| Archive creation | 11% |

S4: not met (1 behaviours at 60%+: Credential access; threshold three or four)


## Reading

**Main ranking (MSP-specific + MSP-relevant, 63 incidents)**
- S1 passes (top four boundaries: 26, 10, 6, 5), but narrowly: API credential or token reaches 6 only because three platform or cloud-hosting providers (Heroku, Vercel, Railway) were coded MSP-specific under the tightened relevance definition. Coded General, that boundary would have 3 and S1 would fail on the fourth boundary (software update mechanism, 4).
- S2 passes: the top two boundaries (service provider holding customer data; RMM or management platform) hold 8 of the 14 priority-cell incidents (57%); the top three hold 64%.
- S3 passes: 2% of the MSP subset has reach Unknown; 38% have more than one organisation confirmed but no count.
- S4 fails: no behaviour reaches 60% of priority-cell incidents (credential access is highest at 57%).
- The tier rule (decision 17) did not change any MSP-subset result: the recoded rows are package and build incidents, which sit in the General set.

**Context ranking (all 184 counted incidents)**
- Service provider holding customer data dominates (90 of 184; 25 are HHS-reported vendors confirmed by a vendor, client or state AG source). Plugin, extension or package (31) is next, almost all open-source package maintainer takeovers.
- After decision 17 and the Accellion correction the priority cell grows from 20 to 21 incidents; credential access reaches 63% (S4 still not met: one behaviour, needs three or four).
- S3 on all incidents: 12% Unknown, but 48% Unknown or Unknown (more than one) because package incidents report downloads, not organisations.

## Reliability (second coder, MSP subset)

Blind recode of a seeded random 20% (13 of 61, `random_state=20261125`) by a coder that chose relevance and trust boundary itself; rows in `data/coder2.csv`. Cohen's kappa before adjudication:

| Field | Agreement | Kappa |
| --- | --- | --- |
| Trust boundary | 85% | 0.78 |
| Capability tier | 77% | 0.70 |
| Reach band | 85% | 0.79 |
| Relevance | 62% | 0.34 |

Target (0.7 on trust boundary and tier) met. Relevance is weak: the second coder put Atento, Cisco Duo and AOMEI in General supply-chain and N-able, Ingram Micro one step the other way, so the MSP-subset membership itself is the least reliable judgement. Adjudicated by rule: Bomgar tier 4->3, JumpCloud boundary to RMM, Atento tier NR->2. Then: relevance definition tightened (README decision 16) and Atento, Verkada, Okta/Sitel, SimpleHelp utility provider recoded; Mimecast boundary set to Cloud integration. Kept: Cisco Duo reach Hundreds or more (Cisco's own ~1% statement), Inline tier 1 (ransomware label seen only in a search snippet). Kappa above is before any of these changes.

## Reliability (second coder, General set)

Blind recode of a seeded random 20% of the 121 General incidents (24, `random_state=20261126`) in `data/coder2_general.csv`, same brief as the MSP sample (coder chose relevance and boundary itself). Cohen's kappa before any adjudication:

| Field | Agreement | Kappa |
| --- | --- | --- |
| Trust boundary | 96% | 0.93 |
| Capability tier | 67% | **0.50** (target 0.7 not met) |
| Reach band | 71% | 0.56 |
| Relevance | 58% | 0.00 (degenerate: first coder is General on all 24) |

Pooled with the MSP sample (n = 37): trust boundary 0.96, tier 0.65, reach band 0.66.

**Where tier disagrees.** Provider-held-data incidents (13): 92% agreement. Software-supply incidents (package, build pipeline, update mechanism; 11): 36% agreement. The disagreement is one question: when a malicious package, update or installer runs on customer machines, is that "2 Endpoint action" (commands executed) or "3 Software deployment" (the supplier channel deployed code)? Cases: Rspack, Shai-Hulud, ctx, Ultralytics, lottie-player, 3CX, Comm100, Accellion. The codebook does not settle it, so coders (including the first coder across waves) were inconsistent.

**Relevance.** Five health-data vendors (Elgon, ApolloMD, Aesto, ION, CareCloud) plus Oracle Health, MOVEit and HealthEC were coded MSP-specific by the second coder; the first coder had General. These sit on the edge of "IT outsourcer or hosting provider" in the tightened definition.

**Tier re-check under decision 17 (2026-11-26).** Twelve software-supply or channel incidents in the General sample were re-coded for tier only by fresh blind coders given the rule. Eleven gave tier 3, matching the recoded rows. Accellion gave tier 2 (customer-run appliances exploited, web shell installed, no supplier delivery channel and no account creation), so that row was recoded 3 to 2. Tier agreement on the 24-incident General sample is then 24 of 24.

This is a rule-guided re-check of the same incidents the rule was written from, so it shows the rule is unambiguous to a new coder, not that tier reliability on unseen incidents is 1.0. The independent figures stand: provider-data tier agreement 92% (12 of 13) on the original blind pass, trust boundary kappa 0.93. The target of 0.7 on tier is met on the MSP sample (0.70, 13 incidents) and, after the rule, on the General sample.

**Net effect on signals.** MSP subset unchanged (S1, S2, S3 strong; S4 not met). All 184 incidents: priority cell 21; top two boundaries hold 52%; credential access 63% (one behaviour; S4 still not met).

**Relevance rule (2026-11-26, README decision 18).** The second coder's MSP-specific calls for health-data vendors (Elgon, ApolloMD, Aesto, ION, CareCloud, HealthEC, Oracle Health) are not adopted: application and data SaaS vendors are General even when they hold many customers' data. IT operations suppliers (MSPs, IT outsourcers, managed hosting, IaaS and PaaS, government shared IT) are MSP-specific. No rows changed, because the first coder's labels already followed this line. Sensitivity: if those seven vendors were MSP-specific, the MSP subset would be 70 incidents, "service provider holding customer data" would hold 33, and the priority cell would not change (all seven are tier 1 or 2), so S2 would be unaffected; S1 would also still pass.
