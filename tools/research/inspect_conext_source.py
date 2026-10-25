#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

paths=[
    "accepted-papers/","accepted-papers.html","accepted/","accepted.html",
    "program/","program.html","papers/","papers.html","technical-program/",
]
for year in [2023,2024,2025,2026]:
    base=f"https://conferences2.sigcomm.org/co-next/{year}/"
    print(f"YEAR={year}")
    for p in paths:
        url=base+p
        try:
            r=requests.get(url,timeout=20,headers={"User-Agent":"advanced-network-course-source-inspector/1.0"},allow_redirects=True)
        except Exception as e:
            print(f"  {p} ERROR {e}")
            continue
        if r.status_code != 200:
            continue
        soup=BeautifulSoup(r.text,"html.parser")
        title=" ".join(soup.title.stripped_strings) if soup.title else ""
        text=" ".join(soup.stripped_strings)
        score=sum(k in text.lower() for k in ["accepted paper","technical program","paper title","authors"])
        print(f"  {p} -> {r.url} bytes={len(r.content)} title={title!r} score={score} h2={len(soup.find_all('h2'))} li={len(soup.find_all('li'))} tr={len(soup.find_all('tr'))}")
        if score:
            for tag in ["h2","h3","li","tr","p"]:
                vals=[]
                for el in soup.find_all(tag):
                    t=" ".join(el.stripped_strings)
                    if len(t)>=12:
                        vals.append(t[:220])
                    if len(vals)>=5:
                        break
                if vals:
                    print(f"    {tag}: " + " || ".join(vals))
    print("----")
