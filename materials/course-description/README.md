# Course description

Student-facing Persian course guide for **Advanced Networks — Fall 2026**.

This document uses the supplied Sharif LaTeX template rather than a separate course-specific layout.

- Source: `main.tex`
- Shared template files: `LaTeX_Common/`
- Engine: XeLaTeX
- CI: `.github/workflows/build-course-description.yml`
- Committed PDF: `course-description.pdf`
- Actions artifact: `advanced-networks-course-description`

## Template assets

The source preserves the template's original font locations:

- `LaTeX_Common/fonts/BNazanin/BNAZANIN.TTF`
- `LaTeX_Common/fonts/BNazanin/BNAZANB.TTF`
- `LaTeX_Common/fonts/LatinModernRoman/LMR_Regular.otf`

When those bundled template fonts are present, XeLaTeX uses them directly. CI has a packaged-font fallback so the document remains buildable in an environment where the local template font binaries are not available.

The Sharif cover layout is retained under `LaTeX_Common/cover/`.

On successful builds of `main`, CI rebuilds and commits `course-description.pdf` when it has changed. Pull requests build the PDF for verification but do not push generated files.

The appendix is derived from the current project taxonomy in `materials/assessments/PROJECT_IDEA_POOL.md` and the ranked domain/aspect counts in `materials/assessments/data/PROJECT_DOMAIN_ASPECT_COUNTS.csv`.
