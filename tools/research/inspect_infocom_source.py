#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

H={"User-Agent":"Mozilla/5.0 (compatible; advanced-network-course-source-inspector/1.0)"}
for year in [2023, 2024, 2025, 2026]:
    url=f"https://topcsuniv.org/japan/conferences/infocom/{year}/"
    r=requests.get(url,timeout=30,headers=H)
    print(f"YEAR={year} STATUS={r.status_code} URL={r.url} BYTES={len(r.content)}",flush=True)
    r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser")
    papers=soup.select("ol.explorer-papers > li")
    print(f"PAPERS={len(papers)} H2={[x.get_text(' ',strip=True) for x in soup.find_all('h2')]}",flush=True)
    print("PAGINATION CANDIDATES:",flush=True)
    for a in soup.find_all("a",href=True):
        txt=" ".join(a.stripped_strings)
        href=a.get("href")
        low=(txt+" "+href).lower()
        if any(k in low for k in ["next","prev","page=","pagination","offset","cursor","more"]):
            print(f"  {txt!r} -> {href}",flush=True)
    for nav in soup.find_all(["nav","div"],class_=lambda x: x and any(k in " ".join(x if isinstance(x,list) else [x]).lower() for k in ["pag","pager"])):
        print("NAV="+str(nav)[:4000].replace("\n"," "),flush=True)
    scripts=soup.find_all("script")
    for s in scripts:
        src=s.get("src")
        txt=s.string or ""
        if src and any(k in src.lower() for k in ["paper","page","explor"]):
            print("SCRIPT SRC",src,flush=True)
        if txt and any(k in txt.lower() for k in ["pagination","page_size","pagesize","offset"]):
            print("SCRIPT TEXT",txt[:2500],flush=True)
    print("----",flush=True)
