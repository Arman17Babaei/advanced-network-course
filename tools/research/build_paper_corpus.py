#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
CFG = json.loads((ROOT / "tools/research/paper_corpus_config.json").read_text(encoding="utf-8"))
OUT = ROOT / "materials/assessments/data"
OUT.mkdir(parents=True, exist_ok=True)
YEARS = CFG["years"]
VENUES = CFG["venues"]
CATEGORIES = CFG["categories"]
S = requests.Session()
S.headers.update({"User-Agent": "advanced-network-course-paper-corpus/1.0"})
# Keep source queries deliberately serial to be respectful of public metadata APIs.
STOP = {
    "the","and","for","with","from","into","using","via","towards","toward","based",
    "system","systems","framework","method","approach","efficient","effective","new",
    "this","that","over","under","through","without","between","across","their","our",
}

def norm(x):
    return re.sub(r"\s+", " ", html.unescape(str(x or ""))).strip()

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def get_json(url, params=None, attempts=6, pause=1.5):
    err = None
    for i in range(attempts):
        try:
            r = S.get(url, params=params, timeout=60)
            if r.status_code == 429:
                time.sleep(max(10, pause * (i + 2)))
                continue
            r.raise_for_status()
            return r.json()
        except Exception as e:
            err = e
            time.sleep(pause * (i + 1))
    raise RuntimeError(f"request failed: {url}: {err}")

def query_for(spec, year):
    return " ".join([*(f"venue:{x}" for x in spec["terms"]), f"year:{year}"])

def accepts(spec, raw_venue):
    v = norm(raw_venue).lower()
    return any(x.lower() in v for x in spec["match"])

def dblp(spec, year):
    q = query_for(spec, year)
    out, offset = [], 0
    while True:
        data = get_json(
            "https://dblp.org/search/publ/api",
            {"q": q, "format": "json", "h": 1000, "f": offset},
            pause=2.0,
        )
        h = data.get("result", {}).get("hits", {})
        batch = h.get("hit", []) or []
        if isinstance(batch, dict):
            batch = [batch]
        for hit in batch:
            info = hit.get("info", {})
            if str(info.get("year", "")) == str(year) and accepts(spec, info.get("venue", "")):
                out.append(info)
        sent = int(h.get("@sent", len(batch)) or len(batch))
        total = int(h.get("@total", 0) or 0)
        offset += sent
        if sent == 0 or offset >= total:
            break
        time.sleep(2.0)
    return out

def author_list(info):
    raw = (info.get("authors") or {}).get("author", [])
    if isinstance(raw, dict):
        raw = [raw]
    ans = []
    for a in raw:
        n = norm(a.get("text") if isinstance(a, dict) else a)
        n = re.sub(r"\s+\d{4}$", "", n)
        if n:
            ans.append(n)
    return ans

def nines_2026():
    url = "https://2026.nines-conference.org/accepted"
    try:
        r = S.get(url, timeout=60)
        r.raise_for_status()
    except Exception:
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    rows = []
    for li in soup.find_all("li"):
        a = li.find("a")
        if not a:
            continue
        title = norm(a.get_text(" ", strip=True)).rstrip(".")
        if not title or title.lower() in {
            "home","papers","talk","contributed talks","recorded stream","recorded pods","cfp","faq","sop","organizers"
        }:
            continue
        txt = norm(li.get_text(" ", strip=True))
        rest = txt[len(norm(a.get_text(" ", strip=True))):].lstrip(". ")
        rest = re.sub(r"\s+Talk\s*$", "", rest)
        rest = re.sub(r"\s*\([^)]*\)", "", rest).replace("∗", "").replace("*", "")
        authors = [norm(x) for x in rest.split(",") if norm(x)]
        href = a.get("href") or url
        if href.startswith("/"):
            href = "https://2026.nines-conference.org" + href
        rows.append({
            "title": title,
            "authors": {"author": [{"text": x} for x in authors]},
            "venue": "NINeS",
            "year": "2026",
            "type": "Conference and Workshop Papers",
            "ee": href,
            "url": href,
            "key": "nines/2026/" + slug(title)[:100],
        })
    return rows

def row_from(info, spec, year, source):
    doi = norm(info.get("doi", "")).lower().replace("https://doi.org/", "")
    return {
        "title": norm(info.get("title", "")).rstrip("."),
        "authors": "; ".join(author_list(info)),
        "venue": spec["name"],
        "raw_venue": norm(info.get("venue", "")),
        "year": year,
        "venue_kind": spec["kind"],
        "doi": doi,
        "url": norm(info.get("ee") or info.get("url")),
        "dblp_url": norm(info.get("url")) if source == "dblp" else "",
        "dblp_key": norm(info.get("key")) if source == "dblp" else "",
        "metadata_source": source,
        "paper_type": norm(info.get("type")),
        "openalex_id": "",
        "keywords": "",
        "keyword_provenance": "",
        "topics": "",
        "primary_topic": "",
        "categories": "",
        "network_relevance_score": 0,
        "network_relevant": False,
    }

def dedupe(rows):
    kept = {}
    for r in rows:
        k = (r["doi"], slug(r["title"]), r["year"])
        if k not in kept:
            kept[k] = r
            continue
        old = kept[k]
        if old["metadata_source"] != "dblp" and r["metadata_source"] == "dblp":
            old, r = r, old
            kept[k] = old
        for f in ("doi","url","dblp_url","dblp_key","authors"):
            if not old.get(f) and r.get(f):
                old[f] = r[f]
    return sorted(kept.values(), key=lambda r: (r["year"], r["venue"].lower(), r["title"].lower()))

def openalex(rows):
    by_doi = defaultdict(list)
    for r in rows:
        if r["doi"]:
            by_doi[r["doi"]].append(r)
    dois = sorted(by_doi)
    print(f"OpenAlex enrichment for {len(dois)} DOI-bearing records", flush=True)
    for i in range(0, len(dois), 25):
        chunk = dois[i:i+25]
        try:
            data = get_json(
                "https://api.openalex.org/works",
                {
                    "filter": "doi:" + "|".join(chunk),
                    "per-page": 100,
                    "select": "id,doi,title,publication_year,keywords,topics,primary_topic",
                },
                pause=1.0,
            )
        except Exception as e:
            print(f"WARNING OpenAlex batch {i}: {e}", file=sys.stderr)
            continue
        for w in data.get("results", []) or []:
            doi = norm(w.get("doi")).lower().replace("https://doi.org/", "")
            if doi not in by_doi:
                continue
            kws = sorted(
                [(norm(x.get("display_name")), float(x.get("score") or 0)) for x in (w.get("keywords") or []) if norm(x.get("display_name"))],
                key=lambda x: -x[1],
            )
            topics = [norm(x.get("display_name")) for x in (w.get("topics") or []) if norm(x.get("display_name"))]
            primary = norm((w.get("primary_topic") or {}).get("display_name"))
            for r in by_doi[doi]:
                r["openalex_id"] = norm(w.get("id"))
                if kws:
                    r["keywords"] = "; ".join(x[0] for x in kws[:10])
                    r["keyword_provenance"] = "OpenAlex model-generated keywords"
                r["topics"] = "; ".join(topics[:3])
                r["primary_topic"] = primary
        time.sleep(0.15)

def title_fallback(title, limit=8):
    low = title.lower()
    domain = sorted({p for ps in CATEGORIES.values() for p in ps}, key=len, reverse=True)
    out = [p for p in domain if p in low][:limit]
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

def categorize(r, spec_by_name):
    if not r["keywords"]:
        r["keywords"] = "; ".join(title_fallback(r["title"]))
        r["keyword_provenance"] = "deterministic title-derived fallback"
    blob = " ".join((r["title"], r["keywords"], r["topics"], r["primary_topic"])).lower()
    title = r["title"].lower()
    scored = []
    for cat, phrases in CATEGORIES.items():
        score = sum(2 if p in title else 1 for p in phrases if p in blob)
        if score:
            scored.append((score, cat))
    scored.sort(key=lambda x: (-x[0], x[1]))
    r["categories"] = "; ".join(x[1] for x in scored[:3]) if scored else "Other / adjacent"
    prior = 1 if spec_by_name[r["venue"]].get("core") else 0
    lexical = scored[0][0] if scored else 0
    r["network_relevance_score"] = min(10, prior + lexical)
    r["network_relevant"] = bool(prior or lexical >= 2)

def write(rows, coverage):
    fields = [
        "title","authors","venue","raw_venue","year","venue_kind","doi","url","dblp_url","dblp_key",
        "metadata_source","paper_type","openalex_id","keywords","keyword_provenance","topics","primary_topic",
        "categories","network_relevance_score","network_relevant",
    ]
    with (OUT / "recent_networking_papers.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    with (OUT / "recent_networking_papers.jsonl").open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    with (OUT / "PAPER_CORPUS_COVERAGE.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["venue","kind","year","records","status","query"])
        w.writeheader()
        w.writerows(coverage)

    by_vy = Counter((r["venue"], r["year"]) for r in rows)
    prov = Counter(r["keyword_provenance"] for r in rows)
    cats, kws = Counter(), Counter()
    for r in rows:
        if r["network_relevant"]:
            for x in r["categories"].split("; "):
                cats[x] += 1
        for x in r["keywords"].split("; "):
            if x:
                kws[x] += 1
    lines = [
        "# Paper Corpus Summary","",
        f"Generated from the reproducible corpus pipeline. Total records: {len(rows):,}.",
        f"Rule-based network-relevant records: {sum(bool(r['network_relevant']) for r in rows):,}.","",
        "OpenAlex keywords are model-generated aboutness labels, not author-supplied keywords. The keyword_provenance column records whether a row uses OpenAlex enrichment or the deterministic title fallback.","",
        "## Coverage by venue and year","",
        "| Venue | 2023 | 2024 | 2025 | 2026 | 2027 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for spec in VENUES:
        lines.append("| " + spec["name"] + " | " + " | ".join(str(by_vy.get((spec["name"], y), 0)) for y in YEARS) + " |")
    lines += ["","## Keyword provenance","","| Source | Papers |","| --- | ---: |"]
    for k, n in prov.most_common():
        lines.append(f"| {k or 'missing'} | {n:,} |")
    lines += ["","## Network-relevant category counts","","| Category | Papers |","| --- | ---: |"]
    for k, n in cats.most_common():
        lines.append(f"| {k} | {n:,} |")
    lines += ["","## Most common keywords","","| Keyword | Papers |","| --- | ---: |"]
    for k, n in kws.most_common(100):
        lines.append(f"| {k} | {n:,} |")
    lines += [
        "","## Scope notes","",
        "- 2027 remains empty until accepted-paper or proceedings metadata is available.",
        "- NINeS 2026 uses its official accepted-paper page if DBLP has no records.",
        "- IEEE Transactions coverage is limited to the networking, distributed, mobile, cloud, multimedia, communications, and dependability journals listed in paper_corpus_config.json.",
        "- Category and network-relevance labels are reproducible discovery heuristics, not bibliometric ground truth.",
        "- PAPER_CORPUS_COVERAGE.csv records the exact query status for every venue-year.",
    ]
    (OUT / "PAPER_CORPUS_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def main():
    rows, coverage = [], []
    for spec in VENUES:
        allowed = spec.get("years", YEARS)
        for year in YEARS:
            if year not in allowed:
                coverage.append({"venue":spec["name"],"kind":spec["kind"],"year":year,"records":0,"status":"not-applicable","query":""})
                continue
            print(f"DBLP {spec['name']} {year}", flush=True)
            status = "ok"
            try:
                info = dblp(spec, year)
                if not info:
                    status = "no-records"
            except Exception as e:
                print(f"WARNING {spec['name']} {year}: {e}", file=sys.stderr)
                info, status = [], "query-failed"
            if spec["name"] == "NINeS" and year == 2026 and not info:
                info = nines_2026()
                if info:
                    status = "official-fallback"
            source = "official venue page" if status == "official-fallback" else "dblp"
            rows.extend(row_from(x, spec, year, source) for x in info)
            coverage.append({"venue":spec["name"],"kind":spec["kind"],"year":year,"records":len(info),"status":status,"query":query_for(spec,year)})
            time.sleep(1.0)
    rows = dedupe(rows)
    print(f"Metadata records: {len(rows)}", flush=True)
    openalex(rows)
    by_name = {x["name"]: x for x in VENUES}
    for r in rows:
        categorize(r, by_name)
    write(rows, coverage)
    print(f"Wrote {len(rows)} records", flush=True)

if __name__ == "__main__":
    main()
