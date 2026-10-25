#!/usr/bin/env python3
import re, requests, time
from collections import Counter
H={"User-Agent":"advanced-network-course-source-inspector/1.0 (mailto:arman17babaei@users.noreply.github.com)"}
stem="10.1109/ICDCS57875.2023"
rows=[]; errors=[]
for n in range(1,131):
    doi=f"{stem}.{n:05d}"
    ok=False
    for attempt in range(4):
        try:
            r=requests.get("https://api.crossref.org/works/"+doi,headers=H,timeout=20)
            if r.status_code==404:
                ok=True; break
            if r.status_code in (429,500,502,503,504):
                time.sleep(0.5*(attempt+1)); continue
            r.raise_for_status()
            x=r.json().get("message") or {}
            title=(x.get("title") or [""])[0]
            page=str(x.get("page") or "")
            authors=[]
            for a in x.get("author") or []:
                name=" ".join(y for y in [a.get("given",""),a.get("family","")] if y).strip()
                if name: authors.append(name)
            m=re.match(r"^(\d+)\s*[-–]\s*(\d+)$",page)
            span=(int(m.group(2))-int(m.group(1))+1) if m else None
            rows.append((n,doi,title,page,span,len(authors)))
            ok=True; break
        except Exception as e:
            if attempt==3: errors.append((doi,repr(e)))
            time.sleep(0.3*(attempt+1))
    time.sleep(0.08)
print(f"FOUND={len(rows)} ERRORS={len(errors)}",flush=True)
sp=Counter(x[4] for x in rows)
print("SPANS="+repr(dict(sorted(sp.items(),key=lambda z:(z[0] is None,z[0] or 0)))),flush=True)
full=[x for x in rows if x[4] is not None and x[4]>=10 and not re.match(r"^(Poster|Demo:|Workshop)",x[2],re.I)]
print(f"FULL_CANDIDATES={len(full)}",flush=True)
for x in rows:
    if x[4] is None or x[4]<10 or re.match(r"^(Poster|Demo:|Workshop)",x[2],re.I):
        print(f"NONFULL | {x[0]:05d} | span={x[4]} | page={x[3]!r} | {x[2]}",flush=True)
if errors:
    print("ERRORS",errors[:10],flush=True)
