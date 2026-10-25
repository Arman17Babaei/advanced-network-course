#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

H={"User-Agent":"advanced-network-course-source-inspector/1.0"}
for year in [2023,2026]:
    url=f"https://dblp.org/db/conf/infocom/infocom{year}.html"
    r=requests.get(url,headers=H,timeout=60)
    print(f"YEAR={year} STATUS={r.status_code} FINAL={r.url} BYTES={len(r.content)} CONTENT_TYPE={r.headers.get('content-type')}",flush=True)
    print("RAW_START="+" ".join(r.text[:2500].split()),flush=True)
    soup=BeautifulSoup(r.text,"html.parser")
    print(
        f"li={len(soup.find_all('li'))} li.entry={len(soup.select('li.entry'))} "
        f"article={len(soup.find_all('article'))} cite={len(soup.find_all('cite'))} "
        f"span.title={len(soup.select('span.title'))}",
        flush=True,
    )
    classes={}
    for li in soup.find_all("li")[:200]:
        key=" ".join(li.get("class") or [])
        classes[key]=classes.get(key,0)+1
    print("LI_CLASSES="+repr(sorted(classes.items(), key=lambda x:-x[1])[:20]),flush=True)
    for sel in ["li.entry","article","cite.data","cite","span.title"]:
        els=soup.select(sel)
        print(f"SEL={sel} N={len(els)}",flush=True)
        for el in els[:3]:
            print("  "+" ".join(el.stripped_strings)[:500],flush=True)
