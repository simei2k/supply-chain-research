# Signals (Stage 5)

Computed 2026-11-25 by `scripts/signals.py msp` from `data/coded.csv` and `data/candidates.csv` (working copy after commit 3ec7d1f, with the verification batch and decisions 12-15 applied; recompute after committing). **Provisional:** MSP subset only; General incidents not yet coded; no second-coder check yet.

## Scope: MSP-specific + MSP-relevant (61 coded incidents)

### S1 Volume

- Counted incidents (all relevance): 232 (threshold 60+)
- Counted MSP-specific + MSP-relevant: 61 (threshold 30+); coded: 61
- Coded rows in scope by trust boundary (top four need 5+ each):

| Trust boundary | Incidents | Priority cell |
| --- | --- | --- |
| Service provider holding customer data | 27 | 6 |
| RMM or management platform | 10 | 2 |
| Remote-access tool | 5 | 0 |
| Backup or security-management platform | 4 | 1 |
| Software update mechanism | 4 | 1 |
| Identity provider | 3 | 1 |
| API credential or token | 3 | 1 |
| Cloud integration | 2 | 1 |
| Vendor or developer account | 2 | 0 |
| Plugin, extension or package | 1 | 1 |

S1: not met (top four: Service provider holding customer data 27, RMM or management platform 10, Remote-access tool 5, Backup or security-management platform 4)

### S2 Prevalence x impact

- Priority-cell incidents (tier 3-4, reach Dozens or more): 14 of 61
- Share held by the top 2 boundaries by prevalence: 57%
- Share held by the top 3 boundaries by prevalence: 57%

S2: strong (threshold 50%)

### S3 Reach codability

- Reach band Unknown: 0%
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

## Reading

- S1 fails only on the fourth boundary: Backup or security-management platform and Software update mechanism have 4 each (need 5). The 45 KEV flaws "exploited, no downstream reach reported" (21 RMM, 20 backup/security) are not counted.
- S2 passes: Service provider holding customer data and RMM hold 8 of the 14 priority-cell incidents (57%).
- S3 passes: no MSP-subset incident has reach Unknown; 38% have more than one organisation confirmed but no count.
- S4 fails: no behaviour reaches 60% of priority-cell incidents; credential access is highest at 57%. Priority-cell incidents mix hosting ransomware, token abuse and software pushes, so behaviours do not converge across all of them; per-boundary convergence may be the better framing.

## Reliability (second coder, MSP subset)

Blind recode of a seeded random 20% (13 of 61, `random_state=20261125`) by a coder that chose relevance and trust boundary itself; rows in `data/coder2.csv`. Cohen's kappa before adjudication:

| Field | Agreement | Kappa |
| --- | --- | --- |
| Trust boundary | 85% | 0.78 |
| Capability tier | 77% | 0.70 |
| Reach band | 85% | 0.79 |
| Relevance | 62% | 0.34 |

Target (0.7 on trust boundary and tier) met. Relevance is weak: the second coder put Atento, Cisco Duo and AOMEI in General supply-chain and N-able, Ingram Micro one step the other way, so the MSP-subset membership itself is the least reliable judgement. Adjudicated by rule: Bomgar tier 4->3, JumpCloud boundary to RMM, Atento tier NR->2. Left for decision: Mimecast boundary (backup/security vs cloud integration), Cisco Duo reach (Hundreds vs Unknown (more than one)), Inline tier (1 vs 2), and the relevance disagreements.
