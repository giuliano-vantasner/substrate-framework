# P179 Impact Analysis

P179 adds exact and numerical modules and exports without changing an existing
canonical symbol.

The GitNexus index was refreshed at framework HEAD `ae5449e` before analysis.
Upstream impact for `static_spherical_sine_gordon_reduction` returned zero
direct callers, zero affected processes, zero affected modules, and LOW risk.
The repository exposes only two generic verifier flows (`Run -> Check` and
`Main -> Check`), neither of which contains the new symbol. The change detector
found no affected indexed process; untracked new files were therefore audited
manually rather than treated as invisible proof of safety.

Direct consumers found by source search are the two new test modules, P179's
primary verifier, and the package export file. The numerical module directly
depends on the unchanged shared `solve_bvp_evidence` and `solve_ivp_evidence`
APIs. No existing caller, signature, convention, or accepted claim is changed.

The scientific graph impact is additive: C-STG-002 depends on C-STG-001,
C-PDE-005, and C-PDE-009; C-PDE-013 depends on C-STG-002 and C-PDE-012. SC2's
disposition, generated docs, release memory, and claim memory are affected.
TX1 is the only pending source reverse consumer and remains pending after one
recorded native replay. This is a LOW code risk with a MEDIUM governance
surface, controlled by claim-level review and the complete source graph replay.
