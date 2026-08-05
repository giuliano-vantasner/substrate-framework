# P200 Impact Analysis

P200 adds one dataclass, one exact function, package exports, and focused tests
inside the existing branching module. It changes no existing function
signature, output, normalization, convention, or accepted value.

The GitNexus index was refreshed from stale commit `1a58aa0` to exact P200
implementation commit `38bccd4`. Upstream impact for
`population_dependent_weight_ledger`, including tests at confidence at least
0.8 through depth three, reports no callers, processes, or affected modules
and low risk. The repository process inventory contains one generic
run-to-check process, which is unaffected. Change detection against base
`d5a8125` reports 45 changed symbols in 21 files, no affected symbols or
processes, and low risk.

Manual search identifies the package root, `tests/test_branching.py`, both P200
verifiers, the graph replay, the MD5 source mapping, and pending MD6. Historical
campaign and memory mentions of C-BRN-002 are review provenance rather than API
callers. The earlier P193 proposal was never accepted and concerned a distinct
duplicate composition surface.

The changed branching tests, existing branching tests, two exact verifiers,
and ten-node source graph must pass together. Registry, release, docs, queue,
and accepted memory change only at promotion. MD6 remains individually pending
and cannot import a material weight, isotope map, physical branch, reaction,
rate, or debt-closure conclusion from P200.
