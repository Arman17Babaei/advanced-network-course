#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

for year in [2023, 2024, 2025, 2026]:
    base=f"https://conferences2.sigcomm.org/co-next/{year}/"
    r=requests.get(base,timeout=30,headers={"User-Agent":"advanced-network-course-source-inspector/1.0"})
    print(f"YEAR={year} STATUS={r.status_code} URL={r.url}")
    r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser")
    seen=set()
    for a in soup.find_all("a",href=True):
        text=" ".join(a.stripped_strings)
        href=urljoin(base,a["href"])
        blob=(text+" "+href).lower()
        if any(k in blob for k in ["accept","paper","program"]):
            if (text,href) not in seen:
                seen.add((text,href))
                print(f"  {text!r} -> {href}")
    print("----")
