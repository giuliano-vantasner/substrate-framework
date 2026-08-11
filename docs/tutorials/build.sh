#!/usr/bin/env bash
# Build a tutorial document through the canonical chain MD -> LaTeX -> PDF.
#
# Usage: docs/tutorials/build.sh <tutorial-dir>
#   <tutorial-dir> must contain exactly one *.md source (the canonical document).
#   Produces <name>.tex and <name>.pdf next to it.
#
# Prerequisites: pandoc, xelatex (texlive-xetex + texlive-latex-recommended
# + texlive-latex-extra + texlive-fonts-recommended).
set -euo pipefail

dir="${1:?usage: build.sh <tutorial-dir>}"
cd "$dir"

sources=(*.md)
[[ ${#sources[@]} -eq 1 && -f ${sources[0]} ]] || {
  echo "error: $dir must contain exactly one .md source, found: ${sources[*]}" >&2
  exit 1
}
name="${sources[0]%.md}"

pandoc "$name.md" --standalone -V documentclass=article -V geometry:margin=2.5cm \
  --top-level-division=section -o "$name.tex"

xelatex -interaction=nonstopmode -halt-on-error "$name.tex" >/dev/null
xelatex -interaction=nonstopmode -halt-on-error "$name.tex" >/dev/null

rm -f "$name.aux" "$name.log" "$name.out" "$name.toc"
echo "built: $name.tex, $name.pdf"
