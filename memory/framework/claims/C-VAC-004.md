---
description: Accepted framework claim C-VAC-004
author: framework-registry
created: '2026-08-11T13:50:00Z'
updated: '2026-08-11T13:50:00Z'
tags:
- substrate-framework
- accepted-claim
- C-VAC-004
category: claims
confidence: established
status: active
---
# C-VAC-004

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-RGE-003's positive formal one-loop energy and paired inverse-energy length map and C-VAC-003's exact affine matter-induced connection-field kinetic family, separately supply positive exact lengths ell0 and ell1, positive exact conversions K0 and K1, exact real local and finite matching coordinates with sum Z_ref, and nonnegative exact invariant complex-scalar and Dirac weights W_s and W_f. Define E0=K0/ell0, E1=K1/ell1, R_ell=ell1/ell0, R_K=K1/K0, and b=W_s/3+4*W_f/3. Then E0/E1=R_ell/R_K, the exact scale logarithm is L=log(R_ell/R_K), and the complete affine composition is Z(E1)=Z_ref+b*L/(8*pi^2). A common positive rescaling of ell0 and ell1 leaves R_ell, L, and Z unchanged while shifting both absolute energies; at fixed lengths, changing either conversion changes L. On C-RGE-003's consistently paired specialization E1=E0*exp(-X), X=8*pi^2/(b0*g^2), ell0=K0/E0, and ell1=K1/E1, one has R_ell=R_K*exp(X), so L=X without requiring K0=K1 and Z(E1)=Z_ref+b/(b0*g^2). Only under the separately declared zero-matching specialization Z_ref=0 and a provably positive b does the positive inverse kinetic coordinate equal b0*g^2/b. Holding physical lengths fixed while changing a conversion, inserting an unpaired positive soliton or threshold factor, reversing an unpaired orientation, or changing Z_ref changes the relevant logarithm or total. The composition imports the logarithm from the accepted one-loop kinetic theorem; dimensional power zero is a constant rather than a logarithm, and dimensions do not select a unique form factor. This theorem does not identify either length or energy with a lattice, granularity, soliton, Compton scale, QCD, confinement, hadron, cutoff, observation, or substrate object; select b0, g^2, a conversion, matter content, group, matching boundary, absolute scale, or perturbative domain; or turn the inverse kinetic coordinate into a physical gauge coupling.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-RGE-003, C-VAC-003. Assumptions: The two lengths and two inverse-length energy conversions are separately supplied positive exact quantities; the theorem selects neither their physical labels nor their values., The formal one-loop branch retains C-RGE-003's positive reference energy, coupling squared, beta coefficient, conversion data, scale orientation, and domain qualifications., The affine family retains C-VAC-003's declared connection-field convention, exact invariant matter weights, local coefficient, finite matching offset, and independent real reference value., Cancellation of unequal conversions occurs only when each length is consistently paired with the energy it defines; at fixed physical lengths an unpaired conversion or soliton coefficient remains load-bearing., The zero-matching inverse coordinate requires a separately imposed Z_ref=0 and a provably positive total matter coefficient. General positivity and a physical coupling interpretation require further premises., Common length rescaling preserves relative data but changes both absolute energies, so it does not establish an absolute scale., The logarithmic dependence is inherited from the accepted one-loop kinetic theorem rather than selected by dimensions or by power exponent zero., No accepted claim identifies the formal scales, matter, group, boundary, inverse kinetic coordinate, or one-loop parameters with observations or a substrate realization.. Comparators: GK3D3 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its exact conditional ratio, log-exp reduction, conversion cancellation, explicit zero branch, and common-rescaling identity survive, while its physical scale identifications, erased boundary, parameter-free coupling, log uniqueness, sampled perturbativity, QCD, and substrate readings are corrected, qualified, or rejected, C-RGE-003 remains the distinct formal two-length transmutation and identifiability theorem with no kinetic family or physical labels, C-VAC-003 remains the distinct scalar-loop and affine kinetic-boundary theorem with no length-energy scale identification, C-IDN-002 independently establishes that AS7's gravity-plus-length system retains a null direction and that backsubstitution is inverse reconstruction.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.139.0` with provenance `campaigns/P187-gk3d3-transmutation-logarithm-audit/adjudication.yaml`.

- `campaigns/P187-gk3d3-transmutation-logarithm-audit/verify.py`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/reviews/independent_scale_kinetic_review.py`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/reviews/replay_source_graph.py`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/reviews/C-VAC-004-claim-review.md`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/reviews/source_adjudication.md`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/reviews/impact_analysis.md`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/attempts/0005/result.yaml`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/attempts/0007/result.yaml`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/attempts/0011/result.yaml`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/evidence/formula-freeze.yaml`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/evidence/input-provenance.yaml`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/evidence/dependency-audit.yaml`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/evidence/consumer-audit.yaml`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/evidence/candidate-comparison.yaml`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/evidence/primary-provenance.yaml`
- `campaigns/P187-gk3d3-transmutation-logarithm-audit/evidence/independent-provenance.yaml`
- `memory/vantasner/decisions/C-VAC-004-review.md`
- `memory/vantasner/decisions/GK3D3-qualified-review.md`
- `src/substrate_framework/kinetic_scale_matching.py`
- `tests/test_kinetic_scale_matching.py`
