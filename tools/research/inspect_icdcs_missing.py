#!/usr/bin/env python3
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))
import build_paper_corpus as c
cfg=json.loads((ROOT/"tools/research/paper_corpus_config.json").read_text())
spec=next(x for x in cfg["conferences"] if x["name"]=="ICDCS")
for y in [2023,2024,2025,2026]:
    rows=c.openalex_conference(spec,y)
    miss=[r for r in rows if not r.get("authors")]
    print(f"YEAR={y} TOTAL={len(rows)} MISSING={len(miss)}")
    for r in miss:
        print("MISSING |",r["title"],"|",r.get("doi") or r.get("url"),"|",r.get("paper_type"),"|",r.get("raw_venue"))
