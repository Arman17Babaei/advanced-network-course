# Course description

Student-facing Persian course guide for **Advanced Networks — Fall 2026**.

- Source: `main.tex`
- Engine: XeLaTeX
- CI: `.github/workflows/build-course-description.yml`
- Committed PDF: `course-description.pdf`
- Actions artifact: `advanced-networks-course-description`

On successful builds of `main`, CI rebuilds and commits `course-description.pdf` when it has changed. Pull requests build the PDF for verification but do not push generated files.

The appendix is derived from the current project taxonomy in `materials/assessments/PROJECT_IDEA_POOL.md` and the ranked domain/aspect counts in `materials/assessments/data/PROJECT_DOMAIN_ASPECT_COUNTS.csv`.
