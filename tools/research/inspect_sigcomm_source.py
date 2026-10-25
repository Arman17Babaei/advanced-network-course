#!/usr/bin/env python3
import json
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
cfg = json.loads((ROOT / "tools/research/paper_corpus_config.json").read_text())
spec = next(x for x in cfg["conferences"] if x["name"] == "SIGCOMM")

for year, url in spec["official_urls"].items():
    r = requests.get(url, timeout=30, headers={"User-Agent":"advanced-network-course-source-inspector/1.0"})
    print(f"YEAR={year} STATUS={r.status_code} URL={r.url} BYTES={len(r.content)}")
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    for tag in ["h1","h2","h3","h4","li","tr","p","strong"]:
        els = soup.find_all(tag)
        vals = []
        for el in els:
            text = " ".join(el.stripped_strings)
            if len(text) >= 8:
                vals.append(text[:240])
            if len(vals) >= 12:
                break
        print(f"TAG={tag} COUNT={len(els)}")
        for v in vals:
            print(f"  {v}")
    print("----")

# Focused 2026 table sanity check
url = spec["official_urls"]["2026"]
r = requests.get(url, timeout=30, headers={"User-Agent":"advanced-network-course-source-inspector/1.0"})
soup = BeautifulSoup(r.text, "html.parser")
rows = soup.find_all("tr")
print(f"2026_TR_TOTAL={len(rows)} TH_TOTAL={len(soup.find_all('th'))} TD_TOTAL={len(soup.find_all('td'))}")
for idx in list(range(min(3,len(rows)))) + list(range(max(0,len(rows)-3),len(rows))):
    cells = [" ".join(x.stripped_strings) for x in rows[idx].find_all(["th","td"])]
    print(f"ROW[{idx}] CELLS={len(cells)} :: " + " || ".join(cells)[:600])
