# P158 Additive Non-Abelian Scalar-Loop API Impact Analysis

P158 adds `SU2ScalarVacuumPolarization` and
`su2_scalar_qed2_vacuum_polarization` in a new pure canonical module and
exports them from the package. It changes no accepted symbol, connection sign,
curvature convention, Abelian kernel, or existing API.

A fresh single-worker GitNexus index contains 22,902 nodes, 36,080 edges, 342
clusters, and seven execution flows. Upstream impact for the new function is
LOW with no pre-existing impacted symbol, module, or process. The new class
has one direct package-export import and no affected process; package-wide
transitive import edges are graph overapproximation rather than callers.
Change detection against the source-aware freeze reports LOW risk, 77 new or
touched symbols in ten files, and zero affected processes. The process catalog
contains only unrelated three-step campaign check flows.

Exact lexical inspection closes the graph ambiguity. The new names occur only
in their definitions, the package export, P158's primary verifier, and the
focused test module. There is no pre-existing canonical consumer to migrate.
The source-level consumers are governed separately by the frozen 11-node graph:
W2 and W7 retain only their accepted conditional boundaries; M1 and M2 already
require a separately declared kinetic normalization; pending YM2 and GK1 gain
no authority and retain explicit corrections for their later adjudications.

The focused and adjacent replay passed 38 tests, the primary and independent
oracles passed 32 and 20 checks, and the frozen source graph replayed 132
source predicates through 21 graph checks. No canonical file changed after
those focused results. The terminal transaction must still run the one full
integrated validation gate after registry, release, disposition, generated
state, and memory agree. No impact-analysis debt remains.
