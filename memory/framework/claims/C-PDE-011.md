---
description: Accepted framework claim C-PDE-011
author: framework-registry
created: '2026-08-04T06:25:00Z'
updated: '2026-08-04T06:25:00Z'
tags:
- substrate-framework
- accepted-claim
- C-PDE-011
category: claims
confidence: established
status: active
---
# C-PDE-011

## Statement
The accepted statement is reproduced exactly from the claim registry.

In the normalized dimensionless 1+1 sine-Gordon model, consider phi_tt-phi_xx+sin(phi)=J-gamma*phi_t on -80<=x<=80 with zero initial field and velocity, homogeneous Dirichlet endpoints, and final time 410. Let omega_d=1/sqrt(2), eta=sqrt(1-omega_d^2), tau=4/omega_d, and J=A*sech(eta*x)*exp(-(t-30)^2/(2*tau^2))*sin(omega_d*(t-30)), where A is fixed so the declared full-line temporal proxy integral f(t)^2 dt is 400. Let gamma vanish for |x|<=40 and equal ((|x|-40)/40)^2 outside. Centered homogeneous-Dirichlet leapfrog evolutions with spatial steps 0.05, 0.025, and 0.0125, timestep 0.4*dx, radius-12 diagnostics, and the late window t>320 give constrained exact C-SG-001 center-trace fits with relative RMS errors 0.0197 through 0.0220 and fitted frequencies 0.295653, 0.250839, and 0.239700; successive frequency differences decrease by about four. The late core energies 15.4464, 15.6667, and 15.7115 differ from the corresponding C-SG-002 fitted energies by less than 1.2 percent, while final radius-12 field-velocity snapshot fits have joint relative L2 errors 0.0572, 0.0609, and 0.0966. The final-energy minus source-work plus damping-loss residual, relative to source work, decreases from 1.08e-3 to 1.36e-4 to 3.03e-5. Timestep halving, outer domain 120, sponge widths 30 and 50, adaptive DOP853 at dx=0.05 and 0.025, an independent rising-crossing frequency estimate, planted exact breathers, and nonbreather counterstates preserve the bounded verdict. Changing only the proxy target from 400 to 380 or 420 breaks the composite classifier. This is simulation evidence for one exact-source, finite-box, finite-time formation trajectory close to the exact rest breather family. It establishes no robust parameter interval, preferential fast or resonant seeding, slow-drive exclusion, equal-work comparison, continuum or asymptotic existence, physical deposition mechanism, voltage-slew law, probability, population, absolute scale, particle identity, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `simulation_evidence`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `qualified`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-SG-001, C-SG-002, C-SG-012. Assumptions: The normalized 1+1 sine-Gordon equation, exact rest-breather family, energy function, and stress-energy signs are those of C-SG-001, C-SG-002, and C-SG-012., The localized source, amplitude proxy, zero initial data, homogeneous Dirichlet walls, damping profile, domain, final time, and diagnostic radius are declared dimensionless model data and are not derived from a medium or physical deposition process., The source's full-line integral f(t)^2 dt is a waveform normalization only; actual source work is integral J*phi_t dx dt and is tracked separately with damping loss., Exact-family trace and snapshot fits constrain amplitude, width, velocity, and energy through one frequency and phase; their quoted errors and all formation conclusions remain finite-grid and finite-time evidence., The damping layer is an outer-boundary device, and no infinite-domain or asymptotic stability limit is inferred from finite-time domain and sponge sensitivity.. Comparators: SA3 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64, opened only after the candidate contract and selection criteria were frozen.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.77.0` with provenance `campaigns/P089-sa3-driven-pde-seeding-audit/adjudication.yaml`.

- `campaigns/P089-sa3-driven-pde-seeding-audit/verify.py`
- `campaigns/P089-sa3-driven-pde-seeding-audit/attempts/0004/result.yaml`
- `campaigns/P089-sa3-driven-pde-seeding-audit/attempts/0005/result.yaml`
- `campaigns/P089-sa3-driven-pde-seeding-audit/reviews/independent_adaptive_review.py`
- `campaigns/P089-sa3-driven-pde-seeding-audit/evidence/fine-adaptive-refinement.yaml`
- `campaigns/P089-sa3-driven-pde-seeding-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-PDE-011-review.md`
- `tests/test_sine_gordon_1d.py`
- `tests/test_numerics.py`
