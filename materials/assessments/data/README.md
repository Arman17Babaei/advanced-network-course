# Recent networking paper corpus

This directory contains the machine-readable literature corpus used to ground the Advanced Networks project idea pool.

## Current corpus

The validated snapshot contains:

- **9,991 conference papers** from the requested conference series;
- **6,968 networking-relevant IEEE Transactions papers**;
- **16,959 unique records** in the combined corpus.

The active time window is **2023–2027**. As of 25 October 2026, the conference corpus is populated through the available 2026 proceedings; 2027 remains empty until actual publication/acceptance metadata exists.

## Files

- `all_conference_papers.csv` — complete collected conference inventory for the requested venue series.
- `ieee_transactions_network.csv` — combined networking-only IEEE Transactions subset.
- `master_paper_corpus.csv` — master combined corpus with explicit keyword provenance columns.
- `recent_networking_papers.csv` — analysis-facing copy of the combined corpus used for project-area mining.
- `PAPER_CORPUS_COVERAGE.csv` — venue/year coverage.
- `PAPER_CORPUS_SUMMARY.md` — generated counts, keyword provenance, and category statistics.
- `venues/` — frozen per-conference snapshots.
- `transactions/` — frozen per-journal networking subsets.

Each paper row contains title, authors, venue, year, DOI or canonical URL, keyword labels, keyword provenance, normalized categories, and source metadata where available. The assembled master also includes `source_keywords_or_index_terms` and `derived_keywords`, so source-provided terms are structurally separate from inferred labels.

## Conference coverage

The frozen conference snapshots cover:

- SIGCOMM
- CoNEXT
- NSDI
- ICNP
- INFOCOM
- SIGMETRICS / POMACS
- IMC
- ACM Multimedia
- NINeS
- MobiCom
- MMSys
- IPDPS
- ICDCS
- OSDI
- USENIX Security

Each venue was validated independently before its CSV was frozen. Validation checks yearly paper counts, author coverage, publication links, keyword availability, and sample records. Exact yearly counts are enforced where a reliable official count is known.

## IEEE Transactions

IEEE Transactions are intentionally handled differently from conference proceedings. The Transactions family is too broad to include indiscriminately, so only networking-relevant papers are retained.

Core networking journals are retained broadly. Adjacent journals are filtered using explicit networking/networked-systems signals in paper titles and paper-level keyword metadata. The checked-in journal snapshots include networking subsets from journals such as:

- IEEE Transactions on Networking
- IEEE Transactions on Network and Service Management
- IEEE Transactions on Mobile Computing
- IEEE Transactions on Wireless Communications
- IEEE Transactions on Communications
- IEEE Transactions on Vehicular Technology
- IEEE Transactions on Green Communications and Networking
- IEEE Transactions on Parallel and Distributed Systems
- IEEE Transactions on Cloud Computing
- IEEE Transactions on Multimedia
- IEEE Transactions on Dependable and Secure Computing
- IEEE Transactions on Network Science and Engineering

The combined assembler rejects Transactions rows that are not marked network-relevant.

## Keyword provenance

Keyword provenance is explicit:

- OpenAlex paper keywords are stored as **OpenAlex model-generated keywords**; they are not represented as author-supplied keywords.
- Publisher/Crossref keywords or subjects are retained when available.
- When a source exposes no usable keywords, deterministic title- or title/abstract-derived terms are generated and marked as inferred.

Current provenance totals are recorded in `PAPER_CORPUS_SUMMARY.md`.

## Reproducibility

Source configuration is versioned in:

`tools/research/paper_corpus_config.json`

The main reusable utilities are:

- `validate_venue.py` — validate one conference source/snapshot;
- `export_validated_venue.py` — freeze a validated conference snapshot;
- `validate_transaction_journal.py` — validate one networking Transactions subset;
- `export_transaction_journal.py` — freeze one validated journal subset;
- `assemble_validated_corpus.py` — validate and assemble the frozen snapshots into the master corpus;
- `fix_snapshot_text.py` — idempotent text-encoding normalization for snapshots.

The assembler is **fail-closed**: it refuses to generate a master corpus when required metadata is missing, conference coverage falls below configured thresholds, exact counts disagree where specified, or a Transactions row violates the networking-only invariant.
