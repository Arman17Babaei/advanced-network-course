#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))
import build_paper_corpus as c
from validate_transaction_journal import is_network_paper

specs=[
 ("IEEE Transactions on Mobile Computing","https://openalex.org/S69141925"),
 ("IEEE Transactions on Network and Service Management","https://openalex.org/S173527311"),
 ("IEEE Transactions on Vehicular Technology","https://openalex.org/S10936095"),
 ("IEEE Transactions on Network Science and Engineering","https://openalex.org/S2484352698"),
]
for name,sid in specs:
    print("\nJOURNAL",name,sid)
    rows=c.collect_works([sid],2025,venue_override=name,kind="journal",core=False)
    print("RAW",len(rows))
    kept=[]
    for r in rows:
        c.categorize(r)
        if is_network_paper(r):
            kept.append(r)
    print("FILTERED",len(kept))
    for r in rows[:5]:
        print("RAW_SAMPLE",r["title"],"|",r["keywords"],"|",r["primary_topic"])
    for r in kept[:5]:
        print("KEPT_SAMPLE",r["title"],"|",r["keywords"])
