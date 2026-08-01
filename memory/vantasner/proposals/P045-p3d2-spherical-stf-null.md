---
description: Derive the spherical STF null and audit P3D2's scalar-moment frequency claim
author: vantasner
created: '2026-08-01T20:06:19Z'
updated: '2026-08-01T20:21:47Z'
tags:
- substrate-framework
- campaign-proposal
- spherical-moments
- migration-P3D2
category: proposals
confidence: exploratory
status: archived
---
# P045 P3D2 Spherical STF Null Audit

## Question and Positive Deliverable

P045 must derive a reusable exact theorem for the Cartesian second moment and
both accepted STF conventions of an arbitrary integrable spherical density. It
must then decide whether the accepted radial sine-Gordon branch has a resolved
oscillating core energy-radius moment near twice its field fundamental. The
positive objects are the exact tensor theorem and, only if refinement closes,
the finite-time numerical characterization; a gravitational slogan is neither.

## Base Release and Provenance

The accepted base is `v0.39.0` at framework commit `aca7e79`, containing
fifty-three claims. `C-MOM-001` fixes moment and STF conventions, while
`C-PDE-001` supplies the declared radial equation, initial data, solver, and
finite-time evidence. P3D2 is pending source evidence at `substrate@6d1f4e0`,
SHA-256 `72802a3bb3ed46be3bf7b96e035028b0ded352ae02e587cb14b9db902b2125cb`.
Memory search found the new P3D2 continuation target and prior warnings that
moment kinematics do not create a gravity theory; it found no authoritative
spherical moment claim. P3D3 and P3D4 remain pending prospective consumers.

## Invariants, Conventions, and Allowed Imports

For a radial density `rho(r)`, define
`J=integral rho(r)*r^2 d^3x=4*pi*integral rho(r)*r^4 dr` and
`I_ij=integral rho*x_i*x_j d^3x`. The accepted normalized tensor is
`I_STF=I-delta*Tr(I)/3`; the triple convention is `Q=3*I_STF`. The exact
spherical theorem must not assume the sine-Gordon equation. The numerical
moment, if retained, is a core diagnostic with an explicit radius and is not a
conserved charge. No retarded field, gravitational coupling, flux law, or
radiation conclusion is an allowed import.

## Candidate Preregistration

The alternatives are frozen from queue metadata before reading the complete
P3D2 executable or its reported comparison values.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact spherical null plus numeric scalar-moment characterization | Radial density and accepted finite-time IVP | Core radius, mesh, time window | Native moment theorem plus compatible numeric consumer | Exact angular tensor, deformation guard, solver/refinement and two frequency routes |
| B | Exact spherical null only | Integrable radial density | Scalar radial moment `J` | Native exact theorem | Numeric frequency fails a preregistered sensitivity gate |
| C | Physical no-radiation theorem | Imported gravity mapping | Coupling and far-zone assumptions | Conflict | Absence of accepted field/flux dynamics |

## Selection Criteria and Blinding

Selection is ordered by exact angular closure, arbitrary-density scope,
normalized/triple convention consistency, a non-spherical mutation,
dependency/parameter economy, canonical implementation, numerical solver and
refinement status, independent reconstruction, and physical-scope honesty.
The source's FFT peaks, ratios, amplitudes, and tolerances remain blinded until
the moment definition, analysis windows, estimator cross-checks, and pass
criteria are frozen.

## Proposed Claim Delta

Provisional `C-MOM-003` would state the exact isotropic second moment and STF
null for every integrable radial density, depending on `C-MOM-001` only for
conventions. Provisional `C-PDE-002` would depend on `C-PDE-001` and record only
a resolution-bounded core energy-radius moment frequency if two estimators and
mesh, timestep, window, domain, and core-radius studies agree. Neither claim
would establish physical radiation or non-radiation.

## Implementation and Oracle Plan

A pure moment API will construct the isotropic tensor from scalar `J`, return
normalized and triple STF forms, and encode an axisymmetric quadrupolar
deformation for sensitivity. SymPy will integrate the sphere exactly and
derive the Legendre-deformation coefficients; direct angular quadrature will
be independent regression evidence. The radial solver will record the core
diagnostic `4*pi*integral_0^R r^4 T00 dr` at centered sample times rather than
P3D2 duplicating its evolution code. A numeric claim requires clean finite
solver output, nontrivial relative moment variation, FFT and crossing or
time-domain period agreement near twice the center fundamental within five
percent, two settled windows, meshes `0.1/0.05/0.025`, timestep halving,
domains 160/200/240, and core radii around the declared baseline. A weak
dispersive seed must not satisfy the combined persistent-core verdict.

## Attempts and Continuation

Attempt `0001` stopped before simulation because structural equality did not
normalize a correct symbolic P2 trace; attempt `0002` repairs the comparison
with an explicit simplified difference while leaving the scientific contract
unchanged. The repaired route will audit every subclaim and compare Candidate
A against B. A frequency
that changes materially with core radius, window, or resolution is retained as
attempt evidence and selects Candidate B; exact symmetry does not rescue that
numeric claim. Technical solver defects are repaired without changing the
frozen physical criteria.

Attempt `0002` then passed the full primary oracle but failed the independent
peak-period threshold because it treated maxima as exactly located on a
0.2-unit sampling grid. Attempt `0003` retains the threshold and replaces
sample-bin maxima by three-point quadratic peak times, while leaving the
independent DOP853 trajectory and FFT route unchanged.

## Debt Ledger

This ledger tracks angular normalization, STF convention, radial-moment
definition, numerical sensitivity, and the physical interpretation boundary.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Spherical isotropy may be asserted from symmetry alone | Perform exact angular integration and independent quadrature | discharged by symbolic and direct angular routes |
| Normalized and triple STF conventions may be mixed | Return and mutate both conventions explicitly | discharged by exact API and one-third mutations |
| A zero assembled tensor may be tautological | Derive it from angular moments and require an `l=2` deformation to be nonzero | discharged; source numeric zero classified as regression |
| The scalar radial moment may use an unstated core cutoff | Encode the cutoff in the diagnostic and vary it | discharged with accepted 20-30 range and radius-40 counterexample |
| One FFT bin may create frequency doubling | Use two windows and an independent time-domain estimator | discharged by sub-bin FFT and interpolated peak periods |
| The P3D1 solver may be copied into a consumer | Extend and call the canonical radial module | discharged by reusable moment diagnostics |
| An STF null may be called a physical radiation null | Keep gravity absent from accepted statements and source disposition | discharged by separate claims and qualified source review |

## Review and Promotion Plan

The exact theorem and any numeric characterization receive separate claim
reviews and verification axes. Promotion requires importable APIs/tests,
immutable attempts, source reproduction/adjudication, direct and prospective
consumer inventory, qualified P3D2 disposition, registry/release/docs/memory
synchronization, targeted replay, and one unchanged-boundary repository gate.

## Done Gate

P045 closes only when angular algebra, arbitrary-density scope, both STF
conventions, deformation sensitivity, numerical moment definition, solver and
refinement status, frequency evidence, source scope, consumers, disposition,
and campaign debt are all resolved.
