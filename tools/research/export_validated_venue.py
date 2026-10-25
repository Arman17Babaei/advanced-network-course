#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/research"))

import build_paper_corpus as corpus

CFG = json.loads((ROOT / "tools/research/paper_corpus_config.json").read_text(encoding="utf-8"))
OUT = ROOT / "materials/assessments/data/venues"
OUT.mkdir(parents=True, exist_ok=True)

FIELDS = corpus.FIELDS

def rows_for(spec, year):
    rows, _ = corpus.conference_rows_for(spec, year, force_live=True)
    return rows

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--venue", required=True)
    args = p.parse_args()

    spec = next((x for x in CFG["conferences"] if x["name"] == args.venue), None)
    if not spec:
        raise SystemExit(f"Unknown venue: {args.venue}")

    years = [y for y in CFG["years"] if y in set(spec.get("years", CFG["years"])) and y <= int(spec.get("validate_through", 2026))]
    rows = []
    for year in years:
        yr = rows_for(spec, year)
        for r in yr:
            corpus.categorize(r)
        if len(yr) < int(spec["hard_min"]):
            raise SystemExit(f"{args.venue} {year}: only {len(yr)} rows")
        rows.extend(yr)

    rows = corpus.dedupe(rows)
    slug = corpus.slug(args.venue).replace("-", "_")
    path = OUT / f"{slug}.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(corpus.public_row(r))

    print(f"WROTE {len(rows)} rows to {path.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
