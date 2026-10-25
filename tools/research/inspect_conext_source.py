#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

H={"User-Agent":"advanced-network-course-source-inspector/1.0"}
for year in [2023,2024,2025,2026]:
    url=f"https://conferences2.sigcomm.org/co-next/{year}/partials/accepted-papers.html"
    r=requests.get(url,timeout=15,headers=H)
    print(f"YEAR={year} STATUS={r.status_code} BYTES={len(r.content)} URL={r.url}",flush=True)
    if r.status_code!=200:
        print("----",flush=True); continue
    soup=BeautifulSoup(r.text,"html.parser")
    for tag in ["h1","h2","h3","h4","li","tr","p","strong","b"]:
        els=soup.find_all(tag)
        vals=[]
        for el in els:
            t=" ".join(el.stripped_strings)
            if len(t)>=8:
                vals.append(t[:260])
            if len(vals)>=10:
                break
        print(f"  TAG={tag} COUNT={len(els)}",flush=True)
        for v in vals:
            print("    "+v,flush=True)
    print("----",flush=True)
