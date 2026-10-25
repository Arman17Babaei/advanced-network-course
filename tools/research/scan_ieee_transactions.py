#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re,sys,time
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))
import build_paper_corpus as corpus
from validate_transaction_journal import is_network_paper

CFG=json.loads((ROOT/"tools/research/paper_corpus_config.json").read_text(encoding="utf-8"))
YEARS=CFG["years"]
OUT=ROOT/"materials/assessments/data/transactions"
OUT.mkdir(parents=True,exist_ok=True)

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
        "select":"id,display_name,type,works_count,issn,issn_l,host_organization_name"
    },max_pages=10):
        name=corpus.norm(s.get("display_name"))
        if corpus.norm(s.get("type"))!="journal" or not NAME_RX.search(name):
            continue
        found[corpus.norm(s["id"])]=s
    return sorted(found.values(),key=lambda x:corpus.norm(x.get("display_name")).lower())

def collect_network_rows(sources):
    by_id={corpus.norm(s["id"]):s for s in sources}
    source_ids=list(by_id)
    kept=[]
    raw_counts=Counter()
    kept_counts=Counter()
    for year in YEARS:
        if year==2027:
            # Keep already-indexed early-access 2027 papers if present.
            pass
        for i in range(0,len(source_ids),8):
            batch=source_ids[i:i+8]
            rows=corpus.collect_works(batch,year,venue_override=None,kind="journal",core=False)
            for r in rows:
                if not r.get("authors"):
                    continue
                corpus.categorize(r)
                raw_counts[(r["venue"],year)]+=1
                if r["venue"] in CORE_ALL or is_network_paper(r):
                    r["network_relevant"]=True
                    r["network_relevance_score"]=max(2,int(r.get("network_relevance_score") or 0))
                    kept.append(r)
                    kept_counts[(r["venue"],year)]+=1
            print(f"YEAR={year} SOURCES={i+1}-{min(i+8,len(source_ids))}/{len(source_ids)} KEPT={len(kept)}",flush=True)
            time.sleep(.03)
    return corpus.dedupe(kept),raw_counts,kept_counts

def write_outputs(sources,rows,raw_counts,kept_counts):
    path=OUT/"ieee_transactions_network.csv"
    corpus.write_csv(path,rows)
    with (OUT/"IEEE_TRANSACTIONS_SOURCES.csv").open("w",encoding="utf-8",newline="") as f:
        fields=["source_id","display_name","issn_l","works_count","raw_2023_2027","network_2023_2027"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for s in sources:
            name=corpus.norm(s.get("display_name"))
            w.writerow({
                "source_id":corpus.norm(s.get("id")),
                "display_name":name,
                "issn_l":corpus.norm(s.get("issn_l")),
                "works_count":s.get("works_count") or 0,
                "raw_2023_2027":sum(raw_counts[(name,y)] for y in YEARS),
                "network_2023_2027":sum(kept_counts[(name,y)] for y in YEARS),
            })
    with (OUT/"IEEE_TRANSACTIONS_COVERAGE.csv").open("w",encoding="utf-8",newline="") as f:
        fields=["venue","year","raw_records","network_records"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for s in sources:
            name=corpus.norm(s.get("display_name"))
            for y in YEARS:
                w.writerow({"venue":name,"year":y,"raw_records":raw_counts[(name,y)],"network_records":kept_counts[(name,y)]})
    print(f"WROTE {len(rows)} network-relevant papers to {path.relative_to(ROOT)}")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--write",action="store_true"); args=p.parse_args()
    sources=discover_sources()
    print(f"SOURCES={len(sources)}")
    for s in sources:
        print(f"SOURCE | {s.get('display_name')} | {s.get('id')} | {s.get('issn_l')} | works={s.get('works_count')}")
    if len(sources)<40:
        raise SystemExit(f"source discovery unexpectedly small: {len(sources)}")
    rows,raw,kept=collect_network_rows(sources)
    print(f"NETWORK_ROWS={len(rows)}")
    by_year=Counter(int(r["year"]) for r in rows)
    for y in YEARS: print(f"NETWORK_YEAR={y} COUNT={by_year[y]}")
    by_venue=Counter(r["venue"] for r in rows)
    print("TOP_NETWORK_JOURNALS")
    for venue,n in by_venue.most_common(30): print(f" {n:5d} | {venue}")
    if len(rows)<1500:
        raise SystemExit(f"network corpus unexpectedly small: {len(rows)}")
    if any(not r.get("authors") or not r.get("keywords") or not (r.get("doi") or r.get("url")) for r in rows):
        raise SystemExit("retained rows have incomplete required metadata")
    if args.write: write_outputs(sources,rows,raw,kept)
    print("VALIDATION PASSED")

if __name__=="__main__": main()
