# Recent paper corpus

This directory will contain the machine-readable literature corpus used to ground the Advanced Networks project idea pool.

## Current status

Corpus generation is being rebuilt **venue by venue**. Generated paper files are intentionally not checked in until each source adapter has passed validation for plausible paper counts and metadata completeness.

For each venue, the validator checks:

- paper count against a conservative minimum for each established year;
- author metadata coverage;
- DOI or canonical URL coverage;
- keyword coverage, with provenance recorded explicitly;
- sample records so the resolved proceedings can be manually sanity-checked.

The per-venue validator is:

```bash
python tools/research/validate_venue.py --venue SIGCOMM
```

The shared source configuration is in `tools/research/paper_corpus_config.json`.

## Target generated files

Once all requested venues have validated:

- `all_conference_papers.csv` — one row per collected conference paper;
- `recent_networking_papers.csv` — network-relevant papers used for project-area mining;
- `PAPER_CORPUS_COVERAGE.csv` — venue/year coverage and source provenance;
- `PAPER_CORPUS_SUMMARY.md` — compact audit summary;
- an IEEE Transactions dataset restricted to selected networking Transactions journals and then filtered to network-relevant papers.

## Keyword provenance

Publisher-provided keywords or index terms are kept when a source exposes them. Crossref subjects are kept when available. If neither is available, deterministic title/abstract-derived terms may be used, but those rows are labeled as inferred rather than presented as author keywords.

No unvalidated generated snapshot should be committed to this directory.
