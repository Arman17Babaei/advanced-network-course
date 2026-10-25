#!/usr/bin/env python3
import requests

H={"User-Agent":"advanced-network-course-source-inspector/1.0"}
base="https://api.crossref.org/works"
year=2026
stem="10.1109/INFOCOM59046.2026"
common={
  "filter":f"from-pub-date:{year}-01-01,until-pub-date:{year}-12-31,prefix:10.1109",
  "rows":1000,
  "select":"DOI,title,container-title,event,type"
}
variants=[
  ("query",stem),
  ("query.bibliographic",stem),
  ("query.container-title","IEEE INFOCOM 2026"),
  ("query.container-title","INFOCOM 2026"),
]
for key,val in variants:
    params=dict(common); params[key]=val
    r=requests.get(base,params=params,headers=H,timeout=45)
    print(f"VARIANT {key}={val!r} STATUS={r.status_code} URL={r.url}",flush=True)
    r.raise_for_status()
    msg=r.json().get("message") or {}
    items=msg.get("items") or []
    matches=[x for x in items if str(x.get("DOI","")).lower().startswith(stem.lower()+".")]
    print(f"  TOTAL={msg.get('total-results')} ITEMS={len(items)} MATCHES={len(matches)}",flush=True)
    for x in matches[:5]:
        print(f"   - {x.get('DOI')} | {(x.get('title') or [''])[0]} | {(x.get('container-title') or [''])[0]}",flush=True)
