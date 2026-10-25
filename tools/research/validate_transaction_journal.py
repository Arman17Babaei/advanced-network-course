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
    # Internet / packet networking
    "networking", "computer network", "communication network", "mobile network",
    "edge network", "data center network", "datacenter network", "cluster network",
    "network traffic", "network resource", "network slicing", "network telemetry",
    "network measurement", "network management", "network function", "network security",
    "network protocol", "network topology", "network planning", "network coding",
    "routing", "router", "internet", "packet", "packet scheduling", "switch",
    "transport layer", "transport protocol", "congestion control", "tcp", "quic",
    "rdma", "roce", "bgp", "dns", "ipv6", "cdn", "traffic engineering", "sdn",
    "software-defined network", "nfv", "service function", "content delivery",
    "peer-to-peer", "p2p", "interconnect", "collective communication",
    "all-reduce", "all-to-all", "coflow", "bandwidth allocation",

    # Wireless/mobile networking. Avoid bare "wireless", "5g", "6g", or
    # "network" because those admit physical-layer and neural-network papers.
    "wireless network", "wireless communication", "wireless link", "wi-fi", "wifi",
    "wlan", "cellular network", "5g network", "6g network", "radio access network",
    "ran", "handover", "satellite network", "satellite communication",
    "leo network", "non-terrestrial network", "ntn", "vehicular network", "v2x",
    "device-to-device communication", "d2d", "mesh network", "ad hoc network",
    "sensor network", "lpwan", "lora", "spectrum allocation", "channel access",
    "medium access", "mac protocol",

    # Networked/distributed systems
    "task offloading", "computation offloading", "mobile edge computing",
    "multi-access edge computing", "edge-cloud", "cloud-edge",
    "communication-efficient", "communication overhead", "communication scheduling",
    "semantic communication",
]
def _has_term(blob, term):
    # Require lexical boundaries so short acronyms such as RAN do not match
    # unrelated words such as "transfer".
    return re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", blob) is not None


def is_network_paper(r):
    # Broad Transactions journals contain sensing, ML, signal-processing and
    # device papers alongside networking. Restrict inclusion to explicit
    # network/system signals in the paper title and paper-level keywords.
    # OpenAlex topic labels remain available later for categorization.
    blob = " ".join([
        str(r.get("title") or ""),
        str(r.get("keywords") or ""),
    ])
    return any(corpus.phrase_present(blob, term) for term in NETWORK_TERMS)


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
