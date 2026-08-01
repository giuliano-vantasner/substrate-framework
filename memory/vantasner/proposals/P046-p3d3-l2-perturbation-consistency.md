---
description: Construct the self-consistent l=2 perturbation sector and audit P3D3
author: vantasner
created: '2026-08-01T20:30:44Z'
updated: '2026-08-01T21:00:24Z'
tags:
- substrate-framework
- campaign-proposal
- l2-perturbation
- migration-P3D3
category: proposals
confidence: exploratory
status: archived
---
# P046 P3D3 l=2 Perturbation Consistency Audit

## Question and Positive Deliverable

P046 must determine whether P3D3's multiplicative quadrupolar deformation of
the accepted radial sine-Gordon trajectory solves the full 3+1 equation. If it
does not, the campaign must construct the correct importable l=2 perturbation
sector, including its exact equation and, if the frozen numerical gates close,
a finite-time evolved perturbation. A residual or no-go alone is attempt
evidence and does not complete this positive objective.

## Base Release and Provenance

The accepted base is `v0.40.0` at framework commit `5bcb4b9`.
`C-PDE-001` supplies the declared radial equation and finite-time background;
`C-MOM-003` supplies exact spherical and P2-deformed moment algebra;
`C-PDE-002` is a cutoff-qualified scalar core diagnostic and is not needed for
field consistency. P3D3 is pending source evidence at `substrate@6d1f4e0`,
SHA-256 `3f4532bac5e517b1324bf74153da9acdc9ef1cb10f53fc3df8cd0483d51e8fa2`.
Memory search found the current done-gate effort and accepted P3D2 context but
no authoritative P3D3 result. P3D4 remains pending.

## Invariants, Conventions, and Allowed Imports

The full equation is
`u_tt-u_rr-2*u_r/r-(Delta_Omega u)/r^2+sin(u)=0`, with regularity at the
origin and an explicit finite-domain outer boundary. For
`Y=P2(cos(theta))`, `Delta_Omega Y=-6Y`. A regular l=2 perturbation behaves as
`r^2` near the origin. The accepted radial background is finite-time
simulation evidence, not an exact periodic solution. Moment algebra does not
prove field consistency, conservation, gravitational coupling, or radiation.
No pending P3D4 statement or undeclared gravity theory is an allowed import.

## Candidate Preregistration

The alternatives are frozen from queue metadata and accepted dependencies
before reading the complete P3D3 executable or its reported values.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Evolve the true linearized l=2 perturbation | Accepted radial background and infinitesimal amplitude | Initial perturbation, mesh, timestep, domain | Native compatible extension | Exact linearization, regular finite evolution, refinement, and independent route |
| B | Exact perturbation equation without numeric promotion | Accepted radial equation and spherical-harmonic algebra | None beyond perturbation convention | Native exact statement | Exact residual and Taylor coefficient; numeric gates fail or remain unnecessary |
| C | Multiplicative finite deformation is self-consistent | Prescribed `u=P*(1+aY)` | Deformation amplitude `a` | Expected conflict | Nonzero full-PDE residual or harmonic leakage |

## Selection Criteria and Blinding

Selection is ordered by exact full-equation closure, compatibility with the
accepted radial sector, origin and boundary regularity, assumption and
parameter economy, dimensional and limiting behavior, solver/refinement
status, independent reconstruction, mutation sensitivity, and strict
field-versus-moment scope. P3D3's reported quadrupole values and static check
thresholds remain blinded until the residual, linearized equation, numerical
data, norms, refinements, and source-disposition criteria are frozen.

## Proposed Claim Delta

Provisional `C-PDE-003` would state the exact l=2 linearized sine-Gordon
equation about any radial solution and the exact residual of the multiplicative
P3D3 ansatz, depending on `C-PDE-001` for the declared model. Provisional
`C-PDE-004` would separately record a specified finite-time perturbation
evolution only if solver, refinement, regularity, boundary, amplitude, and
independent-method gates close. Existing `C-MOM-003` remains the authority for
prescribed P2 density moments; no gravity claim is proposed.

## Implementation and Oracle Plan

A pure package API will expose `P2`, the exact multiplicative-ansatz residual,
and the linearized l=2 operator. SymPy is the primary oracle for angular
eigenvalues, nonlinear residual reduction, Taylor separation, and harmonic
leakage. The load-bearing counterexample evaluates the residual away from
zeros of `P`, `Y`, and `a`; a mutation that deletes the angular barrier must
fail. If numerical promotion is attempted, the coupled background and
perturbation system will declare equations, domain, centered spatial operator,
regular origin treatment, boundary data, floating-point precision, timestep,
stopping time, error norm, and solver status. It will use at least three
spatial resolutions, timestep halving, domain variation, amplitude scaling,
and an adaptive-IVP or soluble static-background cross-check. Campaign code
will import package APIs and replay P044/P045 consumers affected by any solver
extension.

## Attempts and Continuation

Six attempts are preserved. Attempt `0001` repaired two over-tight regression
thresholds; attempt `0002` repaired a mesh-dependent sampling mismatch;
attempt `0003` repaired a symbolic variable shadowed by a numeric array.
Attempt `0004` passes the unchanged exact, refinement, soluble-limit, and
independent-method criteria. Attempt `0005` exposed successful check counts
being returned as nonzero process statuses; attempt `0006` repairs that shared
workflow defect without rewriting immutable campaigns and replays every
consumer with status zero. Candidate A is selected. Candidate C fails the exact
residual, regularity, angular-energy, and harmonic-leakage gates.

## Debt Ledger

This ledger tracks exact residual closure, perturbative order, angular
harmonics, origin/boundary regularity, numerical sensitivity, source mapping,
and the gravity interpretation boundary.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| The source deformation may omit angular gradients or nonlinear mixing | Reproduce it and evaluate the full exact residual | discharged by exact residual, omitted-gradient audit, and P4 leakage |
| The true l=2 sector is not yet importable | Derive a pure API and exact tests | discharged by `sine_gordon_l_modes.py` and targeted tests |
| A finite-time perturbation claim may be numerically fragile | Close solver, refinement, amplitude, domain, and independent-route gates or omit it | discharged by attempt 0004 and DOP853 review |
| A nonzero moment may be mistaken for a physical waveform | Keep accepted claims gravity-free and audit every source sentence | discharged by separate field/moment claims and qualified source review |
| Direct and prospective consumers are not yet replayed | Inventory and execute affected paths before promotion | discharged by status-zero P044/P045 replay; P3D4/QB2/QB3/BX1 recorded as pending |

## Review and Promotion Plan

Exact and numerical statements receive separate claim reviews and evidence
axes. Promotion requires importable APIs/tests, immutable attempts, source
reproduction and adjudication, impact analysis, qualified or refuted P3D3
disposition with exact remaining subclaims, registry/release/docs/memory
synchronization, targeted consumer replay, and one unchanged-boundary full
repository gate.

## Done Gate

P046 closes with `C-PDE-003/004`, qualified P3D3 mapping, canonical release and
memory generation, exact/numeric/independent oracles, status-zero consumer
replay, and the unchanged promotion-boundary repository gate passing. The debt
ledger is empty.
