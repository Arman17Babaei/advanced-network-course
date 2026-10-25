#!/usr/bin/env python3
import json,requests
source="https://openalex.org/S69141925"
filters=[
 f"primary_location.source.id:{source},publication_year:2024,topics.subfield.id:https://openalex.org/subfields/1705",
 f"primary_location.source.id:{source},publication_year:2024,primary_topic.subfield.id:https://openalex.org/subfields/1705",
]
for f in filters:
    r=requests.get("https://api.openalex.org/works",params={"filter":f,"per-page":1,"select":"id,display_name"},timeout=30,headers={"User-Agent":"advanced-network-course/1.0"})
    print("FILTER",f)
    print("STATUS",r.status_code)
    try:
        d=r.json(); print("COUNT",(d.get("meta") or {}).get("count")); print("ERROR",d.get("error"))
    except Exception:
        print(r.text[:500])
