#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))
import build_paper_corpus as c
queries=[
 "IEEE Transactions on Vehicular Technology",
 "IEEE Transactions on Green Communications and Networking",
 "IEEE Transactions on Dependable and Secure Computing",
 "IEEE Transactions on Network Science and Engineering",
]
for q in queries:
    print("QUERY",q)
    for s in c.oa_list("sources",{"search":q,"select":"id,display_name,type,works_count,issn,issn_l,host_organization_name"},max_pages=1):
        n=c.norm(s.get("display_name"))
        if n.lower()==q.lower():
            print(json.dumps(s,ensure_ascii=False))
