#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))
import build_paper_corpus as corpus

CFG=json.loads((ROOT/"tools/research/paper_corpus_config.json").read_text(encoding="utf-8"))
TX=CFG["ieee_transactions"]
NAME_RX=re.compile(r"^IEEE(?:/ACM)? Transactions (?:on|of) ",re.I)

known_names=set()
known_ids=set()
for spec in TX.get("journal_specs",[]):
    known_names.add((spec.get("canonical_name") or spec["name"]).lower())
    known_names.add(spec["name"].lower())
    if spec.get("source_id"):
        known_ids.add(spec["source_id"])
    for ids in spec.get("source_ids_by_year",{}).values():
        known_ids.update(ids)

found={}
for s in corpus.oa_list("sources",{
    "search":"IEEE Transactions",
    "select":"id,display_name,type,works_count,issn,issn_l,host_organization_name"
},max_pages=10):
    name=corpus.norm(s.get("display_name"))
    if corpus.norm(s.get("type"))!="journal" or not NAME_RX.search(name):
        continue
    found[corpus.norm(s["id"])]=s

rows=sorted(found.values(),key=lambda x:corpus.norm(x.get("display_name")).lower())
print(f"MATCHED_SOURCES={len(rows)}")
for s in rows:
    sid=corpus.norm(s.get("id"))
    name=corpus.norm(s.get("display_name"))
    known=sid in known_ids or name.lower() in known_names
    print(
        "KNOWN" if known else "UNSCANNED",
        "|",name,
        "|",sid,
        "| issn_l=",corpus.norm(s.get("issn_l")),
        "| works=",s.get("works_count") or 0,
    )
