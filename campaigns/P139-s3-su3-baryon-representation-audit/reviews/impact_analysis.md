# P139 impact analysis

P139 adds a pure `su3_representations.py` module and root-package exports. It
does not change C-LIE-001 generators, C-LIE-002 center functions, accepted WZW
or topology modules, numeric solvers, units, or any historical campaign. The
new APIs validate exact inputs and have no import-time simulation or output.

After indexing the working tree, GitNexus reports 19,489 nodes, 30,670 edges,
306 clusters, and eight generic campaign-check flows. Upstream impact for
`SU3Irrep` is LOW: the only depth-one dependent is the package export file,
there are no affected execution processes, and the depth-two list consists of
root-package importers rather than callers of the new API. `detect_changes`
reports LOW risk, one tracked `__all__` symbol, and no affected process. Direct
git status remains authoritative for the new untracked module and campaign
records.

The semantic novelty query returns no process and no preexisting general irrep
definition. Its nearest older definitions are `su3.py`, which provides only
explicit fundamental invariants and center operations, and `gauge_beta.py`,
which consumes separately supplied finite representation tables.

The frozen source graph covers S3, five declared dependencies, and thirteen
reverse consumers with overlap. All seventeen hashes and all 195 static
predicates are pinned; the 39-check graph replay passes. S2 and WZ3 retain
their already classified immutable alias-only replay paths backed by
`np.trapezoid`; S3 and all mutable P139 code have no compatibility event.

Focused package tests pass 31 checks, the primary verifier passes 28, and the
independent tableau review passes 16. Qualified consumers retain independent
accepted closures, duplicate WM2 gains no authority, and seven pending
consumers remain pending. Final risk is LOW; the remaining replay is the
claim/release/disposition/generated-memory transaction and one integrated gate.
