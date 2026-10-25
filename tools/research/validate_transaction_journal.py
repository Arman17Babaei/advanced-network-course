#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))
import build_paper_corpus as corpus

CFG=json.loads((ROOT/"tools/research/paper_corpus_config.json").read_text(encoding="utf-8"))
TX=CFG["ieee_transactions"]

NETWORK_TERMS = [
    "network", "networking", "routing", "router", "internet", "packet", "switch",
    "transport", "congestion", "tcp", "quic", "rdma", "roce", "bgp", "dns",
    "ipv6", "cdn", "wireless", "wi-fi", "wifi", "wlan", "cellular", "5g", "6g",
    "radio access", "ran", "handover", "network slicing", "satellite", "leo",
    "non-terrestrial", "ntn", "vehicular network", "v2x", "device-to-device",
    "d2d", "mesh network", "ad hoc network", "sensor network", "lpwan", "lora",
    "communication network", "network traffic", "traffic engineering", "sdn",
    "software-defined network", "network function", "nfv", "service function",
    "content delivery", "peer-to-peer", "p2p", "network telemetry",
    "network measurement", "interconnect", "collective communication",
    "all-reduce", "all-to-all", "coflow", "bandwidth allocation",
]

def is_network_paper(r):
    subfields = set(r.get("_topic_subfields") or [])
    if r.get("_primary_subfield"):
        subfields.add(r["_primary_subfield"])
    if "Computer Networks and Communications" in subfields:
        return True
    blob = " ".join([
        str(r.get("title") or ""),
        str(r.get("keywords") or ""),
        str(r.get("topics") or ""),
        str(r.get("primary_topic") or ""),
    ]).lower()
    return any(term in blob for term in NETWORK_TERMS)

def rows_for(spec, year):
    source_ids = spec.get("source_ids_by_year", {}).get(str(year)) or ([spec["source_id"]] if spec.get("source_id") else [])
    venue_name = spec.get("canonical_name") or spec["name"]
    rows=corpus.collect_works(source_ids, year, venue_override=venue_name, kind="journal", core=False)
    rows=corpus.dedupe(rows)
    # Journal metadata may include front matter; research-paper inventory requires authors.
    rows=[r for r in rows if r.get("authors")]
    for r in rows:
        corpus.categorize(r)
        if spec.get("relevance_mode")=="all":
            r["network_relevant"]=True
            r["network_relevance_score"]=max(2,int(r.get("network_relevance_score") or 0))
    if spec.get("relevance_mode")=="filter":
        rows=[r for r in rows if is_network_paper(r)]
        for r in rows:
            r["network_relevant"]=True
            r["network_relevance_score"]=max(2,int(r.get("network_relevance_score") or 0))
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
        min_count = int(spec.get("hard_min_by_year", {}).get(str(year), spec.get("hard_min",1)))
        if 2023 <= year <= int(spec.get("validate_through",2026)) and n < min_count:
            failures.append(f"{year}: count {n} < minimum {min_count}")
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
