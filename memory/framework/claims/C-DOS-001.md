---
description: Accepted framework claim C-DOS-001
author: framework-registry
created: '2026-08-11T21:10:00Z'
updated: '2026-08-11T21:10:00Z'
tags:
- substrate-framework
- accepted-claim
- C-DOS-001
category: claims
confidence: established
status: active
---
# C-DOS-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let d and b be separately supplied positive integers, let V and c be positive reals, let omega_0 be a nonnegative real, and use the declared isotropic continuum phase-space measure b*V*d^d k/(2*pi)^d with dispersion omega(k)=sqrt(omega_0^2+c^2*k^2). Write S_(d-1)=2*pi^(d/2)/Gamma(d/2). On the open band omega>omega_0 the density of states is g_(d,b)(omega)=b*V*S_(d-1)*omega*(omega^2-omega_0^2)^((d-2)/2) /((2*pi)^d*c^d), and it is zero below the gap. Its integral from the threshold to omega(K) is exactly N_(d,b)(K)=b*V*S_(d-1)*K^d/(d*(2*pi)^d), independent of omega_0. Therefore a separately supplied positive continuum target N has the unique positive matching cutoff K=(N*d*(2*pi)^d/(b*V*S_(d-1)))^(1/d). In d=1 the open-band density has an integrable threshold singularity, in d=2 it has a finite threshold limit, and in d>=3 it tends to zero. For d=3 the per-branch density is V*omega*sqrt(omega^2-omega_0^2)/(2*pi^2*c^3); choosing b=3 and separately supplying N=3*V/a^3 gives the conditional corollary K=(6*pi^2)^(1/3)/a. The continuum integral is not an exact finite periodic lattice-point count or dynamical-matrix rank, the matched cutoff is not a derived microscopic Brillouin-zone boundary, and none of these identities derives a cell complex, branch degeneracy, participation fraction, coupling, state, channel, rate, material, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: Spatial dimension d and branch degeneracy b are independent supplied positive integers; neither is derived from the other., V and c are positive, omega_0 is nonnegative, K is positive, the dispersion is isotropic and radial, and the continuum phase-space measure is explicitly declared., The density is an open-band statement. Its d=1 threshold value is not assigned pointwise even though the singularity is integrable; below the gap the density is zero., The continuum count is exact for its declared measure but is not a finite lattice rank. Exact sites, components, constraints, topology, divisibility, and boundary data are outside the claim., The target N is an input to cutoff matching. The theorem derives neither N nor a microscopic Brillouin zone., C-MED-003 and C-SG-018 are one-dimensional scalar comparison claims, not dependencies and not an accepted three-dimensional lift., No participating-mode count, coupling, state, spectral weight, transition channel, probability, rate, material parameter, or substrate conclusion follows without additional accepted premises.. Comparators: MD1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; prior graph replay and the generated queue exposed its formulas, so P196 froze general-d domains, candidate distinctions, structural criteria, and mutations before renewed execution, C-SG-018 supplies the accepted one-dimensional scalar dispersion and explicitly does not establish a density-of-states theorem or three-dimensional medium, C-KRN-001 uses a separately declared radial dimension and measure for a distinct inverse-kernel theorem, not for mode counting.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.145.0` with provenance `campaigns/P196-md1-mode-counting-audit/adjudication.yaml`.

- `campaigns/P196-md1-mode-counting-audit/verify.py`
- `campaigns/P196-md1-mode-counting-audit/reviews/independent_mode_counting_review.py`
- `campaigns/P196-md1-mode-counting-audit/reviews/replay_source_graph.py`
- `campaigns/P196-md1-mode-counting-audit/reviews/C-DOS-001-claim-review.md`
- `campaigns/P196-md1-mode-counting-audit/reviews/MD1-disposition-review.md`
- `campaigns/P196-md1-mode-counting-audit/reviews/source_adjudication.md`
- `campaigns/P196-md1-mode-counting-audit/reviews/impact_analysis.md`
- `campaigns/P196-md1-mode-counting-audit/attempts/0004/result.yaml`
- `campaigns/P196-md1-mode-counting-audit/attempts/0005/result.yaml`
- `campaigns/P196-md1-mode-counting-audit/attempts/0006/result.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/formula-freeze.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/input-provenance.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/dependency-audit.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/consumer-audit.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/candidate-comparison.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/implementation-audit.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/gitnexus-impact.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/primary-provenance.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/source-reproduction.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/consumer-reproduction.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/compatibility-audit.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/source-audit.yaml`
- `campaigns/P196-md1-mode-counting-audit/evidence/check-adjudication.yaml`
- `memory/vantasner/decisions/C-DOS-001-review.md`
- `memory/vantasner/decisions/MD1-qualified-review.md`
- `src/substrate_framework/mode_counting.py`
- `tests/test_mode_counting.py`
