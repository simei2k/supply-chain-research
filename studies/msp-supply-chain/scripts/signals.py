"""Stage 5: compute signals S1-S4 (TASK.md) from data/coded.csv and data/candidates.csv.

Usage: python scripts/signals.py [msp|all]   (default msp: MSP-specific + MSP-relevant, README decision 11)
Prints a Markdown block; signals.md is written from it by hand with the date and commit.
"""
import os, sys
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
scope = sys.argv[1] if len(sys.argv) > 1 else "msp"
MSP = ["MSP-specific", "MSP-relevant"]
BEH = ["Shell/PowerShell", "Remote command", "Software deployment", "Services/tasks", "Credential access",
       "Security-tool interference", "Backup disruption", "Lateral movement (beh.)", "Archive creation",
       "Exfiltration", "Ransomware"]

cand = pd.read_csv(os.path.join(D, "candidates.csv"), dtype=str).fillna("")
coded = pd.read_csv(os.path.join(D, "coded.csv"), dtype=str, keep_default_na=False)
counted = cand[cand.status == "Counted (first pass)"]
sub = coded[coded.Relevance.isin(MSP)] if scope == "msp" else coded
n_msp_counted = counted.relevance.isin(MSP).sum()

pc_mask = sub["Capability tier (reported)"].str[0].isin(["3", "4"]) & sub["Reach band"].isin(["Dozens", "Hundreds or more"])
pc = sub[pc_mask]
prev = sub["Trust boundary"].value_counts()
top = list(prev.index[:4])

out = [f"## Scope: {'MSP-specific + MSP-relevant' if scope == 'msp' else 'all coded'} ({len(sub)} coded incidents)", ""]
# S1
out += ["### S1 Volume", "",
        f"- Counted incidents (all relevance): {len(counted)} (threshold 60+)",
        f"- Counted MSP-specific + MSP-relevant: {n_msp_counted} (threshold 30+); coded: {coded.Relevance.isin(MSP).sum()}",
        f"- Coded rows in scope by trust boundary (top four need 5+ each):", ""]
out += ["| Trust boundary | Incidents | Priority cell |", "| --- | --- | --- |"]
for tb, n in prev.items():
    out.append(f"| {tb} | {n} | {(pc['Trust boundary'] == tb).sum()} |")
s1 = len(counted) >= 60 and n_msp_counted >= 30 and all(prev[t] >= 5 for t in top)
out += ["", f"S1: {'strong' if s1 else 'not met'} (top four: {', '.join(f'{t} {prev[t]}' for t in top)})", ""]
# S2
out += ["### S2 Prevalence x impact", "", f"- Priority-cell incidents (tier 3-4, reach Dozens or more): {len(pc)} of {len(sub)}"]
for k in (2, 3):
    share = pc["Trust boundary"].isin(prev.index[:k]).mean() if len(pc) else 0
    out.append(f"- Share held by the top {k} boundaries by prevalence: {share:.0%}")
s2 = len(pc) and pc["Trust boundary"].isin(prev.index[:3]).mean() >= 0.5
out += ["", f"S2: {'strong' if s2 else 'not met'} (threshold 50%)", ""]
# S3
unk = (sub["Reach band"] == "Unknown").mean()
unk_any = sub["Reach band"].str.startswith("Unknown").mean()
out += ["### S3 Reach codability", "",
        f"- Reach band Unknown: {unk:.0%}",
        f"- Unknown or Unknown (more than one): {unk_any:.0%} (no count, but more than one organisation confirmed)",
        "", f"S3: {'strong' if unk <= 0.4 else 'not met'} on Unknown alone; {'strong' if unk_any <= 0.4 else 'not met'} counting both (threshold 40% or less)", ""]
# S4
rep = pc[(pc[BEH] == "Y").any(axis=1)]
share = (rep[BEH] == "Y").mean().sort_values(ascending=False) if len(rep) else pd.Series(dtype=float)
conv = [b for b, v in share.items() if v >= 0.6]
out += ["### S4 Behaviour convergence", "", f"- Priority-cell incidents reporting any behaviour: {len(rep)} of {len(pc)}", "",
        "| Behaviour | Share of those incidents |", "| --- | --- |"]
out += [f"| {b} | {v:.0%} |" for b, v in share.items()]
out += ["", f"S4: {'strong' if len(conv) >= 3 else 'not met'} ({len(conv)} behaviours at 60%+: {', '.join(conv) or 'none'}; threshold three or four)", ""]
print("\n".join(out))
