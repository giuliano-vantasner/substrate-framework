---
description: Independent review of C-WID-001 conditional axial Ward and pion-pole theorem
author: vantasner-review
created: '2026-08-02T22:00:00Z'
updated: '2026-08-02T22:00:00Z'
tags:
- substrate-framework
- claim-review
- axial-ward-identity
category: decisions
confidence: established
status: archived
---
# C-WID-001 Claim Review

## Claim Under Review

C-WID-001 states an exact theorem conditional on one complete Minkowski
axial-current convention, equal-mass on-shell spinors, and a separately
declared form-factor PCAC source. It derives the normalized divergence,
retains pion-pole dominance as an additional premise, separates a regular
induced remainder, evaluates the pole-point residue, and proves that the
zero-transfer and chiral limits of the PCAC kernel do not commute. It assigns
no QCD, pion, nucleon, measured-coupling, or substrate interpretation.

## Sourced Inputs

The review reads release `v0.56.0`, the conditional ceilings C-SYM-001,
C-CHI-001, C-CHI-002, C-GMR-001, and C-QBL-003, the frozen P063 contract, PG4
at SHA-256 `e13e6853...`, attempts 0001 through 0005, both primary-literature
records, the source reproduction and data-flow audit, the canonical axial
module, focused tests, both exact verifiers, and the impact report. PG4's
physical-current, PCAC, pole-dominance, state, coupling, and substrate
headlines remain outside the proposed claim.

## Independence

The independent route imports no `axial_ward` API. It constructs explicit
Dirac gamma matrices and Breit-frame spinors, evaluates the axial and induced
terms with a fresh Minkowski contraction, performs the pole residue directly
with `sympy.residue`, and redoes the remainder and iterated-limit algebra from
the declared formulas. It shares no expected PG4 residual or source output.

## Verification Status

The maximum verdict is `symbolic_verified`. The primary verifier passes 31
checks and the independent route passes 20. All promoted expressions reduce
to exact evaluated matrices, rational functions, residues, or limits; no
unevaluated integral, root, or condition remains. The generalized PCAC source
and pole-dominance form are visibly declared premises rather than outputs of
the algebra.

## Sensitivity and Counterexamples

Omitting the induced `2M` scale breaks mass dimensions and changes the full
divergence. Explicit spinors fix the plus sign of the Minkowski `q^mu G_P`
term; reversing the pole sign prevents pointwise GT reduction. A finite
regular remainder preserves the pole residue but changes the off-zero Ward
residual. A nonzero coupling slope separates the zero-transfer and pion-pole
values. The two iterated pole-kernel limits are one and zero, while fixed-
ratio paths retain a continuum of values `1/(1+rho)`.

## Framework Compatibility

The claim is an additive conditional theorem and changes no accepted symbol.
It preserves every existing nonphysical ceiling and explicitly declares
Lorentz, spinor, current, PCAC, form-factor, regularity, and positivity
premises. Primary literature is used only to audit conventional scope; no
lattice result or empirical parameter is imported.

## Dependency and Consumer Replay

The accepted dependency closure is empty because the theorem begins from its
own declared current and PCAC premises rather than pretending that the prior
classical coordinate claims supply them. Consumers are the new pure module,
focused tests, P063 verifiers, governance, generated docs and memory, and
future current audits. GitNexus classifies the edit as additive; targeted and
full workflow replay remain the promotion gates.

## Competing Candidate Audit

Candidates A through E and structural criteria were frozen before PG4 was
opened. Candidates B and C are selected for convention closure, explicit
premise separation, correct residues and limits, and exact sensitivity.
Candidate A fails the full convention-sensitive matching. Candidate D adds a
field ontology without supplying the general result. No phenomenological
number selects the theorem.

## Four-Axis Decision

The axes support a new exact conditional theorem with no challenge or
supersession relationship.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: new dependency-free declared-current and PCAC theorem

## Promotion Transaction

Promotion adds C-WID-001 to release `v0.57.0`, archives P063 and this review,
exports and tests the canonical API, qualifies PG4, updates the editable
disposition registry, and regenerates the queue, docs, and accepted memory.
Primary, independent, focused, governance, graph-change, one full workflow,
and diff gates must pass.

## Continuation if Not Accepted

This clause is inactive because the exact conditional theorem is accepted. A
future physical-current claim must separately derive its action, symmetry,
states, current normalization, PCAC identity, pole coupling, and substrate
map rather than importing those nouns into this theorem.

## Done Gate

The claim-level debt is empty after canonical replay and synchronization. The
parent corpus effort remains active because later queue units are pending.

## Cross-References

See P063, PG4, `axial_ward.py`, `test_axial_ward.py`, C-GTR-001, release
`v0.57.0`, and the parent migration effort.
