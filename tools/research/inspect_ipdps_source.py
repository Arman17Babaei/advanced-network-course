#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
H={"User-Agent":"Mozilla/5.0 (compatible; advanced-network-course-source-inspector/1.0)"}
for year in [2023,2024]:
    url=f"https://www.ipdps.org/ipdps{year}/{year}-advance-program.html"
    soup=BeautifulSoup(requests.get(url,timeout=40,headers=H).text,"html.parser")
    print(f"YEAR={year}",flush=True)
    for tr in soup.find_all("tr"):
        cells=tr.find_all("td",recursive=False)
        if len(cells)<2: continue
        lis=cells[1].find_all("li")
        if not lis: continue
        paperish=sum(1 for li in lis if li.find("em"))
        if not paperish: continue
        left=" ".join(cells[0].stripped_strings)
        print(f"ROW LABEL={left!r} LI={len(lis)} PAPERISH={paperish}",flush=True)
        if "parallel technical" not in left.lower() and "best paper" not in left.lower():
            print("  MARKUP="+str(tr)[:12000].replace("\n"," "),flush=True)
    print("----",flush=True)
