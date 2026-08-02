---
description: Derive angular-defect energy ledgers and audit ME2 half-quantum selection
author: vantasner
created: '2026-08-03T03:20:00Z'
updated: '2026-08-03T04:20:00Z'
tags:
- substrate-framework
- campaign-proposal
- half-quantum-vortex
- migration-ME2
category: proposals
confidence: exploratory
status: archived
---
# P068 ME2 Half-Quantum Vortex Energetics Audit

## Question and Positive Deliverable

P068 must deliver importable exact ledgers for angular-defect self energy,
fixed-total-charge splitting across near and far scales, projective versus full
polar-order topology, and the stiffness/core threshold for a half-quantum pair
to beat one integer vortex. Reproducing `2*(1/2)^2=1/2` or rejecting ME2's
always-favored headline does not complete the campaign.

## Base Release and Provenance

The accepted base is `v0.61.0` at scientific commit `417d55e`; parent-effort
synchronization is commit `beb6ed2`. The predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. ME2 is
`/home/dan/substrate/merged-framework/bridges/phase-20/bridge_ME2_half_quantum_vortex.py`,
17211 bytes, with inventory and reproduced SHA-256
`40eec343312cc85d442471a224c0501071ea556308b517e5c8b1efe067a789e4`.
The generated queue marks ME2 pending and names ME1 and O1. ME1 is now
qualified through C-SPN-001; O1 remains pending. The clean framework tree,
history, seven-check preflight, registry, current release, accepted spin-one
module, generated synopsis, package searches, templates, and repository memory
were inspected before this contract. Memory contains no accepted half-quantum
vortex energy theorem. ME2's executable body and detailed output remain
unopened.

## Invariants, Conventions, and Allowed Imports

C-SPN-001 supplies only the projective polar ray orbit `RP2`. P068 may use
exact two-dimensional Dirichlet integration, fixed-degree Cauchy-Schwarz,
positive logarithmic scales, and explicit covering/deck transformations. The
spatial domain, total boundary charge, phase and director fields, independent
stiffnesses, core radii, separation scale, and core energies must remain
visible inputs. An isolated annular self energy is not a complete multi-defect
energy. A director half-turn is not a combined half-quantum vortex until the
condensate phase and full order parameter are supplied.

## Candidate Preregistration

The candidate set is frozen before ME2's executable is opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal ME2 | Its common prefactor and additive self energies represent the same fixed-boundary problem | `K,R,xi,q` | Narrow scalar arithmetic may survive; global preference and topology likely require missing premises | Hash-pinned execution and data-flow audit |
| B | Exact annular self energy | One angular field of declared degree on an annulus | `K,q,xi,R` | `pi*K*q^2*log(R/xi)` is exact and minimizes at uniform angular winding | Direct integration and circlewise lower bound |
| C | Fixed-charge shell ledger | Separated equal defects, matched near radius `d`, common far boundary | `n,Q,xi,d,R,K` | The far shell retains `Q^2`, so the total ratio is not generally `1/n` | One-defect, `d=xi`, `d=R`, and omitted-far-field mutations |
| D | Covering-space topology | Projective and full polar manifolds are separately typed | none | `pi1(RP2)=Z2`, while the full polar manifold has deck group `Z`; generator squares differ | Explicit deck composition and covering kernels |
| E | Two-stiffness/core threshold | Declared phase/director textures and core energies | `K_phase,K_dir,E_half,E_int` | A half pair is favored only under an explicit inequality, not convexity alone | Equal/unequal stiffness and core-energy mutations |
| F | Independent-copy ratio | Two noninteracting identical annuli with no shared far field | `K,L` | The ratio `1/2` is exact only for that conditional comparison | Type the domains and reject reuse at fixed total boundary charge |

## Selection Criteria and Blinding

Selection is ordered by accepted closure; exact domain and boundary typing;
correct logarithmic normalization; fixed-total-charge and separation limits;
explicit stiffness and core bookkeeping; correct cover composition; mutation
sensitivity; and parameter economy. The source's printed `1/2`, generalized
`1/n`, and familiar half-quantum label cannot select the physical verdict.

## Proposed Claim Delta

Provisional C-DEF-001 may state exact annular and matched-shell energy ledgers,
the two distinct polar topology groups, and a conditional half-pair preference
inequality. It may depend on C-SPN-001 only for the projective ray orbit. It may
not establish a material stiffness, core energy, condensate realization,
equilibrium separation, true finite-domain interaction solution, vortex
existence or stability, experimental phase, or substrate mechanism. ME2 will
map only to subclaims it actually supports.

## Implementation and Oracle Plan

A pure module `angular_defects.py` may expose exact annular energy, a
fixed-total-charge matched-shell ledger, polar deck transformations, and a
two-stiffness/core comparison. SymPy exact integration and algebra fit the
energy obligations; finite group/deck composition fits the topology. The
independent route will derive the circlewise degree lower bound and covering
groups without importing the canonical API. Mutations will remove the far
shell, change total charge, collapse the separation to the core, swap `Z2`
and `Z`, force equal stiffnesses, and hide core terms. No numerical quadrature,
PDE solve, or empirical comparator is appropriate for these exact conditional
ledgers. A true two-core finite-domain minimizer would be a different numerical
claim and is outside this campaign unless the exact shell model proves
insufficient for the positive object.

## Attempts and Continuation

Attempt 0001 will preserve ME2's native process and trace every energy and
topology check. If the source adds isolated self energies, omits far-field or
core terms, or conflates projective and full order parameters, that failure is
recorded and Candidates B-E continue. Candidate F cannot close P068 alone.

## Debt Ledger

The campaign tracks domain, interaction, topology, stiffness, core,
dependency, verification, and synchronization debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| ME2's executable and output are unaudited | Hash-check, execute, preserve output, and trace all four checks | discharged by attempt 0001 and source audit |
| The `1/2` ratio may compare independent copies rather than one fixed-boundary configuration | Type domains and derive the near/far fixed-charge ledger | discharged by the matched-shell theorem |
| RP2 may be conflated with the full polar condensate manifold | Construct both covers and compare generator squares | discharged by the explicit Z2 and Z deck groups |
| A common stiffness and zero core cost may be hidden | Expose independent stiffnesses and core energies and derive the preference inequality | discharged by the half-pair residual |
| Arbitrary `1/n` splitting may violate allowed topology | Classify allowed loop charges before applying convexity | discharged; RP2 and full polar groups remain distinct |
| Pending O1 may be imported as authority | Audit the source dependency and exclude all unaccepted physical premises | discharged; O1 remains excluded |
| Verifier sensitivity, review, and synchronization are incomplete | Complete exact mutations, independent derivation, impact replay, claim review, disposition, release, docs, queue, and memory | discharged at the v0.62.0 promotion boundary |

## Review and Promotion Plan

Any proposed claim receives independent review of the Dirichlet normalization,
degree lower bound, near/far ledger, cover groups, generator composition,
stiffness/core threshold, and interpretation ceiling. ME2 receives a terminal
disposition only through the authoritative queue with durable evidence.
Accepted logic moves into the package with focused tests and one full
promotion-boundary workflow gate.

## Done Gate

P068 closes only when the positive importable ledgers, sensitive exact
oracles, independent derivation, source adjudication, claim-level decision,
downstream replay, canonical synchronization, and empty campaign debt all
pass. A scalar convexity ratio or a source tally alone is not completion.

## Adjudication Outcome

Candidates B through E are accepted in C-DEF-001. Candidate A survives only
for independent-copy arithmetic, projective order two, and the scalar U1
guard; Candidate F is the vanished-far-shell endpoint rather than the complete
object. ME2 is qualified. The exact primary route passes 43 checks, the
independent route passes 17 checks, focused/governance replay passes 31 tests,
and the full workflow passes all 541 tests. The v0.62.0 registry, release,
queue, generated docs, and accepted memory agree.

## Cross-References

See C-SPN-001, P067, ME2's generated source record, release `v0.61.0`, and the
parent migration effort.
