---
description: Construct finite-time radial sine-Gordon oscillon evidence and audit P3D1
author: vantasner
created: '2026-08-01T19:41:35Z'
updated: '2026-08-01T19:57:49Z'
tags:
- substrate-framework
- campaign-proposal
- radial-pde
- migration-P3D1
category: proposals
confidence: exploratory
status: archived
---
# P044 P3D1 Radial Sine-Gordon Oscillon Audit

## Question and Positive Deliverable

P044 must construct a genuine numerical solution of a declared 3+1 radial
sine-Gordon initial-value problem and establish finite-time localization and
oscillation with explicit numerical and boundary error control. It must then
separate that positive simulation object from exact-periodic, asymptotic-
lifetime, gravitational, and particle interpretations. A Derrick no-go or a
long-lived-looking center trace without a verified PDE solution is not
completion.

## Base Release and Provenance

The accepted base is `v0.38.0` at framework commit `9413dbf`, with fifty-two
claims and no accepted radial sine-Gordon PDE claim. `C-SG-001` supplies only
the normalized 1+1 potential convention and an exact one-dimensional limit.
P3D1 is pending candidate evidence at `substrate@6d1f4e0`, SHA-256
`f93b8dabfca0c49fb0bf1101c926e79c43dc2e9ebb35882083611a12ca9514fa`.
Memory search found project aspirations but no authoritative 3D oscillon
existence result. P3D1's cited C1, E1, E2, FS2/FS4, and later P3D units are not
accepted dependencies for this campaign.

## Invariants, Conventions, and Allowed Imports

The declared model uses action density
`u_t^2/2-|grad u|^2/2-(1-cos u)` in dimensionless 3+1 flat spacetime. Radial
variation gives `u_tt-u_rr-2u_r/r+sin u=0`, regularity requires `u_r(0,t)=0`,
and energy uses `4*pi*integral r^2(u_t^2/2+u_r^2/2+1-cos u)dr`. The outer
boundary and its causal/reflection window will be explicit. A finite-domain,
finite-time numerical trajectory earns simulation evidence only.

## Candidate Preregistration

The concepts and evidence thresholds are frozen from the queue question before
the full P3D1 executable body or any reported lifetime and frequency is read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Refined radial IVP oscillon | Declared 3+1 action and finite initial data | Gaussian amplitude/width, domain, mesh, time window | Compatible numerical extension | PDE residual, energy/boundary control, core retention, repeated oscillation, frequency, refinements |
| B | Fourier/BVP quasi-breather | Periodic core plus explicit tail condition | Harmonics, truncation radius, tail amplitude | Compatible if IVP is ambiguous | Collocation residual, harmonic convergence, independent time evolution |
| C | Enveloped 1D breather | Declared lift without radial dynamics | Envelope width | Conflict | Nonzero radial PDE residual or failed conservation |

## Selection Criteria and Blinding

Selection is ordered by equation fidelity, regularity, boundary causality,
energy balance, localization, repeated oscillation, below-threshold frequency,
mesh/time/domain convergence, independent-method agreement, mutation
sensitivity, and parameter economy. Source center amplitudes, lifetime labels,
frequency estimates, and exponential claims remain blinded until equations,
initial data, metrics, and pass thresholds are fixed.

## Proposed Claim Delta

Provisional `C-PDE-001` would record simulation evidence for one fully specified
radial sine-Gordon IVP over a finite time window, including resolution bounds,
energy balance, core-energy retention, and dominant frequency. It would not
assert an exact breather, eternal or exponentially long lifetime, uniqueness,
stability basin, astrophysical object, gravitational source, or substrate
identity.

## Implementation and Oracle Plan

A pure radial-PDE module will expose the action-derived equation, finite-
difference radial operator, energy and core-energy metrics, and a solver that
returns status and diagnostics without running at import. The primary method
will use method-of-lines with explicit tolerances on a stated domain and mesh;
the independent route will use a staggered or leapfrog finite-difference
evolution with a stated Courant factor. The origin stencil enforces even radial
regularity. The outer boundary will be causally separated from the core metric
window or its flux will be measured. Mesh, timestep/tolerance, and domain
refinements will track center traces, energy drift, core retention, and
dominant frequency in declared norms. A linear radial solution or small-
amplitude dispersive case will validate the operator; geometric-term removal,
origin mishandling, and weak/dispersive initial data are mutations.

## Attempts and Continuation

Attempt `0001` will hash-check and reproduce P3D1, inventory its equation,
origin and outer boundaries, initial data, integrator, energy, lifetime,
frequency, radiation, and downstream claims, then rebuild the strongest
supportable positive object. Numerical instability triggers method/timestep
repair; rapid dispersion triggers alternate preregistered initial data or
Candidate B rather than weaker thresholds.

## Debt Ledger

This ledger tracks equation derivation, singular origin treatment, boundary
effects, numerical convergence, localization, frequency, and epistemic scope.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| The 3D radial equation may be asserted rather than varied | Derive the radial Euler-Lagrange equation and energy exactly | discharged by exact variation and continuity identity |
| The `2/r` term is singular at the origin | Derive and test a regular origin stencil or transformed variable | discharged by soluble mode and independent `v=r*u` route |
| Outer-boundary reflection may mimic persistence | Use a causal window, larger domains, or controlled outgoing flux | discharged by domains 160/200/240 and causal closed-box audit |
| One center trace may look oscillatory without localization | Track core and total energy plus radial profiles | discharged by energy retention and radii 10/20/30/40 fractions |
| A single mesh/time step may create a numerical oscillon | Run mesh and timestep/tolerance refinement and an independent method | discharged by three meshes, timestep halving, and DOP853 review |
| A dominant FFT bin may be window dependent | State sampling/window and refine or cross-check zero crossings | discharged by two windows and crossing estimates |
| Finite-time persistence may be called exact existence or exponential lifetime | Restrict the claim to verified simulation time and metrics | discharged by qualified claim wording and source adjudication |
| Later quadrupole/gravity conclusions may be imported | Keep P3D2/P3D3 outside accepted dependencies | discharged; pending units remain prospective consumers only |

## Review and Promotion Plan

The provisional claim receives an independent integrator and radial-energy
review. Promotion requires reusable APIs/tests, immutable failed and passing
attempts, source adjudication, claim-level review, terminal P3D1 disposition,
downstream impact replay, registry/release/docs/memory synchronization, and one
full unchanged-boundary repository gate.

## Done Gate

P044 closes only when the radial equation, origin, boundary, solver status,
energy, localization, frequency, convergence, independent method, mutations,
source scope, consumers, disposition, and campaign debt are all resolved.
