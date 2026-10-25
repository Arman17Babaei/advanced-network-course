#!/usr/bin/env python3
import re
import requests
from bs4 import BeautifulSoup

H={"User-Agent":"Mozilla/5.0 (compatible; advanced-network-course-source-inspector/1.0)"}
for year in [2023, 2024, 2025, 2026]:
    url=f"https://ssl.linklings.net/conferences/ipdps/ipdps{year}_program/views/at_a_glance.html"
    r=requests.get(url,timeout=45,headers=H)
    print(f"YEAR={year} STATUS={r.status_code} URL={r.url} BYTES={len(r.content)}",flush=True)
    if r.status_code != 200:
        continue
    soup=BeautifulSoup(r.text,"html.parser")
    print("TITLE", soup.title.get_text(" ",strip=True) if soup.title else "",flush=True)
    for tag in ["a","tr","li","div","span"]:
        els=soup.find_all(tag)
        print(f"TAG={tag} COUNT={len(els)}",flush=True)
    # Print likely session/paper links and their containing markup.
    shown=0
    for a in soup.find_all("a",href=True):
        txt=" ".join(a.stripped_strings)
        href=a.get("href","")
        blob=(txt+" "+href).lower()
        if any(k in blob for k in ["paper", "session", "technical", "event", "presentation"]):
            print(f"A {txt!r} -> {href}",flush=True)
            parent=a.find_parent(["tr","li","div","td"])
            if parent:
                print("PARENT="+str(parent)[:2200].replace("\n"," "),flush=True)
            shown+=1
            if shown>=20: break
    # inspect class vocabulary
    classes={}
    for el in soup.find_all(True):
        for cl in el.get("class") or []:
            classes[cl]=classes.get(cl,0)+1
    print("TOP_CLASSES",sorted(classes.items(), key=lambda x:-x[1])[:40],flush=True)
    # rough text markers
    text=" ".join(soup.stripped_strings)
    for pat in ["Technical Session","Workshop","Tutorial","Poster","Keynote","Algorithms","Architecture","System Software"]:
        print(f"MARKER {pat}={len(re.findall(re.escape(pat),text,re.I))}",flush=True)
    print("----",flush=True)
