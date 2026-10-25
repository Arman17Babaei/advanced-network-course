#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/research"))
import build_paper_corpus as corpus

CFG=json.loads((ROOT/"tools/research/paper_corpus_config.json").read_text(encoding="utf-8"))
TX=CFG["ieee_transactions"]

STRONG_NETWORK_TERMS = [
    # Packet / Internet / transport / network control.
    "computer network", "networking", "network traffic", "network resource",
    "network slicing", "network telemetry", "network measurement",
    "network management", "network function", "network security",
    "network protocol", "network planning", "routing", "router",
    "packet scheduling", "packet network", "transport protocol", "transport layer",
    "congestion control", "tcp", "quic", "rdma", "roce", "bgp", "dns", "ipv6",
    "content delivery network", "cdn", "traffic engineering",
    "software-defined network", "sdn", "network function virtualization", "nfv",
    "service function chain", "network service", "peer-to-peer", "p2p",
    "network interconnect", "collective communication", "all-reduce", "all-to-all",
    "coflow",

    # Wireless/mobile network architecture and control. Deliberately avoid
    # bare "wireless", "wifi", "5g", "6g", "internet", "bandwidth allocation",
    # and "spectrum allocation": those admit sensing and PHY-only papers.
    "wireless network", "cellular network", "5g network", "6g network",
    "radio access network", "ran", "handover", "satellite network",
    "non-terrestrial network", "ntn", "vehicular network", "vehicular ad hoc network",
    "v2x", "vehicle-to-everything", "device-to-device network", "mesh network",
    "ad hoc network", "sensor network", "lpwan", "lora network",
    "channel access", "medium access", "mac protocol",

    # Networked/distributed systems where communication placement/control is
    # part of the system design rather than incidental.
    "task offloading", "computation offloading", "mobile edge computing",
    "multi-access edge computing", "vehicular edge computing", "edge-cloud",
    "cloud-edge", "communication scheduling", "communication overhead",
]

WEAK_NETWORK_TERMS = [
    "wifi", "wi-fi", "wireless communication", "5g", "6g",
    "device-to-device communication", "semantic communication",
    "edge computing", "internet of things", "iot", "bandwidth allocation",
    "spectrum allocation",
]

SYSTEM_CONTEXT_TERMS = [
    "network", "routing", "traffic", "transport", "packet", "latency", "throughput",
    "quality of service", "qos", "handover", "offloading", "edge", "cloud",
    "resource allocation", "scheduling", "congestion", "service", "protocol",
    "topology", "link", "base station", "access point", "roadside unit",
]

NON_NETWORK_DOMINANT_TERMS = [
    "antenna", "beamforming", "channel estimation", "channel modeling",
    "channel model", "modulation", "waveform", "radar", "localization",
    "object detection", "image reconstruction", "activity recognition",
    "gesture recognition", "handwriting recognition", "brain network",
    "protein network", "social network analysis", "power grid",
]

def _contains(blob, term):
    return corpus.phrase_present(blob, term)

def is_network_paper(r):
    # High-precision course filter.  The journal may be about mobility,
    # communications, graph/network science, security, multimedia, or cloud
    # systems; retain a paper only when its title/keywords make a network
    # architecture, protocol, transport, routing, network-control, or
    # communication-placement problem explicit.
    title = str(r.get("title") or "")
    keywords = str(r.get("keywords") or "")
    blob = f"{title} {keywords}"

    strong = [t for t in STRONG_NETWORK_TERMS if _contains(blob, t)]
    if strong:
        return True

    weak = [t for t in WEAK_NETWORK_TERMS if _contains(blob, t)]
    context = [t for t in SYSTEM_CONTEXT_TERMS if _contains(blob, t)]
    if len(weak) >= 1 and len(context) >= 2:
        # Guard against common sensing/PHY cases where Wi-Fi/wireless/5G is
        # merely the measurement substrate rather than the networking object.
        dominant = [t for t in NON_NETWORK_DOMINANT_TERMS if _contains(blob, t)]
        if dominant and len(context) < 3:
            return False
        return True

    return False

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
