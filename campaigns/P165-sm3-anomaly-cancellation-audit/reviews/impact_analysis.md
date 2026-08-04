# P165 Impact Analysis

GitNexus was refreshed at framework commit `cd163cf`: 24,168 nodes, 37,936
edges, 358 clusters, and six detected flows. The CLI reports the index current;
the MCP overview resource retained a cached four-commit-stale label, but symbol
impact queries resolved every new P165 API from the refreshed graph.

`chiral_anomaly_ledger` has one depth-one caller,
`five_row_chiral_anomaly_ledger`, inside the same new module. The three public
five-row functions have no external framework callers. Every queried symbol is
LOW risk and affects zero execution flows. Comparing P165 with `a4f780b` maps
119 changed graph symbols in 23 files to zero affected pre-existing symbols or
flows, also LOW risk.

The semantic source graph is wider than the code-call graph because predecessor
scripts cite SM3 in prose. Fifteen hash-pinned nodes replay 132 lexical and 132
runtime predicates plus fifteen assertions. All are native in the current
NumPy environment. WM1 and WM2 retype the table; WM5 and WM7 dynamically reuse
WM1, not SM3; FG3 keeps the per-generation anomaly coefficient symbolic; and
the remaining reverse references are prose provenance. Existing accepted
claims already qualify those tables and interpretations, so C-ANO-001 is an
additive compatible extension with no accepted API break.
