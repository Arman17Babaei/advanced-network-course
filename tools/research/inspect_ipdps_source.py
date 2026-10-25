#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
H={"User-Agent":"Mozilla/5.0 (compatible; advanced-network-course-source-inspector/1.0)"}
for year in [2023,2024]:
    url=f"https://www.ipdps.org/ipdps{year}/{year}-advance-program.html"
    soup=BeautifulSoup(requests.get(url,timeout=40,headers=H).text,"html.parser")
    print(f"YEAR={year}",flush=True)
    total_li=0; total_em=0
    for tr in soup.find_all("tr"):
        cells=tr.find_all("td",recursive=False)
        if len(cells)<2: continue
        left=" ".join(cells[0].stripped_strings)
        if "parallel technical" not in left.lower() and "best paper" not in left.lower():
            continue
        for idx,li in enumerate(cells[1].find_all("li")):
            ems=li.find_all("em")
            total_li+=1; total_em+=len(ems)
            if len(ems)!=1:
                print(f"ROW={left!r} LI_INDEX={idx} EM_COUNT={len(ems)}",flush=True)
                print("LI="+str(li)[:10000].replace("\n"," "),flush=True)
                for j,em in enumerate(ems):
                    print(f"  EM[{j}]={' '.join(em.stripped_strings)}",flush=True)
    print(f"TOTAL_LI={total_li} TOTAL_EM={total_em}",flush=True)
    print("----",flush=True)
