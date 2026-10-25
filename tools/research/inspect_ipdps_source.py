#!/usr/bin/env python3
import requests, re
from bs4 import BeautifulSoup

H={"User-Agent":"Mozilla/5.0 (compatible; advanced-network-course-source-inspector/1.0)"}

for year in [2023,2024,2025]:
    url=f"https://www.ipdps.org/ipdps{year}/{year}-advance-program.html"
    r=requests.get(url,timeout=40,headers=H); r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser")
    print(f"OFFICIAL YEAR={year} BYTES={len(r.content)}",flush=True)
    # Main conference technical-session rows: inspect table rows whose right
    # cell contains a numbered Session heading and multiple LI paper entries.
    hits=[]
    for tr in soup.find_all("tr"):
        txt=" ".join(tr.stripped_strings)
        if re.search(r"\bSession\s+\d+[A-Z]?\s*:",txt,re.I) and tr.find_all("li"):
            hits.append(tr)
    print(f"TECH_ROWS={len(hits)} LI_IN_TECH_ROWS={sum(len(x.find_all('li')) for x in hits)}",flush=True)
    for tr in hits[:4]:
        print("TECH_ROW="+str(tr)[:9000].replace("\n"," "),flush=True)
    print("----",flush=True)

year=2026
url="https://ssl.linklings.net/conferences/ipdps/ipdps2026_program/views/by_sub_type.html"
r=requests.get(url,timeout=40,headers=H); r.raise_for_status()
soup=BeautifulSoup(r.text,"html.parser")
print(f"LINKLINGS 2026 BYTYPE BYTES={len(r.content)}",flush=True)
for st in soup.select(".section-title"):
    txt=" ".join(st.stripped_strings)
    print("SECTION_TITLE="+txt,flush=True)
    if txt.strip().lower()=="papers":
        par=st.parent
        print("PAPERS_PARENT="+str(par)[:30000].replace("\n"," "),flush=True)
        # follow next siblings too, since section content may not be nested.
        sib=st.parent.find_next_sibling()
        n=0
        while sib is not None and n<4:
            print(f"PAPERS_SIB[{n}]="+str(sib)[:12000].replace("\n"," "),flush=True)
            sib=sib.find_next_sibling(); n+=1
