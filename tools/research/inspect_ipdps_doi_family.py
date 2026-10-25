#!/usr/bin/env python3
import collections, concurrent.futures, re, requests

H={"User-Agent":"advanced-network-course-source-inspector/1.0 (https://github.com/Arman17Babaei/advanced-network-course)"}
families={
  2023:("10.1109/IPDPS54959.2023",140),
  2024:("10.1109/IPDPS57955.2024",150),
  2025:("10.1109/IPDPS64566.2025",160),
  2026:("10.1109/IPDPS65963.2026",180),
}

def get_one(stem,n):
    doi=f"{stem}.{n:05d}"
    url="https://api.crossref.org/works/"+doi
    try:
        r=requests.get(url,headers=H,timeout=20)
        if r.status_code==404:
            return None
        r.raise_for_status()
        x=(r.json().get("message") or {})
        title=(x.get("title") or [""])[0]
        page=str(x.get("page") or "")
        authors=[]
        for a in x.get("author") or []:
            name=" ".join(y for y in [a.get("given",""),a.get("family","")] if y).strip()
            if name: authors.append(name)
        return (n,doi,title,page,authors,x.get("type",""),x.get("container-title") or [])
    except Exception as e:
        return ("ERR",doi,repr(e),"",[],"",[])

for year,(stem,maxn) in families.items():
    vals=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        for x in ex.map(lambda n:get_one(stem,n), range(1,maxn+1)):
            if x is not None: vals.append(x)
    errs=[x for x in vals if x[0]=="ERR"]
    vals=[x for x in vals if x[0]!="ERR"]
    spans=collections.Counter()
    for x in vals:
        m=re.match(r"^(\d+)\s*[-–]\s*(\d+)$",x[3])
        spans[(int(m.group(2))-int(m.group(1))+1) if m else None]+=1
    print(f"YEAR={year} FOUND={len(vals)} ERRORS={len(errs)} SPANS={dict(sorted(spans.items(),key=lambda z:(z[0] is None,z[0] or 0)))}",flush=True)
    print("SHORT_OR_NONPAGED:",flush=True)
    for x in vals:
        m=re.match(r"^(\d+)\s*[-–]\s*(\d+)$",x[3])
        span=(int(m.group(2))-int(m.group(1))+1) if m else None
        if span is None or span<=6:
            print(f"  {x[0]:05d} | span={span} page={x[3]!r} | {x[2]} | authors={len(x[4])}",flush=True)
    print("BOUNDARY:",flush=True)
    for x in vals[:5]+vals[-5:]:
        print(f"  {x[0]:05d} | page={x[3]!r} | {x[2]} | authors={len(x[4])}",flush=True)
    if errs:
        print("ERROR SAMPLE",errs[:5],flush=True)
    print("----",flush=True)
