#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

H={"User-Agent":"advanced-network-course-source-inspector/1.0"}

# Inspect 2026 accepted-paper entry markup.
url="https://conferences2.sigcomm.org/co-next/2026/partials/accepted-papers.html"
r=requests.get(url,timeout=15,headers=H); r.raise_for_status()
soup=BeautifulSoup(r.text,"html.parser")
lis=soup.find_all("li")
print(f"2026 LI_COUNT={len(lis)}", flush=True)
for idx in [0,1,2,len(lis)-1]:
    li=lis[idx]
    print(f"2026_LI[{idx}]={str(li)[:2600].replace(chr(10),' ')}", flush=True)

# Probe likely 2025 program templates exposed by the app routes.
base="https://conferences2.sigcomm.org/co-next/2025/"
for path in [
    "partials/program.html",
    "partials/pprogram.html",
    "partials/toc.html",
    "partials/programatglance.html",
]:
    u=base+path
    rr=requests.get(u,timeout=15,headers=H)
    print(f"2025 PATH={path} STATUS={rr.status_code} BYTES={len(rr.content)}",flush=True)
    if rr.status_code!=200:
        continue
    ss=BeautifulSoup(rr.text,"html.parser")
    print(
        f"  h2={len(ss.find_all('h2'))} h3={len(ss.find_all('h3'))} "
        f"li={len(ss.find_all('li'))} tr={len(ss.find_all('tr'))} "
        f"b={len(ss.find_all('b'))} strong={len(ss.find_all('strong'))}",
        flush=True,
    )
    for tag in ["h2","h3","li","tr","p","b","strong"]:
        vals=[]
        for el in ss.find_all(tag):
            t=" ".join(el.stripped_strings)
            if len(t)>=10:
                vals.append(t[:300])
            if len(vals)>=8:
                break
        if vals:
            print(f"  {tag}: " + " || ".join(vals), flush=True)
