# Signals (Stage 5)

Computed 2026-11-25 by `scripts/signals.py` from `data/coded.csv` (184 counted incidents, all coded) and `data/candidates.csv`. Recompute after committing and note the commit here. **Provisional:** the second-coder check below covers the MSP subset only; the General incidents (121) have not been double-coded.

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
| Service provider holding customer data | 90 | 8 |
| Plugin, extension or package | 31 | 2 |
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

- Priority-cell incidents (tier 3-4, reach Dozens or more): 20 of 184
- Share held by the top 2 boundaries by prevalence: 50%
- Share held by the top 3 boundaries by prevalence: 60%

S2: strong (threshold 50%)

### S3 Reach codability

- Reach band Unknown: 12%
- Unknown or Unknown (more than one): 48% (no count, but more than one organisation confirmed)

S3: strong on Unknown alone; not met counting both (threshold 40% or less)

### S4 Behaviour convergence

- Priority-cell incidents reporting any behaviour: 19 of 20

| Behaviour | Share of those incidents |
| --- | --- |
| Software deployment | 58% |
| Credential access | 58% |
| Exfiltration | 47% |
| Shell/PowerShell | 37% |
| Lateral movement (beh.) | 37% |
| Ransomware | 37% |
| Remote command | 32% |
| Security-tool interference | 26% |
| Services/tasks | 21% |
| Backup disruption | 16% |
| Archive creation | 11% |

S4: not met (0 behaviours at 60%+: none; threshold three or four)


## Reading

**Main ranking (MSP-specific + MSP-relevant, 63 incidents)**
- S1 passes (top four boundaries: 26, 10, 6, 5), but narrowly and for a judgement reason: API credential or token reaches 6 only because three platform or cloud-hosting providers (Heroku, Vercel, Railway) were coded MSP-specific under the tightened relevance definition. Coded General, API credential or token would have 3 and S1 would fail on the fourth boundary (software update mechanism, 4).
- S2 passes: the top two boundaries (service provider holding customer data; RMM or management platform) hold 8 of the 14 priority-cell incidents (57%); the top three hold 64%.
- S3 passes: 2% of the MSP subset has reach Unknown; 38% have more than one organisation confirmed but no count.
- S4 fails: no behaviour reaches 60% of priority-cell incidents (credential access is highest at 57%). The preset test is across all priority-cell incidents; convergence within a single boundary would be exploratory only.

**Context ranking (all 184 counted incidents)**
- Service provider holding customer data dominates (90 of 184; 25 of these are HHS-reported vendors confirmed by a vendor, client or state AG source). Plugin, extension or package (31) is the next largest, almost all open-source package maintainer takeovers.
- S3 on all incidents: 12% Unknown, but 48% Unknown or Unknown (more than one) because package incidents report downloads, not organisations.
- Known limit: all-incident reach is weakly coded for open-source packages, where downloads are not organisations.

## Reliability (second coder, MSP subset)

Blind recode of a seeded random 20% (13 of 61, `random_state=20261125`) by a coder that chose relevance and trust boundary itself; rows in `data/coder2.csv`. Cohen's kappa before adjudication:

| Field | Agreement | Kappa |
| --- | --- | --- |
| Trust boundary | 85% | 0.78 |
| Capability tier | 77% | 0.70 |
| Reach band | 85% | 0.79 |
| Relevance | 62% | 0.34 |

Target (0.7 on trust boundary and tier) met. Relevance is weak: the second coder put Atento, Cisco Duo and AOMEI in General supply-chain and N-able, Ingram Micro one step the other way, so the MSP-subset membership itself is the least reliable judgement. Adjudicated by rule: Bomgar tier 4->3, JumpCloud boundary to RMM, Atento tier NR->2. Then: relevance definition tightened (README decision 16) and Atento, Verkada, Okta/Sitel, SimpleHelp utility provider recoded; Mimecast boundary set to Cloud integration. Kept: Cisco Duo reach Hundreds or more (Cisco's own ~1% statement), Inline tier 1 (ransomware label seen only in a search snippet). Kappa above is before any of these changes.
