# G3 source adjudication

G3 is qualified, not accepted wholesale. Native execution exits cleanly and
prints all eleven checks passing. It contains no NumPy integration call, so no
compatibility overlay is involved. Several narrow symbolic results are sound:
the declared canonical scalar action gives the standard stress and trace, the
static scalar Euler equation is exact, the static stress divergence factors
through the scalar residual, on-shell stress is conserved, and the wrong kinetic
sign has negative gradient energy.

Those results do not establish G3's headline. The executable source declares a
positive `kappa` but never loads it. It independently chooses
`g=diag(-1,1,C,C)` with `C=1+exp(-x^2)/5` and
`phi=log(1+3*exp(-x^2)/10)`, then computes only `G_tt/T_tt` at `x=1` and checks
that its magnitude is nonzero. Exact reconstruction gives

`kappa_fit=(3+10e)^2*(-10e-1)/(18*(1+10e+25e^2))`,

which is negative. After that point fit, the exact covariant Einstein residuals
are zero only in `tt`; they are `2/(1+5e)` in `xx` and `-1/(5e)` in each
transverse component. The massless scalar residual is also nonzero. This is not
a solution of the source's declared coupled equations.

The optical contrast does not repair it. G3's own small-amplitude calculation
has `G_tt=O(epsilon)` and `T_tt=O(epsilon^2)`, so at its `x=1` profile the ratio
is `-e/epsilon+1/2` and diverges rather than tending to the zero coupling named
by the check title and result prose. Its imported nonminimal optical-dilaton
`Delta` is not componentwise matched to the canonical stress. Nor does
`Delta=0` characterize vacuum: `n=exp(x)` has nonzero gradient while the stated
Delta vanishes at `x=2`. Constant `n` gives canonical vacuum only jointly with
`V(phi0)=0`; G3 separately sends its Liouville amplitude to zero.

C-STG-001 is the corrected positive object. For the declared mostly-plus action

`S=int sqrt(-g) [R/(2*kappa) - (partial phi)^2/2 - V(phi)] d^4x`,

the stress is
`T_ab=phi_a*phi_b-g_ab*((partial phi)^2/2+V)`. With `V=0`, positive `kappa`,
and `t>0`, the spatially flat FLRW metric and homogeneous scalar

`a(t)=a0*(t/t0)^(1/3)`,

`phi(t)=phi0 plus_or_minus sqrt(2/(3*kappa))*log(t/t0)`

solve every Einstein component and the scalar equation exactly. They have
`H=1/(3t)`, `rho=p=1/(3*kappa*t^2)`, `R=-2/(3t^2)`, and Kretschmann scalar
`20/(27*t^4)`. A fresh four-dimensional Christoffel-to-Riemann reconstruction,
contracted Bianchi check, direct stress derivation, trace, continuity, and
curvature contraction reproduce the result without importing the package.
Wrong expansion exponent, scalar normalization, and kinetic sign all fail.

This exact solution is homogeneous and extensive on noncompact spatial slices;
it is not a localized breather geometry. It fixes no refractive map, potential
for G3's static witness, transverse compactification, physical coupling,
material mechanism, observation, or substrate ontology.

Decision: promote C-STG-001 and qualify G3 through its exact canonical stress,
static scalar variation, conservation identity, and kinetic-sign guard only.
Reject its one-point coupling as a solution, the `Delta=0` vacuum equivalence,
the zero optical-coupling prose, and every breather-sourced, independent-route,
physical-gravity, and substrate interpretation. The exact primary and
independent derivations, source counterexamples, mutations, frozen graph,
compatibility classification, and scope audit leave no hidden debt in the
qualified result.
