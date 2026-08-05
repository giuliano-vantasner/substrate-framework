# P187 Impact Analysis

P187 adds two result dataclasses and two pure factory functions in a new module,
then exports them from the package root. It changes no existing public
signature, canonical symbol, one-loop convention, scale orientation, or affine
boundary implementation. The new wrapper calls the accepted C-RGE-003 scale
ledger and C-VAC-003 kinetic ledger rather than duplicating either derivation.

The refreshed GitNexus index contains 28,719 nodes, 44,565 edges, 393 clusters,
and two generic execution flows. `inverse_length_scale_kinetic_evidence` has
one direct internal caller, LOW risk, and no affected flow.
`one_loop_scale_matched_kinetic_evidence` has no indexed upstream caller, LOW
risk, and no affected flow. The parent
`one_loop_inverse_energy_length_ledger` has two direct callers and the parent
`matter_induced_kinetic_evidence` has one direct and one indirect caller; both
are LOW risk with no affected flow. The graph does not attribute test calls to
the new public functions even with test inclusion requested, so repository
text and AST inventories supplement rather than silently trust that omission.

A transaction comparison against base commit `ba1cbaf` reports 111 changed
symbols in 28 files, zero affected indexed processes, and LOW risk. The count
includes the complete P187 proposal, evidence, implementation, tests, and
verifiers through commit `8acfaf2`. Repository search identifies the focused
tests and primary verifier as canonical API call sites; the independent review
intentionally imports neither new function nor either scientific parent API.

The source narrative graph carries a separate MEDIUM governance risk. GK3D1
and GK3D2 cite the later GK3D3 result in a narrative cycle but are already
qualified and cannot gain authority retroactively. GK3D4, GK3D5, and GK3D6 are
forward consumers. EL2 and HE5 are transitive. GK3D4 inherits the erased
boundary and parameter-free sector normalizations; GK3D5 attempts to supply a
physical infrared excitation; GK3D6 introduces an order-one mass factor but
still calls the common hierarchy and leading-log accuracy derived. Each must
be adjudicated individually under C-VAC-004's conditional ceiling.

GitNexus analysis generated a temporary AGENTS block, `CLAUDE.md`, and
`.claude` skill copies. They were removed with patch edits because they are
host integration artifacts, not framework evidence or project-authored
process changes. Overall implementation risk is LOW and source-governance
propagation risk is MEDIUM. Controls are the 51 focused tests, 31 primary
checks, 20 independent checks, exact reverse-consumer replay, and one
integrated promotion gate.
