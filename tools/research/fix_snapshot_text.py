#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from ftfy import fix_text

ROOT = Path(__file__).resolve().parents[2]

def clean_csv(path: Path) -> tuple[int,int]:
    with path.open("r", encoding="utf-8", newline="") as f:
        rows=list(csv.DictReader(f))
        fields=list(rows[0].keys()) if rows else []

    changed_rows=0
    changed_cells=0
    for row in rows:
        row_changed=False
        for k,v in list(row.items()):
            if v is None:
                continue
            fixed=fix_text(v)
            if fixed != v:
                row[k]=fixed
                changed_cells+=1
                row_changed=True
        if row_changed:
            changed_rows+=1

    if changed_rows:
        with path.open("w", encoding="utf-8", newline="") as f:
            w=csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
    return changed_rows, changed_cells

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    args=ap.parse_args()
    paths=[ROOT / p for p in args.paths] if args.paths else sorted((ROOT/"materials/assessments/data/venues").glob("*.csv"))
    total_rows=total_cells=0
    for path in paths:
        r,c=clean_csv(path)
        total_rows+=r; total_cells+=c
        print(f"{path.relative_to(ROOT)} changed_rows={r} changed_cells={c}")
    print(f"TOTAL changed_rows={total_rows} changed_cells={total_cells}")

if __name__=="__main__":
    main()
