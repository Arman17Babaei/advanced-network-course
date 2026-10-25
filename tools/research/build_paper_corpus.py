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
        pages = 0
        empty_match_pages = 0
        found_any = False
        while cursor and cursor not in seen_cursors and pages < int(spec.get("max_crossref_pages", 10)):
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
            matched_this_page = 0
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
                    matched_this_page += 1
            pages += 1
            if matched_this_page:
                found_any = True
                empty_match_pages = 0
            elif found_any:
                empty_match_pages += 1
            cursor = norm(msg.get("next-cursor"))
            print(
                f"CROSSREF {spec['name']} {year}: page {pages}, "
                f"matched {matched_this_page}, cumulative {len(rows)}",
                flush=True,
            )
            # query.container-title is a ranked search. Once a venue has been
            # found and then vanishes for two full 1000-result pages, continuing
            # through the publisher's entire annual corpus only adds unrelated
            # records.
            if found_any and empty_match_pages >= 2:
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
    rows = []
    seen_urls = set()

    paper_nodes = []
    for tag in soup.find_all(["article", "div"]):
        classes = " ".join(tag.get("class") or [])
        if "node-paper" in classes or "node--type-paper" in classes:
            if tag.find("a", href=lambda x: x and path_marker in x):
                paper_nodes.append(tag)

    for node in paper_nodes:
        a = node.find("a", href=lambda x: x and path_marker in x)
        if not a:
            continue
        url = urljoin(index_url, a.get("href"))
        if url in seen_urls:
            continue
        seen_urls.add(url)
        title = norm(a.get_text(" ", strip=True)).rstrip(".")
        if not title:
            continue

        authors = ""
        for tag in node.find_all(["div","p","span"]):
            classes = " ".join(tag.get("class") or []).lower()
            if "paper-people" in classes or ("people" in classes and "paper" in classes):
                authors = norm(tag.get_text(" ", strip=True))
                if authors:
                    break

        if not authors:
            h = a.find_parent(["h2","h3","h4"])
            if h:
                nxt = h.find_next_sibling()
                hops = 0
                while nxt is not None and hops < 5:
                    txt = norm(nxt.get_text(" ", strip=True)) if hasattr(nxt, "get_text") else ""
                    if txt and not txt.lower().startswith(("available media","abstract","download")):
                        authors = txt
                        break
                    nxt = nxt.find_next_sibling()
                    hops += 1

        abstract = ""
        for tag in node.find_all(["div","p"]):
            classes = " ".join(tag.get("class") or []).lower()
            if "abstract" in classes:
                abstract = norm(tag.get_text(" ", strip=True))
                if abstract:
                    break

        keyword_tags = node.find_all(attrs={"class": re.compile(r"keyword", re.I)})
        publisher_keywords = []
        for tag in keyword_tags:
            txt = norm(tag.get_text(" ", strip=True))
            if txt and txt not in publisher_keywords:
                publisher_keywords.append(txt)
        if publisher_keywords:
            kw = "; ".join(publisher_keywords)
            provenance = "publisher metadata keywords"
        else:
            kw, provenance = _usenix_keywords(title, abstract)

        rows.append({
            "title": title,
            "authors": authors,
            "venue": spec["name"],
            "raw_venue": spec["name"],
            "year": year,
            "venue_kind": "conference",
            "source_id": "",
            "doi": "",
            "url": url,
            "openalex_id": "",
            "metadata_source": "USENIX technical sessions",
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

    rows = dedupe(rows)
    print(f"USENIX {spec['name']} {year}: kept {len(rows)} from {len(paper_nodes)} paper nodes", flush=True)
    return rows


def official_list_conference(spec, year, url):
    soup = BeautifulSoup(get_html(url), "html.parser")
    rows = []
    seen = set()

    # Accepted-paper/program pages in the SIGCOMM family and ICNP generally
    # represent each paper as a leaf list item or a compact paragraph/block.
    candidates = []
    for li in soup.find_all("li"):
        if li.find("li"):
            continue
        strings = [norm(x) for x in li.stripped_strings if norm(x)]
        if len(strings) >= 2:
            candidates.append(strings)

    # ICNP-style accepted pages may use paragraph/div blocks instead of lists.
    if len(candidates) < int(spec.get("hard_min", 1)):
        for tag in soup.find_all(["p","div"]):
            if tag.find(["p","div"], recursive=False):
                continue
            strings = [norm(x) for x in tag.stripped_strings if norm(x)]
            if 2 <= len(strings) <= 8:
                candidates.append(strings)

    skip_prefixes = (
        "home","call for","registration","program committee","conference information",
        "deadline","session chair","break","lunch","opening remarks","closing remarks",
        "keynote","panel","award","cycle 1","cycle 2","accepted papers","technical program",
    )
    for strings in candidates:
        title = strings[0]
        title = re.sub(r"\s+(?:Long|Short)\s*$", "", title, flags=re.I).strip()
        if len(title) < 12 or title.lower().startswith(skip_prefixes):
            continue
        if re.match(r"^\d{1,2}:\d{2}", title):
            continue

        authors = strings[1] if len(strings) > 1 else ""
        if not authors or authors.lower().startswith(("abstract", "available media", "session chair")):
            continue

        # Author lines on these pages either contain comma/semicolon-separated
        # names or affiliation parentheses. This rejects navigation prose.
        if not any(ch in authors for ch in [",",";","("]) and len(authors.split()) < 2:
            continue

        key = slug(title)
        if not key or key in seen:
            continue
        seen.add(key)
        abstract = ""
        for s in strings[2:]:
            if s.lower().startswith("abstract"):
                abstract = re.sub(r"^abstract\s*:\s*", "", s, flags=re.I)
                break
        kw, provenance = _usenix_keywords(title, abstract)
        rows.append({
            "title": title.rstrip("."),
            "authors": authors,
            "venue": spec["name"],
            "raw_venue": spec["name"],
            "year": year,
            "venue_kind": "conference",
            "source_id": "",
            "doi": "",
            "url": url,
            "openalex_id": "",
            "metadata_source": "official accepted/program page",
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
    rows = dedupe(rows)
    print(f"OFFICIAL {spec['name']} {year}: kept {len(rows)} from {url}", flush=True)
    return rows


def crossref_doi_stem(spec, year, stem):
    base = "https://api.crossref.org/works"
    prefix = stem.split("/", 1)[0]
    rows = []
    cursor = "*"
    pages = 0
    while cursor and pages < 5:
        params = {
            "filter": (
                f"from-pub-date:{year}-01-01,"
                f"until-pub-date:{year}-12-31,"
                f"prefix:{prefix}"
            ),
            "query.container-title": spec.get(
                "query",
                f"IEEE International Parallel and Distributed Processing Symposium IPDPS {year}"
            ),
            "rows": 1000,
            "cursor": cursor,
            "select": "DOI,title,author,container-title,URL,type,subject,abstract,published",
        }
        data = get_json(base, params=params, attempts=6, pause=1.0)
        msg = data.get("message") or {}
        items = msg.get("items") or []
        if not items:
            break
        matched = 0
        for item in items:
            doi = norm(item.get("DOI")).lower()
            if not doi.startswith(stem.lower() + "."):
                continue
            row = _crossref_item_row(
                item, spec["name"], year, "conference", spec.get("core", False), "Crossref DOI-family"
            )
            if row:
                rows.append(row)
                matched += 1
        pages += 1
        cursor = norm(msg.get("next-cursor"))
        print(f"DOI-FAMILY {spec['name']} {year}: page {pages}, matched {matched}", flush=True)
        if matched == 0 and rows:
            break
        time.sleep(0.05)
    rows = dedupe(rows)
    print(f"DOI-FAMILY {spec['name']} {year}: kept {len(rows)}", flush=True)
    return rows


def enrich_missing_authors_from_crossref(rows):
    missing = [r for r in rows if not r.get("authors") and r.get("doi")]
    if not missing:
        return
    print(f"Crossref author enrichment for {len(missing)} rows", flush=True)
    for idx, r in enumerate(missing, start=1):
        doi = r["doi"]
        try:
            data = get_json(
                "https://api.crossref.org/works/" + requests.utils.quote(doi, safe=""),
                attempts=4,
                pause=0.5,
            )
        except Exception as e:
            print(f"WARNING Crossref DOI author lookup {doi}: {e}", file=sys.stderr)
            continue
        item = data.get("message") or {}
        authors = []
        for a in item.get("author") or []:
            name = norm(" ".join(x for x in [a.get("given",""), a.get("family","")] if x))
            if name:
                authors.append(name)
        if authors:
            r["authors"] = "; ".join(authors)
            if r.get("metadata_source") == "OpenAlex":
                r["metadata_source"] = "OpenAlex + Crossref author enrichment"
        if idx % 25 == 0:
            print(f"Crossref author enrichment: {idx}/{len(missing)}", flush=True)
        time.sleep(0.03)


def enrich_missing_authors_from_semantic_scholar(rows):
    missing = [r for r in rows if not r.get("authors") and r.get("doi")]
    if not missing:
        return
    print(f"Semantic Scholar author enrichment for {len(missing)} rows", flush=True)
    endpoint = "https://api.semanticscholar.org/graph/v1/paper/batch"
    for start in range(0, len(missing), 50):
        batch = missing[start:start+50]
        payload = {"ids": ["DOI:" + r["doi"] for r in batch]}
        data = None
        for attempt in range(4):
            try:
                resp = S.post(
                    endpoint,
                    params={"fields": "title,authors,externalIds"},
                    json=payload,
                    timeout=45,
                )
                if resp.status_code == 429:
                    time.sleep(2 ** (attempt + 1))
                    continue
                resp.raise_for_status()
                data = resp.json()
                break
            except Exception as e:
                if attempt == 3:
                    print(f"WARNING Semantic Scholar author batch: {e}", file=sys.stderr)
                else:
                    time.sleep(attempt + 1)
        if not isinstance(data, list):
            continue
        for r, item in zip(batch, data):
            if not item:
                continue
            authors = [norm(a.get("name")) for a in (item.get("authors") or []) if norm(a.get("name"))]
            if authors:
                r["authors"] = "; ".join(authors)
                r["metadata_source"] = (r.get("metadata_source") or "OpenAlex") + " + Semantic Scholar author enrichment"
        time.sleep(0.2)


def openalex_conference(spec, year):
    rows = collect_works(
        spec.get("source_ids", []),
        year,
        venue_override=spec["name"],
        kind="conference",
        core=spec.get("core", False),
    )
    rows = dedupe(rows)
    enrich_missing_authors_from_crossref(rows)
    enrich_missing_authors_from_semantic_scholar(rows)
    print(f"OPENALEX {spec['name']} {year}: kept {len(rows)}", flush=True)
    return rows


def dblp_html_conference(spec, year, url):
    """Parse one static DBLP proceedings page.

    This uses the human-facing HTML, not the DBLP search/XML APIs that are
    intermittently blocked on hosted runners.
    """
    soup = BeautifulSoup(get_html(url), "html.parser")
    rows = []
    entries = soup.select("li.entry")
    for entry in entries:
        classes = set(entry.get("class") or [])
        if "inproceedings" not in classes and "article" not in classes:
            continue

        title_tag = entry.select_one(".title")
        if title_tag is None:
            # DBLP currently renders titles in span.title; retain a fallback
            # in case markup changes slightly.
            title_tag = entry.find(["span","div"], class_=re.compile(r"title", re.I))
        title = norm(title_tag.get_text(" ", strip=True)) if title_tag else ""
        if not title:
            continue

        authors = []
        # DBLP's stable semantic markup is Schema.org itemprop=author/name.
        for a in entry.select('[itemprop="author"] [itemprop="name"]'):
            name = norm(a.get_text(" ", strip=True))
            if name and name not in authors:
                authors.append(name)
        if not authors:
            for a in entry.select('[itemprop="author"]'):
                name = norm(a.get_text(" ", strip=True))
                if name and name not in authors:
                    authors.append(name)
        if not authors:
            for a in entry.select(".authors a"):
                name = norm(a.get_text(" ", strip=True))
                if name and name not in authors:
                    authors.append(name)

        doi = ""
        link = ""
        for a in entry.find_all("a", href=True):
            href = norm(a.get("href"))
            if "doi.org/" in href.lower():
                doi = href.lower().split("doi.org/",1)[1]
                link = href
                break
        if not link:
            ee = entry.select_one("nav.publ a[href]")
            if ee:
                link = norm(ee.get("href"))

        kw, provenance = _usenix_keywords(title, "")
        rows.append({
            "title": title.rstrip("."),
            "authors": "; ".join(authors),
            "venue": spec["name"],
            "raw_venue": spec["name"],
            "year": year,
            "venue_kind": "conference",
            "source_id": "",
            "doi": doi,
            "url": link or url,
            "openalex_id": "",
            "metadata_source": "DBLP static proceedings HTML",
            "paper_type": "conference paper",
            "keywords": kw,
            "keyword_provenance": provenance,
            "topics": "",
            "primary_topic": "",
            "categories": "",
            "network_relevance_score": 0,
            "network_relevant": False,
            "_core": bool(spec.get("core", False)),
            "_abstract": "",
        })
    rows = dedupe(rows)
    print(f"DBLP-HTML {spec['name']} {year}: kept {len(rows)} from {len(entries)} entries", flush=True)
    return rows



def ipdps_official(spec, year):
    """Collect IPDPS main-conference contributed papers from official programs.

    2023-2024: the IPDPS advance-program HTML embeds full title/author data
    inside rows labelled Parallel Technical Sessions.
    2025: Linklings' at-a-glance page provides all main-conference presentation
    slots; best-paper presentations duplicate papers and are removed by title.
    2026: Linklings' By Event Type page exposes an explicit Papers section,
    separate from workshops, tutorials, keynotes, and social events.
    """
    rows = []

    def make_row(title, authors, url, abstract=""):
        title = norm(title).rstrip(".")
        authors = norm(authors)
        if not title or not authors:
            return
        kw, provenance = _usenix_keywords(title, abstract)
        rows.append({
            "title": title,
            "authors": authors,
            "venue": spec["name"],
            "raw_venue": spec["name"],
            "year": year,
            "venue_kind": "conference",
            "source_id": "",
            "doi": "",
            "url": url,
            "openalex_id": "",
            "metadata_source": "official IPDPS program",
            "paper_type": "main conference paper",
            "keywords": kw,
            "keyword_provenance": provenance,
            "topics": "",
            "primary_topic": "",
            "categories": "",
            "network_relevance_score": 0,
            "network_relevant": False,
            "_core": bool(spec.get("core", False)),
            "_abstract": norm(abstract),
        })

    if year in {2023, 2024}:
        url = f"https://www.ipdps.org/ipdps{year}/{year}-advance-program.html"
        soup = BeautifulSoup(get_html(url), "html.parser")

        def parse_program_li(li):
            """Split malformed schedule list items into individual papers.

            The 2023 program has two HTML defects: one <li> contains two papers,
            and another contains two papers where the second title is split
            across adjacent <em> tags.  Treat adjacent <em> tags as one title;
            a later <em> after author text starts a new paper.
            """
            container = li.find("p") or li
            papers = []
            current = None
            for node in container.children:
                name = getattr(node, "name", None)
                if name == "em":
                    title_part = norm(node.get_text(" ", strip=True))
                    if not title_part:
                        continue
                    if current is None or current["authors"]:
                        current = {"title": title_part, "authors": ""}
                        papers.append(current)
                    else:
                        current["title"] = norm(current["title"] + " " + title_part)
                    continue
                if name == "br":
                    continue
                if hasattr(node, "get_text"):
                    txt = norm(node.get_text(" ", strip=True))
                else:
                    txt = norm(str(node))
                if txt and current is not None:
                    current["authors"] = norm(current["authors"] + " " + txt)
            return [p for p in papers if p["title"] and p["authors"]]

        for tr in soup.find_all("tr"):
            cells = tr.find_all("td", recursive=False)
            if len(cells) < 2:
                continue
            left = norm(cells[0].get_text(" ", strip=True))
            low = left.lower()
            if "parallel technical" not in low and "best paper" not in low:
                continue
            right = cells[1]
            for li in right.find_all("li"):
                for paper in parse_program_li(li):
                    make_row(paper["title"], paper["authors"], url)

    elif year == 2025:
        url = "https://ssl.linklings.net/conferences/ipdps/ipdps2025_program/views/at_a_glance.html"
        soup = BeautifulSoup(get_html(url), "html.parser")
        for slot in soup.select(".slot-wrapper"):
            title_tag = slot.select_one(".slot-title")
            authors_tag = slot.select_one(".author-names")
            if title_tag is None or authors_tag is None:
                continue
            title = norm(title_tag.get_text(" ", strip=True))
            authors = norm(authors_tag.get_text(" ", strip=True))
            abstract_tag = slot.select_one(".slot-abstract")
            abstract = norm(abstract_tag.get_text(" ", strip=True)) if abstract_tag else ""
            make_row(title, authors, url, abstract)

    elif year == 2026:
        url = "https://ssl.linklings.net/conferences/ipdps/ipdps2026_program/views/by_sub_type.html"
        soup = BeautifulSoup(get_html(url), "html.parser")
        papers_container = None
        for section in soup.select(".section-title"):
            if norm(section.get_text(" ", strip=True)).lower() == "papers":
                papers_container = section.parent.find_next_sibling("div", class_="section-entry")
                break
        if papers_container is None:
            raise RuntimeError("IPDPS 2026: explicit Papers section not found")
        for slot in papers_container.select(".slot-entry"):
            title_tag = slot.select_one(".slot-title")
            authors_tag = slot.select_one(".slot-authors")
            if title_tag is None or authors_tag is None:
                continue
            title = norm(title_tag.get_text(" ", strip=True))
            authors = norm(authors_tag.get_text(" ", strip=True))
            abstract_tag = slot.select_one(".slot-abstract")
            abstract = norm(abstract_tag.get_text(" ", strip=True)) if abstract_tag else ""
            make_row(title, authors, url, abstract)
    else:
        return []

    # Best-paper plenaries can repeat papers already mapped to a technical
    # session. For this venue the paper title is the stable identity.
    by_title = {}
    for r in rows:
        key = slug(r["title"])
        if key not in by_title:
            by_title[key] = r
    rows = sorted(by_title.values(), key=lambda r: r["title"].lower())

    expected = {int(k): int(v) for k, v in spec.get("expected_counts", {}).items()}
    if year in expected and len(rows) != expected[year]:
        raise RuntimeError(
            f"IPDPS {year}: parsed {len(rows)} unique main papers; expected {expected[year]}"
        )
    print(f"IPDPS-OFFICIAL {year}: kept {len(rows)} unique main papers", flush=True)
    return rows


def topcsuniv_conference(spec, year):
    """Collect the published INFOCOM main-track papers from TopCsUniv.

    The source exposes DOI, title, and authors and paginates at 100 records.
    We require the parsed row count to equal the edition's declared count.
    """
    if year == 2027:
        return []
    base = spec["url_template"].format(year=year)
    rows = []
    declared = None
    total_pages = 1

    for page in range(1, 20):
        url = base if page == 1 else base.rstrip("/") + f"/page/{page}/"
        soup = BeautifulSoup(get_html(url), "html.parser")

        if page == 1:
            h2 = soup.find("h2")
            h2_text = norm(h2.get_text(" ", strip=True) if h2 else "")
            m = re.search(rf"\b{year}\b.*?(\d+)\s+papers", h2_text, re.I)
            if not m:
                raise RuntimeError(f"{spec['name']} {year}: cannot parse declared paper count from {h2_text!r}")
            declared = int(m.group(1))
            pager = soup.select_one("nav.explorer-pagination span")
            if pager:
                pm = re.search(r"(\d+)\s*/\s*(\d+)", norm(pager.get_text(" ", strip=True)))
                if pm:
                    total_pages = int(pm.group(2))

        paper_nodes = soup.select("ol.explorer-papers > li")
        for li in paper_nodes:
            title_tag = li.select_one("a.paper-title")
            authors_tag = li.select_one("p.explorer-authors")
            if title_tag is None or authors_tag is None:
                continue
            title = norm(title_tag.get_text(" ", strip=True)).rstrip(".")
            authors = norm(authors_tag.get_text(" ", strip=True))
            href = norm(title_tag.get("href"))
            doi = ""
            if "doi.org/" in href.lower():
                doi = href.lower().split("doi.org/", 1)[1].strip("/")
            kw, provenance = _usenix_keywords(title, "")
            rows.append({
                "title": title,
                "authors": authors,
                "venue": spec["name"],
                "raw_venue": spec["name"],
                "year": year,
                "venue_kind": "conference",
                "source_id": "",
                "doi": doi,
                "url": href or url,
                "openalex_id": "",
                "metadata_source": "TopCsUniv published main-track inventory",
                "paper_type": "conference paper",
                "keywords": kw,
                "keyword_provenance": provenance,
                "topics": "",
                "primary_topic": "",
                "categories": "",
                "network_relevance_score": 0,
                "network_relevant": False,
                "_core": bool(spec.get("core", False)),
                "_abstract": "",
            })

        print(
            f"TOPCSUNIV {spec['name']} {year}: page {page}/{total_pages}, "
            f"page_records={len(paper_nodes)}, cumulative={len(rows)}",
            flush=True,
        )
        if page >= total_pages:
            break
        time.sleep(0.05)

    rows = dedupe(rows)
    if declared is None or len(rows) != declared:
        raise RuntimeError(
            f"{spec['name']} {year}: parsed {len(rows)} papers but source declares {declared}"
        )
    print(f"TOPCSUNIV {spec['name']} {year}: validated {len(rows)} published papers", flush=True)
    return rows


def dblp_toc_api_conference(spec, year):
    """Collect one proceedings volume from DBLP's exact TOC JSON API.

    The TOC query is much more reliable than DBLP's human-facing HTML and
    avoids fuzzy venue search. DBLP caps a response at 100 hits, so paginate
    with the documented first-hit offset.
    """
    if year == 2027:
        return []
    toc = spec["toc_template"].format(year=year)
    url = "https://dblp.org/search/publ/api"
    rows = []
    offset = 0
    total = None
    while total is None or offset < total:
        data = get_json(
            url,
            params={
                "format": "json",
                "h": 100,
                "f": offset,
                "q": f"toc:{toc}:",
            },
            attempts=6,
            pause=1.0,
        )
        hits = (data.get("result") or {}).get("hits") or {}
        total = int(hits.get("@total") or 0)
        batch = hits.get("hit") or []
        if isinstance(batch, dict):
            batch = [batch]
        if not batch:
            break

        for hit in batch:
            info = hit.get("info") or {}
            if int(info.get("year") or 0) != int(year):
                continue
            title = norm(info.get("title")).rstrip(".")
            if not title:
                continue

            raw_authors = (info.get("authors") or {}).get("author") or []
            if isinstance(raw_authors, (str, dict)):
                raw_authors = [raw_authors]
            authors = []
            for a in raw_authors:
                name = norm(a.get("text") if isinstance(a, dict) else a)
                # DBLP appends a four-digit disambiguation suffix to common names.
                name = re.sub(r"\s+\d{4}$", "", name)
                if name:
                    authors.append(name)

            doi = norm(info.get("doi")).lower()
            ee = info.get("ee") or ""
            if isinstance(ee, list):
                ee = next((x for x in ee if "doi.org/" in str(x).lower()), ee[0] if ee else "")
            link = norm(ee) or norm(info.get("url"))
            if not doi and "doi.org/" in link.lower():
                doi = link.lower().split("doi.org/", 1)[1]

            kw, provenance = _usenix_keywords(title, "")
            rows.append({
                "title": title,
                "authors": "; ".join(authors),
                "venue": spec["name"],
                "raw_venue": norm(info.get("venue")) or spec["name"],
                "year": year,
                "venue_kind": "conference",
                "source_id": "",
                "doi": doi,
                "url": link,
                "openalex_id": "",
                "metadata_source": "DBLP exact TOC JSON API",
                "paper_type": norm(info.get("type")) or "conference paper",
                "keywords": kw,
                "keyword_provenance": provenance,
                "topics": "",
                "primary_topic": "",
                "categories": "",
                "network_relevance_score": 0,
                "network_relevant": False,
                "_core": bool(spec.get("core", False)),
                "_abstract": "",
            })

        sent = int(hits.get("@sent") or len(batch))
        if sent <= 0:
            break
        offset += sent
        print(
            f"DBLP-TOC {spec['name']} {year}: {offset}/{total} records fetched",
            flush=True,
        )
        time.sleep(0.05)

    rows = dedupe(rows)
    print(f"DBLP-TOC {spec['name']} {year}: kept {len(rows)}", flush=True)
    return rows


def mobicom_official(spec, year, url, program=False):
    soup = BeautifulSoup(get_html(url), "html.parser")
    rows = []
    seen = set()
    skip = (
        "accepted papers","summer round","winter round","program","session ",
        "workshop","tutorial","registration","break","lunch","keynote",
        "test-of-time","test of time","poster","demo","student research",
    )

    for li in soup.find_all("li"):
        if li.find("li"):
            continue
        parts = [norm(x) for x in li.stripped_strings if norm(x)]
        if len(parts) < 2:
            continue
        full = " ".join(parts)
        m = re.search(r"\bAuthors?\s*:\s*", full, flags=re.I)
        if m:
            title = norm(full[:m.start()])
            authors = norm(full[m.end():])
        else:
            title = parts[0]
            authors = " ".join(parts[1:])

        low = title.lower().strip()
        if len(title) < 10 or low.startswith(skip):
            continue
        if low.startswith(("paper:", "room:", "day ")):
            continue
        # A research-paper author line nearly always contains an affiliation in
        # parentheses or multiple author separators. This filters navigation,
        # room names, and workshop links from program pages.
        if not ("(" in authors or "," in authors or ";" in authors):
            continue
        if program and any(x in low for x in ("award talk", "work-in-progress")):
            continue

        key = slug(title)
        if not key or key in seen:
            continue
        seen.add(key)
        kw, provenance = _usenix_keywords(title, "")
        rows.append({
            "title": title.rstrip("."),
            "authors": authors,
            "venue": spec["name"],
            "raw_venue": spec["name"],
            "year": year,
            "venue_kind": "conference",
            "source_id": "",
            "doi": "",
            "url": url,
            "openalex_id": "",
            "metadata_source": "official program page" if program else "official accepted-paper page",
            "paper_type": "conference paper",
            "keywords": kw,
            "keyword_provenance": provenance,
            "topics": "",
            "primary_topic": "",
            "categories": "",
            "network_relevance_score": 0,
            "network_relevant": False,
            "_core": bool(spec.get("core", False)),
            "_abstract": "",
        })

    # Other editions render a paper as one leaf paragraph/div with title and
    # author spans but no explicit "Authors:" label.
    if len(rows) < int(spec.get("hard_min", 1)):
        for tag in soup.find_all(["p","div"]):
            if tag.find(["p","div"], recursive=False):
                continue
            parts = [norm(x) for x in tag.stripped_strings if norm(x)]
            if len(parts) < 2:
                continue
            title = parts[0]
            authors = " ".join(parts[1:])
            low = title.lower().strip()
            if len(title) < 10 or low.startswith(skip):
                continue
            if not ("(" in authors or "," in authors or ";" in authors):
                continue
            key = slug(title)
            if key in seen:
                continue
            seen.add(key)
            kw, provenance = _usenix_keywords(title, "")
            rows.append({
                "title": title.rstrip("."), "authors": authors, "venue": spec["name"],
                "raw_venue": spec["name"], "year": year, "venue_kind":"conference",
                "source_id":"", "doi":"", "url":url, "openalex_id":"",
                "metadata_source":"official program page" if program else "official accepted-paper page",
                "paper_type":"conference paper", "keywords":kw, "keyword_provenance":provenance,
                "topics":"", "primary_topic":"", "categories":"",
                "network_relevance_score":0, "network_relevant":False,
                "_core":bool(spec.get("core",False)), "_abstract":"",
            })

    # Some accepted pages render title/author pairs as headings plus paragraphs.
    if len(rows) < int(spec.get("hard_min", 1)):
        for h in soup.find_all(["h3","h4","h5"]):
            title = norm(h.get_text(" ", strip=True))
            if not title or title.lower().startswith(skip):
                continue
            nxt = h.find_next_sibling()
            while nxt is not None and not norm(nxt.get_text(" ", strip=True) if hasattr(nxt,"get_text") else ""):
                nxt = nxt.find_next_sibling()
            if nxt is None:
                continue
            authors = norm(nxt.get_text(" ", strip=True)) if hasattr(nxt,"get_text") else ""
            authors = re.sub(r"^Authors?\s*:\s*", "", authors, flags=re.I)
            if len(title) < 10 or len(authors) < 5:
                continue
            key = slug(title)
            if key in seen:
                continue
            seen.add(key)
            kw, provenance = _usenix_keywords(title, "")
            rows.append({
                "title": title.rstrip("."), "authors": authors, "venue": spec["name"],
                "raw_venue": spec["name"], "year": year, "venue_kind":"conference",
                "source_id":"", "doi":"", "url":url, "openalex_id":"",
                "metadata_source":"official program page" if program else "official accepted-paper page",
                "paper_type":"conference paper", "keywords":kw, "keyword_provenance":provenance,
                "topics":"", "primary_topic":"", "categories":"",
                "network_relevance_score":0, "network_relevant":False,
                "_core":bool(spec.get("core",False)), "_abstract":"",
            })

    rows = dedupe(rows)
    print(f"MOBICOM-OFFICIAL {year}: kept {len(rows)}", flush=True)
    return rows


def openalex_issn_conference(spec, year):
    source_ids = []
    for issn in spec.get("issns", []):
        try:
            s = get_json(f"{OPENALEX}/sources/issn:{issn}")
        except Exception as e:
            print(f"WARNING OpenAlex ISSN {issn}: {e}", file=sys.stderr)
            continue
        sid = norm(s.get("id"))
        if sid and sid not in source_ids:
            source_ids.append(sid)
            print(f"ISSN {issn} -> {s.get('display_name')} ({sid})", flush=True)
    rows = collect_works(
        source_ids, year,
        venue_override=spec["name"], kind="conference", core=spec.get("core", False)
    )
    rows = dedupe(rows)
    print(f"OPENALEX-ISSN {spec['name']} {year}: kept {len(rows)}", flush=True)
    return rows


def imc_2023_program(spec, year, url):
    soup = BeautifulSoup(get_html(url), "html.parser")
    rows = []
    seen = set()

    # The 2023 schedule nests each paper under its session. Identify papers by
    # their title anchor, then read the Long/Short marker, authors, and abstract
    # from the containing list item rather than requiring a leaf DOM node.
    for a in soup.find_all("a", href=True):
        title = norm(a.get_text(" ", strip=True))
        if len(title) < 10:
            continue
        li = a.find_parent("li")
        if li is None:
            continue
        parts = [norm(x) for x in li.stripped_strings if norm(x)]
        try:
            pos = parts.index(title)
        except ValueError:
            continue
        tail = parts[pos + 1:]
        type_pos = next((i for i,x in enumerate(tail) if x.lower() in {"long","short"}), None)
        if type_pos is None:
            continue
        ptype = tail[type_pos].title()
        after_type = tail[type_pos + 1:]
        if not after_type:
            continue

        abstract_pos = next(
            (i for i,x in enumerate(after_type) if x.lower().startswith("abstract:")),
            None,
        )
        if abstract_pos is None or abstract_pos == 0:
            continue
        authors = norm(" ".join(after_type[:abstract_pos]))
        abstract = norm(after_type[abstract_pos])
        abstract = re.sub(r"^abstract\s*:\s*", "", abstract, flags=re.I)
        if len(authors) < 5:
            continue

        key = slug(title)
        if key in seen:
            continue
        seen.add(key)
        kw, provenance = _usenix_keywords(title, abstract)
        rows.append({
            "title": title.rstrip("."),
            "authors": authors,
            "venue": spec["name"],
            "raw_venue": spec["name"],
            "year": year,
            "venue_kind": "conference",
            "source_id": "",
            "doi": "",
            "url": urljoin(url, a.get("href") or ""),
            "openalex_id": "",
            "metadata_source": "official IMC program page",
            "paper_type": ptype,
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

    rows = dedupe(rows)
    print(f"IMC-PROGRAM {year}: kept {len(rows)}", flush=True)
    return rows


def sigcomm_official(spec, year):
    url = spec["official_urls"].get(str(year))
    if not url:
        return []
    soup = BeautifulSoup(get_html(url), "html.parser")
    rows = []

    def add_row(title, authors, note=""):
        title = norm(title).rstrip(".")
        authors = norm(authors)
        if not title or not authors:
            return
        rows.append({
            "title": title,
            "authors": authors,
            "venue": "SIGCOMM",
            "raw_venue": "ACM SIGCOMM",
            "year": year,
            "venue_kind": "conference",
            "source_id": "",
            "doi": "",
            "url": url,
            "openalex_id": "",
            "metadata_source": "official SIGCOMM accepted-paper page" + (f" ({note})" if note else ""),
            "paper_type": "conference paper",
            "keywords": "",
            "keyword_provenance": "",
            "topics": "",
            "primary_topic": "",
            "categories": "",
            "network_relevance_score": 0,
            "network_relevant": False,
            "_core": True,
        })

    if year == 2023:
        for h in soup.find_all("h2"):
            parent = h.find_parent("tr") or h.find_parent("li") or h.parent
            p = parent.find("p") if parent else None
            if p:
                add_row(h.get_text(" ", strip=True), p.get_text(" ", strip=True))

    elif year == 2024:
        ps = [p for p in soup.find_all("p") if norm(p.get_text(" ", strip=True))]
        if len(ps) % 2 != 0:
            raise RuntimeError(f"SIGCOMM 2024 unexpected paragraph count: {len(ps)}")
        for i in range(0, len(ps), 2):
            title = norm(ps[i].get_text(" ", strip=True))
            title = re.sub(r"\s+(Research|Experience)\s+Track$", "", title, flags=re.I)
            add_row(title, ps[i+1].get_text(" ", strip=True))

    elif year == 2025:
        ps = [p for p in soup.find_all("p") if norm(p.get_text(" ", strip=True))]
        # First paragraph is descriptive prose; the remainder is title/author pairs.
        if ps and "program will cover" in norm(ps[0].get_text(" ", strip=True)).lower():
            ps = ps[1:]
        if len(ps) % 2 != 0:
            raise RuntimeError(f"SIGCOMM 2025 unexpected paragraph count after intro: {len(ps)}")
        for i in range(0, len(ps), 2):
            add_row(ps[i].get_text(" ", strip=True), ps[i+1].get_text(" ", strip=True))

    elif year == 2026:
        declared = None
        for p in soup.find_all("p"):
            m = re.search(r"The following\s+(\d+)\s+papers have been accepted", norm(p.get_text(" ", strip=True)), re.I)
            if m:
                declared = int(m.group(1))
                break
        for tr in soup.find_all("tr"):
            b = tr.find("b")
            span = tr.find("span", class_="table-description")
            if b and span:
                add_row(
                    b.get_text(" ", strip=True),
                    span.get_text(" ", strip=True),
                    note=f"page declares {declared} papers; DOM contains paper rows parsed here" if declared else "",
                )
        if declared is not None and declared != len(rows):
            print(
                f"WARNING SIGCOMM 2026 official page declares {declared} papers "
                f"but exposes {len(rows)} parseable paper rows",
                file=sys.stderr,
            )

    else:
        return []

    rows = dedupe(rows)
    for r in rows:
        categorize(r)
    return rows


def conext_official(spec, year):
    source = spec["official_sources"].get(str(year))
    if not source:
        return []
    url = source["url"]
    soup = BeautifulSoup(get_html(url), "html.parser")
    rows = []

    def make_row(title, authors, paper_url=None, abstract="", paper_type="conference paper"):
        title = norm(title).rstrip(".")
        authors = norm(authors)
        if not title or not authors:
            return
        row = {
            "title": title,
            "authors": authors,
            "venue": "CoNEXT",
            "raw_venue": "ACM CoNEXT",
            "year": year,
            "venue_kind": "conference",
            "source_id": "",
            "doi": "",
            "url": paper_url or url,
            "openalex_id": "",
            "metadata_source": "official CoNEXT accepted-paper/program page",
            "paper_type": paper_type,
            "keywords": "",
            "keyword_provenance": "",
            "topics": "",
            "primary_topic": "",
            "categories": "",
            "network_relevance_score": 0,
            "network_relevant": False,
            "_core": True,
            "_abstract": norm(abstract),
        }
        if paper_url and "dl.acm.org/doi/" in paper_url:
            row["doi"] = paper_url.split("dl.acm.org/doi/", 1)[1].split("?",1)[0].strip("/")
        rows.append(row)

    if year in {2023, 2024}:
        for li in soup.find_all("li"):
            b = li.find("b")
            if not b:
                continue
            title = b.get_text(" ", strip=True)
            # Extract author text from the entry after the title node.
            clone = BeautifulSoup(str(li), "html.parser")
            bb = clone.find("b")
            if bb:
                bb.decompose()
            authors = clone.get_text(" ", strip=True)
            make_row(title, authors)

    elif year == 2025:
        for li in soup.find_all("li"):
            strong = li.find("strong")
            text = norm(li.get_text(" ", strip=True))
            if not strong or "ACM DL" not in text or "PDF" not in text:
                continue

            # The Long/Short and award labels are nested inside <strong>;
            # remove them before reading the paper title.
            sc = BeautifulSoup(str(strong), "html.parser")
            for span in sc.find_all("span"):
                span.decompose()
            title = norm(sc.get_text(" ", strip=True))

            title_box = strong.parent
            authors_box = title_box.find_next_sibling("div") if title_box else None
            authors = norm(authors_box.get_text(" ", strip=True) if authors_box else "")

            dl = None
            for a in li.find_all("a", href=True):
                href = norm(a.get("href"))
                if "dl.acm.org/doi/" in href and "/pdf/" not in href:
                    dl = href
                    break

            abstracts = []
            for p in li.find_all("p"):
                t = norm(p.get_text(" ", strip=True))
                if t:
                    abstracts.append(t)

            label = strong.find("span")
            ptype = norm(label.get_text(" ", strip=True)) if label else "conference paper"
            make_row(title, authors, dl, " ".join(abstracts), ptype)

    elif year == 2026:
        for li in soup.find_all("li"):
            u = li.find("u")
            if not u:
                continue
            title = u.get_text(" ", strip=True)
            clone = BeautifulSoup(str(li), "html.parser")
            uu = clone.find("u")
            if uu:
                uu.decompose()
            authors = clone.get_text(" ", strip=True)
            make_row(title, authors)

    rows = dedupe(rows)
    for r in rows:
        # Use abstract-aware deterministic terms when the official program
        # provides an abstract; otherwise categorization falls back to title.
        if not r["keywords"] and r.get("_abstract"):
            blob = (r["title"] + " " + r["_abstract"]).lower()
            terms = []
            for phrases in CATEGORIES.values():
                for phrase in phrases:
                    if phrase in blob and phrase not in terms:
                        terms.append(phrase)
            if terms:
                r["keywords"] = "; ".join(sorted(terms, key=len, reverse=True)[:12])
                r["keyword_provenance"] = "deterministic title/abstract category terms"
        categorize(r)
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

def static_csv_conference(spec, year):
    path = ROOT / spec["snapshot"]
    rows = []
    with path.open("r", encoding="utf-8", newline="") as f:
        for raw in csv.DictReader(f):
            if int(raw.get("year") or 0) != int(year):
                continue
            r = dict(raw)
            r["year"] = int(r["year"])
            r["network_relevance_score"] = int(r.get("network_relevance_score") or 0)
            r["network_relevant"] = str(r.get("network_relevant","")).lower() == "true"
            r["_core"] = bool(spec.get("core", False))
            rows.append(r)
    rows = dedupe(rows)
    print(f"STATIC {spec['name']} {year}: loaded {len(rows)} from {spec['snapshot']}", flush=True)
    return rows


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



def conference_rows_for(spec, year, force_live=False):
    provider = spec.get("live_provider") if force_live and spec.get("live_provider") else spec["provider"]

    if provider == "static_csv":
        return static_csv_conference(spec, year), spec["snapshot"]
    if provider == "sigcomm_official":
        return sigcomm_official(spec, year), "SIGCOMM official accepted-paper page"
    if provider == "conext_official":
        return conext_official(spec, year), "CoNEXT official accepted/program page"
    if provider == "nines":
        rows = nines_2026(spec) if year == 2026 else []
        return rows, "NINeS official accepted-paper page"
    if provider == "usenix":
        rows = [] if year == 2027 else usenix_conference(spec, year)
        return rows, "USENIX technical sessions"
    if provider == "crossref":
        return crossref_conference(spec, year), "Crossref"
    if provider == "openalex":
        rows = openalex_conference(spec, year)
        source = "OpenAlex pinned venue series"
        if not rows and str(year) in spec.get("doi_stems", {}):
            rows = crossref_doi_stem(spec, year, spec["doi_stems"][str(year)])
            source = "Crossref DOI family"
        if not rows and str(year) in spec.get("official_urls", {}):
            rows = official_list_conference(spec, year, spec["official_urls"][str(year)])
            source = "official accepted-paper page"
        return rows, source
    if provider == "openalex_crossref":
        rows = openalex_conference(spec, year)
        source = "OpenAlex pinned venue series"
        if not rows:
            rows = crossref_conference(spec, year)
            source = "Crossref fallback"
        return rows, source
    if provider == "official_list":
        url = spec.get("official_urls", {}).get(str(year))
        return (official_list_conference(spec, year, url) if url else []), "official accepted/program page"
    if provider == "dblp_html":
        url = spec["url_template"].format(year=year)
        return ([] if year == 2027 else dblp_html_conference(spec, year, url)), "DBLP static proceedings page"
    if provider == "dblp_toc_api":
        return dblp_toc_api_conference(spec, year), "DBLP exact TOC JSON API"
    if provider == "topcsuniv":
        return topcsuniv_conference(spec, year), "TopCsUniv published main-track inventory"
    if provider == "ipdps_official":
        return ipdps_official(spec, year), "official IPDPS main-conference program"
    if provider == "mixed_static":
        durl = spec.get("dblp_urls", {}).get(str(year))
        ourl = spec.get("official_urls", {}).get(str(year))
        if durl:
            return dblp_html_conference(spec, year, durl), "DBLP static proceedings page"
        if ourl:
            return official_list_conference(spec, year, ourl), "official accepted/program page"
        return [], "not yet available"
    if provider == "doi_family":
        stem = spec.get("doi_stems", {}).get(str(year))
        return (crossref_doi_stem(spec, year, stem) if stem else []), ("Crossref exact DOI family" if stem else "not yet available")
    if provider == "mixed_openalex_official":
        if year in set(spec.get("openalex_years", [])):
            return openalex_conference(spec, year), "OpenAlex pinned venue series"
        url = spec.get("official_urls", {}).get(str(year))
        return (official_list_conference(spec, year, url) if url else []), ("official accepted/program page" if url else "not yet available")
    if provider == "mobicom_official":
        url = spec.get("official_urls", {}).get(str(year))
        rows = mobicom_official(
            spec, year, url,
            program=year in set(spec.get("program_years", []))
        ) if url else []
        return rows, ("MobiCom official program/accepted page" if url else "not yet available")
    if provider == "openalex_issn":
        return (openalex_issn_conference(spec, year) if year != 2027 else []), "OpenAlex exact proceedings ISSN"
    if provider == "imc_mixed":
        url = spec.get("official_urls", {}).get(str(year))
        if year == 2023 and url:
            rows = imc_2023_program(spec, year, url)
        else:
            rows = official_list_conference(spec, year, url) if url else []
        return rows, ("IMC official program/accepted page" if url else "not yet available")
    raise RuntimeError(f"unknown provider {provider} for {spec['name']}")


def main():
    conference_rows = []
    coverage = []
    failures = []

    active_conferences = [s for s in CONFERENCES if s.get("enabled", True)]
    for spec in active_conferences:
        allowed = set(spec.get("years", YEARS))
        for year in YEARS:
            if year not in allowed:
                coverage.append({
                    "venue":spec["name"],"kind":"conference","year":year,"records":0,
                    "status":"not-applicable","source_ids":"","source_names":"",
                })
                continue

            provider = spec["provider"]
            if provider == "static_csv":
                rows = static_csv_conference(spec, year)
                source_name = spec["snapshot"]
            elif provider == "nines":
                rows = nines_2026(spec) if year == 2026 else []
                source_name = "NINeS official accepted-paper page"
            elif provider == "usenix":
                rows = [] if year == 2027 else usenix_conference(spec, year)
                source_name = "USENIX technical sessions"
            elif provider == "crossref":
                rows = crossref_conference(spec, year)
                source_name = "Crossref"
            elif provider == "openalex":
                rows = openalex_conference(spec, year)
                source_name = "OpenAlex pinned venue series"
                if not rows and str(year) in spec.get("doi_stems", {}):
                    rows = crossref_doi_stem(spec, year, spec["doi_stems"][str(year)])
                    source_name = "Crossref DOI family"
                if not rows and str(year) in spec.get("official_urls", {}):
                    rows = official_list_conference(spec, year, spec["official_urls"][str(year)])
                    source_name = "official accepted-paper page"
            elif provider == "openalex_crossref":
                rows = openalex_conference(spec, year)
                source_name = "OpenAlex pinned venue series"
                if not rows:
                    rows = crossref_conference(spec, year)
                    source_name = "Crossref fallback"
            elif provider == "official_list":
                url = spec.get("official_urls", {}).get(str(year))
                rows = official_list_conference(spec, year, url) if url else []
                source_name = "official accepted/program page"
            elif provider == "dblp_html":
                url = spec["url_template"].format(year=year)
                rows = [] if year == 2027 else dblp_html_conference(spec, year, url)
                source_name = "DBLP static proceedings page"
            elif provider == "mixed_static":
                durl = spec.get("dblp_urls", {}).get(str(year))
                ourl = spec.get("official_urls", {}).get(str(year))
                if durl:
                    rows = dblp_html_conference(spec, year, durl)
                    source_name = "DBLP static proceedings page"
                elif ourl:
                    rows = official_list_conference(spec, year, ourl)
                    source_name = "official accepted/program page"
                else:
                    rows = []
                    source_name = "not yet available"
            elif provider == "doi_family":
                stem = spec.get("doi_stems", {}).get(str(year))
                rows = crossref_doi_stem(spec, year, stem) if stem else []
                source_name = "Crossref exact DOI family" if stem else "not yet available"
            elif provider == "mixed_openalex_official":
                if year in set(spec.get("openalex_years", [])):
                    rows = openalex_conference(spec, year)
                    source_name = "OpenAlex pinned venue series"
                else:
                    url = spec.get("official_urls", {}).get(str(year))
                    rows = official_list_conference(spec, year, url) if url else []
                    source_name = "official accepted/program page" if url else "not yet available"
            elif provider == "mobicom_official":
                url = spec.get("official_urls", {}).get(str(year))
                rows = mobicom_official(
                    spec, year, url,
                    program=year in set(spec.get("program_years", []))
                ) if url else []
                source_name = "MobiCom official program/accepted page" if url else "not yet available"
            elif provider == "openalex_issn":
                rows = openalex_issn_conference(spec, year) if year != 2027 else []
                source_name = "OpenAlex exact proceedings ISSN"
            elif provider == "imc_mixed":
                url = spec.get("official_urls", {}).get(str(year))
                if year == 2023 and url:
                    rows = imc_2023_program(spec, year, url)
                else:
                    rows = official_list_conference(spec, year, url) if url else []
                source_name = "IMC official program/accepted page" if url else "not yet available"
            else:
                raise RuntimeError(f"unknown provider {provider} for {spec['name']}")

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

    tx_sources = discover_ieee_transactions_sources()
    min_sources = int(TX_CFG.get("minimum_sources", 1))
    if len(tx_sources) < min_sources:
        print(
            f"\nTRANSACTIONS SOURCE VALIDATION FAILED: "
            f"{len(tx_sources)} < {min_sources} matched journals",
            file=sys.stderr,
        )
        sys.exit(2)

    tx_rows = []
    source_ids = [norm(x.get("id")) for x in tx_sources]
    batch_size = int(TX_CFG.get("source_batch_size", 10))
    for year in YEARS:
        if year == 2027 and not TX_CFG.get("include_2027", True):
            continue
        year_rows = []
        for i in range(0, len(source_ids), batch_size):
            batch = source_ids[i:i+batch_size]
            rows = collect_works(batch, year, venue_override=None, kind="journal", core=False)
            year_rows.extend(rows)
            print(
                f"TRANSACTIONS {year}: sources {i+1}-{min(i+batch_size, len(source_ids))}/"
                f"{len(source_ids)}, cumulative {len(year_rows)}",
                flush=True,
            )
        year_rows = dedupe(year_rows)
        tx_rows.extend(year_rows)
        print(f"COUNT IEEE Transactions {year}: {len(year_rows)}", flush=True)

    conferences, tx, network = write_outputs(conference_rows, tx_rows, coverage)

    author_missing = sum(not r["authors"] for r in conferences)
    keyword_missing = sum(not r["keywords"] for r in conferences)
    if conferences and author_missing / len(conferences) > 0.02:
        failures.append(f"conference author metadata missing for {author_missing}/{len(conferences)} records")
    if keyword_missing:
        failures.append(f"conference keywords missing after fallback for {keyword_missing} records")
    expected_floor = sum(int(s["hard_min"]) for s in active_conferences)
    if len(conferences) < expected_floor:
        failures.append(f"conference corpus unexpectedly small: {len(conferences)} < {expected_floor}")
    if TX_CFG.get("enabled", True) and not tx:
        failures.append("IEEE Transactions network subset is empty")

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
