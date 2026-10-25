#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CFG = json.loads((ROOT / "tools/research/paper_corpus_config.json").read_text(encoding="utf-8"))
DATA = ROOT / "materials/assessments/data"
VENUES = DATA / "venues"
TX = DATA / "transactions"

REQUIRED = [
    "title","authors","venue","year","keywords","keyword_provenance",
    "url","doi","categories","network_relevant"
]

MASTER_FIELDS = [
    "title","authors","venue","year","venue_kind","doi","url",
    "keywords","keyword_provenance","topics","primary_topic",
    "categories","network_relevance_score","network_relevant",
    "metadata_source","paper_type","source_id","openalex_id","raw_venue",
    "corpus_source"
]

def read_csv(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        rows=list(csv.DictReader(f))
    if not rows:
        raise RuntimeError(f"{path}: no data rows")
    missing=[x for x in REQUIRED if x not in rows[0]]
    if missing:
        raise RuntimeError(f"{path}: missing columns {missing}")
    return rows

def write_csv(path: Path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f, fieldnames=MASTER_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k:r.get(k,"") for k in MASTER_FIELDS})

def norm_key(r):
    doi=(r.get("doi") or "").lower().strip()
    if doi:
        return ("doi",doi)
    title=re.sub(r"[^a-z0-9]+"," ",(r.get("title") or "").lower()).strip()
    return ("title",title,(r.get("venue") or "").lower(),str(r.get("year") or ""))

def validate_rows(path, rows):
    failures=[]
    for i,r in enumerate(rows,2):
        for field in ("title","authors","venue","year","keywords"):
            if not (r.get(field) or "").strip():
                failures.append(f"{path}:{i}: missing {field}")
        year=str(r.get("year") or "")
        if year not in {"2023","2024","2025","2026","2027"}:
            failures.append(f"{path}:{i}: year {year!r} outside corpus window")
        if not ((r.get("doi") or "").strip() or (r.get("url") or "").strip()):
            failures.append(f"{path}:{i}: missing DOI/URL")
    return failures

def main():
    failures=[]
    conference_rows=[]
    venue_counts=Counter()
    conference_specs={s["name"]:s for s in CFG["conferences"]}

    for name,spec in conference_specs.items():
        snap=spec.get("snapshot")
        if not snap:
            failures.append(f"{name}: no frozen snapshot configured")
            continue
        path=ROOT/snap
        if not path.exists():
            failures.append(f"{name}: missing snapshot {snap}")
            continue
        rows=read_csv(path)
        failures.extend(validate_rows(snap, rows))
        for r in rows:
            r["corpus_source"]="conference_snapshot"
            conference_rows.append(r)
            venue_counts[(name,int(r["year"]))]+=1

        allowed=set(spec.get("years",CFG["years"]))
        end=int(spec.get("validate_through",2026))
        for year in CFG["years"]:
            if year not in allowed or year>min(end,2026):
                continue
            n=venue_counts[(name,year)]
            if n<int(spec["hard_min"]):
                failures.append(f"{name} {year}: {n} < hard minimum {spec['hard_min']}")
        for ys,expected in spec.get("expected_counts",{}).items():
            y=int(ys); n=venue_counts[(name,y)]
            if n!=int(expected):
                failures.append(f"{name} {y}: {n} != expected {expected}")

    tx_rows=[]
    broad_tx=TX/"ieee_transactions_network.csv"
    if broad_tx.exists() and broad_tx.stat().st_size>100:
        # Prefer the Transactions-wide discovery sweep when available. It
        # scans every matching IEEE(/ACM) Transactions journal title and
        # retains only papers that pass the same high-precision network filter.
        tx_files=[broad_tx]
        tx_source="ieee_transactions_wide_network_subset"
    else:
        # Safe fallback while a broad sweep is unavailable/rate-limited:
        # combine the individually validated networking journal snapshots.
        tx_files=sorted(p for p in TX.glob("ieee_transactions_*.csv") if p.name != "ieee_transactions_network.csv")
        tx_source="ieee_transactions_validated_journal_subset"

    if not tx_files:
        failures.append("no Transactions snapshots found")
    for path in tx_files:
        rows=read_csv(path)
        failures.extend(validate_rows(str(path.relative_to(ROOT)),rows))
        for r in rows:
            if str(r.get("network_relevant","")).lower() not in {"true","1","yes"}:
                failures.append(f"{path.name}: non-network row retained: {r.get('title')}")
            r["corpus_source"]=tx_source
            tx_rows.append(r)

    # Keep one record per publication identity within the combined corpus.
    combined=[]
    seen=set()
    for r in conference_rows+tx_rows:
        k=norm_key(r)
        if k in seen:
            continue
        seen.add(k)
        combined.append(r)

    conference_rows.sort(key=lambda r:(int(r["year"]),r["venue"].lower(),r["title"].lower()))
    tx_rows.sort(key=lambda r:(int(r["year"]),r["venue"].lower(),r["title"].lower()))
    combined.sort(key=lambda r:(int(r["year"]),r["venue"].lower(),r["title"].lower()))

    if failures:
        print("VALIDATION FAILED",file=sys.stderr)
        for x in failures[:200]:
            print(" - "+x,file=sys.stderr)
        if len(failures)>200:
            print(f" - ... {len(failures)-200} more",file=sys.stderr)
        raise SystemExit(2)

    write_csv(DATA/"all_conference_papers.csv",conference_rows)
    write_csv(DATA/"ieee_transactions_network.csv",tx_rows)
    write_csv(DATA/"recent_networking_papers.csv",combined)

    # Coverage table.
    with (DATA/"PAPER_CORPUS_COVERAGE.csv").open("w",encoding="utf-8",newline="") as f:
        fields=["venue","year","records","kind"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for name in conference_specs:
            for year in CFG["years"]:
                w.writerow({"venue":name,"year":year,"records":venue_counts[(name,year)],"kind":"conference"})
        tx_counts=Counter((r["venue"],int(r["year"])) for r in tx_rows)
        for venue in sorted({r["venue"] for r in tx_rows}):
            for year in CFG["years"]:
                w.writerow({"venue":venue,"year":year,"records":tx_counts[(venue,year)],"kind":"journal-network-subset"})

    # Summary.
    tx_counts=Counter((r["venue"],int(r["year"])) for r in tx_rows)
    keyword_prov=Counter(r.get("keyword_provenance","") or "missing" for r in combined)
    cat_counts=Counter()
    for r in combined:
        for c in (r.get("categories") or "").split("; "):
            if c:
                cat_counts[c]+=1

    lines=[
        "# Paper Corpus Summary","",
        f"Conference papers: **{len(conference_rows):,}**.",
        f"Networking-relevant IEEE Transactions papers: **{len(tx_rows):,}**.",
        f"Combined unique records: **{len(combined):,}**.","",
        "## Conference coverage","",
        "| Venue | 2023 | 2024 | 2025 | 2026 | 2027 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name in conference_specs:
        lines.append("| "+name+" | "+" | ".join(str(venue_counts[(name,y)]) for y in CFG["years"])+" |")
    lines += ["","## Networking Transactions coverage","",
              "| Journal | 2023 | 2024 | 2025 | 2026 | 2027 |",
              "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for venue in sorted({r["venue"] for r in tx_rows}):
        lines.append("| "+venue+" | "+" | ".join(str(tx_counts[(venue,y)]) for y in CFG["years"])+" |")

    lines += ["","## Keyword provenance","",
              "| Provenance | Records |","| --- | ---: |"]
    for p,n in keyword_prov.most_common():
        lines.append(f"| {p} | {n:,} |")

    lines += ["","## Category counts","",
              "| Category | Records |","| --- | ---: |"]
    for c,n in cat_counts.most_common():
        lines.append(f"| {c} | {n:,} |")

    lines += ["","## Invariants","",
              "- Every conference row has title, authors, venue, year, keyword metadata, and a DOI or canonical URL.",
              "- Conference snapshots satisfy their configured per-year minimums; exact expected counts are enforced where known.",
              "- IEEE Transactions inputs are networking-only subsets; the assembler prefers the Transactions-wide filtered sweep when available and otherwise falls back to individually validated journal snapshots.",
              "- Keyword provenance is explicit; inferred keywords are not represented as publisher/author keywords.",
              "- 2027 is populated only when records already exist in the source metadata.",
              ""]
    (DATA/"PAPER_CORPUS_SUMMARY.md").write_text("\n".join(lines),encoding="utf-8")
    print(f"VALIDATED conference={len(conference_rows)} transactions={len(tx_rows)} combined={len(combined)}")
    print("WROTE materials/assessments/data/recent_networking_papers.csv")

if __name__=="__main__":
    main()
