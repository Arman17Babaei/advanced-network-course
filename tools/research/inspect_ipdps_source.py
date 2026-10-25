#!/usr/bin/env python3
import re, requests
from bs4 import BeautifulSoup

H={"User-Agent":"Mozilla/5.0 (compatible; advanced-network-course-source-inspector/1.0)"}
year=2023
url=f"https://www.ipdps.org/ipdps{year}/{year}-advance-program.html"
r=requests.get(url,timeout=40,headers=H); r.raise_for_status()
soup=BeautifulSoup(r.text,"html.parser")

selected=set()
for tr in soup.find_all("tr"):
    cells=tr.find_all("td",recursive=False)
    if len(cells)<2: continue
    left=" ".join(cells[0].stripped_strings)
    if "parallel technical" in left.lower() or "best paper" in left.lower():
        for li in cells[1].find_all("li"):
            em=li.find("em")
            if em:
                selected.add(" ".join(em.stripped_strings).strip(" ."))

print(f"SELECTED={len(selected)}",flush=True)

print("UNSELECTED_EM_CANDIDATES",flush=True)
seen=set()
for em in soup.find_all("em"):
    txt=" ".join(em.stripped_strings).strip(" .")
    if not (15 <= len(txt) <= 260) or txt in selected or txt in seen:
        continue
    seen.add(txt)
    tr=em.find_parent("tr")
    label=""
    if tr:
        cells=tr.find_all("td",recursive=False)
        if cells:
            label=" ".join(cells[0].stripped_strings)
    # Exclude obvious affiliations/abstract prefixes but print everything else.
    if re.search(r"^(abstract|recipient|the university|university|argonne|nvidia|intel|oak ridge)",txt,re.I):
        continue
    print(f"EM | ROW={label!r} | {txt}",flush=True)

print("NONLI_EM_IN_SCHEDULE_ROWS",flush=True)
for tr in soup.find_all("tr"):
    cells=tr.find_all("td",recursive=False)
    if len(cells)<2: continue
    left=" ".join(cells[0].stripped_strings)
    if not re.search(r"(session|technical|plenary|industry|panel|award)",left,re.I):
        continue
    for em in cells[1].find_all("em"):
        if em.find_parent("li") is not None:
            continue
        txt=" ".join(em.stripped_strings).strip(" .")
        if 15 <= len(txt) <= 300:
            print(f"NONLI | ROW={left!r} | {txt}",flush=True)

print("TITLELIKE_STRONG_P",flush=True)
for tr in soup.find_all("tr"):
    cells=tr.find_all("td",recursive=False)
    if len(cells)<2: continue
    left=" ".join(cells[0].stripped_strings)
    if "parallel technical" in left.lower() or "best paper" in left.lower():
        continue
    for p in cells[1].find_all("p"):
        txt=" ".join(p.stripped_strings).strip()
        if 20 <= len(txt) <= 250 and p.find(["em","strong"]):
            if not re.search(r"^(session chair|moderator|panel members|abstract|read |recipient)",txt,re.I):
                print(f"P | ROW={left!r} | {txt}",flush=True)
