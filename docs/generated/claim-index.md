<!-- GENERATED: scripts/render_docs.py; DO NOT EDIT -->
# Accepted claim index

This document is generated from `governance/claims.yaml`.

## C-OG-001

For every positive twice-differentiable static index n(x) and c0 > 0, the declared 1+1 metric g = diag(-1/n, n/c0^2) has Ricci scalar R = c0^2*(n*n_xx - 2*n_x^2)/n^3 and satisfies Box_g(log(n)) = R. Among twice-differentiable scalar compositions f(n) satisfying Box_g(f(n)) = R for every such profile, exactly f(n) = log(n) + C work.

- Accepted in: `v0.4.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: none

## C-OG-002

Conditional on C-OG-001 and the imported constitutive relation n = 1/(1 + 2*Phi/c0^2), the optical dilaton is log(n) = -log(1 + 2*Phi/c0^2), with leading weak-field term -2*Phi/c0^2. The metric's static slow coordinate-geodesic acceleration is exactly -(1 + 2*Phi/c0^2)*Phi_x; under Phi = lambda*U it satisfies acceleration/lambda -> -U_x as lambda -> 0+.

- Accepted in: `v0.4.0`
- Verification: `symbolic_verified`
- Compatibility: `compatible_extension`
- Dependencies: C-OG-001

## C-SG-001

For every real omega with 0 < omega < 1, eta = sqrt(1-omega^2), and real x,t, the field phi(x,t) = 4 atan(eta sin(omega t)/(omega cosh(eta x))) is spatially localized, periodic with period 2*pi/omega, and satisfies phi_tt - phi_xx + sin(phi) = 0 identically in normalized units.

- Accepted in: `v0.1.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: none

## C-SG-002

The C-SG-001 breather has conserved normalized Hamiltonian energy E(omega) = 16 sqrt(1-omega^2); E approaches the two-kink threshold 16 as omega -> 0+ and approaches 0 as omega -> 1-.

- Accepted in: `v0.1.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-SG-001

## C-SG-003

For every real omega with 0 < omega < 1, the C-SG-001 breather's canonical action normalized by J = (1/(2*pi))*closed_integral(p dq) is J(omega) = 16 arccos(omega). It satisfies dE/dJ = omega, maps the family onto 0 < J < 8*pi, and has inverse parameterization omega = cos(J/16) and E = 16 sin(J/16).

- Accepted in: `v0.2.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-SG-001, C-SG-002

## C-SG-004

For every real omega with 0 < omega < 1, the C-SG-001 breather's period-averaged squared-gradient integral is Gbar = (1/T)*integral_0^T dt integral_R dx phi_x^2 = 16*(sqrt(1-omega^2) - omega*arccos(omega)) = E - omega*J. It satisfies dGbar/domega = -J, approaches 16 as omega -> 0+, and approaches 0 as omega -> 1-. Gbar is the full squared-gradient integral; its Hamiltonian energy contribution is Gbar/2.

- Accepted in: `v0.3.0`
- Verification: `symbolic_verified`
- Compatibility: `native`
- Dependencies: C-SG-001, C-SG-002, C-SG-003
