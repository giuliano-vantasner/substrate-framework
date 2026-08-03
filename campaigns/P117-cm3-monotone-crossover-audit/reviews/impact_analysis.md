# P117 Canonical Impact Analysis

The proposed package change is additive and LOW risk in the indexed framework
graph. GitNexus was refreshed with `gitnexus analyze --index-only` at framework
commit `acb0ce8`. Upstream impact queries at depth three for all eight public
functions in `src/substrate_framework/crossovers.py` report zero production
callers, zero affected processes, and zero affected modules.

The exact text and import audit finds callers only in P117's primary verifier
and `tests/test_crossovers.py`; the independent review deliberately imports no
crossover implementation. The graph result is therefore not used as proof of
absence: those concrete callers are covered by 45 primary checks and 15 package
tests.

The scientific source graph is separate from the code-call graph. Two direct
and three indirect hash-pinned descendants replay 148 checks. CM1 is a cycle
return and the other source descendants are pending. Candidate edges define
replay scope only; passing scripts do not promote their narratives or create
accepted authority.
