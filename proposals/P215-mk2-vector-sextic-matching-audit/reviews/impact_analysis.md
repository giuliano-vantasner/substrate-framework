# P215 impact analysis

P215 adds two pure APIs to `hls_reduction.py`, exports them from the package,
adds exact tests, promotes C-VEC-002, and qualifies MK2. It renames no symbol
and changes no existing API result.

Direct accepted consumers are C-EFT-001's generic elimination,
C-CHI-001's Pauli convention, and C-BPS-001's sextic convention. Their
statements and implementations remain unchanged; the new conditional API
calls the existing eliminator. C-VEC-001's SU(2) leading connection theorem
also remains unchanged and supplies a ceiling rather than a dependency.

The pinned reverse source consumers are MK3 through MK6, MR2, MR4, and MR6.
They replay cleanly as noncanonical evidence but cannot inherit the rejected
physical MK2 relation. MR2's pi-squared warning agrees with the accepted
conversion but remains pending for its own individual adjudication. Dirty
untracked phase-47 and phase-48 work is absent from source commit `6d1f4e0`
and the pinned inventory, so it is not allowed to alter this impact set.

Generated consumers are the claim index, release manifest, accepted claim
memory, migration queue, campaign decision memory, and migration effort
record. No Lean theorem, formal import, numerical solver, external data file,
or host-specific artifact changes. The promotion gate must replay package
tests, P059 and P140 predecessor verifiers, P215 primary and independent
routes, the source graph, generation, memory, and full repository validation.
