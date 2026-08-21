---
description: 'P240 attempt 0042: exact R-scaling pencil classification of the fixed-J
  hedgehog stability window (issue 151)'
author: giuliano
created: '2026-08-21T14:20:25.191924+00:00'
updated: '2026-08-21T14:20:25.191924+00:00'
tags:
- substrate-framework
- campaign
- m5
- issue-151
- stability
- pencil
category: efforts
confidence: working
status: active
---

## Question and Positive Deliverable

Phase 1 of issue #151 asked whether the R >= 7.5 marginally stable spherically symmetric fixed-J hedgehog is an intrinsic minimum, a boundary artifact, or a near-critical state, and demanded the critical radius with an explanation.

## Method (derivation-first, revised at owner direction)

The owner redirected the attempt away from numerical ladder fishing toward derivation first. The exact scaling identity E(R)[c] = R^3 V[c] + (C[c] + Phi[c])/R with Phi = 1/(4I) holds at the discrete level under fixed-quadrature x-space evaluation, so H(R) = R^3 A + R^-1 D exactly, A = nabla^2 V and D = nabla^2(C + Phi). All stability questions reduce to the spectrum of two R-independent matrices on the branch background; lambda_min(A) > 0 would prove stability for every radius.

## Result

lambda_min(A) is negative on every measured branch background: -9.94e-4 (R=6), -1.08e-4 (R=8), -6.1e-6 (R=10), -2.10e-6 (R=12, converged under order refinement), quadrature-independent to 8 digits. Branch lambda_min is positive inside the window but decays with basis order; the rescue is the R^-4-scaled D class. Verdict: finite stability window (~7.5 to ~80 by hypothesis-grade extrapolation), structural marginality, no intrinsic minimum anywhere.

## Reusable Mechanisms

Three mechanisms from this attempt are reusable by later P240 work.

- Fixed-quadrature x-space evaluator (attempts/0042/xspace_energy.py) makes the scaling identity exact at the discrete level; whole-Hessian two-radius extraction recovers A and D without differentiating components.
- Separate-component double-backward is unreliable for derivative-carrying energy components (spurious inertia Hessian observed); whole-Hessian autograd was validated against cross-difference finite differences.
- Hand transcription of cpu_energy must keep delta = split_amplitude * sine(mu)^2 in the polar/azimuthal coupling; dropping it produced 1-88 percent component errors that passed casual inspection.

## Continuation State

Attempt 0042 landed as evidence; the campaign objective (issue #151 ladder through Phase 4) stays open. Next decisive actions recorded in attempts/0042/result.yaml: identify the negative eigenvector channel of A, verify the second-crossing prediction near R ~ 80 with converged roots, then run the relaxed fixed-J pair oracle inside the window.

