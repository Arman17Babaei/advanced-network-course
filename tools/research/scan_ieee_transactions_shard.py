#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))

import build_paper_corpus as corpus
from validate_transaction_journal import is_network_paper

CFG=json.loads((ROOT/"tools/research/paper_corpus_config.json").read_text(encoding="utf-8"))
YEARS=CFG["years"]
NAME_RX=re.compile(r"^IEEE(?:/ACM)? Transactions (?:on|of) ",re.I)
CORE_ALL={
    "IEEE/ACM Transactions on Networking",
    "IEEE Transactions on Networking",
    "IEEE Transactions on Network and Service Management",
}

def discover_sources():
    found={}
    for s in corpus.oa_list("sources",{
        "search":"IEEE Transactions",
        "select":"id,display_name,type,works_count,issn,issn_l,host_organization_name",
    },max_pages=10):
        name=corpus.norm(s.get("display_name"))
        if corpus.norm(s.get("type"))!="journal" or not NAME_RX.search(name):
            continue
        found[corpus.norm(s["id"])]=s
    return list(found.values())

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--shard",type=int,required=True)
    p.add_argument("--shards",type=int,required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    if not (0 <= args.shard < args.shards):
        raise SystemExit("invalid shard index")

    sources=discover_sources()
    if len(sources)<100:
        raise SystemExit(f"source discovery unexpectedly small: {len(sources)}")

    # Largest journals are spread round-robin across shards so one shard does
    # not inherit all high-volume sources.
    ordered=sorted(
        sources,
        key=lambda s:(-int(s.get("works_count") or 0),corpus.norm(s.get("display_name")).lower())
    )
    mine=[s for i,s in enumerate(ordered) if i % args.shards == args.shard]
    ids=[corpus.norm(s["id"]) for s in mine]
    print(f"SHARD={args.shard}/{args.shards} SOURCES={len(mine)} TOTAL_SOURCES={len(sources)}",flush=True)
    for s in mine:
        print(f"SOURCE | {corpus.norm(s.get('display_name'))} | {corpus.norm(s.get('id'))} | works={s.get('works_count') or 0}",flush=True)

    kept=[]
    raw=Counter()
    accepted=Counter()

    # Batch several source IDs into each OpenAlex request, keeping request
    # volume bounded while preserving each paper's actual journal name.
    for year in YEARS:
        for i in range(0,len(ids),8):
            batch=ids[i:i+8]
            rows=corpus.collect_works(batch,year,venue_override=None,kind="journal",core=False)
            for r in rows:
                if not r.get("authors"):
                    continue
                corpus.categorize(r)
                raw[(r["venue"],year)]+=1
                if r["venue"] in CORE_ALL or is_network_paper(r):
                    r["network_relevant"]=True
                    r["network_relevance_score"]=max(2,int(r.get("network_relevance_score") or 0))
                    kept.append(r)
                    accepted[(r["venue"],year)]+=1
            print(
                f"PROGRESS shard={args.shard} year={year} "
                f"sources={i+1}-{min(i+8,len(ids))}/{len(ids)} kept={len(kept)}",
                flush=True,
            )
            time.sleep(0.10)

    kept=corpus.dedupe(kept)
    if any(not r.get("authors") or not r.get("keywords") or not (r.get("doi") or r.get("url")) for r in kept):
        raise SystemExit("retained shard rows have incomplete metadata")

    out=Path(args.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    corpus.write_csv(out,kept)

    meta=out.with_suffix(".json")
    meta.write_text(json.dumps({
        "shard":args.shard,
        "shards":args.shards,
        "source_count":len(mine),
        "network_rows":len(kept),
        "sources":[
            {
                "id":corpus.norm(s.get("id")),
                "name":corpus.norm(s.get("display_name")),
                "works_count":int(s.get("works_count") or 0),
            } for s in mine
        ],
        "raw_counts":{f"{v}|{y}":n for (v,y),n in raw.items()},
        "network_counts":{f"{v}|{y}":n for (v,y),n in accepted.items()},
    },indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"WROTE {len(kept)} rows to {out}",flush=True)

if __name__=="__main__":
    main()
