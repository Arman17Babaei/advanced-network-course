#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CFG=json.loads((ROOT/"tools/research/paper_corpus_config.json").read_text(encoding="utf-8"))
DATA=ROOT/"materials/assessments/data"

INPUT_FIELDS=[
    "title","authors","venue","raw_venue","year","venue_kind","source_id","doi","url","openalex_id",
    "metadata_source","paper_type","keywords","keyword_provenance","topics","primary_topic",
    "categories","network_relevance_score","network_relevant",
]
OUTPUT_FIELDS=INPUT_FIELDS+["source_index_terms","derived_keywords"]

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
    if doi:
        return ("doi",doi)
    title=re.sub(r"[^a-z0-9]+"," ",(r.get("title") or "").lower()).strip()
    return ("title",title,int(r["year"]),r.get("venue") or "")

def dedupe(rows):
    out={}
    for r in rows:
        k=key(r)
        if k not in out:
            out[k]=r
        else:
            score=lambda x:sum(bool(x.get(f)) for f in ("authors","keywords","doi","url","openalex_id","topics"))
            if score(r)>score(out[k]):
                out[k]=r
    return sorted(out.values(),key=lambda r:(int(r["year"]),str(r["venue"]).lower(),str(r["title"]).lower()))

def keyword_columns(r):
    kw=str(r.get("keywords") or "")
    prov=str(r.get("keyword_provenance") or "").lower()
    source_markers=("publisher metadata","publisher-provided","crossref subject","author keyword","index term")
    if any(x in prov for x in source_markers):
        return kw,""
    return "",kw

def output_row(r):
    out={k:r.get(k,"") for k in INPUT_FIELDS}
    source_terms,derived=keyword_columns(r)
    out["source_index_terms"]=source_terms
    out["derived_keywords"]=derived
    return out

def write(path,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=OUTPUT_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(output_row(r))

def validate(rows,label):
    bad=[]
    for i,r in enumerate(rows,start=2):
        for field in ("title","authors","venue","year","keywords","keyword_provenance"):
            if not r.get(field):
                bad.append(f"{label}:{i}: missing {field}")
        if not (2023 <= int(r.get("year") or 0) <= 2027):
            bad.append(f"{label}:{i}: year outside 2023-2027")
    return bad

def main():
    conferences=[]
    coverage=[]
    failures=[]
    frozen_specs=[s for s in CFG["conferences"] if s.get("snapshot")]
    for spec in frozen_specs:
        snap=spec["snapshot"]
        path=ROOT/snap
        if not path.exists():
            failures.append(f"missing venue snapshot: {snap}")
            continue
        rows=read_csv(path)
        failures.extend(validate(rows,snap))
        conferences.extend(rows)
        by_year=Counter(r["year"] for r in rows)
        for y in CFG["years"]:
            coverage.append({
                "venue":spec["name"],"kind":"conference","year":y,
                "records":by_year[y],"source":snap,
            })

    conferences=dedupe(conferences)
    conference_venues={r["venue"] for r in conferences}
    if len(conference_venues)<15:
        failures.append(f"only {len(conference_venues)} conference venues in frozen corpus; expected at least 15")

    tx_path=DATA/"transactions/ieee_transactions_network.csv"
    if not tx_path.exists():
        failures.append(f"missing {tx_path.relative_to(ROOT)}")
        transactions=[]
    else:
        transactions=dedupe(read_csv(tx_path))
        failures.extend(validate(transactions,str(tx_path.relative_to(ROOT))))
        if len(transactions)<1500:
            failures.append(f"Transactions-wide network subset too small: {len(transactions)} < 1500")
        tx_by_vy=Counter((r["venue"],r["year"]) for r in transactions)
        for (venue,year),n in sorted(tx_by_vy.items()):
            coverage.append({
                "venue":venue,"kind":"journal","year":year,
                "records":n,"source":"transactions/ieee_transactions_network.csv",
            })

    master=dedupe(conferences+transactions)
    network=dedupe([r for r in conferences if r["network_relevant"]]+transactions)

    if failures:
        print("ASSEMBLY VALIDATION FAILED")
        for x in failures[:100]:
            print(" -",x)
        if len(failures)>100:
            print(f" - ... {len(failures)-100} additional failures")
        raise SystemExit(2)

    for name,rows in [
        ("all_conference_papers.csv",conferences),
        ("ieee_transactions_network.csv",transactions),
        ("master_paper_corpus.csv",master),
        ("recent_networking_papers.csv",network),
    ]:
        write(DATA/name,rows)

    with (DATA/"PAPER_CORPUS_COVERAGE.csv").open("w",encoding="utf-8",newline="") as f:
        fields=["venue","kind","year","records","source"]
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(coverage,key=lambda r:(r["kind"],r["venue"].lower(),r["year"])))

    prov=Counter(r["keyword_provenance"] for r in master)
    cats=Counter()
    for r in network:
        for cat in str(r.get("categories") or "").split("; "):
            if cat and cat!="Other / adjacent":
                cats[cat]+=1
    conference_counts=Counter((r["venue"],r["year"]) for r in conferences)
    tx_counts=Counter((r["venue"],r["year"]) for r in transactions)
    tx_journals=Counter(r["venue"] for r in transactions)

    lines=[
        "# Paper Corpus Summary","",
        f"Conference papers: **{len(conferences):,}** across **{len(conference_venues)}** requested venues.",
        f"Network-relevant IEEE Transactions papers: **{len(transactions):,}** across **{len(tx_journals)}** Transactions journals.",
        f"Master corpus rows: **{len(master):,}**.",
        f"Network-relevant analysis rows: **{len(network):,}**.","",
        "## Conference coverage","",
        "| Venue | 2023 | 2024 | 2025 | 2026 | 2027 | Total |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for spec in frozen_specs:
        vals=[conference_counts[(spec["name"],y)] for y in CFG["years"]]
        lines.append("| "+spec["name"]+" | "+" | ".join(f"{x:,}" for x in vals)+f" | {sum(vals):,} |")

    lines += ["","## IEEE Transactions networking subset","",
              "TON and TNSM research papers are retained in full. Other Transactions papers must pass the high-precision network-systems relevance filter.","",
              "| Journal | Retained papers |","| --- | ---: |"]
    for venue,n in tx_journals.most_common():
        lines.append(f"| {venue} | {n:,} |")

    lines += ["","### Transactions by year","",
              "| Year | Papers |","| --- | ---: |"]
    for y in CFG["years"]:
        lines.append(f"| {y} | {sum(n for (v,yy),n in tx_counts.items() if yy==y):,} |")

    lines += ["","## Keyword provenance","",
              "The output keeps the original keywords field and its provenance. source_index_terms is populated only when the source exposes publisher/index metadata; derived_keywords contains model-generated or deterministic inferred labels. Inferred labels are never presented as author keywords.","",
              "| Provenance | Rows |","| --- | ---: |"]
    for k,n in prov.most_common():
        lines.append(f"| {k or 'missing'} | {n:,} |")

    lines += ["","## Network-project categories","",
              "| Category | Papers |","| --- | ---: |"]
    for k,n in cats.most_common():
        lines.append(f"| {k} | {n:,} |")

    lines += ["","## Scope notes","",
              "- The requested window is 2023–2027. 2027 remains empty where no official/publisher paper metadata is available yet.",
              "- Conference data is read only from frozen, individually validated venue snapshots.",
              "- The Transactions-wide file scans matching IEEE/ACM Transactions journal titles and retains only networking-systems papers, except TON/TNSM as noted above.",
              "- The master corpus can therefore be regenerated without re-querying conference endpoints.",
    ]
    (DATA/"PAPER_CORPUS_SUMMARY.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    print(f"ASSEMBLED conferences={len(conferences)} venues={len(conference_venues)} transactions={len(transactions)} journals={len(tx_journals)} master={len(master)} network={len(network)}")
    print("ASSEMBLY VALIDATION PASSED")

if __name__=="__main__":
    main()
