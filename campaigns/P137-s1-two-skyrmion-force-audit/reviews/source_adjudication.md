# S1 source adjudication

S1 is qualified, not accepted wholesale. It natively executes eleven checks,
but the tally combines three different objects: the accepted declared
one-coordinate optical action, a supplied Yukawa index profile, and assigned
schematic spin/isospin literals. There is no derivation connecting those
objects into a physical two-Skyrmion or nucleon force.

The optical variation in S1.1 reproduces C-CC-001. For the separately declared
profile `delta_n=kappa*exp(-mR)/R`, its derivative, sign, and exponential decay
are exact. The corrected negative Yukawa well in S1.3 is only the first-order
term: the exact zero-velocity C-CC-001 potential for finite positive index is
`c0^2*(n^-2-1)/4`. The source does not derive `kappa`, `m`, or the profile from a
field equation. C-MED-001 separately blocks density-only sourcing in the
accepted co-scaled constitutive ansatz.

S1.6 is rejected as numerical evidence. Its implemented acceleration omits the
final `1/R` in the derivative of its own Yukawa profile, so the source RHS is
larger than the exact RHS by `R`. The sign-only trajectory still passes. The
script also does not check `solve_ivp.success` and performs no step, tolerance,
domain, method, or independent-solver refinement.

The `R^-2` massless B=1 endpoint in S1.4 is already conditional C-RPROF-001
algebra and creates no physical pion or Skyrmion. S1.5 and S1.G2 assign
`tau_A.tau_B` as plus or minus three, inspect two spin directions, and add
schematic scalars. They do not construct a source-coupled energy or optimize
the full relative-orientation space. The cited ANW 1983 paper concerns static
single-nucleon properties; later primary work treats the dipole description as
a long-range approximation and requires separate classical and quantization
steps for a nucleon potential.

P137 supplies a corrected positive object as C-SKY-001. Conditional on a
declared three-component massive linear field and two equal triplet point-
dipole sources, isolated-self-energy subtraction leaves an exact Yukawa-Hessian
cross term. Fresh Cartesian/Fourier derivation and Rodrigues certificates prove
the global SO(3) minimum and maximum. A pi rotation about any axis perpendicular
to separation is most attractive; a pi rotation about the separation axis is
most repulsive. The attractive fixed-orientation force is strictly inward for
positive source magnitude and exponentially finite-range for positive mass.

C-SKY-001 remains a declared long-range linear-field theorem. It establishes
no nonlinear Skyrme action, B=1 solution, two-center minimizer, short-range
core, quantization, nucleon state, nuclear binding, material, or observation.
No historical consumer inherits it automatically.

Decision: accept C-SKY-001 as `symbolic_verified`; qualify S1 through
C-CC-001, C-VIR-001, C-RPROF-001, and C-SKY-001; reject the broader physical
and numerical readings.
