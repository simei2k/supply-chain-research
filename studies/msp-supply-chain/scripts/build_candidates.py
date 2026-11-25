"""Stage 3: merge every candidate pool into data/candidates.csv, one row per supplier event.

Usage: python scripts/build_candidates.py

Hand decisions live in data/dedupe/events.csv (one row per event) and data/dedupe/event_map.csv
(which pool row belongs to which event; `match` is a prefix of the row's name, or a substring of the
business associate for HHS). Rules applied by the script:
  - KEV campaign keys not in the map become "Exploited, no downstream reach reported" events.
  - HHS: only hacking rows. Vendors not in the map become their own event: counted (first pass) when
    HHS shows more than one customer (2+ rows, or wording such as "on behalf of" covered entities),
    otherwise "To verify". Covered-entity rows with no identified vendor are tallied, not turned into events.
Writes data/candidates.csv and the generated part of data/logged.csv (hand-added logged rows are kept).
"""
import csv, os, re, sys
from datetime import date
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
C = os.path.join(D, "candidates")
TODAY = date.today().isoformat()
LUMP = {"E219", "E220", "E214"}  # events that group unrelated cases; logged one row per pool row

events = pd.read_csv(os.path.join(D, "dedupe", "events.csv"), dtype=str).fillna("")
emap = pd.read_csv(os.path.join(D, "dedupe", "event_map.csv"), dtype=str)
assert events.event_id.is_unique, "duplicate event_id"
unknown = set(emap.event_id) - set(events.event_id)
assert not unknown, f"map points to unknown events: {unknown}"

# ---- load pools as (pool, name, match_text, year, link) ----
rows = []
def add(pool, df, name, year, link=None, match=None):
    for _, r in df.iterrows():
        hint = re.match(r"\[([EH]\d{3})\]", str(r.get("Coding notes", "")))  # Stage 4B rows carry their event id
        rows.append(dict(pool=pool, name=str(r[name]), match=str(r[match or name]), hint=hint.group(1) if hint else "",
                         year=str(r[year])[:4] if year else "", link=str(r[link]) if link and pd.notna(r[link]) else ""))

add("coded", pd.read_csv(os.path.join(D, "coded.csv")), "Incident", "Year", "Primary source")
lg = pd.read_csv(os.path.join(D, "logged.csv"))
add("logged", lg[~lg.ID.str.match(r"^(E|K|H)\d|^(E|K|H)-")], "Incident", "Year", "Source")
add("sheet_other", pd.read_csv(os.path.join(C, "sheet_other_candidates.csv")), "Incident", "Year")
add("sweep", pd.read_csv(os.path.join(C, "sheet_source_sweep.csv")), "Incident", "Year", "Source link")
add("news", pd.read_csv(os.path.join(C, "news_candidates.csv")), "incident", "date", "outlet_link")
bt = pd.read_csv(os.path.join(C, "breaking_trust_firstpass.csv")); bt.columns = ["date", "name"] + list(bt.columns[2:])
add("bt", bt, "name", "date")
add("cncf", pd.read_csv(os.path.join(C, "cncf_candidates.csv")), "name", "year", "links")
add("mitre", pd.read_csv(os.path.join(C, "mitre_campaigns.csv")), "name", "first_seen", "attack_url")
add("headlines", pd.read_csv(os.path.join(C, "headline_candidates.csv")), "incident", "date", "headline_link")
add("vcdb", pd.read_csv(os.path.join(C, "vcdb_partner.csv")), "victim", "year", "reference", match="incident_id")

pool_rows = pd.DataFrame(rows)
def assign(r):
    if r.hint:
        return r.hint
    m = emap[(emap.pool == r.pool) & emap.match.map(lambda k: r.match.startswith(k))]
    if m.empty:
        sys.exit(f"UNMAPPED {r.pool}: {r.name}")
    return m.loc[m.match.str.len().idxmax(), "event_id"]
pool_rows["event_id"] = pool_rows.apply(assign, axis=1)

# ---- KEV: by campaign key ----
kev = pd.read_csv(os.path.join(C, "kev_candidates.csv"))
kmap = dict(emap[emap.pool == "kev"][["match", "event_id"]].values)
auto = []
for i, (key, g) in enumerate(kev.groupby("campaign_key", sort=True)):
    eid = kmap.get(key)
    if not eid:
        eid = f"K{i+1:03d}"
        auto.append(dict(event_id=eid, incident=f"{key} exploited ({', '.join(g.cveID)})", year=str(key)[-4:],
                         relevance="MSP-relevant", trust_boundary=g.trust_boundary.iloc[0],
                         status="Exploited, no downstream reach reported", rule="KEV flaw exploited, no downstream reach reported",
                         note=f"KEV ransomware use: {(g.ransomware == 'Known').sum()} of {len(g)} CVEs"))
    rows_k = dict(pool="kev", name=key, match=key, year=str(key)[-4:], link="https://www.cisa.gov/known-exploited-vulnerabilities-catalog", event_id=eid)
    pool_rows = pd.concat([pool_rows, pd.DataFrame([rows_k])], ignore_index=True)
missing = set(kmap) - set(kev.campaign_key)
assert not missing, f"KEV map keys not in pool: {missing}"

# ---- HHS: hacking rows grouped by business associate ----
hhs = pd.read_csv(os.path.join(C, "hhs_business_associate.csv"))
hhs = hhs[hhs.hacking]
hmap = emap[emap.pool == "hhs"]
norm = lambda s: re.sub(r"[^a-z0-9]+", " ", re.sub(r",? (inc|llc|l\.l\.c|corp|corporation|co|ltd|lp|pllc|pc)\.?$", "", s.lower().strip())).strip()
multi_words = r"covered entities|on behalf of|multiple (?:covered|clients|customers)|its clients|its customers|several (?:covered|clients)"
unmatched_ce = hhs[hhs.business_associate.isna()]
known = hhs[hhs.business_associate.notna()].copy()
def hhs_event(ba):
    m = hmap[hmap.match.map(lambda k: k.lower() in ba.lower())]
    return m.loc[m.match.str.len().idxmax(), "event_id"] if len(m) else None
known["event_id"] = known.business_associate.map(hhs_event)
known["bak"] = known.business_associate.map(norm)
for j, (bak, g) in enumerate(known[known.event_id.isna()].groupby("bak", sort=True)):
    eid = f"H{j+1:03d}"
    multi = len(g) >= 2 or g.desc.fillna("").str.contains(multi_words, case=False, regex=True).any()
    auto.append(dict(event_id=eid, incident=f"{g.business_associate.iloc[0]} breach", year=g.submitted.min()[:4],
                     relevance="General supply-chain", trust_boundary="Service provider holding customer data",
                     status="Counted (first pass)" if multi else "To verify",
                     rule="" , note=f"HHS only: {len(g)} row(s); " + ("more than one customer shown in HHS" if multi else "multi-customer exposure not yet shown")))
    known.loc[g.index, "event_id"] = eid
# relevance review of HHS vendors (data/dedupe/hhs_relevance.csv)
rel_path = os.path.join(D, "dedupe", "hhs_relevance.csv")
hrel = pd.read_csv(rel_path) if os.path.exists(rel_path) else pd.DataFrame(columns=["match", "relevance", "basis"])
for a in auto:
    if a["event_id"].startswith("H"):
        ba = a["incident"][: -len(" breach")].strip()
        m = hrel[hrel.match == ba]
        if len(m):
            a["relevance"] = m.relevance.iloc[0]
            a["note"] += "; relevance reviewed: " + m.basis.iloc[0]
unused = set(hrel.match) - {a["incident"][: -len(" breach")].strip() for a in auto if a["event_id"].startswith("H")}
assert not unused, f"hhs_relevance rows matching no HHS event: {unused}"
hhs_pool = known.assign(pool="hhs", name=known.business_associate + " / " + known.entity, match=known.business_associate,
                        year=known.submitted.str[:4], link="https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf")
pool_rows = pd.concat([pool_rows, hhs_pool[["pool", "name", "match", "year", "link", "event_id"]]], ignore_index=True)
hhs_people = pd.to_numeric(known.individuals_affected, errors="coerce").groupby(known.event_id).sum()

# ---- assemble events ----
ev = pd.concat([events, pd.DataFrame(auto)], ignore_index=True).set_index("event_id")
g = pool_rows.groupby("event_id")
ev["sources_merged"] = g.pool.agg(lambda s: ";".join(sorted(set(s))))
ev["pool_rows"] = g.size()
ev["hhs_individuals"] = hhs_people
ev["links"] = g.link.agg(lambda s: " ; ".join(list(dict.fromkeys(x for x in s if x.startswith("http")))[:3]))
orphan = ev[ev.pool_rows.isna()]
assert orphan.empty, f"events with no pool rows: {list(orphan.index)}"
ev["pool_rows"] = ev.pool_rows.astype(int)
ev = ev.reset_index()
cols = ["event_id", "incident", "year", "relevance", "trust_boundary", "status", "rule", "sources_merged", "pool_rows", "hhs_individuals", "links", "note"]
ev[cols].to_csv(os.path.join(D, "candidates.csv"), index=False, float_format="%.0f")

# ---- logged.csv: keep hand rows, regenerate the rest ----
hand = lg[~lg.ID.str.match(r"^(E|K|H)\d|^(E|K|H)-")]
gen = []
for _, e in ev[ev.status.isin(["Logged", "Exploited, no downstream reach reported"])].iterrows():
    if e.event_id == "E207":
        continue  # Snowflake already a hand row (P10)
    if e.event_id in LUMP:
        for _, r in pool_rows[pool_rows.event_id == e.event_id].iterrows():
            gen.append([f"{e.event_id}-{r.pool}", r["name"], r.year, e.note, e.rule, r.link, TODAY])
    else:
        gen.append([e.event_id, e.incident, e.year, e.note or e.status, e.rule or e.status, e.links, TODAY])
gen.append(["H-UNMATCHED", f"HHS covered-entity hacking breaches with business associate unidentified ({len(unmatched_ce)} rows)", "2021-2026",
            "Vendor not named in HHS data; rows under 100,000 people not hand-matched (README decision 7)", "Vendor unidentified; no supplier event can be formed",
            "data/candidates/hhs_business_associate.csv", TODAY])
out = pd.concat([hand, pd.DataFrame(gen, columns=hand.columns)], ignore_index=True)
out.to_csv(os.path.join(D, "logged.csv"), index=False)

# ---- report ----
print(f"Pool rows in: {len(pool_rows)} mapped (+{len(unmatched_ce)} HHS rows with no vendor)")
print(pool_rows.pool.value_counts().to_string())
print(f"\nEvents after dedupe: {len(ev)}")
print(ev.status.value_counts().to_string())
print("\nBy relevance x status:")
print(pd.crosstab(ev.relevance, ev.status, margins=True).to_string())
print("\nExploited, no downstream reach reported, by trust boundary:")
print(ev[ev.status.str.startswith("Exploited")].trust_boundary.value_counts().to_string())
print(f"\nlogged.csv rows: {len(out)}")
