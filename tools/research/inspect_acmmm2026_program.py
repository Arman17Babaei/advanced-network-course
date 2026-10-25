#!/usr/bin/env python3
import re,requests
from bs4 import BeautifulSoup

url="https://2026.acmmm.org/site/technical-programme.html"
r=requests.get(url,timeout=60,headers={"User-Agent":"advanced-network-course/1.0"})
r.raise_for_status()
print("BYTES",len(r.content),"CT",r.headers.get("content-type"))
s=BeautifulSoup(r.text,"html.parser")
needle=None
for t in s.find_all(string=re.compile(r"Poster-Wm-A1")):
    needle=t.parent
    break
print("NEEDLE",needle)
if needle:
    p=needle
    for level in range(6):
        print("LEVEL",level,"TAG",p.name,"CLASS",p.get("class"),"TEXT",p.get_text(" ",strip=True)[:800])
        print("HTML",str(p)[:4000])
        p=p.parent
        if p is None: break
print("CLASS_COUNTS")
from collections import Counter
cnt=Counter()
for tag in s.find_all(True):
    for cls in tag.get("class") or []:
        if any(k in cls.lower() for k in ("paper","poster","slot","session","programme","program","event")):
            cnt[cls]+=1
for k,v in cnt.most_common(80):
    print(v,k)
