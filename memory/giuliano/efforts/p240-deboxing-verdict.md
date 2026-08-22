---
description: "P240 attempt 0044: de-boxing resolves gap 5 \u2014 the clock is a finite-size-confined\
  \ state, not an isolated particle"
author: giuliano
created: '2026-08-22T00:12:20.609306+00:00'
updated: '2026-08-22T00:12:20.609306+00:00'
tags:
- substrate-framework
- campaign
- m5
- issue-151
- de-boxing
- stability
category: efforts
confidence: working
status: active
---

## Question and Positive Deliverable

Issue 151 Phase 3 asked whether the certified fixed-J hedgehog survives without walls. Attempt 0044 answers it with a derivation-first protocol: symbolic second variation of the potential around the rank-1 projector background (sympy, Richardson-verified against the certified formula), then a clean continuation ladder with two hard gates — quadrature scaled to basis order and cross-quadrature acceptance at doubled nodes.

## Result

The de-boxed limit does not exist as an isolated particle: E(R) grows linearly along the clean branch with no plateau, and lambda_min(A) is negative on every background, flattening near -(5+/-2)e-7 with no zero crossing. The exact pencil gives finite stability windows per background; the self-consistent branch is stable only for R in roughly [8, 34]. The negative direction is purely split-channel at every radius — the same channel whose softness attempt 0041 found at small R.

The symbolic derivation explains the structure: V2 around the projector is exactly diag(5,3,3,0,0,6)/2 in the local frame, so two shear channels are exactly potential-flat (gradient-stiffened only) and the split channel carries the persistent negative curvature. The free-wall variation completes the picture: releasing the rank-1 pinning at R=8 converges to a stable minimum 16 percent lighter with the clock sector invariant (omega 0.73923 vs 0.73929) — pinning distorted the profile's dress but never the clock; at R=16 free and pinned coincide.

## Reusable Mechanisms

- Aliasing gate: roots solved at insufficient quadrature reproduce their solving-grid energy but diverge by up to 15 orders under independent quadrature — spurious stationary points invisible to any single-grid check. Acceptance requires energy reproduction at doubled quadrature to 1e-6.
- Direct component-Hessian extraction (nabla^2 of the volume term alone) avoids the large-number cancellation that breaks two-radius matrix extraction at high basis order; both methods agree to 7 digits where the latter is clean.

## Continuation State

Gap five closes negatively: confinement is load-bearing; the object exists as a finite-size-confined state in R in [~8, ~34]. The pair/Newton question has no de-boxed realization in this model class; any extension must exploit the two exactly flat shear channels as the long-range multipole sector (asymptotic pairing). Coulomb item 5 remains defined-blocked.

