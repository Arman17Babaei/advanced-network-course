#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/research"))

import build_paper_corpus as corpus

CFG = json.loads((ROOT / "tools/research/paper_corpus_config.json").read_text(encoding="utf-8"))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--venue", required=True)
    p.add_argument("--year", type=int, action="append")
    p.add_argument("--live", action="store_true", help="Validate the live provider instead of a frozen snapshot")
    args = p.parse_args()

    spec = next((x for x in CFG["conferences"] if x["name"] == args.venue), None)
    if not spec:
        raise SystemExit(f"Unknown venue: {args.venue}")

    allowed_years = set(spec.get("years", CFG["years"]))
    years = args.year or [
        y for y in CFG["years"]
        if y in allowed_years and 2023 <= y <= int(spec.get("validate_through", 2026))
    ]
    failures = []

    for year in years:
        rows, source_name = corpus.conference_rows_for(spec, year, force_live=args.live)
        provider = spec.get("live_provider") if args.live and spec.get("live_provider") else spec["provider"]

        for r in rows:
            corpus.categorize(r)

        n = len(rows)
        authors = sum(bool(r.get("authors")) for r in rows)
        links = sum(bool(r.get("doi") or r.get("url")) for r in rows)
        keywords = sum(bool(r.get("keywords")) for r in rows)
        min_count = int(spec["hard_min"])

        print(f"VENUE={args.venue} YEAR={year} PROVIDER={provider} SOURCE={source_name}")
        print(f"COUNT={n} AUTHORS={authors}/{n} LINKS={links}/{n} KEYWORDS={keywords}/{n}")
        print("SAMPLE:")
        for r in rows[:5]:
            print(f" - {r['title']} | {r['authors']} | {r.get('doi') or r.get('url')} | {r['keywords']}")

        if n < min_count:
            failures.append(f"{year}: count {n} < minimum {min_count}")
        if n and authors / n < 0.98:
            failures.append(f"{year}: author coverage {authors}/{n} < 98%")
        if n and links / n < 0.98:
            failures.append(f"{year}: DOI/URL coverage {links}/{n} < 98%")
        if n and keywords / n < 1.0:
            failures.append(f"{year}: keyword coverage {keywords}/{n} < 100% after fallback")

    if failures:
        print("VALIDATION FAILED", file=sys.stderr)
        for f in failures:
            print(" - " + f, file=sys.stderr)
        raise SystemExit(2)

    print("VALIDATION PASSED")

if __name__ == "__main__":
    main()
