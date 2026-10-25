#!/usr/bin/env python3
import requests

H={"User-Agent":"advanced-network-course-source-inspector/1.0"}
base="https://api.openalex.org"
r=requests.get(base+"/sources",params={"search":"INFOCOM","per-page":50},headers=H,timeout=30)
print("SOURCES_STATUS",r.status_code,flush=True)
r.raise_for_status()
sources=r.json().get("results",[])
for s in sources:
    name=s.get("display_name","")
    if "INFOCOM" not in name.upper() and "COMPUTER COMMUNICATIONS" not in name.upper():
        continue
    sid=s.get("id")
    print(f"SOURCE {sid} TYPE={s.get('type')} WORKS={s.get('works_count')} NAME={name}",flush=True)
    try:
        rr=requests.get(base+"/works",params={
            "filter":f"primary_location.source.id:{sid},publication_year:2026",
            "per-page":5,
            "select":"id,display_name,publication_year,primary_location"
        },headers=H,timeout=30)
        print(f"  2026_STATUS={rr.status_code}",flush=True)
        if rr.status_code==200:
            data=rr.json()
            print(f"  2026_COUNT={(data.get('meta') or {}).get('count')}",flush=True)
            for w in data.get("results",[])[:5]:
                print("   - "+str(w.get("display_name")),flush=True)
    except Exception as e:
        print("  ERROR",repr(e),flush=True)
