# PG1 source adjudication

PG1 reproduces four symbolic checks and contains useful conditional model
algebra, but it does not derive the physical pion or a quantum Goldstone
particle from the accepted framework. P060 therefore qualifies the source:
the exact classical stationary symmetry-Hessian theorem and its declared
O(4)/SU(2) coordinate examples survive, while the chiral, pion, GMOR,
Skyrmion, and substrate narratives remain unaccepted.

## Reproduction and object boundary

The SHA-256-pinned PG1 file at `substrate@6d1f4e0` exits cleanly under Python
3.12.2, SymPy 1.14.0, and NumPy 2.5.1 with `ALL 4 CHECKS PASS`. It never calls
`np.trapz`; P060 uses no quadrature and adds no compatibility alias. The
executed objects are a declared radial quartic, a derivative carrier built
from Pauli matrices, two group-dimension subtractions, and a linearly tilted
quartic. No accepted chiral action, order parameter, physical field map,
quantum state, charge algebra, spectral pole, or substrate-to-pion mechanism
is constructed.

## Exact stationary symmetry-Hessian theorem

For a real coordinate column `phi`, a twice-differentiable potential `V`, and
a supplied linear generator `T_a`, define the actual infinitesimal invariance
residual `r_a=grad(V)^T*T_a*phi`. Direct differentiation gives

`grad(r_a)=H*T_a*phi+T_a^T*grad(V)`.

If `r_a` vanishes identically and the declared vacuum `v` is actually
stationary, then `H(v)*T_a*v=0`. The rank of the matrix with columns `T_a*v`
counts the independent zero directions. If the supplied generators form an
independent basis, the kernel dimension of that coefficient-to-tangent map is
the stabilizer dimension. A separately proven positive-definite kinetic
metric `K` converts the result into zero modes of the generalized quadratic
operator `K^-1*H`. It neither creates Hessian zeros nor supplies a quantum
particle interpretation.

The canonical implementation returns the raw invariance, stationarity,
differentiated-identity, tangent, and Hessian-kernel residuals even when a
premise fails. At a nonstationary point an invariant potential need not have a
tangent Hessian zero. An anisotropic mass term and a linear tilt make the
relevant invariance residual nonzero and lift the corresponding curvature.
Dependent generator labels do not inflate tangent rank and cannot be called a
stabilizer basis.

## O(4) specialization and actual count

P060 constructs all six standard antisymmetric generators of `so(4)`. At
`(v,0,0,0)` their tangent matrix has rank three, and its coefficient kernel
has dimension three. For

`V=lambda*(phi^T*phi-v^2)^2`,

the exact Hessian is `diag(8*lambda*v^2,0,0,0)`. Thus the declared model has
three independent classical quadratic zero directions and one radial
curvature for positive `lambda` and nonzero `v`. At the symmetric stationary
point `phi=0`, all six tangents vanish and the broken-tangent rank is zero,
showing why `dim(G)-dim(H)` labels alone are not an oracle.

For `V-c*sigma`, a shifted stationary point `s0` satisfies
`c=4*lambda*s0*(s0^2-v^2)` and has transverse curvature `c/s0`. This is an
exact sigma-model identity, not a derivation of the Gell-Mann–Oakes–Renner
relation or a measured pion mass.

## SU(2) coordinate normalization

For the declared coordinates `U=exp(i*tau_a*pi_a/F)`, direct Pauli
multiplication gives `Tr(tau_a*tau_b)=2*delta_ab` and hence
`Tr(dU*dU^dagger)=2*sum_a(dpi_a^2)/F^2` at quadratic order. Therefore the
prefactor `F^2/4` gives `L_quad=sum_a(dpi_a^2)/2` and kinetic metric `I`, while
`F^2/16` gives `L_quad=sum_a(dpi_a^2)/8` and kinetic metric `I/4` in those same
coordinates.

PG1's executed predicate correctly checks both coefficients, but its final
RESULT says the `F^2/16` expression is canonical one half. That printed
sentence is wrong by a factor of four unless the coordinate is separately
rescaled. Such a rescaling changes the coordinate convention; it does not
make both coefficients simultaneously canonical for the same `pi_a`.

The source's mass-absence check introduces bare symbols that never enter an
expression built only from declared derivative symbols. Its dispersion check
then substitutes `m_pi=0` into an assumed polynomial. P060 instead keeps the
potential Hessian and kinetic metric as distinct inputs; only a declared
derivative-only action has zero potential curvature.

## Quantum and physical interpretation ceiling

Goldstone, Salam, and Weinberg's quantum theorem concerns a continuous
Lagrangian symmetry, its vacuum realization, and zero-mass spin-zero
particles ([Physical Review 127, 965](https://journals.aps.org/pr/abstract/10.1103/PhysRev.127.965)).
Those quantum objects are stronger than P060's finite-dimensional classical
Hessian theorem and are not constructed here. Adkins, Nappi, and Witten study
a declared chiral theory and Skyrme model
([Nuclear Physics B 228, 552](https://www.sciencedirect.com/science/article/abs/pii/055032138390559X));
that model provenance does not establish the same field content in this
framework.

Names cannot close the gap. Relabeling the O(4) coordinates leaves every
source predicate unchanged. Pending PG2, PG4, and S2 supply no accepted
explicit-breaking, pion-to-nucleon, hedgehog, decay-constant, or physical
field-map premise. The prose relation `F_pi^2=8J/a` is not exercised and is
not imported.

## Disposition

PG1 maps to C-SYM-001's exact stationary symmetry-Hessian and tangent-rank
theorem and C-CHI-001's declared O(4) and SU(2) quadratic specializations. It
does not establish a framework chiral symmetry action or its breaking, a
quantum Goldstone particle, a physical pion or sigma, GMOR, a Skyrmion or
nucleon connection, a decay constant, a pion mass, an absolute scale, or a
substrate realization. Its structured disposition is `qualified`.
