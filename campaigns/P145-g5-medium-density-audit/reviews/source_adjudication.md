# G5 source adjudication

G5 is qualified, not accepted wholesale. Native execution exits cleanly and
reports all fifteen checks passing, and its source has no NumPy integration
compatibility event. That tally proves the raw arithmetic, symbolic
substitution, and selected wrong-form inequalities that execute. It does not
validate the unit types or independence of the headline medium quantities.

The first displayed relation is the exact SI identity
`epsilon_0*mu_0=1/c^2`. Current SI fixes `c` exactly and makes
`epsilon_0=1/(mu_0*c^2)`; epsilon and mu therefore share one uncertainty and
are not two independent empirical medium inputs. Reproducing c from their
product is a constants regression, not a prediction of an elastic substrate.

The central density claim is dimensionally invalid. In SI M,L,T,I order,
permittivity has column `(-1,-3,4,2)`, while mass density has
`(1,-3,0,0)`. Dividing epsilon by two changes no dimension. Both L2 forms are
permittivities because `1/(mu_0*c^2)=epsilon_0`. G5 operates on raw floats,
then prints kg/m^3; it never runs its dimension helper on either L2 expression.

The energy claim has the same defect. Inverse permeability has column
`(-1,-1,2,2)`, whereas stiffness and energy density have
`(1,-1,-2,0)`. Bare `1/(2*mu_0)` is not J/m^3. A mechanical dictionary
needs a common dimensioned calibration, and its quadratic energy also needs a
dimensionless strain amplitude. An electromagnetic energy density instead
needs a field amplitude squared. G5 supplies neither and again checks only raw
decimals.

The accepted correction is C-MED-005. The general SI dictionary
`rho=a*epsilon`, `K=b*mu_inverse` requires both conversion factors to have
dimension `(2,0,-4,-2)`. It gives
`c_m^2=(b/a)*mu_inverse/epsilon`, so for positive factors the mechanical and
electromagnetic speeds agree exactly iff `a=b`. Their common value remains a
free calibration: rescaling it changes density, stiffness, and energy while
leaving speed fixed. For dimensionless strain `xi`,
`u=K*xi^2/2` and `u/c_m^2=a*epsilon*xi^2/2`; at unit strain this is half the
inertial coefficient, not that coefficient itself.

G5's first three outputs are not three independent predictions. Their log rows
on `(epsilon,mu,kappa)` have rank two and L3 is exactly L1 plus L2. The source
linkage guard merely counts whether names occur in hand-built Python sets.
Adding L4 raises the full output rank to three only because free kappa supplies
the third input direction. The one left-null relation is the already imposed
L3 product identity, not a new physical constraint.

The L4 algebra is conditionally true but does not derive gravity. After
`kappa=8*pi*G_eff` and `epsilon_0*mu_0=1/c^2` are supplied, the displayed
formula is a substitution. Its dimension check first assigns kappa the SI
dimension of Newton G. A coupling multiplying energy density in an Einstein
equation instead has G/c^4 dimension, and a mass-density source requires G/c^2.
C-GRV-001 already governs this source-typing ceiling. G1 through G4 are
qualified and contribute no rejected material or physical-gravity authority.

Decision: promote C-MED-005 and qualify G5 through C-MED-001, C-MED-005,
C-IDN-001, and C-GRV-001. Retain its exact SI product, wrong-form dimension
guards, free-kappa derivative, and conditional L4 only under those ceilings.
Do not promote its mass density, strain-energy density, three-independent-
prediction claim, physical medium, absolute gravity, observed value, or
substrate mechanism. Primary, fresh independent, focused, and frozen-graph
routes pass 36, 20, 17, and 34 checks, with 145 graph predicates and no
unresolved campaign debt.
