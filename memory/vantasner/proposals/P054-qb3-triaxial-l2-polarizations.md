---
description: Audit QB3 through regular l=2 dynamics and temporal-rank-safe polarization algebra
author: vantasner
created: '2026-08-02T09:30:00Z'
updated: '2026-08-02T09:30:00Z'
tags:
- substrate-framework
- campaign-proposal
- l2-perturbation
- migration-QB3
category: proposals
confidence: exploratory
status: active
---
# P054 QB3 Triaxial l=2 and Polarization Audit

## Question and Positive Deliverable

P054 must produce the strongest positive nonaxisymmetric l=2 object naturally
supported by the accepted radial sine-Gordon and moment framework. The object
must distinguish exact m-degeneracy, triaxial spatial tensors, two TT basis
coordinates, and two independent temporal source modes. If QB3's claimed
eigenmode is not a solution of the full time-dependent perturbation problem,
that failure is preserved while Candidate B, C, or D continues to a positive
exact, Floquet, or finite-time construction.

## Base Release and Provenance

The accepted base is `v0.47.0` at framework commit `fd5ee0b`; its scientific
transaction is `b82b3f9`. QB3 is pending at `substrate@6d1f4e0`, path
`merged-framework/bridges/phase-16/bridge_QB3_triaxial_nonaxisymmetric.py`,
SHA-256 `e9626f2e4829084635386eea271d0abdd39c81dfcd6899765d2f4bffac83e0c8`.
Its cited FS2, GW1, GW3, M2, P3D1 through P3D4, QB1, and future QB4 are
navigation evidence only; authority enters through their accepted mappings
and qualifications. Repository memory finds only prospective-consumer
warnings and no accepted QB3 result. The executable and all QB3 numerical
values remain unopened until this contract is frozen.

## Invariants, Conventions, and Allowed Imports

For every radial background P, the first-order mode
`u=P+epsilon*psi_lm*Y_lm` obeys the C-PDE-003 equation
`psi_tt-psi_rr-2*psi_r/r+l(l+1)*psi/r^2+cos(P)*psi=0`; for l=2, regularity is
`psi=O(r^2)`. The radial operator depends on l but not m. This exact degeneracy
does not supply a periodic separated solution, frequency, normalization, or
second independent temporal coefficient. The C-PDE-006 background is a
qualified finite-box harmonic branch with radiative wall channels.

Real Cartesian STF tensors, normalized versus triple moment conventions, and
the two-dimensional TT image follow C-MOM-001, C-MOM-003, C-GW-001, and
C-GW-002. Conditional waveform or power formulas retain their explicit G, R,
quadrupole scale, source-conservation, and far-zone premises. A generic frame
may give nonzero plus and cross coordinates for one fixed STF direction, but
coordinate rank two is not temporal source rank two. Standard real spherical
harmonics, exact angular integration, and audited SciPy spectral/evolution
methods are allowed. No source eigenvalue, amplitude, width, line frequency,
or waveform is an input.

## Candidate Preregistration

The candidate set is frozen from queue metadata and accepted structure before
the source implementation is opened.

| Candidate | Construction | New assumptions and parameters | Natural-fit prediction | Decisive oracle |
| --- | --- | --- | --- | --- |
| A | Literal QB3 radial eigenproblem, real m=2 deformation, moment, and TT output | Every averaged coefficient, wall, normalization, amplitude, and time factor must be declared | May reproduce a triaxial tensor but can fail the full time-dependent equation or temporal-rank claim | Hash-pinned run, residual substitution, origin and wall audit, refinements, convention mutations, and rank counterexamples |
| B | Exact real-l=2 basis/STF map plus m-degeneracy and temporal-rank theorem | No dynamical parameter beyond accepted radial coefficient functions | Supplies a reusable positive theorem and exposes whether “two polarizations” means basis dimension or two source modes | SymPy angular integrals, tensor eigenstructure, arbitrary-frame TT projection, rank/determinant tests, rotations, and zero/axisymmetric limits |
| C | Regular Floquet problem around C-PDE-006 | Finite wall, harmonic truncation, radial/time discretization, monodromy phase convention | Directly tests periodic l=2 eigenmode or instability, but inherits the finite-box ceiling | Matrix-free monodromy or harmonic-Floquet residual, mesh/time/harmonic/wall/tolerance refinement, reciprocal-pair or energy checks, and independent evolution/vacuum limit |
| D | Two independent real l=2 finite-time components | Initial profiles, phases, finite interval, domain, mesh, moment estimator | Can establish a rank-two finite-time coefficient trajectory without claiming periodicity | Regular PDE evolution, convergence, zero/half/phase mutations, moment and conservation diagnostics, and independent method |

## Selection Criteria and Blinding

Selection is ordered by the exact C-PDE-003 operator and origin law, explicit
real-harmonic and STF conventions, temporal-rank honesty, solver and residual
quality, independent refinement, finite-box boundary honesty, assumption and
parameter economy, correct vacuum and symmetry limits, and compatibility with
conditional gravity ceilings. Numerical similarity to QB3, P3D4, or a claimed
frequency cannot select the concept. The comparator gate opens only after the
manifest, this contract, the rank metric, PDE residual, boundary model,
mutations, refinement plan, and interpretation ceiling are frozen.

## Proposed Claim Delta

Provisional `C-PDE-009` may state exact m-degeneracy of the regular l=2
linearized radial equation and prove that replacing `cos(P(r,t))` by a time
average defines a different operator unless a separate equivalence theorem
applies. Provisional `C-GW-007` may map a general real l=2 angular coefficient
to normalized and triple STF tensors, arbitrary-view TT coordinates, and an
exact temporal-rank criterion. A numerical `C-PDE-010` or `C-GW-008` is
admissible only if Candidate C or D resolves a genuine regular object with all
solver, residual, refinement, boundary, and independent-method gates.

Direct consumers are the QB3 disposition and later QB4. The exact claims may
also clarify C-PDE-004/C-GW-006 rotations without changing their finite-time
evidence. No accepted claim will identify TT image dimension with a graviton
count, a triaxial tensor with two independent time modes, or conditional
waveform algebra with physical radiation.

## Implementation and Oracle Plan

Canonical exact APIs will represent real l=2 STF basis tensors, angular-to-
tensor coefficients, TT coordinates, rotations, and temporal coefficient
rank without simulation at import. Existing TT and l-mode APIs will be reused
or extended only after GitNexus impact review. SymPy and exact matrix algebra
fit degeneracy, angular normalization, eigenstructure, TT projection,
rotation, phase, and rank obligations.

If Candidate C is selected, float64 SciPy work will state the periodic
background reconstruction, equation, radial domain, origin and wall data,
spatial operator, time integrator, monodromy action, multiplier norm and
residual, mesh/time/harmonic/wall/tolerance refinements, conserved symplectic
or energy diagnostic where applicable, and an independent direct evolution or
vacuum spherical-Bessel limit. Thresholds will use declared coefficient,
energy, or residual scales. Candidate D will analogously state its two initial
components, phase and amplitude mutations, finite causal interval, PDE and
moment convergence, conservation or controlled boundary flux, and independent
route.

Load-bearing mutations change l(l+1), origin order, real-harmonic
normalization, m=2 sine/cosine orientation, normalized/triple STF scale,
polarization basis normalization, observer frame, coefficient phase, and
temporal-rank determinant. A one-scalar triaxial tensor and two proportional
coefficient traces are explicit counterexamples to the inference from two
nonzero readouts to two independent modes.

## Attempts and Continuation

Attempt 0001 will hash-check and reproduce QB3, then audit the exact radial
equation, time averaging, angular field, regular origin, boundary conditions,
moment normalization, TT basis, temporal-rank claim, solver status, and every
reported numerical value. A literal failure routes first to Candidate B's
exact positive theorem, then to Candidate C or D according to structural fit.
An unsuccessful Floquet solve is not completion; representation, discretized
monodromy, harmonic expansion, and finite-time alternatives remain available.

## Debt Ledger

This ledger tracks source reproduction, PDE equivalence, regularity, angular
normalization, triaxial tensor construction, temporal source rank, finite-box
spectral evidence, conservation and boundary conditions, conditional gravity,
independent evidence, consumers, and canonical state.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| QB3's literal eigenproblem, deformation, tensor, transform, and current-environment behavior are unaudited | Hash-check, run, and preserve the complete result or failure | open |
| The claimed averaged radial eigenproblem may not solve C-PDE-003 | Substitute the full ansatz, compare operators exactly, and use Floquet/evolution evidence for any dynamical promotion | open |
| Real l=2 angular and STF normalizations are not canonicalized for triaxial data | Implement exact basis-to-tensor and rotation APIs with wrong-normalization probes | open |
| Two TT coordinate readouts may be conflated with two independent temporal modes | Define and mutate a temporal-rank oracle with proportional and phase-shifted counterexamples | open |
| Regular finite-box nonaxisymmetric dynamics are unresolved | Complete Candidate C or D with status, residual, refinement, boundary, conservation, and independent-method evidence if a numerical claim is promoted | open |
| Physical radiation and graviton language may exceed accepted imports | Audit local conservation, moment scale, conditional waveform premises, and every excluded interpretation | open |
| Consumers and generated state are unreplayed | Complete impact analysis, targeted consumers, one final repository gate, and queue regeneration | open |

## Review and Promotion Plan

Each exact and numerical claim receives a separate four-axis review from raw
artifacts and frozen criteria. Accepted definitions move under
`src/substrate_framework/` with focused tests. QB3 receives a structured
terminal disposition in authoritative `migration/dispositions.yaml`, and the
queue is regenerated. Promotion requires a pinned release if claims change,
generated docs and accepted memory, affected-consumer replay, one final
`scripts/validate.sh`, `git diff --check`, and an empty campaign ledger.

## Done Gate

P054 closes only when the positive nonaxisymmetric l=2 object, full operator
and regularity audit, tensor and temporal-rank theorem, any promoted numerical
dynamics, source disposition, sensitive independent oracles, claim-level
reviews, consumer replay, canonical synchronization, and empty campaign debt
all pass. The parent migration then continues to the next pending unit.
