"""Extract Stage 1 candidate pools (2021 to freeze) from sources cloned outside the repo.

Usage: python scripts/extract_pools.py ~/research-data
Writes data/candidates/{cncf_candidates,mitre_campaigns,vcdb_partner}.csv
Links and facts only; no article text.
"""
import csv, glob, json, os, re, sys

ROOT = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/research-data")
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "candidates")
START, FREEZE = "2021-01-01", "2026-11-30"


def write(name, rows, cols):
    with open(os.path.join(OUT, name), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


# --- CNCF catalog: parse the README index table ---
cdir = os.path.join(ROOT, "cncf-tag-security/community/catalog/compromises")
rows = []
for line in open(os.path.join(cdir, "README.md"), encoding="utf-8"):
    m = re.match(r"\|\s*\[(.+?)\]\((.+?)\)\s*\|\s*(\d{4})\s*\|\s*(.+?)\s*\|\s*(.*)\|\s*$", line)
    if not m or int(m.group(3)) < 2021:
        continue
    links = re.findall(r"\]\((https?://[^)]+)\)", m.group(5))
    rows.append(dict(name=m.group(1), year=m.group(3),
                     compromise_type=re.sub(r"\s*<br>\s*", "; ", m.group(4)),
                     catalog_file=m.group(2), links=" ; ".join(links)))
write("cncf_candidates.csv", rows, ["name", "year", "compromise_type", "catalog_file", "links"])

# --- MITRE ATT&CK: campaigns (and groups) using T1195* or T1199 ---
b = json.load(open(os.path.join(ROOT, "attack-stix-data/enterprise-attack/enterprise-attack.json")))
objs = {o["id"]: o for o in b["objects"]}
tech = {}
for o in b["objects"]:
    if o["type"] == "attack-pattern" and not o.get("revoked"):
        for r in o.get("external_references", []):
            if r.get("source_name") == "mitre-attack" and re.match(r"T1195|T1199$", r["external_id"]):
                tech[o["id"]] = r["external_id"]
hits = {}
for o in b["objects"]:
    if o["type"] == "relationship" and o["relationship_type"] == "uses" and o["target_ref"] in tech:
        src = objs.get(o["source_ref"])
        if src and src["type"] == "campaign" and not src.get("revoked"):
            hits.setdefault(src["id"], set()).add(tech[o["target_ref"]])
rows = []
for cid, ts in hits.items():
    c = objs[cid]
    first, last = c.get("first_seen", "")[:10], c.get("last_seen", "")[:10]
    if (last or first) < START or (first and first > FREEZE):
        continue
    ext = next(r for r in c["external_references"] if r.get("source_name") == "mitre-attack")
    refs = [r["url"] for r in c["external_references"] if r.get("url") and "attack.mitre.org" not in r["url"]]
    rows.append(dict(campaign_id=ext["external_id"], name=c["name"], first_seen=first, last_seen=last,
                     techniques=";".join(sorted(ts)), attack_url=ext.get("url", ""), refs=" ; ".join(refs[:8])))
rows.sort(key=lambda r: r["first_seen"])
write("mitre_campaigns.csv", rows, ["campaign_id", "name", "first_seen", "last_seen", "techniques", "attack_url", "refs"])

# --- VCDB: incidents 2021+ with a partner route in ---
rows = []
for f in glob.glob(os.path.join(ROOT, "VCDB/data/json/validated/*.json")):
    d = json.load(open(f))
    y = d.get("timeline", {}).get("incident", {}).get("year")
    if not y or y < 2021:
        continue
    act = d.get("action", {})
    why = []
    if "partner" in d.get("actor", {}):
        why.append("actor.partner")
    for a in ("hacking", "malware", "social", "misuse"):
        if "Partner" in act.get(a, {}).get("vector", []):
            why.append(f"{a}.vector=Partner")
    sec = d.get("victim", {}).get("secondary", {})
    if sec.get("amount") or sec.get("victim_id"):
        why.append("victim.secondary")
    if not why:
        continue
    v = d.get("victim", {})
    rows.append(dict(incident_id=d.get("incident_id", ""), year=y, victim=v.get("victim_id", ""),
                     industry=v.get("industry", ""), country=";".join(v.get("country", [])),
                     why=";".join(why), secondary_amount=sec.get("amount", ""),
                     summary=(d.get("summary") or "")[:200].replace("\n", " "),
                     reference=d.get("reference", "")[:300], file=os.path.basename(f)))
rows.sort(key=lambda r: (r["year"], r["victim"]))
write("vcdb_partner.csv", rows, ["incident_id", "year", "victim", "industry", "country", "why",
                                 "secondary_amount", "summary", "reference", "file"])
