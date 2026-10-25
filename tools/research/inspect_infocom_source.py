#!/usr/bin/env python3
import collections
import re
import time
import requests

H={"User-Agent":"advanced-network-course-source-inspector/1.0 (https://github.com/Arman17Babaei/advanced-network-course)"}
base="https://api.crossref.org/works"
families={2025:"10.1109/INFOCOM55648.2025",2026:"10.1109/INFOCOM59046.2026"}
front=re.compile(r"(?i)^(table of contents|program|committees?|index page|message from|.*chair.?s? welcome|technical program committee)")
for year,stem in families.items():
    params={
      "filter":f"from-pub-date:{year}-01-01,until-pub-date:{year}-12-31,prefix:10.1109",
      "query.container-title":f"IEEE INFOCOM {year}",
      "rows":1000,
      "select":"DOI,title,container-title,event,type,page,author,URL"
    }
    data=None
    for attempt in range(6):
        r=requests.get(base,params=params,headers=H,timeout=60)
        print(f"YEAR={year} ATTEMPT={attempt+1} STATUS={r.status_code}",flush=True)
        if r.status_code==200:
            data=r.json(); break
        if r.status_code==429:
            time.sleep(4*(attempt+1)); continue
        r.raise_for_status()
    if data is None:
        raise SystemExit(f"Could not fetch {year}")
    items=(data.get("message") or {}).get("items") or []
    matches=[x for x in items if str(x.get("DOI","")).lower().startswith(stem.lower()+".")]
    dist=collections.Counter()
    candidate=0
    no_page_candidates=[]
    for x in matches:
        title=(x.get("title") or [""])[0]
        p=str(x.get("page") or "")
        m=re.match(r"^(\d+)\s*-\s*(\d+)$",p)
        span=(int(m.group(2))-int(m.group(1))+1) if m else None
        dist[span]+=1
        is_main = span is not None and 8 <= span <= 10
        if span is None and title and not front.match(title.strip()):
            is_main=True
            no_page_candidates.append((title,p,x.get("DOI")))
        if is_main:
            candidate+=1
    print(f"YEAR={year} FAMILY={len(matches)} DIST={dict(dist)} MAIN_CANDIDATES={candidate}",flush=True)
    print(f"NO_PAGE_CANDIDATES={len(no_page_candidates)}",flush=True)
    for x in no_page_candidates[:20]:
        print(" - "+" | ".join(str(v) for v in x),flush=True)
    time.sleep(6)
