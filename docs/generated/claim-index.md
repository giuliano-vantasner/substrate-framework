<!-- GENERATED: scripts/render_docs.py; DO NOT EDIT -->
# Accepted claim index

This document is generated from `governance/claims.yaml`.

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
