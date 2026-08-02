# P077 Source Adjudication: AS6

AS6 is qualified. Its reciprocal-map algebra survives, but its claim that an
accepted framework duality selects `beta^2=4*pi` does not.

## Reproduction

The hash-pinned source exits cleanly and prints `ALL 9 CHECKS PASS`. Its exact
fixed-point and substitution arithmetic reproduce, and it uses no NumPy
integration or trapezoidal alias. The tally does not establish that the map is
a physical duality, that a theory must occupy its fixed subfamily, or that its
physical labels are dependency closed.

## Reciprocal-Map Audit

For every separately supplied positive coefficient `A`, the map
`D_A(x)=A/x` is an involution, every orbit has product `A`, and the unique
positive fixed coordinate is `sqrt(A)`. AS6's coefficient `A=16*pi^2`
therefore gives `4*pi` exactly. Changing the coefficient to `25*pi^2` moves
the fixed coordinate to `5*pi`, and choosing `A=t^2` makes any supplied
positive target `t` fixed. The coefficient is a load-bearing premise, not an
output of fixed-point algebra.

Generic positive coordinates remain valid off-fixed dual pairs. For example,
`D_9(2)=9/2` and applying the map again returns 2, although neither coordinate
is the fixed point 3. A duality relation therefore does not require
`x=D_A(x)`; restricting a theory to a self-dual subfamily is a separate
premise or selection problem.

## Normalization Audit

Under the positive coordinate change `x'=rho*x`, conjugating the same map
requires `A'=rho^2*A`, and the numeric fixed coordinate becomes
`rho*sqrt(A)`. Holding `A` fixed fails this conjugation. Consequently a numeric
value such as `4*pi` is meaningful only after the coupling coordinate and map
normalization have been fixed independently.

AS6 constructs no Lagrangian, Hamiltonian, partition function, observable,
field transformation, domain, or solution-family equivalence. The accepted
C-SG-001 model is the classical normalized `c=m=beta=1` sine-Gordon equation;
there is no accepted dictionary that turns its fixed beta convention into the
quantum coupling coordinate used in AS6.

## Primary-Literature Audit

Coleman's [1975 paper](https://doi.org/10.1103/PhysRevD.11.2088) supports the
narrow statement that `beta^2=4*pi` is the free-massive-Fermi point in his
explicit quantum sine-Gordon/massive-Thirring normalization. It does not state
AS6's reciprocal map and does not supply a normalization map from C-SG-001.

Lecheminant, Gogolin, and Nersesyan's
[self-dual sine-Gordon paper](https://arxiv.org/abs/cond-mat/0203294) defines a
self-dual *extension* with both `cos(beta*Phi)` and
`cos(beta_tilde*Theta)`. Equal dimensions and equal amplitudes make that
two-field action invariant under `Phi<->Theta`. Its XY normalization has
`beta=N/sqrt(K)` and `beta_tilde=2*pi*sqrt(K)`, so exchanging them maps
`x=beta^2` to `4*pi^2*N^2/x`. Thus at `N=2` it conditionally realizes AS6's
`16*pi^2/x` map and fixed coordinate `4*pi`. The same N=2 equal-amplitude
model has one massive and one massless Majorana sector; unequal amplitudes
make both massive. AS6 and the accepted root contain neither the dual field,
the second cosine, equal amplitudes, nor an accepted `N=2` dictionary. The
paper therefore supplies a legitimate conditional model for the algebra, but
not ordinary one-cosine sine-Gordon self-duality or a mechanism selecting the
accepted framework's coupling.

## Phase, Hierarchy, and Physical-Label Audit

The source phase `exp(i*x/4)` equals `-1` at `x=4*pi`, but also at `12*pi` and
infinitely many other positive coordinates, so that predicate cannot uniquely
select `4*pi` or derive fermionic statistics.

Substituting the supplied `x=4*pi` and hard-coded `b0=7` into
`8*pi^2/(b0*x)` does give `2*pi/7`. C-RGE-003's accepted inverse-energy
orientation gives the equal-conversion transmuted/reference length ratio
`exp(+2*pi/7)`. AS6 instead labels `exp(-2*pi/7)` as `a/xi`, repeating the
reversed AS1/AS5 physical assignment. The reciprocal-map algebra derives
neither `b0=7`, an absolute scale, nor the `a,xi` labels.

Arithmetic on supplied `0.6 fm`, `1e5 fm`, and `3.62 Angstrom` values does not
construct an EFT cutoff, periodic structure, form factor, Bragg condition, or
X-ray scattering oracle. C-TOP-002 explicitly excludes a physical baryon
identification, so AS6's WZ3 analogy cannot supply electric/topological
symmetry or select a coupling. The source itself also records a later
withdrawal of fixed-point occupancy; pending AS7 is not needed or used as
authority for this decision.

## Terminal Decision

AS6 maps to the new C-SYM-002 conditional reciprocal-coupling ledger, plus the
existing interpretation ceilings of C-SG-001, C-RGE-003, C-DIM-008, and
C-TOP-002. It does not establish a physical sine-Gordon/Coulomb-gas duality,
self-dual operating point, Coleman-normalization import, fermion sector, QCD
coefficient, confinement hierarchy, physical cutoff, Bragg response, X-ray
invisibility, baryon identity, or absolute scale.
