#!/usr/bin/env python3
import collections
import re
import requests

H={"User-Agent":"advanced-network-course-source-inspector/1.0"}
base="https://api.crossref.org/works"
families={
  2023:"10.1109/INFOCOM53939.2023",
  2024:"10.1109/INFOCOM52122.2024",
  2025:"10.1109/INFOCOM55648.2025",
  2026:"10.1109/INFOCOM59046.2026",
}
for year,stem in families.items():
    params={
      "filter":f"from-pub-date:{year}-01-01,until-pub-date:{year}-12-31,prefix:10.1109",
      "query.container-title":f"IEEE INFOCOM {year}",
      "rows":1000,
      "select":"DOI,title,container-title,event,type,page,author,URL"
    }
    r=requests.get(base,params=params,headers=H,timeout=60); r.raise_for_status()
    items=(r.json().get("message") or {}).get("items") or []
    matches=[x for x in items if str(x.get("DOI","")).lower().startswith(stem.lower()+".")]
    dist=collections.Counter()
    examples=collections.defaultdict(list)
    for x in matches:
        p=str(x.get("page") or "")
        m=re.match(r"^(\d+)\s*-\s*(\d+)$",p)
        span=(int(m.group(2))-int(m.group(1))+1) if m else None
        dist[span]+=1
        if len(examples[span])<3:
            examples[span].append(((x.get("title") or [""])[0],p,x.get("DOI")))
    print(f"YEAR={year} FAMILY_MATCHES={len(matches)} PAGE_SPANS={dict(sorted(dist.items(),key=lambda z:(z[0] is None,z[0] or 0)))}",flush=True)
    for span,n in sorted(dist.items(),key=lambda z:(z[0] is None,z[0] or 0)):
        print(f" SPAN={span} N={n}",flush=True)
        for title,p,doi in examples[span]:
            print(f"   - {p} | {doi} | {title}",flush=True)
