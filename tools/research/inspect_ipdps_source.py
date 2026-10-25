#!/usr/bin/env python3
import requests, re
from bs4 import BeautifulSoup

H={"User-Agent":"Mozilla/5.0 (compatible; advanced-network-course-source-inspector/1.0)"}

for year in [2023,2024,2025]:
    url=f"https://www.ipdps.org/ipdps{year}/{year}-advance-program.html"
    r=requests.get(url,timeout=40,headers=H)
    print(f"OFFICIAL YEAR={year} STATUS={r.status_code} BYTES={len(r.content)} URL={r.url}",flush=True)
    r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser")
    # Session heading candidates and immediate surrounding markup.
    cand=[]
    for el in soup.find_all(["h2","h3","h4","h5","p","td","div"]):
        txt=" ".join(el.stripped_strings)
        if re.search(r"\bSession\s+\d+[A-Z]?\s*:",txt,re.I):
            cand.append(el)
    print(f"SESSION_CANDIDATES={len(cand)}",flush=True)
    for el in cand[:8]:
        print("SESSION_TEXT="+ " ".join(el.stripped_strings)[:500],flush=True)
        print("SESSION_MARKUP="+str(el)[:2600].replace("\n"," "),flush=True)
        parent=el.parent
        print("PARENT_MARKUP="+str(parent)[:5000].replace("\n"," "),flush=True)
    print(f"LI_COUNT={len(soup.find_all('li'))} STRONG_COUNT={len(soup.find_all(['strong','b']))}",flush=True)
    print("----",flush=True)

for year in [2025,2026]:
    base=f"https://ssl.linklings.net/conferences/ipdps/ipdps{year}_program/views/"
    for page in ["at_a_glance.html","by_sub_type.html"]:
        url=base+page
        r=requests.get(url,timeout=40,headers=H)
        print(f"LINKLINGS YEAR={year} PAGE={page} STATUS={r.status_code} BYTES={len(r.content)}",flush=True)
        if r.status_code!=200: continue
        soup=BeautifulSoup(r.text,"html.parser")
        if page=="by_sub_type.html":
            for h in soup.find_all(["h2","h3","h4","div"],class_=lambda x: x and any(k in " ".join(x if isinstance(x,list) else [x]).lower() for k in ["section","type","title"])):
                txt=" ".join(h.stripped_strings)
                if txt:
                    print("TYPE="+txt[:500],flush=True)
            print("PAGE_TEXT_HEAD="+" ".join(list(soup.stripped_strings)[:500])[:8000],flush=True)
        else:
            sessions=soup.select(".program-session")
            print(f"PROGRAM_SESSIONS={len(sessions)} SLOT_WRAPPERS={len(soup.select('.slot-wrapper'))}",flush=True)
            for sess in sessions[:12]:
                print("SESSION="+str(sess)[:6000].replace("\n"," "),flush=True)
    print("----",flush=True)
