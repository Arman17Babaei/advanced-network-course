#!/usr/bin/env python3
import requests, re
from collections import Counter

H={"User-Agent":"advanced-network-course-source-inspector/1.0 (https://github.com/Arman17Babaei/advanced-network-course)"}
url="https://api.crossref.org/works"
params={
  "filter":"from-pub-date:2023-01-01,until-pub-date:2023-12-31,issn:2575-8411",
  "rows":1000,
  "select":"DOI,title,author,container-title,URL,type,page,subject,abstract,published"
}
r=requests.get(url,params=params,headers=H,timeout=60)
print(f"STATUS={r.status_code} URL={r.url}",flush=True)
r.raise_for_status()
msg=(r.json().get("message") or {})
items=msg.get("items") or []
print(f"TOTAL_RESULTS={msg.get('total-results')} ITEMS={len(items)}",flush=True)

rows=[]
for x in items:
    doi=str(x.get("DOI") or "")
    if not doi.lower().startswith("10.1109/icdcs57875.2023."):
        continue
    title=(x.get("title") or [""])[0]
    page=str(x.get("page") or "")
    authors=[]
    for a in x.get("author") or []:
        name=" ".join(y for y in [a.get("given",""),a.get("family","")] if y).strip()
        if name: authors.append(name)
    m=re.match(r"^(\d+)\s*[-–]\s*(\d+)$",page)
    span=(int(m.group(2))-int(m.group(1))+1) if m else None
    rows.append((doi,title,page,span,len(authors),x.get("type","")))
print(f"FAMILY_ROWS={len(rows)}",flush=True)
spans=Counter(x[3] for x in rows)
print("SPANS="+repr(dict(sorted(spans.items(),key=lambda z:(z[0] is None,z[0] or 0)))),flush=True)
for x in sorted(rows,key=lambda z:z[0]):
    print(f"REC | {x[0]} | span={x[3]} | page={x[2]!r} | authors={x[4]} | {x[1]}",flush=True)
