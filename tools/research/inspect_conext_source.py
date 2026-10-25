#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

H={"User-Agent":"advanced-network-course-source-inspector/1.0"}
url="https://conferences2.sigcomm.org/co-next/2025/partials/program.html"
r=requests.get(url,timeout=20,headers=H); r.raise_for_status()
soup=BeautifulSoup(r.text,"html.parser")

paper_lis=[]
for li in soup.find_all("li"):
    strong=li.find("strong")
    text=" ".join(li.stripped_strings)
    if strong and "ACM DL" in text and "PDF" in text:
        paper_lis.append(li)

print(f"2025_PAPER_LI_COUNT={len(paper_lis)}",flush=True)
for idx in list(range(min(5,len(paper_lis)))) + list(range(max(0,len(paper_lis)-3),len(paper_lis))):
    li=paper_lis[idx]
    print(f"LI[{idx}]={str(li)[:4200].replace(chr(10),' ')}",flush=True)

titles=[]
for li in paper_lis:
    s=li.find("strong")
    if s:
        titles.append(" ".join(s.stripped_strings))
print("TITLES:",flush=True)
for t in titles:
    print(" - "+t,flush=True)
