#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))
import build_paper_corpus as corpus

CFG=json.loads((ROOT/"tools/research/paper_corpus_config.json").read_text(encoding="utf-8"))
TX=CFG["ieee_transactions"]

def rows_for(spec, year):
    rows=corpus.collect_works([spec["source_id"]], year, venue_override=None, kind="journal", core=False)
    rows=corpus.dedupe(rows)
    # Journal metadata may include front matter; research-paper inventory requires authors.
    rows=[r for r in rows if r.get("authors")]
    for r in rows:
        corpus.categorize(r)
        if spec.get("relevance_mode")=="all":
            r["network_relevant"]=True
            r["network_relevance_score"]=max(2,int(r.get("network_relevance_score") or 0))
    if spec.get("relevance_mode")=="filter":
        rows=[r for r in rows if r.get("network_relevant")]
    return rows

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--journal",required=True)
    args=p.parse_args()
    spec=next((x for x in TX.get("journal_specs",[]) if x["name"]==args.journal),None)
    if not spec: raise SystemExit(f"Unknown journal: {args.journal}")
    failures=[]
    for year in CFG["years"]:
        rows=rows_for(spec,year)
        n=len(rows)
        authors=sum(bool(r.get("authors")) for r in rows)
        links=sum(bool(r.get("doi") or r.get("url")) for r in rows)
        keywords=sum(bool(r.get("keywords")) for r in rows)
        print(f"JOURNAL={spec['name']} YEAR={year} COUNT={n} AUTHORS={authors}/{n} LINKS={links}/{n} KEYWORDS={keywords}/{n}")
        print("SAMPLE:")
        for r in rows[:5]:
            print(f" - {r['title']} | {r['authors']} | {r.get('doi') or r.get('url')} | {r['keywords']}")
        if 2023 <= year <= int(spec.get("validate_through",2026)) and n < int(spec.get("hard_min",1)):
            failures.append(f"{year}: count {n} < minimum {spec.get('hard_min')}")
        if n and authors/n < .98: failures.append(f"{year}: author coverage {authors}/{n} < 98%")
        if n and links/n < .98: failures.append(f"{year}: link coverage {links}/{n} < 98%")
        if n and keywords/n < 1: failures.append(f"{year}: keyword coverage {keywords}/{n} < 100%")
    if failures:
        print("VALIDATION FAILED",file=sys.stderr)
        for x in failures: print(" - "+x,file=sys.stderr)
        raise SystemExit(2)
    print("VALIDATION PASSED")

if __name__=="__main__":
    main()
