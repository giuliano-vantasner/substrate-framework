# LB1 Source Adjudication

LB1 is qualified. Its exact energy balance, kinetic average, and form factor
survive, but its full-amplitude e-fold headline does not.

For the accepted normalized sine-Gordon conventions, C-SG-012 specialized to
`R=-Gamma*phi_t` gives the exact local balance. With vanishing boundary flux,
`dE/dt=-Gamma*integral(phi_t^2)dx`. The undamped C-SG-001 breather family and
C-SG-003 action then give the exact period average
`<integral(phi_t^2)dx>=omega*J=16*omega*acos(omega)`. Therefore
`D(omega)=omega*acos(omega)/sqrt(1-omega^2)`. The source's six expensive
mpmath values reproduce this formula. Writing `theta=acos(omega)` makes
`D=theta*cot(theta)`: it tends from zero to one as omega rises from zero to
one, is strictly increasing in omega, and equals `pi/4` at `omega=1/sqrt(2)`.

The source's lifetime semantics fail at finite amplitude. Period averaging and
`dE/dJ=omega` imply `dJ/dt=-Gamma*J`, not global exponential energy. Thus
`J(t)=J0*exp(-Gamma*t)`,
`omega(t)=cos((J0/16)*exp(-Gamma*t))`, and
`E(t)=16*sin((J0/16)*exp(-Gamma*t))`. The source expression
`1/(Gamma*D(omega_initial))` is exactly the initial local tangent time
`-E/E_dot`; freezing it does not integrate the changing rate. The true reduced
energy e-fold time is
`log(theta0/asin(sin(theta0)/e))/Gamma`. At the source working frequency these
dimensionless times are about 1.09344 and 1.27324, respectively.

Independent SciPy field quadrature recovers the kinetic identity and form
factor at four amplitudes. A separate DOP853 action solve and root finder
recover the integrated crossing. Full damped-PDE evidence starts from the
exact phase-zero `omega=1/sqrt(2)` breather under uniform `Gamma=0.02` and zero
drive on domains 60 and 80. Three leapfrog grids, DOP853, a lossless control,
and `Gamma=0.01` at equal slow time give sub-percent trajectory errors,
second-order balance refinement, domain and method agreement, and improving
adiabatic error. The evolving law has about 0.58% fine-grid energy RMS error;
the frozen source law has about 3.14%.

This is simulation evidence for a slow-damping, finite-time adiabatic family
reduction, not an exact damped breather. Radiation, deformation, boundary, and
higher-order averaging errors remain inside the stated numerical ceiling. The
small-action limit does recover exponential energy and e-fold time `1/Gamma`.

LB1 derives no physical medium lifetime. Gamma is an input with normalized
inverse-time units. The source imports no collision, density, cross-section,
material, or physical-unit relation; its backward pointer to pending MC3 is not
authority. LB2's explicitly small-amplitude use is compatible. LB3's
current-frequency local-rate comparison is structurally compatible but remains
pending. LB4 and engineering globalize the small-amplitude exponential and add
unaccepted thermal, survival, and medium premises.

`C-SG-016` therefore records the exact family identities and the narrowly
qualified phase-averaged model with its measured approximation ceiling. It
establishes no exact positive-Gamma breather, global exponential energy or
amplitude law, fixed-frequency finite decay, physical lifetime, medium map,
coherence probability, population, event channel, or substrate realization.
