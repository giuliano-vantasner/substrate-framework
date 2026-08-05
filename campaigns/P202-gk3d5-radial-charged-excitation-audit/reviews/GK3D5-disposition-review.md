# GK3D5 Disposition Review

GK3D5 should be qualified through C-U1-001 and proposed C-QBL-004. Its smooth
conditional potential, radial equation, charge and energy normalization,
origin behavior, scaling identity, and tail exponent survive. A corrected
canonical implementation supplies the missing solver-status, zero-branch,
domain, tolerance, observable, Pohozaev, and independent-method gates.

The source's finite double-precision bisection and fixed-domain integration do
not prove infinite-domain existence. Positivity on a finite interval is not a
ground-state or monotonicity theorem. Its abstract negative potential-energy
coefficient is not an evaluated branch Pohozaev identity. Its refinement
holds the outer domain and shooting classifier fixed and truncates the
observables when growing-tail roundoff turns the profile around.

EM6 does not supply action derivation or VK stability, and accepted
one-dimensional Q-ball claims do not lift to three dimensions. C-PDE-001 is a
separately declared real radial IVP. The fitted `kappa` is a classical profile
inverse length, not a rest mass, propagator pole, or free determinant-field
mass. Neither C-VAC-002 nor C-VAC-003 derives the GK3D5 scalar as physical loop
matter.

The recommended mapping is `[C-U1-001,C-QBL-004]`. No stability, quantum
particle, determinant insertion, physical electric charge, preferred scale,
or substrate realization is accepted. GK3D6 remains pending for its own
audit. Already-qualified EL2 retains its prior mapping and supplies no
retroactive authority.

GK3D5's lazy `getattr(np,"trapezoid",None) or np.trapz` selects the current
name in the present environment. The legacy name is immutable compatibility
provenance only. New canonical and campaign code uses `trapezoid_integral` or
`np.trapezoid`, and zero scientific failures are assigned to version events.
