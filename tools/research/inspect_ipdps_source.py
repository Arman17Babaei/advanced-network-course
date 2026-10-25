#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
H={"User-Agent":"Mozilla/5.0 (compatible; advanced-network-course-source-inspector/1.0)"}
for year in [2023,2024]:
    url=f"https://www.ipdps.org/ipdps{year}/{year}-advance-program.html"
    r=requests.get(url,timeout=40,headers=H); r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser")
    print(f"YEAR={year}",flush=True)
    for tr in soup.find_all("tr"):
        cells=tr.find_all("td",recursive=False)
        if len(cells)<2: continue
        left=" ".join(cells[0].stripped_strings)
        right=" ".join(cells[1].stripped_strings)
        blob=(left+" "+right).lower()
        if ("best paper" in blob or "plenary" in blob) and cells[1].find_all("li"):
            print(f"LEFT={left!r} LI={len(cells[1].find_all('li'))}",flush=True)
            print("ROW="+str(tr)[:16000].replace("\n"," "),flush=True)
    print("----",flush=True)
