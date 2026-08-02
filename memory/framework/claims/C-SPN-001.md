---
description: Accepted framework claim C-SPN-001
author: framework-registry
created: '2026-08-03T03:00:00Z'
updated: '2026-08-03T03:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-SPN-001
category: claims
confidence: established
status: active
---
# C-SPN-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let Psi be a nonzero complex pure spin-1 spinor in the ordered m=(+1,0,-1) basis with the standard Hermitian spin-one matrices. Define n=Psi^dagger*Psi, f_a=Psi^dagger*F_a*Psi, and the singlet amplitude A=Psi_0^2-2*Psi_+*Psi_-. Then the exact invariant is |f|^2+|A|^2=n^2, and the attainable interval is 0<=|f|^2<=n^2. Under the unitary complex-Cartesian convention Psi_+=-(d_x-i*d_y)/sqrt(2), Psi_0=d_z, and Psi_-=(d_x+i*d_y)/sqrt(2), writing d=u+i*v gives f=2*u cross v and A=d dot d. Hence |f|^2=0 exactly when u and v are parallel; modulo global phase and spatial SO(3), these rays form the polar orbit RP^2. The upper endpoint |f|^2=n^2 holds exactly when u and v are orthogonal with equal norm; modulo global phase and SO(3), these rays form the coherent ferromagnetic orbit S^2 with SO(2) stabilizer. Conditional on the supplied fixed-density pure-state functional E_spin=(c2/2)*|f|^2, positive c2 selects precisely the polar projective orbit, negative c2 selects precisely the ferromagnetic projective orbit, and c2=0 leaves every pure spin-1 ray degenerate. The polar-minus-ferromagnetic endpoint energy is -c2*n^2/2. This theorem derives no material sign or magnitude of c2, atomic realization, spatial condensate ground state, full physical order-parameter manifold, defect energetics, finite-temperature phase, mixed-state classification, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: Psi is a nonzero pure three-component complex spinor in the declared basis; a density matrix or mixed state is outside the equality-orbit classification., The norm n is positive and fixed during energy comparison, global phase is quotiented, and spatial rotations use the standard spin-one SO(3) representation., The spin functional and exactly decided real sign of c2 are supplied premises; a spin-independent density term cancels only at fixed n., Gradient, trap, Zeeman, dipolar, thermal, and other omitted terms are absent from the supplied functional, and pending O1, ME2, and ME3 provide no premise.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.61.0` with provenance `campaigns/P067-me1-spin1-orbit-selection/adjudication.yaml`.

- `campaigns/P067-me1-spin1-orbit-selection/verify.py`
- `campaigns/P067-me1-spin1-orbit-selection/attempts/0001/result.yaml`
- `campaigns/P067-me1-spin1-orbit-selection/attempts/0002/result.yaml`
- `campaigns/P067-me1-spin1-orbit-selection/attempts/0003/result.yaml`
- `campaigns/P067-me1-spin1-orbit-selection/reviews/independent_spin1_review.py`
- `campaigns/P067-me1-spin1-orbit-selection/evidence/primary-provenance.yaml`
- `campaigns/P067-me1-spin1-orbit-selection/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-SPN-001-review.md`
- `tests/test_spin1_mean_field.py`
