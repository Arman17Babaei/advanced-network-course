#!/usr/bin/env python3
from __future__ import annotations
import csv,json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CFG=json.loads((ROOT/"tools/research/paper_corpus_config.json").read_text(encoding="utf-8"))
DATA=ROOT/"materials/assessments/data"
FIELDS=[
    "title","authors","venue","raw_venue","year","venue_kind","source_id","doi","url","openalex_id",
    "metadata_source","paper_type","keywords","keyword_provenance","topics","primary_topic",
    "categories","network_relevance_score","network_relevant",
]

def read_csv(path):
    rows=[]
    with path.open("r",encoding="utf-8",newline="") as f:
        for r in csv.DictReader(f):
            r["year"]=int(r.get("year") or 0)
            r["network_relevance_score"]=int(r.get("network_relevance_score") or 0)
            r["network_relevant"]=str(r.get("network_relevant","")).lower()=="true"
            rows.append(r)
    return rows

def key(r):
    doi=(r.get("doi") or "").strip().lower()
    if doi: return ("doi",doi)
    return ("title",(r.get("title") or "").strip().lower(),int(r["year"]),r.get("venue") or "")

def dedupe(rows):
    out={}
    for r in rows:
        k=key(r)
        if k not in out: out[k]=r
        else:
            a=out[k]
            score=lambda x:sum(bool(x.get(f)) for f in ("authors","keywords","doi","url","openalex_id"))
            if score(r)>score(a): out[k]=r
    return sorted(out.values(),key=lambda r:(int(r["year"]),str(r["venue"]).lower(),str(r["title"]).lower()))

def write(path,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
        for r in rows: w.writerow({k:r.get(k,"") for k in FIELDS})

def main():
    conferences=[]
    coverage=[]
    for spec in CFG["conferences"]:
        snap=spec.get("snapshot")
        if not snap: continue
        path=ROOT/snap
        if not path.exists(): raise SystemExit(f"missing venue snapshot: {snap}")
        rows=read_csv(path)
        conferences.extend(rows)
        by_year=Counter(r["year"] for r in rows)
        for y in CFG["years"]:
            coverage.append({
                "venue":spec["name"],"kind":"conference","year":y,
                "records":by_year[y],"source":snap,
            })

    conferences=dedupe(conferences)
    tx_path=DATA/"transactions/ieee_transactions_network.csv"
    transactions=read_csv(tx_path) if tx_path.exists() else []
    transactions=dedupe(transactions)

    master=dedupe(conferences+transactions)
    network=dedupe([r for r in conferences if r["network_relevant"]]+transactions)

    for name,rows in [
        ("all_conference_papers.csv",conferences),
        ("master_paper_corpus.csv",master),
        ("recent_networking_papers.csv",network),
    ]:
        write(DATA/name,rows)

    with (DATA/"PAPER_CORPUS_COVERAGE.csv").open("w",encoding="utf-8",newline="") as f:
        fields=["venue","kind","year","records","source"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(coverage)

    prov=Counter(r["keyword_provenance"] for r in master)
    cats=Counter()
    for r in network:
        for cat in str(r.get("categories") or "").split("; "):
            if cat and cat!="Other / adjacent": cats[cat]+=1
    conference_counts=Counter((r["venue"],r["year"]) for r in conferences)
    tx_counts=Counter((r["venue"],r["year"]) for r in transactions)

    lines=[
        "# Paper Corpus Summary","",
        f"Conference papers: **{len(conferences):,}**.",
        f"Network-relevant IEEE Transactions papers: **{len(transactions):,}**.",
        f"Master corpus rows: **{len(master):,}**.",
        f"Network-relevant analysis rows: **{len(network):,}**.","",
        "## Conference coverage","",
        "| Venue | 2023 | 2024 | 2025 | 2026 | 2027 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for spec in CFG["conferences"]:
        lines.append("| "+spec["name"]+" | "+" | ".join(str(conference_counts[(spec["name"],y)]) for y in CFG["years"])+" |")
    lines += ["","## IEEE Transactions network subset","",
              "| Year | Papers |","| --- | ---: |"]
    for y in CFG["years"]:
        lines.append(f"| {y} | {sum(n for (v,yy),n in tx_counts.items() if yy==y):,} |")
    lines += ["","## Keyword provenance","",
              "| Provenance | Rows |","| --- | ---: |"]
    for k,n in prov.most_common(): lines.append(f"| {k or 'missing'} | {n:,} |")
    lines += ["","## Network-project categories","",
              "| Category | Papers |","| --- | ---: |"]
    for k,n in cats.most_common(): lines.append(f"| {k} | {n:,} |")
    (DATA/"PAPER_CORPUS_SUMMARY.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    required=("title","authors","venue","year","keywords")
    bad=[r for r in master if any(not r.get(x) for x in required)]
    if bad: raise SystemExit(f"{len(bad)} master rows missing required metadata")
    print(f"ASSEMBLED conferences={len(conferences)} transactions={len(transactions)} master={len(master)} network={len(network)}")

if __name__=="__main__": main()
