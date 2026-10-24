# Recent paper corpus

This directory contains the machine-readable literature corpus used to ground the Advanced Networks project idea pool.

## Generated files

- `recent_networking_papers.csv` — one row per paper with title, authors, venue, year, DOI/URL, keywords, keyword provenance, topics, category assignments, and a reproducible network-relevance score.
- `recent_networking_papers.jsonl` — the same data in JSON Lines format.
- `PAPER_CORPUS_SUMMARY.md` — venue/year coverage, keyword provenance, category counts, and the most common keywords.
- `PAPER_CORPUS_COVERAGE.csv` — audit trail showing which venue/year queries returned metadata and which remain unavailable.

The source configuration is in `tools/research/paper_corpus_config.json`, and the builder is `tools/research/build_paper_corpus.py`.

## Provenance

**Bibliographic metadata.** The builder uses DBLP for paper title, authors, venue, year, DOI, and publication URL. The corpus records the DBLP key and URL when present.

**Keywords.** DOI-bearing records are enriched using OpenAlex work keywords. OpenAlex documents these as model-generated aboutness labels produced from a work's title, abstract, and venue; they are not author-supplied keywords. Rows without usable OpenAlex enrichment receive a deterministic title-derived fallback. The exact source is stored in `keyword_provenance`.

This distinction is intentional: the course material should never silently present inferred labels as author keywords.

**Categories.** Categories and `network_relevant` are deterministic heuristic labels generated from the configured topic vocabulary. They are for project-area discovery and reproducibility, not a claim of bibliometric ground truth.

## Scope

The conference corpus covers the requested venue families for 2023–2027 where published metadata exists. Future-year submissions are not counted as papers.

The IEEE Transactions portion is scoped to Transactions journals directly relevant to networking, distributed/mobile/cloud systems, multimedia delivery, communications, and dependability. Pulling every journal whose title begins with “IEEE Transactions” would add large bodies of unrelated work and would not be a meaningful advanced-networking corpus.

## Refreshing

Run:

```bash
python -m pip install requests beautifulsoup4
python tools/research/build_paper_corpus.py
```

The GitHub workflow `.github/workflows/refresh-paper-corpus.yml` can also regenerate the checked-in snapshot. Review `PAPER_CORPUS_COVERAGE.csv` after each refresh because newly released proceedings may appear in DBLP after the conference itself.
