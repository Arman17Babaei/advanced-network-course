#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))
import build_paper_corpus as corpus

def read_csv(path):
    with path.open("r",encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input-dir",required=True)
    p.add_argument("--shards",type=int,required=True)
    p.add_argument("--output-dir",default=str(ROOT/"materials/assessments/data/transactions"))
    args=p.parse_args()

    base=Path(args.input_dir)
    metas=[]
    rows=[]
    for i in range(args.shards):
        csv_matches=list(base.rglob(f"transactions-shard-{i}.csv"))
        json_matches=list(base.rglob(f"transactions-shard-{i}.json"))
        if len(csv_matches)!=1 or len(json_matches)!=1:
            raise SystemExit(
                f"shard {i}: expected one CSV and JSON, got "
                f"{len(csv_matches)} CSV / {len(json_matches)} JSON"
            )
        rows.extend(read_csv(csv_matches[0]))
        metas.append(json.loads(json_matches[0].read_text(encoding="utf-8")))

    source_ids=[]
    for m in metas:
        source_ids.extend(s["id"] for s in m["sources"])
    if len(source_ids)!=len(set(source_ids)):
        raise SystemExit("source partition overlaps across shards")
    if len(source_ids)<100:
        raise SystemExit(f"merged source discovery unexpectedly small: {len(source_ids)}")

    # Convert scalar fields back to the types expected by the common writer.
    for r in rows:
        r["year"]=int(r.get("year") or 0)
        r["network_relevance_score"]=int(r.get("network_relevance_score") or 0)
        r["network_relevant"]=str(r.get("network_relevant","")).lower() in {"true","1","yes"}

    rows=corpus.dedupe(rows)
    if any(not r.get("network_relevant") for r in rows):
        raise SystemExit("merged broad Transactions file contains non-network rows")
    if any(not r.get("title") or not r.get("authors") or not r.get("keywords") or not (r.get("doi") or r.get("url")) for r in rows):
        raise SystemExit("merged broad Transactions file contains incomplete metadata")

    # Compare with the already validated per-journal fallback. A broad sweep may
    # add papers/journals; it must never silently lose the validated baseline.
    fallback=[]
    txdir=ROOT/"materials/assessments/data/transactions"
    for path in sorted(txdir.glob("ieee_transactions_on_*.csv")):
        if path.stat().st_size<=100:
            continue
        for r in read_csv(path):
            r["year"]=int(r.get("year") or 0)
            r["network_relevance_score"]=int(r.get("network_relevance_score") or 0)
            r["network_relevant"]=str(r.get("network_relevant","")).lower() in {"true","1","yes"}
            fallback.append(r)
    fallback=corpus.dedupe(fallback)
    if len(rows)<len(fallback):
        raise SystemExit(
            f"broad sweep retained {len(rows)} rows, below validated fallback {len(fallback)}"
        )

    outdir=Path(args.output_dir)
    outdir.mkdir(parents=True,exist_ok=True)
    corpus.write_csv(outdir/"ieee_transactions_network.csv",rows)

    raw_counts=Counter()
    net_counts=Counter()
    source_records={}
    for m in metas:
        for s in m["sources"]:
            source_records[s["name"]]=s
        for k,n in m.get("raw_counts",{}).items():
            venue,year=k.rsplit("|",1)
            raw_counts[(venue,int(year))]+=int(n)
        for k,n in m.get("network_counts",{}).items():
            venue,year=k.rsplit("|",1)
            net_counts[(venue,int(year))]+=int(n)

    with (outdir/"IEEE_TRANSACTIONS_SOURCES.csv").open("w",encoding="utf-8",newline="") as f:
        fields=["source_id","display_name","works_count","raw_2023_2027","network_2023_2027"]
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        for name,s in sorted(source_records.items(),key=lambda kv:kv[0].lower()):
            w.writerow({
                "source_id":s["id"],
                "display_name":name,
                "works_count":s["works_count"],
                "raw_2023_2027":sum(raw_counts[(name,y)] for y in range(2023,2028)),
                "network_2023_2027":sum(net_counts[(name,y)] for y in range(2023,2028)),
            })

    with (outdir/"IEEE_TRANSACTIONS_COVERAGE.csv").open("w",encoding="utf-8",newline="") as f:
        fields=["venue","year","raw_records","network_records"]
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        for name in sorted(source_records,key=str.lower):
            for y in range(2023,2028):
                w.writerow({
                    "venue":name,
                    "year":y,
                    "raw_records":raw_counts[(name,y)],
                    "network_records":net_counts[(name,y)],
                })

    by_year=Counter(int(r["year"]) for r in rows)
    by_venue=Counter(r["venue"] for r in rows)
    print(f"MERGED_SOURCES={len(source_ids)}")
    print(f"FALLBACK_ROWS={len(fallback)}")
    print(f"BROAD_NETWORK_ROWS={len(rows)}")
    for y in range(2023,2028):
        print(f"YEAR={y} NETWORK_ROWS={by_year[y]}")
    print("TOP_JOURNALS")
    for venue,n in by_venue.most_common(40):
        print(f" {n:5d} | {venue}")
    print("MERGE VALIDATION PASSED")

if __name__=="__main__":
    main()
