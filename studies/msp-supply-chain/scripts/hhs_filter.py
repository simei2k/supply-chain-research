"""Filter HHS OCR breach exports to business-associate breaches, 2021 to freeze.

Usage: python scripts/hhs_filter.py <under_investigation.csv> <archive.csv> data/candidates/hhs_business_associate.csv
Exports come from https://ocrportal.hhs.gov/ocr/breach/breach_report_hip.jsf (CSV icon, each tab).
Keeps the HHS web description (US government text, kept by decision of 2026-11-24) to help identify the business associate.
"""
import sys, pandas as pd
cols = ["entity", "state", "entity_type", "individuals_affected", "submitted", "breach_type", "location", "ba_present", "desc"]
frames = []
for path, tab in ((sys.argv[1], "Under investigation"), (sys.argv[2], "Archive")):
    d = pd.read_csv(path, dtype=str)
    d.columns = cols[: len(d.columns)]
    d["hhs_tab"] = tab
    frames.append(d)
df = pd.concat(frames, ignore_index=True)
df["submitted"] = pd.to_datetime(df.submitted, format="%m/%d/%Y", errors="coerce")
df = df[(df.submitted >= "2021-01-01") & (df.submitted <= "2026-11-30") & (df.ba_present.str.strip().str.lower() == "yes")]
df = df.drop_duplicates(["entity", "submitted", "individuals_affected"])
df["hacking"] = df.breach_type.str.contains("Hacking", na=False)
df["submitted"] = df.submitted.dt.strftime("%Y-%m-%d")
df["desc"] = df.desc.fillna("").str.replace(r"\s+", " ", regex=True).str.strip()
out = df.sort_values("submitted")
out.to_csv(sys.argv[3], index=False)
print(len(out), "BA-present breaches;", int(out.hacking.sum()), "hacking/IT incident")
print(out.groupby(out.submitted.str[:4]).agg(n=("entity", "size"), hacking=("hacking", "sum")))
