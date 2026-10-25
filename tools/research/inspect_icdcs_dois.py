#!/usr/bin/env python3
import concurrent.futures, re, requests
from collections import Counter

H={"User-Agent":"advanced-network-course-source-inspector/1.0 (https://github.com/Arman17Babaei/advanced-network-course)"}
stem="10.1109/ICDCS57875.2023"

def one(n):
    doi=f"{stem}.{n:05d}"
    try:
        r=requests.get("https://api.crossref.org/works/"+doi,headers=H,timeout=20)
        if r.status_code==404: return None
        r.raise_for_status()
        x=r.json().get("message") or {}
        title=(x.get("title") or [""])[0]
        page=str(x.get("page") or "")
        authors=[]
        for a in x.get("author") or []:
            name=" ".join(y for y in [a.get("given",""),a.get("family","")] if y).strip()
            if name: authors.append(name)
        return (n,doi,title,page,authors,x.get("type",""),x.get("container-title") or [])
    except Exception as e:
        return ("ERR",doi,repr(e),"",[],"",[])

vals=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
    for x in ex.map(one,range(1,150)):
        if x: vals.append(x)
errs=[x for x in vals if x[0]=="ERR"]
vals=[x for x in vals if x[0]!="ERR"]

spans=Counter()
for x in vals:
    m=re.match(r"^(\d+)\s*[-–]\s*(\d+)$",x[3])
    span=(int(m.group(2))-int(m.group(1))+1) if m else None
    spans[span]+=1
print(f"FOUND={len(vals)} ERRORS={len(errs)} SPANS={dict(sorted(spans.items(),key=lambda z:(z[0] is None,z[0] or 0)))}",flush=True)
for x in vals:
    m=re.match(r"^(\d+)\s*[-–]\s*(\d+)$",x[3])
    span=(int(m.group(2))-int(m.group(1))+1) if m else None
    print(f"REC | {x[0]:05d} | span={span} | page={x[3]!r} | authors={len(x[4])} | {x[2]}",flush=True)
