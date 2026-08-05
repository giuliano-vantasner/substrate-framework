# P186 Impact Analysis

P186 adds four dataclasses and four pure functions to the existing
`vacuum_polarization` module and exports them from the package root. It changes
no existing public signature, canonical identifier, tensor convention, or
accepted claim implementation. Focused regression covers the pre-existing
scalar D2, Dirac D4, generic beta, and affine-renormalization surfaces.

The refreshed GitNexus index contains 28,489 nodes, 43,791 edges, 393 clusters,
and two generic verifier flows. The Python index did not materialize the four
new factory functions as `Function` nodes, so function-name impact queries
returned `UNKNOWN`; this tool limitation is recorded rather than treated as a
clean bill of health. The corresponding four result dataclasses each report
LOW risk, two direct file-level importers, and no affected execution flow. One
direct importer is the package root; the other is the pre-existing
`nonabelian_vacuum_polarization` module, whose explicit import list contains
only the old scalar-D2 objects and therefore does not consume the new APIs.

A transaction comparison against base commit `e7b2888` reports 188 changed
symbols in 31 files, zero affected indexed processes, and LOW risk. The count
includes the full P186 campaign and earlier self-optimization edits since the
base. Repository text search identifies the new tests and P186 verifiers as
the only call sites. The source narrative graph is a separate MEDIUM governance
risk: GK3D3, GK3D4, and GK3D6 consume GK3D2 directly and must retain the free
matching coordinate; GK3D5 is transitive.

GitNexus analysis generated a temporary AGENTS block, `CLAUDE.md`, and `.claude`
skill copies. They were removed before framework staging because they are host
integration artifacts, not P186 evidence or project-authored process changes.

Overall implementation risk is LOW and source-governance propagation risk is
MEDIUM. The required controls are the 80 focused tests, primary and independent
symbolic verifiers, exact reverse-consumer replay, and one integrated promotion
gate.
