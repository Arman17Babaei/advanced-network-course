#!/usr/bin/env python3
import collections,re,requests
H={"User-Agent":"advanced-network-course-source-inspector/1.0 (https://github.com/Arman17Babaei/advanced-network-course)"}
year=2026; stem="10.1109/INFOCOM59046.2026"
params={
 "filter":"from-pub-date:2026-01-01,until-pub-date:2026-12-31,prefix:10.1109",
 "query.container-title":"IEEE INFOCOM 2026","rows":1000,
 "select":"DOI,title,container-title,event,type,page,author,URL"
}
r=requests.get("https://api.crossref.org/works",params=params,headers=H,timeout=60); r.raise_for_status()
items=(r.json().get("message") or {}).get("items") or []
matches=[x for x in items if str(x.get("DOI","")).lower().startswith(stem.lower()+".")]
containers=collections.Counter()
events=collections.Counter()
for x in matches:
 containers[tuple(x.get("container-title") or [])]+=1
 ev=x.get("event") or {}
 events[str(ev.get("name") or "")]+=1
print("CONTAINERS",flush=True)
for k,n in containers.most_common(): print(n,k,flush=True)
print("EVENTS",flush=True)
for k,n in events.most_common(): print(n,repr(k),flush=True)
print("LONG_NONSTANDARD",flush=True)
for x in matches:
 p=str(x.get("page") or "")
 m=re.match(r"^(\d+)\s*-\s*(\d+)$",p)
 span=(int(m.group(2))-int(m.group(1))+1) if m else None
 if span in {8,9}:
  print(f"SPAN={span} PAGE={p} DOI={x.get('DOI')} EVENT={(x.get('event') or {}).get('name')} CONTAINER={(x.get('container-title') or [''])[0]} TITLE={(x.get('title') or [''])[0]}",flush=True)
