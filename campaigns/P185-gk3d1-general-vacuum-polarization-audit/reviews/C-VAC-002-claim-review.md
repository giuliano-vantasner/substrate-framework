# C-VAC-002 Claim Review

## Proposed statement

C-VAC-002 is a conditional charged-Dirac one-loop theorem. It declares the
quantum action, statistics, tensor and effective-action conventions, regulator,
integration dimension, integer spinor trace, mass, charge, and renormalization
scheme. It derives the integrand Ward difference, general spacelike parameter
master, massless D=2 endpoint, fixed-trace D=4 Laurent and MS-bar family,
below-threshold subtraction and series, and convention-invariant group weight.

## Verification axis

Symbolic verified. The primary verifier passes 27 checks. An independent script
that imports no canonical Dirac polarization module passes 23 checks, including
generic matrix trace algebra, six independently integrated beta coefficients,
the D=4 Gamma-function Laurent limit, and 80-digit adaptive quadrature. Numeric
quadrature is regression evidence only; exact SymPy identities carry the claim.

## Review axis

Accepted. The formula and domains were frozen before implementation. Wrong
inverse-propagator sign, doubled spinor trace, shifted finite counterterm,
threshold crossing, and unpaired generator rescaling all change or invalidate
the relevant result. The source's native nineteen-check tally is not used as a
blanket oracle.

## Compatibility axis

Compatible extension. C-VAC-002 depends on C-GAU-001 and C-DIM-009. It does not
modify C-VAC-001: that claim is a massive complex-scalar D=2 bubble-plus-seagull
theorem whose fixed-momentum massless limit diverges. C-MAX-001 remains an
independently supplied classical kinetic action and coefficient.

## Epistemic axis

Active only within its conditional model. No accepted claim identifies the
Dirac field with substrate matter, chooses a physical dimension or group,
fixes a finite counterterm or matching condition, or converts the loop term
into a total kinetic normalization or observed coupling.

## Claim-level verdict

Accept C-VAC-002 exactly at the reviewed conditional scope. Reject any reading
that analytically continues `2^floor(d/2)`, calls dimensional continuation
regulator-free, merges scalar and fermion statistics, omits `i0` above the pair
threshold, or treats a pole residue/log slope as a selected total Maxwell term.
