#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))
import build_paper_corpus as c

queries=[
 ("IEEE Transactions on Mobile Computing","1536-1233"),
 ("IEEE Transactions on Network and Service Management","1932-4537"),
 ("IEEE Transactions on Vehicular Technology","0018-9545"),
 ("IEEE Transactions on Network Science and Engineering","2327-4697"),
]
for q,issn in queries:
    print("QUERY",q,"ISSN",issn)
    seen=set()
    for params in [
        {"search":q,"select":"id,display_name,type,works_count,issn,issn_l,host_organization_name"},
        {"filter":f"issn:{issn}","select":"id,display_name,type,works_count,issn,issn_l,host_organization_name"},
    ]:
        try:
            for s in c.oa_list("sources",params,max_pages=2):
                sid=c.norm(s.get("id"))
                if sid in seen: continue
                seen.add(sid)
                print(json.dumps(s,ensure_ascii=False))
        except Exception as e:
            print("ERROR",repr(e))
