# PG2 source adjudication

PG2 reproduces four symbolic checks, but its physical headline and trace
normalization do not survive audit. P061 therefore qualifies the source. The
exact periodic-potential calculus, convention-covariant SU(2) kinetic/trace
pair, and algebraic consequences of a separately declared GMOR relation
survive; the derived-GMOR, physical-pion, substrate-identity, coefficient
prediction, and absolute-scale narratives remain unaccepted.

## Reproduction and source boundary

The SHA-256-pinned PG2 file at `substrate@6d1f4e0` exits cleanly under Python
3.12.2, SymPy 1.14.0, and NumPy 2.5.1 with `ALL 4 CHECKS PASS`. It uses pure
SymPy and no numerical quadrature; neither the source nor P061 needs
`np.trapz`, and current framework code adds no compatibility alias.

The run computes a Taylor series of a declared amplitude, an SU(2) diagonal
trace, and scaling of a separately imported relation. It does not construct a
chiral current, QCD vacuum, condensate, physical pion map, decay constant,
quark-mass source, or substrate-to-SU(2) field dictionary.

## Periodic potential and generalized mass

For real `phi`, declared amplitude `A`, positive coordinate scale `F`,
positive multiplier `q`, and positive scalar kinetic coefficient `K`, P061
derives

`V=A*(1-cos(q*phi/F))`.

The origin is stationary, its curvature is `A*q^2/F^2`, its fourth derivative
is `-A*q^4/F^4`, and the scalar generalized mass squared is
`A*q^2/(K*F^2)`. PG2's declared `A=m_pi^2*F_pi^2`, `q=1` has coordinate
curvature `m_pi^2`, exactly as its first check reports. That is a named input
parameterization. With unit kinetic coefficient it has generalized mass
`m_pi^2`; with C-CHI-001's cited `F_pi^2/16` and `pi/F_pi` coordinate, the
kinetic coefficient is `1/4` and the same potential has generalized mass
`4*m_pi^2`.

Local quadratic agreement does not identify a global mechanism. The periodic
potential `h*F^2*(1-cos(phi/F))` and quadratic potential `h*phi^2/2` have the
same origin Hessian `h`; only the first is periodic, and their fourth
derivatives differ by `-h/F^2`. Thus a mass term cannot select a cosine, much
less a substrate ontology.

## SU(2) trace and kinetic convention

For `U=exp(i*q*tau3*pi/F)`, exact Pauli eigenvalues give

`Tr(U-I)=2*cos(q*pi/F)-2`.

Pair the Lagrangian terms `Z*Tr(dU*dU^dagger)+C*Tr(U-I)`. Their scalar kinetic
coefficient and positive-potential curvature are
`K=4*Z*q^2/F^2` and `H=2*C*q^2/F^2`, so the generalized mass is
`H/K=C/(2*Z)`, independent of the coordinate multiplier.

The primary Skyrme source used by PG2 states the paired coefficients
`Z=F_pi^2/16` and `C=m_pi^2*F_pi^2/8`
([Battye et al., Eq. 2](https://arxiv.org/abs/0905.0099)). They give
generalized mass `m_pi^2`. With `q=1`, `K=1/4` and `H=m_pi^2/4`; with the
canonically normalized `q=2`, `K=1` and `H=m_pi^2`. These are the same paired
quadratic physics in rescaled coordinates.

PG2's headline instead says the cited `1/8` trace term equals the full
`m_pi^2*F_pi^2*(cos-1)` expression. It does not: it is one quarter of that
expression. The passing check silently evaluates
`-(m_pi^2*F_pi^2/2)*Tr(U-I)` as a potential, which is four times the cited
trace coefficient. Its final output then names the `1/8` term and the
incompatible `-1/2` equality together. P061's primary and independent routes
both expose the exact factor four.

## Conditional GMOR ledger

P061 represents convention dependence explicitly. For positive quark-mass
sum `m_q`, positive decay scale `F`, positive convention factor `c`, and
negative condensate `Sigma`, a separately declared relation

`M^2*F^2=-c*m_q*Sigma`

has positive solution `M^2=-c*m_q*Sigma/F^2`, log sensitivities
`(1,1,-2,1)` with respect to `(m_q,Sigma,F,c)`, and zero quark-mass limit.
Both sides have mass dimension four when the inputs have dimensions
`(1,3,1,0)`. Scaling `F` by `rho` and `Sigma` by `rho^2` leaves `M^2`
unchanged, proving a continuous free-input family.

The historical GMOR paper is external current-algebra provenance
([Gell-Mann, Oakes, and Renner](https://doi.org/10.1103/PhysRev.175.2195)). A
primary modern derivation displays the current matrix element,
double-commutator mass formula, and a convention-specific condensate
definition ([Cundy and Lee, Eqs. 16, 18, and 27](https://arxiv.org/abs/1111.2638)).
Those sources show why the current, condensate, and decay-constant conventions
are load-bearing. Citation does not make the relation a substrate derivation.

PG2's log exponent one survives only as a conditional algebraic consequence
with other inputs held fixed. Its `F_pi=2*f_pi` prose is internally
inconsistent: substituting that declaration into its displayed
`m_pi^2*F_pi^2=-m_q*Sigma` gives a factor `1/4` in the `f_pi` form, not the
printed factor `1/2`. C-GMR-001 therefore retains `c` rather than canonizing
either unsupported condensate convention.

## Candidate comparison and disposition

Candidate A is rejected as the positive physical route because its clean tally
does not test its load-bearing kinetic, trace-prefactor, field-map, or GMOR
premises. Candidates B and C jointly supply the convention-consistent
periodic and SU(2) objects. Candidate D proves that local mass curvature does
not select a global breaking potential. Candidate E exposes the imported
relation and its free parameters. They were selected by structural fit,
normalization consistency, parameter transparency, limiting behavior, and
mutation sensitivity without physical comparator values.

PG2 maps to C-BRK-001, C-CHI-002, and C-GMR-001 only within their exact
conditional ceilings. It does not establish that the normalized sine-Gordon
root is a physical chiral-breaking term, derive GMOR from the framework,
predict a pion mass or decay constant, fix quark masses or a condensate,
identify a physical pion, import pending S2, or realize a substrate mechanism.
Its structured disposition is `qualified`.
