#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))
import build_paper_corpus as c
from validate_transaction_journal import is_network_paper

source="https://openalex.org/S69141925"; year=2024
full=c.collect_works([source],year,venue_override="IEEE Transactions on Mobile Computing",kind="journal",core=False)
full=[r for r in c.dedupe(full) if r.get("authors") and is_network_paper(r)]
cand=[]
filt=f"primary_location.source.id:{source},publication_year:{year},topics.subfield.id:https://openalex.org/subfields/1705"
for w in c.oa_list("works",{"filter":filt,"select":"id,doi,display_name,publication_year,type,authorships,primary_location,keywords,topics,primary_topic"}):
    r=c.work_row(w,venue_override="IEEE Transactions on Mobile Computing",kind="journal",core=False)
    if r.get("authors") and is_network_paper(r): cand.append(r)
cand=c.dedupe(cand)
key=lambda r:(r.get("doi") or r.get("openalex_id") or r.get("title"))
cs={key(r) for r in cand}
missing=[r for r in full if key(r) not in cs]
print("FULL_STRICT",len(full))
print("SUBFIELD_STRICT",len(cand))
print("MISSING",len(missing))
for r in missing[:30]: print("MISS |",r["title"],"|",r["keywords"],"|",r["primary_topic"])
