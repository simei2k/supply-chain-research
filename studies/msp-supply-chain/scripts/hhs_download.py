"""Download both HHS OCR breach report tabs as CSV (the portal has no direct link).

Usage: python scripts/hhs_download.py ~/research-data/hhs
Writes hhs_under_investigation.csv and hhs_archive.csv there (outside the repo).
Form control IDs (j_idt39, j_idt31, j_idt385) are from the portal as of 2026-11-24 and may change.
The portal sometimes returns an HTML page instead of the CSV; rerun if an export fails.
"""
import os, re, sys, requests
B = "https://ocrportal.hhs.gov/ocr/breach/"
out = os.path.expanduser(sys.argv[1])
s = requests.Session(); s.headers["User-Agent"] = "Mozilla/5.0"
vs = lambda h: re.search(r'javax.faces.ViewState[^>]*?value="([^"]+)"', h).group(1)
mp = lambda d: {k: (None, v) for k, v in d.items()}
h = s.get(B + "breach_frontpage.jsf", timeout=60).text
h = s.post(B + "breach_frontpage.jsf", files=mp({"ocrForm": "ocrForm", "ocrForm:j_idt39": "ocrForm:j_idt39", "javax.faces.ViewState": vs(h)}), timeout=60).text
V = vs(h)
for idx, name in ((0, "under_investigation"), (1, "archive")):
    if idx:
        s.post(B + "breach_report_hip.jsf", headers={"Faces-Request": "partial/ajax"}, timeout=180, files=mp({
            "javax.faces.partial.ajax": "true", "javax.faces.source": "ocrForm:j_idt31", "javax.faces.partial.execute": "ocrForm:j_idt31",
            "javax.faces.partial.render": "ocrForm:breachReports ocrForm:results", "javax.faces.behavior.event": "tabChange",
            "javax.faces.partial.event": "tabChange", "ocrForm:j_idt31_newTab": "ocrForm:j_idt31:archiveTab",
            "ocrForm:j_idt31_tabindex": "1", "ocrForm": "ocrForm", "ocrForm:j_idt31_activeIndex": "1", "javax.faces.ViewState": V}))
    r = s.post(B + "breach_report_hip.jsf", timeout=300, files=mp({"ocrForm": "ocrForm", "ocrForm:j_idt31_activeIndex": str(idx),
                                                                 "ocrForm:j_idt385": "ocrForm:j_idt385", "javax.faces.ViewState": V}))
    assert "csv" in r.headers.get("content-type", ""), f"{name}: export failed ({r.status_code} {r.url} {len(h)})"
    open(os.path.join(out, f"hhs_{name}.csv"), "wb").write(r.content)
    print(name, len(r.content), "bytes")
