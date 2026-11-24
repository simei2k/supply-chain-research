"""Collect headlines (title, link, date only; no article text) from outlet tag/label listings, 2021 to freeze.

Usage: python scripts/harvest_headlines.py data/candidates/headlines_raw.csv
Sources (method added 2026-11-24, see search_terms.md "Added later"):
  - BleepingComputer tag pages: supply-chain-attack, managed-service-provider, ransomware (ransomware added in third pass)
  - The Hacker News Blogger label feeds: "Supply Chain Attack", "Supply Chain", "Supply Chain Security", "Software Supply Chain";
    third pass adds "Cyber Attack", "Threat Intelligence" (site menu categories) and MSP-type labels
Waits 2 seconds between requests.
"""
import csv, html, json, re, sys, time
from datetime import datetime
import requests

START, FREEZE = "2021-01-01", "2026-11-30"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
rows = []

def bc_tag(tag):
    page = 1
    while True:
        url = f"https://www.bleepingcomputer.com/tag/{tag}/" + (f"page/{page}/" if page > 1 else "")
        r = requests.get(url, headers=UA, timeout=60)
        if r.status_code != 200:
            print(f"BC {tag} page {page}: HTTP {r.status_code}, stopping"); break
        h = r.text[r.text.find("bc_latest_news"):]
        items = re.findall(r'<h4><a href="([^"]+)">([^<]+)</a></h4>.*?<li class="bc_news_date">([^<]+)', h, re.S)
        if not items:
            break
        oldest = None
        for link, title, d in items:
            d = datetime.strptime(d.strip(), "%B %d, %Y").strftime("%Y-%m-%d")
            oldest = d
            if START <= d <= FREEZE:
                rows.append(dict(outlet="bleepingcomputer.com", listing=f"tag/{tag}", date=d, title=html.unescape(title).strip(), link=link))
        print(f"BC {tag} page {page}: {len(items)} items, oldest {oldest}")
        if oldest < START:
            break
        page += 1
        time.sleep(2)

def thn_label(label):
    start = 1
    while True:
        url = f"https://thehackernews.com/feeds/posts/default/-/{requests.utils.quote(label)}?alt=json&max-results=100&start-index={start}"
        r = requests.get(url, headers=UA, timeout=60)
        if r.status_code != 200:
            print(f"THN {label} start {start}: HTTP {r.status_code}, stopping"); break
        entries = json.loads(r.text)["feed"].get("entry", [])
        if not entries:
            break
        oldest = None
        for e in entries:
            d = e["published"]["$t"][:10]; oldest = d
            link = next(l["href"] for l in e["link"] if l["rel"] == "alternate")
            if START <= d <= FREEZE:
                rows.append(dict(outlet="thehackernews.com", listing=f"label/{label}", date=d, title=html.unescape(e["title"]["$t"]).strip(), link=link))
        print(f"THN {label} start {start}: {len(entries)} items, oldest {oldest}")
        if oldest < START:
            break
        start += len(entries)
        time.sleep(2)

for t in ("supply-chain-attack", "managed-service-provider", "ransomware"):
    bc_tag(t)
for lab in ("Supply Chain Attack", "Supply Chain", "Supply Chain Security", "Software Supply Chain",
            "Cyber Attack", "Threat Intelligence", "Managed Service Provider", "Managed Service Providers", "MSP", "RMM",
            "Remote Monitoring", "Remote Access", "ScreenConnect", "ConnectWise", "Kaseya", "Third-Party Risk", "OAuth"):
    thn_label(lab)

seen, out = set(), []
for r in rows:
    if r["link"] not in seen:
        seen.add(r["link"]); out.append(r)
with open(sys.argv[1], "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["outlet", "listing", "date", "title", "link"]); w.writeheader(); w.writerows(out)
print(len(out), "unique headlines")
