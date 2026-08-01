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
