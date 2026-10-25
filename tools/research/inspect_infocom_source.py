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
    print("TITLE="+str(soup.title),flush=True)
    for tag in ["article","li","tr","h2","h3","h4","div"]:
        els=soup.find_all(tag)
        print(f"TAG={tag} COUNT={len(els)}",flush=True)
        shown=0
        for el in els:
            txt=" ".join(el.stripped_strings)
            if "INFOCOM" in txt.upper() and len(txt)>40:
                print(f"  SAMPLE {tag}: {txt[:800]}",flush=True)
                print(f"  MARKUP: {str(el)[:1800].replace(chr(10),' ')}",flush=True)
                shown+=1
                if shown>=3: break
    print("----",flush=True)
