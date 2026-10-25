#!/usr/bin/env python3
import re, time, requests
H={"User-Agent":"advanced-network-course-source-inspector/1.0 (https://github.com/Arman17Babaei/advanced-network-course)"}
base="https://api.crossref.org/works"
families={2023:"10.1109/INFOCOM53939.2023",2026:"10.1109/INFOCOM59046.2026"}
for year,stem in families.items():
    params={
      "filter":f"from-pub-date:{year}-01-01,until-pub-date:{year}-12-31,prefix:10.1109",
      "query.container-title":f"IEEE INFOCOM {year}",
      "rows":1000,
      "select":"DOI,title,container-title,event,type,page,author,URL"
    }
    data=None
    for attempt in range(8):
        r=requests.get(base,params=params,headers=H,timeout=60)
        if r.status_code==200:
            data=r.json(); break
        if r.status_code==429:
            time.sleep(5*(attempt+1)); continue
        r.raise_for_status()
    if data is None: raise SystemExit(year)
    items=(data.get("message") or {}).get("items") or []
    matches=[x for x in items if str(x.get("DOI","")).lower().startswith(stem.lower()+".")]
    print(f"YEAR={year} FAMILY={len(matches)}",flush=True)
    if year==2023:
        for x in matches:
            p=str(x.get("page") or "")
            if not re.match(r"^\d+\s*-\s*\d+$",p):
                print(f"NOPAGE | {x.get('DOI')} | {p!r} | {(x.get('title') or [''])[0]}",flush=True)
    else:
        for x in matches:
            p=str(x.get("page") or "")
            m=re.match(r"^(\d+)\s*-\s*(\d+)$",p)
            if not m: continue
            span=int(m.group(2))-int(m.group(1))+1
            if span in {8,9}:
                print(f"SHORTFULL | span={span} | {x.get('DOI')} | {(x.get('title') or [''])[0]}",flush=True)
