---
description: Accepted framework claim C-PDE-005
author: framework-registry
created: '2026-08-02T02:05:00Z'
updated: '2026-08-02T02:05:00Z'
tags:
- substrate-framework
- accepted-claim
- C-PDE-005
category: claims
confidence: established
status: active
---
# C-PDE-005

## Statement
The accepted statement is reproduced exactly from the claim registry.

For the dimensionless three-dimensional radial sine-Gordon equation of C-PDE-001, let H be a finite set of positive odd integers containing one and set u(r,t)=sum_(n in H) a_n(r)*cos(n*omega*t). With S_n[a]=(1/pi)*integral_0^(2*pi) sin(sum_(m in H) a_m(r)*cos(m*tau))*cos(n*tau) dtau, exact Fourier projection gives a_n''+2*a_n'/r+(n*omega)^2*a_n-S_n[a]=0. Odd harmonics give exact half-period antisymmetry. Even radial regularity gives a_n'(0)=0 and the origin curvature law 3*a_n''(0)+(n*omega)^2*a_n(0)-S_n[a](0)=0. In the linear far field each mode obeys a_n''+2*a_n'/r+((n*omega)^2-1)*a_n=0: n*omega<1 is evanescent with rate sqrt(1-(n*omega)^2), n*omega=1 is threshold, and n*omega>1 is radiative with wavenumber sqrt((n*omega)^2-1). A nonzero real radiative one-over-r tail has positive asymptotic energy per unit radial length and hence infinite integrated three-dimensional energy. Thus a sub-threshold fundamental does not localize its higher channels, and a Dirichlet wall on a radiative harmonic fixes a finite-box standing-wave phase rather than proving an infinite-domain finite-energy breather. These exact conditional statements establish no existence, uniqueness, nonzero radiative coefficient, exact periodic solution, lifetime, gravity, particle identity, absolute scale, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-PDE-001. Assumptions: The dimensionless action, radial geometry, potential convention, regularity, and linear mass threshold one are exactly those of C-PDE-001., The amplitudes are sufficiently differentiable, the displayed Fourier projections exist, and the finite odd-harmonic ansatz fixes a common phase origin., The infinite-energy conclusion is conditional on a nonzero real radiative one-over-r coefficient; the theorem does not require every formal solution to excite such a coefficient., A finite outer wall is declared numerical model data and is not identified with spatial infinity.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.46.0` with provenance `campaigns/P052-qb1-radial-harmonic-balance/adjudication.yaml`.

- `campaigns/P052-qb1-radial-harmonic-balance/verify.py`
- `campaigns/P052-qb1-radial-harmonic-balance/attempts/0011/result.yaml`
- `campaigns/P052-qb1-radial-harmonic-balance/attempts/0010/result.yaml`
- `campaigns/P052-qb1-radial-harmonic-balance/reviews/independent_harmonic_review.py`
- `campaigns/P052-qb1-radial-harmonic-balance/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-PDE-005-review.md`
- `tests/test_radial_harmonic_balance.py`
