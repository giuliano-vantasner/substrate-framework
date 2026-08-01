---
description: Audit GW4's circular breather-pair quadrupole waveform
author: vantasner
created: '2026-08-01T18:17:28Z'
updated: '2026-08-01T18:27:49Z'
tags:
- substrate-framework
- campaign-proposal
- circular-pair
- conditional-waveform
- migration-GW4
category: proposals
confidence: working
status: archived
---
# P039 GW4 Circular-Pair Waveform Audit

## Question and Positive Deliverable

P039 must derive the exact quadrupole harmonics and conditional TT polarization
waveforms of a declared equal-mass circular point pair, then decide whether GW4
closes the additional source, binding, and physical-radiation premises needed
to call it a sine-Gordon-breather binary. The positive deliverable is an
arbitrary-inclination, convention-complete reusable theorem; rejecting the
breather ontology alone would not complete the campaign.

## Base Release and Provenance

The accepted base is `v0.34.0` at framework commit `3aed5a3`. Its forty-seven
claims include exact breather energy, conserved source moments, conditional TT
power/waveform algebra, and a normalized TT basis. They do not embed the 1+1
breather in a 3+1 compact stress tensor or derive a bound circular pair. The
pending hash-pinned candidate is GW4 at
`merged-framework/bridges/phase-12/bridge_GW4_breather_quadrupole_waveform.py`,
SHA-256 `0e2637aa188c77a2b976b87e8efffc104eb64c25b759b739d0467d01790c4a15`.
Bundled-memory search found no accepted breather-pair waveform theorem.

## Invariants, Conventions, and Allowed Imports

P039 may use accepted breather profile/energy, source-moment conventions, the
conditional waveform relation of `C-GW-001`, and the normalized basis of
`C-GW-002`. A pair of equal point masses on a declared circular path is a
kinematic model only; its binding stress, orbital law, stability, and breather
identity remain unproved. Normalized `I_STF` uses waveform prefactor `2G/r`,
while the triple source convention `Q=3*I_STF` requires `2G/(3r)`.

## Candidate Preregistration

The alternatives are frozen from queue metadata before the full GW4 executable
body or any source comparator is inspected.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact circular-pair quadrupole and arbitrary-inclination conditional plus/cross waveforms | Declared equal point masses, circular coordinates, conditional TT waveform | Mass, orbital radius, angular frequency, distance, coupling, viewing frame | Compatible specialization | Direct moments, derivatives, TT reconstruction, face-on/edge-on limits, and convention covariance |
| B | Circular-pair moments and harmonic doubling only | Declared point paths | Mass, radius, frequency | Native kinematics if waveform specialization fails | Independent differentiation and Fourier content |
| C | Physical bound sine-Gordon-breather binary radiation | 1+1-to-3+1 embedding, binding law, slow-motion gravity, source closure, detector map | Added FS2/P3D3 and gravitational inputs | Dependency conflict | Accepted closure and local conserved-stress audit |

## Selection Criteria and Blinding

Selection is ordered by exact center-of-mass moments, convention consistency,
explicit orbital inputs, conditional waveform closure, normalized polarization
extraction, arbitrary-inclination and origin limits, harmonic structure,
mutation sensitivity, and accepted dependency closure. No strain magnitude,
astrophysical formula, or GW4 reported coefficient may select a candidate.

## Proposed Claim Delta

Provisional `C-GW-003` would specialize the accepted conditional TT machinery
to a declared equal-mass circular pair and give exact normalized-STF second
derivatives and plus/cross coefficients for a stated viewing geometry. It will
exclude a self-consistent bound stress tensor, Kepler law, breather embedding,
physical gravity, detector strain, radiated energy loss, and substrate
prediction unless independently established.

## Implementation and Oracle Plan

Pure APIs will construct circular-pair moments and project their second
derivatives into normalized TT bases for an arbitrary inclination. SymPy will
verify center-of-mass cancellation, trace removal, frequency doubling,
polarization phases, face-on/edge-on limits, and normalized/triple convention
equivalence. Mutations will change the pair radius convention, quadrupole scale,
waveform prefactor, derivative order, and polarization normalization. An
independent route will differentiate particle coordinates and reconstruct the
same coefficients without the new helper.

## Attempts and Continuation

Attempt `0001` will reproduce GW4 and inventory its mass, orbit, radius,
frequency, quadrupole, waveform, observer, power, FS2/P3D3, and physical-source
assumptions. If the arbitrary-inclination waveform does not close, Candidate B
retains the exact kinematic object while every failed physical premise remains
qualified evidence.

## Debt Ledger

This ledger tracks source closure, orbital inputs, quadrupole normalization,
observer geometry, harmonic content, and physical interpretation.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| A point-pair path may be called an isolated bound source | Supply binding stress or keep the orbit explicitly kinematic | discharged: C-GW-003 and the API declare the path and exclude binding |
| Pending FS2/P3D3 may be smuggled in as accepted | Re-source every embedding and orbital premise or exclude it | discharged: both remain nondependencies and physical embedding is excluded |
| GW2's factor-nine convention error may propagate | Carry I_STF versus Q=3*I_STF through waveform and power factors | discharged: exact inverse coefficient and factor-nine mutation pass |
| One line of sight may be overread as the waveform | Derive arbitrary inclination and check face-on/edge-on limits | discharged: exact arbitrary-inclination formula and both limits pass |
| Harmonic doubling may be asserted from sampled data | Derive exact time dependence and mutation-sensitive derivative factors | discharged: symbolic 2*Omega formulas and derivative mutations pass |

## Review and Promotion Plan

The provisional claim receives an independent particle-coordinate and viewing-
geometry review. Promotion requires pure APIs/tests, immutable attempt evidence,
claim-level adjudication, terminal GW4 disposition, release/docs/memory
synchronization, targeted replay, and one unchanged full repository gate.

## Done Gate

P039 closes only when source status, orbital definitions, convention factors,
waveform premises, inclination limits, harmonics, mutations, source disposition,
consumers, and all campaign debt satisfy the framework contract.

## Adjudication Result

Candidate A is accepted as `C-GW-003`. Thirty-six main checks, nine independent
checks, and focused package replay establish the exact conditional theorem.
GW4 is qualified because its immutable executable stops at removed
`numpy.trapz`, its triple-quadrupole convention overstates the conditional field
by three and power by nine, and its binding, breather embedding, and physical
gravity remain unproved. Campaign debt is empty.
