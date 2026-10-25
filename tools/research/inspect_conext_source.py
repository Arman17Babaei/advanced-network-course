#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

for year in [2023,2024,2025,2026]:
    base=f"https://conferences2.sigcomm.org/co-next/{year}/"
    r=requests.get(base,timeout=10,headers={"User-Agent":"advanced-network-course-source-inspector/1.0"})
    print(f"YEAR={year} STATUS={r.status_code} BYTES={len(r.content)}", flush=True)
    soup=BeautifulSoup(r.text,"html.parser")
    for tag in soup.find_all(["script","link","iframe"]):
        attrs={k:v for k,v in tag.attrs.items() if k in ["src","href","rel","type"]}
        if attrs:
            if "src" in attrs: attrs["src"]=urljoin(base,attrs["src"])
            if "href" in attrs: attrs["href"]=urljoin(base,attrs["href"])
            print(f"  {tag.name} {attrs}", flush=True)
    print("RAW=" + " ".join(r.text.split())[:1800], flush=True)
    print("----", flush=True)
