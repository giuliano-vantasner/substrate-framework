---
description: Classify pure spin-1 orbits and audit ME1 mean-field phase selection
author: vantasner
created: '2026-08-02T15:45:29Z'
updated: '2026-08-03T03:05:00Z'
tags:
- substrate-framework
- campaign-proposal
- spin-1
- migration-ME1
category: proposals
confidence: exploratory
status: archived
---
# P067 ME1 Spin-1 Orbit-Selection Audit

## Question and Positive Deliverable

P067 must deliver an importable exact classification of the spin expectation
attainable by every normalized complex pure spin-1 spinor, prove that the two
endpoint sets are precisely the polar and ferromagnetic orbits, and classify
all minimizers of the explicitly supplied fixed-density mean-field spin
functional for positive, negative, and zero coupling. A comparison of two
representatives or an honest source failure does not complete the campaign.

## Base Release and Provenance

The accepted base is `v0.60.0` at scientific commit `0089e63`; parent-effort
synchronization is commit `b51f139`. The predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. ME1 is
`/home/dan/substrate/merged-framework/bridges/phase-20/bridge_ME1_polar_phase_selection.py`,
18811 bytes, with inventory and reproduced SHA-256
`54d34a026b45d7ae01b53dae022cbcab61f380f4cda289d6a5862d2cc72adc71`.
The queue marks ME1 pending and names O1, ME2, and ME3; none supplies an
accepted dependency. The clean framework tree, history, seven-check physics
preflight, registry, current release, generated synopsis, package surface,
templates, and repository memory were inspected before this contract. Memory
contains no accepted spin-1 phase-selection theorem. ME1's executable body and
detailed output remain unopened.

## Invariants, Conventions, and Allowed Imports

The state is a general complex three-component pure spinor in the ordered
`m=(+1,0,-1)` basis with Hermitian norm `n=Psi^dagger Psi>0`. The standard
spin-1 matrices, global phase action, and spatial `SO(3)` representation must
be explicit. P067 may use exact complex linear algebra, Euclidean rotations,
the Cartesian decomposition `d=u+i v`, Cauchy-Schwarz, and polynomial
identities. It may assume the displayed functional and a real declared `c2`.
It may not import O1's polar phase, any material sign or coupling, an empirical
phase diagram, a continuum ground state, defect energetics, or a substrate
realization. Spin-independent terms are irrelevant only at fixed density;
other omitted terms remain outside the claim.

## Candidate Preregistration

The candidate set is frozen before ME1's executable is opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal ME1 | Source constructs a general complex normalized spinor and the supplied functional | `n=1`, `c2` | Only genuinely derived global and conditional statements survive | Hash-pinned execution plus data-flow and dependency audit |
| B | Singlet-amplitude identity | Standard spin-1 matrices | `n>0` | `|f|^2=n^2-|Psi_0^2-2Psi_+Psi_-|^2` gives the sharp interval | Exact symbolic expansion, scaling, and endpoint mutations |
| C | Cartesian orbit classification | Unitary spherical-to-Cartesian map and `SO(3)` action | `n>0` | Parallel real/imaginary parts are polar; orthogonal equal-norm parts are ferromagnetic | Constructive phase/rotation normal forms in both directions |
| D | Interval minimization | Supplied spin energy at fixed density | `c2` | Sign selects an endpoint; zero coupling leaves every state degenerate | Exact piecewise ledger and wrong-sign/density-power probes |
| E | Local stationary classification | Smooth pure-state sphere modulo symmetries | `c2`, `n` | Independent tangent variation agrees with the global endpoint theorem | Constrained stationary equations or second variation |
| F | Representative-only restriction | Only two named states are available | `n=1`, `c2` | Cannot establish orbit exhaustion or the positive global theorem | Counterexample search over general complex states |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure; general complex-state
coverage; constructive exhaustion of equality orbits; explicit density,
basis, phase, rotation, and energy conventions; correct coupling-sign and
zero-coupling limits; symmetry-native parameter economy; and independent exact
rederivation. The synopsis's values zero and one, the names `RP2` and `S2`, and
the printed `-c2/2` cannot select a proof or repair missing premises.

## Proposed Claim Delta

Provisional C-SPN-001 may state the exact pure spin-1 invariant, endpoint orbit
classification, and conditional minimizers of the supplied fixed-density
energy. It will depend on no pending migration unit. It may not establish the
sign or value of a material coupling, an atomic species, a spatially varying
condensate solution, an experimentally realized phase, a half-quantum vortex,
finite-temperature stability, a particle interpretation, or substrate
physics. ME1 will map only to the exact subclaims it actually supports.

## Implementation and Oracle Plan

A new pure module `spin1_mean_field.py` may expose the standard matrices,
spinor/Cartesian conversion, spin and singlet invariants, orbit classifiers,
and a fixed-density energy-selection ledger. SymPy exact expansion is the
primary oracle for polynomial identities. Constructive Cartesian normal forms
are the primary global-orbit oracle. An independent implementation will start
from the matrices and constrained geometry without importing the canonical
classification API. Mutations will change a matrix sign or normalization,
remove a complex phase, rescale density, reverse `c2`, pass a mixed-state
object, and sample only representatives. Focused package tests, source replay,
claim-level review, staged impact detection, and one full promotion-boundary
workflow gate will follow. No numerical quadrature, ODE/PDE solver, or
resolution study is appropriate for this exact finite-dimensional theorem.

## Attempts and Continuation

Attempt 0001 will preserve ME1's native process and audit each check after the
contract gate. If its state parameterization is incomplete, its orbit proof is
representative-only, or its density/sign logic is wrong, the failure is
recorded and candidates B-E continue. Candidate F cannot close the campaign.

## Debt Ledger

The campaign tracks representation, orbit-exhaustion, density, dependency,
interpretation, verification, and synchronization debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| ME1's executable constructions and output are unaudited | Hash-check, execute, preserve output, and trace each claimed bound, orbit, energy, and guard | discharged by attempt 0001 and the source audit |
| The endpoint values may be representative-only | Prove the invariant interval for every complex pure spinor and construct both equality normal forms | discharged by the singlet and Cartesian exact routes |
| Unit normalization may hide the physical density power | Expose `n`, prove homogeneity, and test `n != 1` | discharged with the exact `n^2` endpoint and density-three mutation |
| Pending O1/ME2/ME3 may be imported as authority | Audit source dependencies against the accepted registry and exclude all pending premises | discharged; all three remain excluded |
| The supplied functional may be inflated into a material or continuum theorem | Encode an explicit interpretation ceiling and mixed/omitted-term counterexamples | discharged in C-SPN-001 and the pure-state API guards |
| Verifier sensitivity, review, and canonical synchronization are incomplete | Complete exact mutations, independent rederivation, impact replay, claim review, disposition, release, docs, queue, and memory | discharged at the v0.61.0 promotion boundary |

## Review and Promotion Plan

The proposed claim receives an independent review of matrix conventions,
polynomial invariant, density scaling, constructive orbit exhaustion,
fixed-density minimizers, coupling boundary, and interpretation ceiling. ME1
receives a terminal disposition only through the authoritative queue with
durable source evidence. Accepted definitions move into the package with
focused tests; generated docs, release, claim registry, durable memory, and the
parent effort synchronize in one promotion transaction.

## Done Gate

P067 closes only when the importable positive classification, sensitive exact
oracles, independent rederivation, source adjudication, claim-level decision,
downstream replay, canonical synchronization, and empty campaign debt all
pass. Source checks or representative energy values alone are not completion.

## Adjudication Outcome

Candidates B, C, and D are accepted in C-SPN-001. Candidate A survives only
as qualified representative and unit-density arithmetic; Candidate E is not
selected because the exact global theorem makes a local Hessian redundant;
Candidate F is rejected. ME1 is qualified. The exact canonical route passes
33 checks, the independent route passes 13 checks, focused/governance replay
passes 30 tests, and the full workflow passes all 527 repository tests. The
v0.61.0 registry, release, queue, generated docs, and accepted memory agree.

## Cross-References

See release `v0.60.0`, ME1's generated source record, the parent migration
effort, and the accepted registry.
