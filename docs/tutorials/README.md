# Tutorials

Pedagogical tutorial documents. Each tutorial lives in its own directory with a
single canonical Markdown source; the LaTeX and PDF artifacts are generated from
it and committed alongside it (the reader-facing chain is MD -> LaTeX -> PDF).

## Prerequisites

- `pandoc`
- TeX Live: `texlive-xetex`, `texlive-latex-recommended`, `texlive-latex-extra`,
  `texlive-fonts-recommended`

## Build

```bash
docs/tutorials/build.sh docs/tutorials/<name>
```

The directory must contain exactly one `*.md` file. The script emits
`<name>.tex` (pandoc, standalone article) and `<name>.pdf` (xelatex, two
passes) next to the source and removes intermediate aux files.

## Conventions

- The `.md` file is the canonical source; never hand-edit the generated `.tex`.
- Math: pandoc markdown with `$...$` / `$$...$$`; explicit equation numbers via
  `\tag{n}` inside display math (continuous numbering per document, matching
  the style of the source preprints).
- Term-definition notes: pandoc footnotes (`[^id]`).
- Every external claim carries a reference (author, title, year, DOI or stable
  URL) in the document's References section.

## Contents

- `smoke/` — minimal document proving the build chain end to end.
