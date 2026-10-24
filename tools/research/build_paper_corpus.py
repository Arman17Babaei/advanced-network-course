#!/usr/bin/env python3
from __future__ import annotations

import csv
import gzip
import html
import json
import math
import re
import sys
import time
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
CFG = json.loads((ROOT / "tools/research/paper_corpus_config.json").read_text(encoding="utf-8"))
OUT = ROOT / "materials/assessments/data"
OUT.mkdir(parents=True, exist_ok=True)
YEARS = CFG["years"]
CONFERENCES = CFG["conferences"]
CATEGORIES = CFG["categories"]
TX_CFG = CFG["ieee_transactions"]

S = requests.Session()
S.headers.update({
    "User-Agent": "advanced-network-course-paper-corpus/2.0 (+https://github.com/Arman17Babaei/advanced-network-course)",
    "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
})
OPENALEX = "https://api.openalex.org"
STOP = {
    "the","and","for","with","from","into","using","via","towards","toward","based",
    "system","systems","framework","method","approach","efficient","effective","new",
    "this","that","over","under","through","without","between","across","their","our",
    "study","analysis","design","paper","performance",
}

def norm(x):
    return re.sub(r"\s+", " ", html.unescape(str(x or ""))).strip()

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", norm(s).lower()).strip("-")

def get_json(url, params=None, attempts=5, pause=1.0):
    err = None
    for i in range(attempts):
        try:
            r = S.get(url, params=params, timeout=45)
            if r.status_code in {429, 500, 502, 503, 504}:
                time.sleep(max(2.0, pause * (2 ** i)))
                continue
            r.raise_for_status()
            return r.json()
        except Exception as e:
            err = e
            time.sleep(pause * (i + 1))
    raise RuntimeError(f"request failed: {url}: {err}")

def get_html(url, attempts=4):
    err = None
    for i in range(attempts):
        try:
            r = S.get(url, timeout=45, headers={"Accept":"text/html,*/*;q=0.8"})
            if r.status_code in {429, 500, 502, 503, 504}:
                time.sleep(2 ** i)
                continue
            r.raise_for_status()
            return r.text
        except Exception as e:
            err = e
            time.sleep(i + 1)
    raise RuntimeError(f"request failed: {url}: {err}")

def oa_list(endpoint, params, max_pages=None):
    # Basic page-based pagination is intentionally used instead of cursor
    # pagination: OpenAlex requires an API key after the first cursor page.
    # Each query here is scoped to one venue/year or journal/year and remains
    # safely below the 10,000-result basic-paging ceiling.
    page = 1
    per_page = 100
    while True:
        p = dict(params)
        p["per-page"] = per_page
        p["page"] = page
        data = get_json(f"{OPENALEX}/{endpoint}", p)
        results = data.get("results", []) or []
        for item in results:
            yield item
        meta = data.get("meta") or {}
        total = int(meta.get("count") or 0)
        if not results or page * per_page >= total:
            break
        page += 1
        if max_pages and page > max_pages:
            break
        if page * per_page > 10000:
            raise RuntimeError(f"basic paging limit exceeded for {endpoint}; split the query more narrowly")
        time.sleep(0.08)

def discover_conference_sources(spec):
    rx = re.compile(spec["source_regex"])
    candidates = {}
    for q in spec.get("search", []):
        for s in oa_list("sources", {
            "search": q,
            "select": "id,display_name,type,works_count,issn_l,host_organization_name",
        }, max_pages=2):
            name = norm(s.get("display_name"))
            if not name or not rx.search(name):
                continue
            sid = norm(s.get("id"))
            typ = norm(s.get("type"))
            score = 0
            if typ == "conference":
                score += 1000
            if q.lower() in name.lower():
                score += 200
            score += min(100, int(math.log10(max(1, int(s.get("works_count") or 1))) * 20))
            old = candidates.get(sid)
            if old is None or score > old["_score"]:
                x = dict(s)
                x["_score"] = score
                candidates[sid] = x
    ordered = sorted(candidates.values(), key=lambda x: (-x["_score"], -int(x.get("works_count") or 0), norm(x.get("display_name"))))
    picked = ordered[:int(spec.get("max_sources", 1))]
    print(f"SOURCES {spec['name']}: " + " | ".join(f"{x.get('display_name')} [{x.get('type')}] {x.get('id')}" for x in picked), flush=True)
    return picked

def discover_ieee_transactions_sources():
    rx = re.compile(TX_CFG["include_regex"])
    found = {}
    for s in oa_list("sources", {
        "search": TX_CFG["source_search"],
        "select": "id,display_name,type,works_count,issn_l,host_organization_name",
    }, max_pages=4):
        name = norm(s.get("display_name"))
        if norm(s.get("type")) != TX_CFG.get("source_type", "journal"):
            continue
        if not rx.search(name):
            continue
        found[norm(s["id"])] = s
    out = sorted(found.values(), key=lambda x: norm(x.get("display_name")).lower())
    print(f"IEEE Transactions sources matched: {len(out)}", flush=True)
    for x in out:
        print(f"  {x.get('display_name')} | {x.get('id')} | works={x.get('works_count')}", flush=True)
    return out

def work_row(w, venue_override=None, kind=None, core=False, metadata_source="OpenAlex"):
    source = ((w.get("primary_location") or {}).get("source") or {})
    raw_venue = norm(source.get("display_name"))
    venue = venue_override or raw_venue
    authors = []
    for a in w.get("authorships") or []:
        name = norm((a.get("author") or {}).get("display_name"))
        if name:
            authors.append(name)
    doi = norm(w.get("doi")).lower().replace("https://doi.org/", "")
    kws = sorted(
        [(norm(x.get("display_name")), float(x.get("score") or 0)) for x in (w.get("keywords") or []) if norm(x.get("display_name"))],
        key=lambda x: -x[1],
    )
    topics = [norm(x.get("display_name")) for x in (w.get("topics") or []) if norm(x.get("display_name"))]
    primary = norm((w.get("primary_topic") or {}).get("display_name"))
    landing = norm((w.get("primary_location") or {}).get("landing_page_url"))
    return {
        "title": norm(w.get("display_name")).rstrip("."),
        "authors": "; ".join(authors),
        "venue": venue,
        "raw_venue": raw_venue,
        "year": int(w.get("publication_year") or 0),
        "venue_kind": kind or norm(source.get("type")) or "unknown",
        "source_id": norm(source.get("id")),
        "doi": doi,
        "url": landing or (f"https://doi.org/{doi}" if doi else norm(w.get("id"))),
        "openalex_id": norm(w.get("id")),
        "metadata_source": metadata_source,
        "paper_type": norm(w.get("type")),
        "keywords": "; ".join(x[0] for x in kws[:10]),
        "keyword_provenance": "OpenAlex model-generated keywords" if kws else "",
        "topics": "; ".join(topics[:3]),
        "primary_topic": primary,
        "categories": "",
        "network_relevance_score": 0,
        "network_relevant": False,
        "_core": bool(core),
    }

def collect_works(source_ids, year, venue_override=None, kind=None, core=False):
    if not source_ids:
        return []
    rows = []
    for i in range(0, len(source_ids), 50):
        chunk = source_ids[i:i+50]
        filt = f"primary_location.source.id:{'|'.join(chunk)},publication_year:{year}"
        for w in oa_list("works", {
            "filter": filt,
            "select": "id,doi,display_name,publication_year,type,authorships,primary_location,keywords,topics,primary_topic",
        }):
            rows.append(work_row(w, venue_override=venue_override, kind=kind, core=core))
    return rows

def nines_2026(spec):
    url = spec["official_2026"]
    soup = BeautifulSoup(get_html(url), "html.parser")
    rows = []
    for li in soup.find_all("li"):
        a = li.find("a")
        if not a:
            continue
        label = norm(a.get_text(" ", strip=True)).rstrip(".")
        if not label or label.lower() in {"home","papers","talk","contributed talks","recorded stream","recorded pods","cfp","faq","sop","organizers"}:
            continue
        href = urljoin(url, a.get("href") or "")
        txt = norm(li.get_text(" ", strip=True))
        rest = txt[len(norm(a.get_text(" ", strip=True))):].lstrip(". ")
        rest = re.sub(r"\s+Talk\s*$", "", rest)
        rest = re.sub(r"\s*\([^)]*\)", "", rest).replace("∗", "").replace("*", "")
        authors = "; ".join(norm(x) for x in rest.split(",") if norm(x))
        rows.append({
            "title": label, "authors": authors, "venue": "NINeS", "raw_venue": "NINeS",
            "year": 2026, "venue_kind": "conference", "source_id": "", "doi": "", "url": href,
            "openalex_id": "", "metadata_source": "official accepted-paper page", "paper_type": "conference paper",
            "keywords": "", "keyword_provenance": "", "topics": "", "primary_topic": "",
            "categories": "", "network_relevance_score": 0, "network_relevant": False, "_core": True,
        })
    return rows

def title_fallback(title, limit=8):
    low = title.lower()
    domain = sorted({p for phrases in CATEGORIES.values() for p in phrases}, key=len, reverse=True)
    out = []
    for p in domain:
        if p in low and p not in out:
            out.append(p)
        if len(out) >= limit:
            return out
    toks = [x for x in re.findall(r"[a-z0-9][a-z0-9+.-]*", low) if len(x) > 2 and x not in STOP and not x.isdigit()]
    for a, b in zip(toks, toks[1:]):
        p = f"{a} {b}"
        if p not in out:
            out.append(p)
        if len(out) >= limit:
            return out
    for x in toks:
        if x not in out:
            out.append(x)
        if len(out) >= limit:
            break
    return out

def categorize(r):
    if not r["keywords"]:
        r["keywords"] = "; ".join(title_fallback(r["title"]))
        r["keyword_provenance"] = "deterministic title-derived fallback"
    blob = " ".join((r["title"], r["keywords"], r["topics"], r["primary_topic"])).lower()
    title = r["title"].lower()
    scored = []
    for cat, phrases in CATEGORIES.items():
        score = sum(3 if p in title else 1 for p in phrases if p in blob)
        if score:
            scored.append((score, cat))
    scored.sort(key=lambda x: (-x[0], x[1]))
    r["categories"] = "; ".join(x[1] for x in scored[:3]) if scored else "Other / adjacent"
    lexical = scored[0][0] if scored else 0
    prior = 2 if r.get("_core") else 0
    r["network_relevance_score"] = min(10, prior + lexical)
    r["network_relevant"] = bool(r.get("_core") or lexical >= 2)

def dedupe(rows):
    kept = {}
    for r in rows:
        key = ("doi", r["doi"]) if r.get("doi") else ("title", slug(r["title"]), r["year"], r["venue"])
        if key not in kept:
            kept[key] = r
            continue
        old = kept[key]
        score_old = sum(bool(old.get(f)) for f in ("authors","keywords","doi","source_id","openalex_id"))
        score_new = sum(bool(r.get(f)) for f in ("authors","keywords","doi","source_id","openalex_id"))
        if score_new > score_old:
            kept[key] = r
    return sorted(kept.values(), key=lambda r: (int(r["year"]), r["venue"].lower(), r["title"].lower()))

FIELDS = [
    "title","authors","venue","raw_venue","year","venue_kind","source_id","doi","url","openalex_id",
    "metadata_source","paper_type","keywords","keyword_provenance","topics","primary_topic",
    "categories","network_relevance_score","network_relevant",
]

def public_row(r):
    return {k:r.get(k,"") for k in FIELDS}

def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(public_row(r))

def write_gzip_csv(path, rows):
    with gzip.open(path, "wt", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(public_row(r))

def write_outputs(conference_rows, tx_rows, coverage, tx_sources):
    all_rows = dedupe(conference_rows + tx_rows)
    for r in all_rows:
        categorize(r)

    conference_names = {x["name"] for x in CONFERENCES}
    conferences = [r for r in all_rows if r["venue"] in conference_names]
    tx = [r for r in all_rows if r["venue"] not in conference_names and re.match(TX_CFG["include_regex"], r["venue"] or "")]
    network = [r for r in all_rows if r["network_relevant"]]

    write_csv(OUT / "all_conference_papers.csv", conferences)
    write_gzip_csv(OUT / "ieee_transactions_papers.csv.gz", tx)
    write_csv(OUT / "recent_networking_papers.csv", network)

    with (OUT / "PAPER_CORPUS_COVERAGE.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["venue","kind","year","records","status","source_ids","source_names"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(coverage)

    with (OUT / "IEEE_TRANSACTIONS_SOURCES.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["source_id","display_name","type","works_count","issn_l"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for s in tx_sources:
            w.writerow({k:s.get(k,"") for k in fields})

    by_vy = Counter((r["venue"], int(r["year"])) for r in conferences)
    prov = Counter(r["keyword_provenance"] for r in all_rows)
    cats = Counter()
    for r in network:
        for x in r["categories"].split("; "):
            if x:
                cats[x] += 1

    lines = [
        "# Paper Corpus Summary","",
        f"Conference records: **{len(conferences):,}**.",
        f"IEEE Transactions records: **{len(tx):,}** across **{len(tx_sources):,}** matching journal sources.",
        f"Network-relevant records used for project-area mining: **{len(network):,}**.","",
        "## Coverage by requested conference and year","",
        "| Venue | 2023 | 2024 | 2025 | 2026 | 2027 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for spec in CONFERENCES:
        lines.append("| " + spec["name"] + " | " + " | ".join(str(by_vy.get((spec["name"], y), 0)) for y in YEARS) + " |")
    lines += [
        "","## Keyword provenance","",
        "OpenAlex keywords are model-generated aboutness labels derived from a work's title, abstract, and venue. They are not represented as author-supplied keywords. Rows without OpenAlex keywords use an explicit deterministic title fallback.","",
        "| Provenance | Records |","| --- | ---: |",
    ]
    for k,n in prov.most_common():
        lines.append(f"| {k or 'missing'} | {n:,} |")
    lines += ["","## Network-relevant category counts","","| Category | Papers |","| --- | ---: |"]
    for k,n in cats.most_common():
        lines.append(f"| {k} | {n:,} |")
    lines += [
        "","## Validation","",
        "The build fails before committing generated files when an established 2023–2026 conference venue returns fewer than its configured minimum number of papers. This prevents empty or obviously truncated metadata responses from being mistaken for a valid corpus.",
        "",
        "2027 conference cells remain zero unless published metadata is actually present. IEEE Transactions rows with publication year 2027 are retained when OpenAlex already exposes them.",
    ]
    (OUT / "PAPER_CORPUS_SUMMARY.md").write_text("\n".join(lines)+"\n", encoding="utf-8")

    readme = """# Recent paper corpus

This directory contains the machine-readable literature corpus used to ground the Advanced Networks project idea pool.

## Files

- all_conference_papers.csv — all papers collected for the requested conference series and available years.
- ieee_transactions_papers.csv.gz — all 2023–2027 works available from OpenAlex for journal sources whose names match IEEE Transactions on ..., IEEE Transactions of ..., or IEEE/ACM Transactions on ....
- recent_networking_papers.csv — the network-relevant subset used to derive project clusters.
- IEEE_TRANSACTIONS_SOURCES.csv — every IEEE Transactions journal source matched by the collector.
- PAPER_CORPUS_COVERAGE.csv — venue/year counts plus the resolved OpenAlex source IDs.
- PAPER_CORPUS_SUMMARY.md — compact audit summary.

## Metadata and keyword provenance

OpenAlex provides title, authors, publication year, DOI/URL, venue/source identity, topics, and keywords for most rows. OpenAlex documents its current keywords as model-generated aboutness labels produced from a work's title, abstract, and venue. They are therefore stored as keywords with keyword_provenance = OpenAlex model-generated keywords, not as author keywords.

When OpenAlex does not provide keywords, the builder creates a deterministic title-derived fallback and marks that provenance explicitly.

NINeS 2026 is collected from the official accepted-paper page because it is a new venue and may not yet have a stable bibliographic source.

## Reproducibility and validation

The source configuration and minimum plausible counts are in tools/research/paper_corpus_config.json. The builder is tools/research/build_paper_corpus.py.

The build is fail-closed: an established 2023–2026 conference venue that resolves to an implausibly small paper count causes the workflow to fail rather than commit a misleading corpus.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    obsolete = OUT / "recent_networking_papers.jsonl"
    if obsolete.exists():
        obsolete.unlink()

    return conferences, tx, network

def main():
    conference_rows = []
    coverage = []
    failures = []

    for spec in CONFERENCES:
        allowed = set(spec.get("years", YEARS))
        if spec["name"] == "NINeS":
            rows_2026 = nines_2026(spec)
            for year in YEARS:
                if year not in allowed:
                    coverage.append({"venue":spec["name"],"kind":"conference","year":year,"records":0,"status":"not-applicable","source_ids":"","source_names":""})
                    continue
                rows = rows_2026 if year == 2026 else []
                conference_rows.extend(rows)
                status = "official-page" if rows else ("not-yet-available" if year == 2027 else "no-records")
                coverage.append({"venue":spec["name"],"kind":"conference","year":year,"records":len(rows),"status":status,"source_ids":"","source_names":"NINeS official accepted-paper page"})
                if year == 2026 and len(rows) < spec["hard_min"]:
                    failures.append(f"{spec['name']} {year}: {len(rows)} < {spec['hard_min']}")
            continue

        sources = discover_conference_sources(spec)
        source_ids = [norm(x.get("id")) for x in sources]
        source_names = [norm(x.get("display_name")) for x in sources]
        if not source_ids:
            failures.append(f"{spec['name']}: no OpenAlex source resolved")
        for year in YEARS:
            if year not in allowed:
                coverage.append({"venue":spec["name"],"kind":"conference","year":year,"records":0,"status":"not-applicable","source_ids":"; ".join(source_ids),"source_names":"; ".join(source_names)})
                continue
            rows = collect_works(source_ids, year, venue_override=spec["name"], kind="conference", core=spec.get("core",False))
            conference_rows.extend(rows)
            status = "ok" if rows else ("not-yet-available" if year == 2027 else "no-records")
            coverage.append({"venue":spec["name"],"kind":"conference","year":year,"records":len(rows),"status":status,"source_ids":"; ".join(source_ids),"source_names":"; ".join(source_names)})
            print(f"COUNT {spec['name']} {year}: {len(rows)}", flush=True)
            if 2023 <= year <= 2026 and len(rows) < int(spec["hard_min"]):
                failures.append(f"{spec['name']} {year}: {len(rows)} < {spec['hard_min']}")

    tx_sources = discover_ieee_transactions_sources()
    if len(tx_sources) < 20:
        failures.append(f"IEEE Transactions source discovery returned only {len(tx_sources)} sources")
    tx_ids = [norm(x.get("id")) for x in tx_sources]
    tx_rows = []
    for year in YEARS:
        if year == 2027 and not TX_CFG.get("include_2027", True):
            continue
        year_rows = []
        # Small source batches keep anonymous basic pagination well below
        # the 10,000-result per-query ceiling while avoiding hundreds of
        # unnecessary round trips.
        for i in range(0, len(tx_ids), 5):
            year_rows.extend(collect_works(tx_ids[i:i+5], year, venue_override=None, kind="journal", core=False))
        tx_rows.extend(year_rows)
        print(f"COUNT IEEE Transactions {year}: {len(year_rows)}", flush=True)

    conferences, tx, network = write_outputs(conference_rows, tx_rows, coverage, tx_sources)

    author_missing = sum(not r["authors"] for r in conferences)
    if conferences and author_missing / len(conferences) > 0.05:
        failures.append(f"conference author metadata missing for {author_missing}/{len(conferences)} records")
    if len(conferences) < 1500:
        failures.append(f"conference corpus unexpectedly small: {len(conferences)}")
    if len(tx) < 3000:
        failures.append(f"IEEE Transactions corpus unexpectedly small: {len(tx)}")
    if any(not r["keywords"] for r in conferences + tx):
        failures.append("one or more rows have no keywords after fallback")

    if failures:
        print("\nVALIDATION FAILED", file=sys.stderr)
        for x in failures:
            print(" - " + x, file=sys.stderr)
        sys.exit(2)

    print(f"VALIDATED: {len(conferences)} conference papers; {len(tx)} IEEE Transactions papers; {len(network)} network-relevant rows", flush=True)

if __name__ == "__main__":
    main()
