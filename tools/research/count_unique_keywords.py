#!/usr/bin/env python3
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/"materials/assessments/data/recent_networking_papers.csv"

def norm_kw(s):
    return re.sub(r"\s+"," ",s.strip()).casefold()

unique=set()
unique_by_prov=defaultdict(set)
occ=Counter()
rows=0
with PATH.open("r",encoding="utf-8",newline="") as f:
    for row in csv.DictReader(f):
        rows+=1
        prov=(row.get("keyword_provenance") or "missing").strip()
        for kw in (row.get("keywords") or "").split(";"):
            k=norm_kw(kw)
            if not k:
                continue
            unique.add(k)
            unique_by_prov[prov].add(k)
            occ[k]+=1

print(f"ROWS={rows}")
print(f"UNIQUE_NORMALIZED_KEYWORDS={len(unique)}")
print(f"TOTAL_KEYWORD_ASSIGNMENTS={sum(occ.values())}")
for prov in sorted(unique_by_prov):
    print(f"PROVENANCE={prov} UNIQUE={len(unique_by_prov[prov])}")
print("TOP20")
for k,n in occ.most_common(20):
    print(f"{n}\t{k}")
