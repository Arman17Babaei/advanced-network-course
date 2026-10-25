#!/usr/bin/env python3
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))
import build_paper_corpus as c

QUERY="IEEE/ACM Transactions on Networking"
for s in c.oa_list("sources", {
    "search": QUERY,
    "select": "id,display_name,type,works_count,issn,issn_l,host_organization_name"
}, max_pages=2):
    name=c.norm(s.get("display_name"))
    if "Transactions on Networking" in name:
        print(json.dumps(s,ensure_ascii=False))
