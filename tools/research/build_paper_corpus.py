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
    per_page = 200
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
            allowed_types = set(spec.get("allow_source_types", ["conference"]))
            if typ not in allowed_types:
                continue
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
    picked = ordered[:int(spec.get("max_sources", 50))]
    print(f"SOURCES {spec['name']}: {len(picked)} matched", flush=True)
    for x in picked:
        print(f"  {x.get('display_name')} [{x.get('type')}] {x.get('id')}", flush=True)
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


def strip_markup(x):
    if not x:
        return ""
    return norm(BeautifulSoup(str(x), "html.parser").get_text(" ", strip=True))

def crossref_ieee_transactions(year):
    """Collect IEEE Transactions journal articles from Crossref for one year.

    IEEE journal articles use the 10.1109 DOI prefix. query.container-title
    provides the broad candidate set; the configured exact name regex is then
    applied locally so unrelated IEEE publications are not admitted.
    """
    rx = re.compile(TX_CFG["include_regex"])
    base = "https://api.crossref.org/works"
    cursor = "*"
    rows = []
    seen_cursors = set()
    retrieved = 0
    while cursor and cursor not in seen_cursors:
        seen_cursors.add(cursor)
        params = {
            "filter": (
                f"from-pub-date:{year}-01-01,"
                f"until-pub-date:{year}-12-31,"
                f"type:journal-article,"
                f"prefix:{TX_CFG.get('crossref_prefix','10.1109')}"
            ),
            "query.container-title": TX_CFG.get("crossref_query", "IEEE Transactions"),
            "rows": 1000,
            "cursor": cursor,
        }
        data = get_json(base, params=params, attempts=6, pause=1.5)
        msg = data.get("message") or {}
        items = msg.get("items") or []
        if not items:
            break
        for item in items:
            containers = item.get("container-title") or []
            raw_venue = norm(containers[0] if containers else "")
            if not raw_venue or not rx.search(raw_venue):
                continue
            title_raw = item.get("title") or []
            title = norm(title_raw[0] if title_raw else "")
            if not title:
                continue
            authors = []
            for a in item.get("author") or []:
                name = norm(" ".join(x for x in [a.get("given",""), a.get("family","")] if x))
                if name:
                    authors.append(name)
            doi = norm(item.get("DOI")).lower()
            subjects = [norm(x) for x in (item.get("subject") or []) if norm(x)]
            abstract = strip_markup(item.get("abstract"))
            semantic_blob = " ".join([title, abstract, " ".join(subjects)]).lower()
            derived_terms = []
            for phrases in CATEGORIES.values():
                for phrase in phrases:
                    if phrase in semantic_blob and phrase not in derived_terms:
                        derived_terms.append(phrase)
            keyword_terms = []
            for term in subjects + sorted(derived_terms, key=len, reverse=True):
                if term and term not in keyword_terms:
                    keyword_terms.append(term)
                if len(keyword_terms) >= 12:
                    break
            if subjects and derived_terms:
                provenance = "Crossref subjects + deterministic title/abstract category terms"
            elif subjects:
                provenance = "Crossref subjects"
            elif derived_terms:
                provenance = "deterministic title/abstract category terms"
            else:
                provenance = ""
            rows.append({
                "title": title.rstrip("."),
                "authors": "; ".join(authors),
                "venue": raw_venue,
                "raw_venue": raw_venue,
                "year": year,
                "venue_kind": "journal",
                "source_id": "",
                "doi": doi,
                "url": norm(item.get("URL")) or (f"https://doi.org/{doi}" if doi else ""),
                "openalex_id": "",
                "metadata_source": "Crossref",
                "paper_type": norm(item.get("type")) or "journal-article",
                "keywords": "; ".join(keyword_terms),
                "keyword_provenance": provenance,
                "topics": "",
                "primary_topic": "",
                "categories": "",
                "network_relevance_score": 0,
                "network_relevant": False,
                "_core": False,
            })
        retrieved += len(items)
        total = int(msg.get("total-results") or 0)
        cursor = norm(msg.get("next-cursor"))
        print(f"CROSSREF IEEE Transactions {year}: scanned {retrieved}/{total}, kept {len(rows)}", flush=True)
        if retrieved >= total:
            break
        time.sleep(0.08)
    return rows

def enrich_openalex_by_doi(rows):
    """Enrich a bounded subset with OpenAlex keywords/topics using DOI OR filters."""
    by_doi = {r["doi"]: r for r in rows if r.get("doi")}
    dois = sorted(by_doi)
    if not dois:
        return
    print(f"OpenAlex DOI enrichment for {len(dois)} selected journal records", flush=True)
    for i in range(0, len(dois), 40):
        chunk = dois[i:i+40]
        filt = "doi:" + "|".join(chunk)
        try:
            works = list(oa_list("works", {
                "filter": filt,
                "select": "id,doi,keywords,topics,primary_topic",
            }, max_pages=2))
        except Exception as e:
            print(f"WARNING DOI enrichment batch {i}: {e}", file=sys.stderr)
            continue
        for w in works:
            doi = norm(w.get("doi")).lower().replace("https://doi.org/", "")
            r = by_doi.get(doi)
            if not r:
                continue
            kws = sorted(
                [(norm(x.get("display_name")), float(x.get("score") or 0))
                 for x in (w.get("keywords") or []) if norm(x.get("display_name"))],
                key=lambda x: -x[1],
            )
            if kws:
                r["keywords"] = "; ".join(x[0] for x in kws[:10])
                r["keyword_provenance"] = "OpenAlex model-generated keywords"
            r["topics"] = "; ".join(
                norm(x.get("display_name")) for x in (w.get("topics") or [])[:3]
                if norm(x.get("display_name"))
            )
            r["primary_topic"] = norm((w.get("primary_topic") or {}).get("display_name"))
            r["openalex_id"] = norm(w.get("id"))
        time.sleep(0.05)


def _crossref_item_row(item, venue, year, kind, core, metadata_source):
    title_raw = item.get("title") or []
    title = norm(title_raw[0] if title_raw else "")
    if not title:
        return None
    containers = item.get("container-title") or []
    raw_venue = norm(containers[0] if containers else venue)
    authors = []
    for a in item.get("author") or []:
        name = norm(" ".join(x for x in [a.get("given",""), a.get("family","")] if x))
        if name:
            authors.append(name)
    doi = norm(item.get("DOI")).lower()
    subjects = [norm(x) for x in (item.get("subject") or []) if norm(x)]
    abstract = strip_markup(item.get("abstract"))
    semantic_blob = " ".join([title, abstract, " ".join(subjects)]).lower()
    terms = []
    for phrases in CATEGORIES.values():
        for phrase in phrases:
            if phrase in semantic_blob and phrase not in terms:
                terms.append(phrase)
    keywords = []
    for term in subjects + sorted(terms, key=len, reverse=True):
        if term and term not in keywords:
            keywords.append(term)
        if len(keywords) >= 12:
            break
    if subjects and terms:
        provenance = "Crossref subjects + deterministic title/abstract category terms"
    elif subjects:
        provenance = "Crossref subjects"
    elif terms:
        provenance = "deterministic title/abstract category terms"
    else:
        provenance = ""
    return {
        "title": title.rstrip("."),
        "authors": "; ".join(authors),
        "venue": venue,
        "raw_venue": raw_venue,
        "year": year,
        "venue_kind": kind,
        "source_id": "",
        "doi": doi,
        "url": norm(item.get("URL")) or (f"https://doi.org/{doi}" if doi else ""),
        "openalex_id": "",
        "metadata_source": metadata_source,
        "paper_type": norm(item.get("type")),
        "keywords": "; ".join(keywords),
        "keyword_provenance": provenance,
        "topics": "",
        "primary_topic": "",
        "categories": "",
        "network_relevance_score": 0,
        "network_relevant": False,
        "_core": bool(core),
        "_abstract": abstract,
    }


def crossref_conference(spec, year):
    rx = re.compile(spec["container_regex"])
    base = "https://api.crossref.org/works"
    rows = []
    types = spec.get("crossref_types", ["proceedings-article"])
    for typ in types:
        cursor = "*"
        seen_cursors = set()
        retrieved = 0
        while cursor and cursor not in seen_cursors:
            seen_cursors.add(cursor)
            params = {
                "filter": (
                    f"from-pub-date:{year}-01-01,"
                    f"until-pub-date:{year}-12-31,"
                    f"type:{typ},"
                    f"prefix:{spec['prefix']}"
                ),
                "query.container-title": spec["query"],
                "rows": 1000,
                "cursor": cursor,
                "select": "DOI,title,author,container-title,URL,type,subject,abstract,published",
            }
            data = get_json(base, params=params, attempts=6, pause=1.0)
            msg = data.get("message") or {}
            items = msg.get("items") or []
            if not items:
                break
            for item in items:
                containers = item.get("container-title") or []
                raw_venue = norm(containers[0] if containers else "")
                if not raw_venue or not rx.search(raw_venue):
                    continue
                row = _crossref_item_row(
                    item, spec["name"], year, "conference", spec.get("core", False), "Crossref"
                )
                if row:
                    rows.append(row)
            retrieved += len(items)
            total = int(msg.get("total-results") or 0)
            cursor = norm(msg.get("next-cursor"))
            if retrieved >= total:
                break
            time.sleep(0.05)
    rows = dedupe(rows)
    print(f"CROSSREF {spec['name']} {year}: kept {len(rows)}", flush=True)
    return rows


def _meta_values(soup, name):
    vals = []
    for tag in soup.find_all("meta", attrs={"name": name}):
        v = norm(tag.get("content"))
        if v:
            vals.append(v)
    return vals


def _usenix_keywords(title, abstract):
    blob = f"{title} {abstract}".lower()
    terms = []
    for phrases in CATEGORIES.values():
        for phrase in phrases:
            if phrase in blob and phrase not in terms:
                terms.append(phrase)
    if terms:
        return "; ".join(sorted(terms, key=len, reverse=True)[:12]), "deterministic title/abstract category terms"
    return "", ""


def usenix_conference(spec, year):
    slug_value = spec["slug"].format(yy=str(year)[2:])
    index_url = f"https://www.usenix.org/conference/{slug_value}/technical-sessions"
    soup = BeautifulSoup(get_html(index_url), "html.parser")
    path_marker = f"/conference/{slug_value}/presentation/"
    links = {}
    for a in soup.find_all("a", href=True):
        href = norm(a.get("href"))
        if path_marker not in href:
            continue
        title = norm(a.get_text(" ", strip=True))
        if not title or len(title) < 8:
            continue
        if title.lower() in {"available media","video","slides","paper","presentation"}:
            continue
        url = urljoin(index_url, href)
        if url not in links or len(title) > len(links[url]):
            links[url] = title

    rows = []
    for idx, (url, listed_title) in enumerate(sorted(links.items()), start=1):
        try:
            psoup = BeautifulSoup(get_html(url), "html.parser")
        except Exception as e:
            print(f"WARNING USENIX page {url}: {e}", file=sys.stderr)
            continue

        citation_title = _meta_values(psoup, "citation_title")
        title = citation_title[0] if citation_title else listed_title
        authors = _meta_values(psoup, "citation_author")
        pdfs = _meta_values(psoup, "citation_pdf_url")
        # Technical-session pages also contain keynotes and panels. Proceedings
        # papers expose citation_pdf_url; require it for the paper inventory.
        if not pdfs:
            continue

        abstract_values = _meta_values(psoup, "description")
        abstract = abstract_values[0] if abstract_values else ""
        keywords = _meta_values(psoup, "citation_keywords")
        if not keywords:
            keywords = _meta_values(psoup, "keywords")
        if keywords:
            kw = "; ".join(dict.fromkeys(keywords))
            provenance = "publisher metadata keywords"
        else:
            kw, provenance = _usenix_keywords(title, abstract)

        rows.append({
            "title": norm(title).rstrip("."),
            "authors": "; ".join(authors),
            "venue": spec["name"],
            "raw_venue": spec["name"],
            "year": year,
            "venue_kind": "conference",
            "source_id": "",
            "doi": "",
            "url": url,
            "openalex_id": "",
            "metadata_source": "USENIX technical sessions + presentation metadata",
            "paper_type": "conference paper",
            "keywords": kw,
            "keyword_provenance": provenance,
            "topics": "",
            "primary_topic": "",
            "categories": "",
            "network_relevance_score": 0,
            "network_relevant": False,
            "_core": bool(spec.get("core", False)),
            "_abstract": abstract,
        })
        if idx % 50 == 0:
            print(f"USENIX {spec['name']} {year}: checked {idx}/{len(links)}, kept {len(rows)}", flush=True)
        time.sleep(0.02)
    rows = dedupe(rows)
    print(f"USENIX {spec['name']} {year}: kept {len(rows)}", flush=True)
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

def write_outputs(conference_rows, tx_rows, coverage):
    all_rows = dedupe(conference_rows + tx_rows)
    for r in all_rows:
        categorize(r)

    conference_names = {x["name"] for x in CONFERENCES}
    conferences = [r for r in all_rows if r["venue"] in conference_names]
    tx = [r for r in all_rows if r["venue"] not in conference_names and re.match(TX_CFG["include_regex"], r["venue"] or "")]
    network = [r for r in conferences + tx if r["network_relevant"]]

    write_csv(OUT / "all_conference_papers.csv", conferences)
    write_gzip_csv(OUT / "ieee_transactions_papers.csv.gz", tx)
    write_csv(OUT / "recent_networking_papers.csv", network)

    with (OUT / "PAPER_CORPUS_COVERAGE.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["venue","kind","year","records","status","source_ids","source_names"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(coverage)

    tx_by_vy = Counter((r["venue"], int(r["year"])) for r in tx)
    tx_venues = sorted({r["venue"] for r in tx})
    with (OUT / "IEEE_TRANSACTIONS_SOURCES.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["display_name","records_2023_2027"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for venue in tx_venues:
            w.writerow({
                "display_name": venue,
                "records_2023_2027": sum(tx_by_vy.get((venue, y), 0) for y in YEARS),
            })

    with (OUT / "IEEE_TRANSACTIONS_COVERAGE.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["venue","year","records"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for venue in tx_venues:
            for year in YEARS:
                w.writerow({"venue": venue, "year": year, "records": tx_by_vy.get((venue, year), 0)})

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
        f"IEEE Transactions records: **{len(tx):,}** across **{len(tx_venues):,}** matching journal titles.",
        f"Network-relevant records used for project-area mining: **{len(network):,}**.","",
        "## Coverage by requested conference and year","",
        "| Venue | 2023 | 2024 | 2025 | 2026 | 2027 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for spec in CONFERENCES:
        lines.append("| " + spec["name"] + " | " + " | ".join(str(by_vy.get((spec["name"], y), 0)) for y in YEARS) + " |")
    lines += [
        "","## Keyword provenance","",
        "Keywords are never silently presented as author keywords. Crossref subjects and publisher metadata are retained when available; otherwise deterministic title/abstract-derived terms are used and marked as such.","",
        "| Provenance | Records |","| --- | ---: |",
    ]
    for k,n in prov.most_common():
        lines.append(f"| {k or 'missing'} | {n:,} |")
    lines += ["","## Network-relevant category counts","","| Category | Papers |","| --- | ---: |"]
    for k,n in cats.most_common():
        lines.append(f"| {k} | {n:,} |")
    lines += [
        "","## Validation","",
        "The build is fail-closed. Established venue-years must meet configured minimum paper counts, and conference records must contain authors and keywords after provenance-aware fallback. Generated files are committed only after validation succeeds.",
        "",
        "2027 conference cells remain zero unless published paper metadata is actually available. IEEE Transactions rows with a 2027 publication year are retained when Crossref already exposes them.",
    ]
    (OUT / "PAPER_CORPUS_SUMMARY.md").write_text("\n".join(lines)+"\n", encoding="utf-8")

    readme = """# Recent paper corpus

This directory contains the machine-readable literature corpus used to ground the Advanced Networks project idea pool.

## Files

- all_conference_papers.csv — all collected papers for the requested conference series and available years.
- ieee_transactions_papers.csv.gz — all 2023–2027 Crossref records whose container title matches IEEE Transactions on ..., IEEE Transactions of ..., or IEEE/ACM Transactions on ....
- recent_networking_papers.csv — the network-relevant subset used to derive project clusters.
- IEEE_TRANSACTIONS_SOURCES.csv — every matched IEEE Transactions journal title and record count.
- IEEE_TRANSACTIONS_COVERAGE.csv — per-journal, per-year counts.
- PAPER_CORPUS_COVERAGE.csv — requested conference venue/year counts and collection status.
- PAPER_CORPUS_SUMMARY.md — compact audit summary.

## Metadata sources

ACM and IEEE conference proceedings are collected from Crossref and filtered by exact venue-family patterns. NSDI, OSDI, and USENIX Security are collected from official USENIX technical-session/presentation metadata. NINeS is collected from its official accepted-paper page.

The IEEE Transactions inventory is collected from Crossref using the IEEE DOI prefix and then filtered locally by journal-title regex.

## Keyword provenance

The corpus distinguishes publisher/Crossref metadata from inferred terms. Crossref subjects and publisher keyword metadata are preserved when available. If a paper exposes no keywords, deterministic terms are derived from its title and abstract and the row records that provenance explicitly.

## Reproducibility and validation

The source configuration and minimum plausible counts are in tools/research/paper_corpus_config.json. The builder is tools/research/build_paper_corpus.py.

The build is fail-closed: if an established venue-year is implausibly small, or required metadata is missing at an unacceptable rate, the workflow fails without committing generated data.
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
        for year in YEARS:
            if year not in allowed:
                coverage.append({
                    "venue":spec["name"],"kind":"conference","year":year,"records":0,
                    "status":"not-applicable","source_ids":"","source_names":"",
                })
                continue

            provider = spec["provider"]
            if provider == "nines":
                rows = nines_2026(spec) if year == 2026 else []
                source_name = "NINeS official accepted-paper page"
            elif provider == "usenix":
                rows = [] if year == 2027 else usenix_conference(spec, year)
                source_name = "USENIX technical sessions"
            elif provider == "crossref":
                rows = crossref_conference(spec, year)
                source_name = "Crossref"
            else:
                raise RuntimeError(f"unknown provider {provider} for {spec['name']}")

            if rows and provider == "crossref":
                enrich_openalex_by_doi(rows)

            conference_rows.extend(rows)
            status = "ok" if rows else ("not-yet-available" if year == 2027 else "no-records")
            coverage.append({
                "venue":spec["name"],"kind":"conference","year":year,"records":len(rows),
                "status":status,"source_ids":"","source_names":source_name,
            })
            print(f"COUNT {spec['name']} {year}: {len(rows)}", flush=True)

            validate_through = int(spec.get("validate_through", 2026))
            if 2023 <= year <= validate_through and len(rows) < int(spec["hard_min"]):
                failures.append(f"{spec['name']} {year}: {len(rows)} < {spec['hard_min']}")

    # Do not spend minutes scanning the very large IEEE Transactions
    # corpus if conference inventory is already incomplete.
    if failures:
        print("\nCONFERENCE VALIDATION FAILED", file=sys.stderr)
        for x in failures:
            print(" - " + x, file=sys.stderr)
        sys.exit(2)

    tx_rows = []
    for year in YEARS:
        if year == 2027 and not TX_CFG.get("include_2027", True):
            continue
        year_rows = crossref_ieee_transactions(year)
        tx_rows.extend(year_rows)
        print(f"COUNT IEEE Transactions {year}: {len(year_rows)}", flush=True)

    conferences, tx, network = write_outputs(conference_rows, tx_rows, coverage)

    author_missing = sum(not r["authors"] for r in conferences)
    keyword_missing = sum(not r["keywords"] for r in conferences)
    if conferences and author_missing / len(conferences) > 0.02:
        failures.append(f"conference author metadata missing for {author_missing}/{len(conferences)} records")
    if keyword_missing:
        failures.append(f"conference keywords missing after fallback for {keyword_missing} records")
    if len(conferences) < 2500:
        failures.append(f"conference corpus unexpectedly small: {len(conferences)}")
    if len(tx) < 3000:
        failures.append(f"IEEE Transactions corpus unexpectedly small: {len(tx)}")

    if failures:
        print("\nVALIDATION FAILED", file=sys.stderr)
        for x in failures:
            print(" - " + x, file=sys.stderr)
        sys.exit(2)

    print(
        f"VALIDATED: {len(conferences)} conference papers; "
        f"{len(tx)} IEEE Transactions papers; {len(network)} network-relevant rows",
        flush=True,
    )

if __name__ == "__main__":
    main()
