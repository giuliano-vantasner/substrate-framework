# W4 source adjudication

W4 is qualified, not accepted wholesale. Native execution exits cleanly with
all eight source checks passing and no NumPy trapezoid compatibility event.
That tally reproduces the code but does not validate the missing-particle or
charged-current headline.

The decisive exact issue is simultaneous four-momentum closure. At
center-of-mass threshold `(m1+m2,0)`, subtracting an observed on-shell vector
`(m1*cosh(theta),m1*sinh(theta))` leaves a residual whose mass-shell defect
relative to `m2` is
`2*m1*(m1+m2)*(1-cosh(theta))`. For positive masses and real rapidity this is
zero only at `theta=0`. Both particles are then at rest. Any nonzero recoil
requires above-threshold energy or a separately modeled non-particle channel.

W4 instead sets `gamma_abs=2-gamma_refl`. It is below one for every moving
observed kink. At the source's `v=0.6` point, the observed mass-eight vector is
`(10,6)` and the residual of the fixed total `(16,0)` is `(6,-6)`. Its invariant
mass is zero, not eight. Assigning opposite momentum therefore does not repair
the energy ledger. Two on-shell equal-mass particles with those momenta require
total energy twenty.

W4.1 and the frequency portion of W4.6 reproduce the accepted breather energy
and scalar threshold-deficit partition. W4.2 correctly distinguishes two
expressions, but equality of their energies does not identify an intact
breather or any event. W4.3 and W4.4 close and bound an algebraic residual, not
an on-shell hidden free kink. W4.5 supplies neither boundary momentum exchange
nor a neutrino state.

The charge guards also fail as physical implications. W4.G1 writes zero into a
Piecewise after assigning zero charge. Its own imported outcome catalog
includes both constituents absorbed with zero reflected charge. W4.G2 obtains
negative residual energy for boosted reflected particles; this signals an
incomplete fixed-total ledger or omitted drive work, not exact zero missing
energy. Charge, boundary storage, radiation, detector acceptance, and particle
identity are separate data.

Decision: promote C-KIN-001 and qualify W4 through that theorem plus the
accepted sine-Gordon energy, stress, boundary, and charge ceilings. Do not
promote a moving hidden free kink, missing-energy fraction as a measured
observable, neutrino recoil, charge-conditioned invisibility, physical V-A
current, weak interaction, detector event, or substrate mechanism. Primary,
fresh independent, focused, and graph routes pass 33, 15, 13, and 25 checks;
the graph pins 63 source predicates and six assertions, with no unresolved
campaign debt.
