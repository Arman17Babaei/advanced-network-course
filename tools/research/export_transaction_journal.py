#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))
import build_paper_corpus as corpus
from validate_transaction_journal import rows_for

CFG=json.loads((ROOT/"tools/research/paper_corpus_config.json").read_text(encoding="utf-8"))
TX=CFG["ieee_transactions"]
OUT=ROOT/"materials/assessments/data/transactions"
OUT.mkdir(parents=True,exist_ok=True)

def slug(s):
    return re.sub(r"[^a-z0-9]+","_",s.lower()).strip("_")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--journal",required=True); args=p.parse_args()
    spec=next((x for x in TX.get("journal_specs",[]) if x["name"]==args.journal),None)
    if not spec: raise SystemExit("Unknown journal")
    rows=[]
    for year in CFG["years"]:
        yr=rows_for(spec,year)
        minc=int(spec.get("hard_min_by_year",{}).get(str(year),spec.get("hard_min",1)))
        if 2023 <= year <= int(spec.get("validate_through",2026)) and len(yr)<minc:
            raise SystemExit(f"{year}: {len(yr)} < {minc}")
        rows.extend(yr)
    rows=corpus.dedupe(rows)
    path=OUT/(slug(spec.get("canonical_name") or spec["name"])+".csv")
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=corpus.FIELDS); w.writeheader()
        for r in rows: w.writerow(corpus.public_row(r))
    print(f"WROTE {len(rows)} rows to {path.relative_to(ROOT)}")
if __name__=="__main__": main()
