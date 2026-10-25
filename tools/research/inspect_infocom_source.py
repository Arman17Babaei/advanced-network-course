#!/usr/bin/env python3
import collections, re, time, requests

H={"User-Agent":"advanced-network-course-source-inspector/1.0 (https://github.com/Arman17Babaei/advanced-network-course)"}
base="https://api.crossref.org/works"
families={
  2023:"10.1109/INFOCOM53939.2023",
  2024:"10.1109/INFOCOM52122.2024",
  2025:"10.1109/INFOCOM55648.2025",
  2026:"10.1109/INFOCOM59046.2026",
}
known={2023:252,2024:256,2025:272,2026:329}
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
        print(f"YEAR={year} ATTEMPT={attempt+1} STATUS={r.status_code}",flush=True)
        if r.status_code==429:
            time.sleep(5*(attempt+1)); continue
        r.raise_for_status()
    if data is None:
        raise SystemExit(f"Could not fetch {year}")

    items=(data.get("message") or {}).get("items") or []
    matches=[x for x in items if str(x.get("DOI","")).lower().startswith(stem.lower()+".")]
    stats=collections.Counter()
    start1=[]
    nonstart=[]
    for x in matches:
        p=str(x.get("page") or "")
        m=re.match(r"^(\d+)\s*-\s*(\d+)$",p)
        if not m:
            stats["no_numeric"]+=1
            continue
        start,end=map(int,m.groups())
        span=end-start+1
        stats[f"span_{span}"]+=1
        stats["start_1" if start==1 else "start_gt1"]+=1
        stats["full_start1" if start==1 and 8<=span<=10 else "other"]+=1
        stats["full_nonstart" if start!=1 and 8<=span<=10 else "other2"]+=1
        rec=(span,p,(x.get("title") or [""])[0],x.get("DOI"))
        (start1 if start==1 else nonstart).append(rec)

    full_start1=[x for x in start1 if 8<=x[0]<=10]
    full_nonstart=[x for x in nonstart if 8<=x[0]<=10]
    print(
      f"YEAR={year} FAMILY={len(matches)} KNOWN_MAIN={known[year]} "
      f"FULL_NONSTART={len(full_nonstart)} FULL_START1={len(full_start1)} "
      f"NO_NUMERIC={stats['no_numeric']}",
      flush=True
    )
    print("START1_FULL:",flush=True)
    for rec in sorted(full_start1)[:100]:
        print(" - "+" | ".join(map(str,rec)),flush=True)
    print("NONSTART_SHORTER_THAN_8:",flush=True)
    for rec in sorted(nonstart):
        if rec[0] < 8:
            print(" - "+" | ".join(map(str,rec)),flush=True)
    print("----",flush=True)
    time.sleep(4)
