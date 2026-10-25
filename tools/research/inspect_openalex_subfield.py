#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))
import build_paper_corpus as c
source="https://openalex.org/S69141925"
rows=list(c.oa_list("works",{
  "filter":f"primary_location.source.id:{source},publication_year:2024",
  "select":"id,display_name,topics,primary_topic"
},max_pages=1))
print("SAMPLE_COUNT",len(rows))
for w in rows[:3]:
    print(json.dumps({"title":w.get("display_name"),"primary_topic":w.get("primary_topic"),"topics":(w.get("topics") or [])[:2]},ensure_ascii=False))
