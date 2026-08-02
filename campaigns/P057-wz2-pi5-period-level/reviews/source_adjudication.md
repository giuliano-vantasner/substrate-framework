# WZ2 Source Adjudication

WZ2 is qualified. Its conditional filling-phase idea survives after an exact
replacement establishes the sphere period, but its advertised map and every
claim that depends on that map fail before numerical accuracy is relevant.

## Reproduction and Decisive Source Failure

The hash-pinned source at `substrate@6d1f4e0` exits cleanly with
`ALL 8 CHECKS PASS` under Python 3.12.2, NumPy 2.5.1, SciPy 1.18.0, and SymPy
1.14.0. WZ2 does not call the removed `np.trapz`; P057 uses neither that legacy
name nor a compatibility alias.

WZ2 defines `U=I+(exp(iF)-1)P` for a rank-one projector. Its eigenvalues are
`exp(iF),1,1`, hence `det U=exp(iF)`. The map is unitary but is not SU(3)-valued
except at isolated radial values. The executable checks unitarity at one point
and never checks determinant one.

The quotient obtained by collapsing the ends of `[0,2*pi] x CP2` is the
suspension of `CP2`, not `S5`. Suspension shifts reduced homology, so it has
`reduced H3=Z` and `reduced H5=Z`, whereas `S5` has zero `H3`; its suspension
poles also do not have sphere links. Thus WZ2 integrates a U(3) construction
over a non-sphere quotient and cannot label the result an SU(3) `pi5` period.

## Validation-Theater Findings

The source uses the trace integral under review to call its cycle a generator,
then uses `round` on four coarse values to select the desired integer. It does
not refine the finite-difference step or compare an independent integral. Its
"doubled map" does not evaluate another map: `F_integral` is multiplied by the
input `nwind`, making the reported factor two true by construction. The open
cycle guard varies the endpoint and therefore compares different chains, not
two parametrizations of the same chain. These checks cannot repair the failed
group and domain hypotheses.

## Exact Replacement Generator

P057 uses Puttmann and Rigas, Lemma 1.1 and Theorem 2.1. For a unit
`z in C3`, their explicit map is

`eta(z)=z*z^T+A(conjugate(z))`,

where `A` is the complex cross-product matrix. Direct polynomial algebra gives
`det eta=|z|^4` and
`eta^dagger eta-I=(|z|^2-1)(I+conjugate(z)*z^T)`, so the restriction is exactly
SU(3)-valued. The first-column projection has regular value `(1,0,0)` at
exactly `z=+(1,0,0)` and `z=-(1,0,0)`. In boundary-oriented frames, both real
Jacobian determinants are `8`, hence the degree is `+2`. The audited fibration
criterion divides this degree by `(3-1)!=2`, independently certifying the
positive primitive `pi5(SU3)` class.

## Exact Period and Independent Regression

The generator is SU(3)-equivariant and the trace form is invariant under its
constant left-right action. Its pullback is therefore an invariant top form on
the transitive oriented SU(3) sphere. One exact evaluation at `(1,0,0)` fixes
the density globally. On the positive tangent frame
`(i e1,e2,i e2,e3,i e3)`, P057 obtains

- `Alt Tr(theta^5)=-480*i`,
- `Omega5=-i Alt Tr(theta^5)=-480`, and
- `integral_S5 Omega5=-480*pi^3` because `Vol(S5)=pi^3`.

Orientation reversal changes the sign. Homotopy invariance and the primitive
generator theorem give `-480*pi^3*n` for class `n`. This exposes WZ2's
load-bearing factor-two error: its `1/(i*240*pi^3)` is not the unit winding
normalization for a primitive SU(3) sphere map.

An independent review reimplements the map without canonical WZW helpers,
uses central finite differences in five hyperspherical coordinates, and
performs five-dimensional tensor Gauss-Legendre cubature. Density errors fall
by a factor of four under each step halving. Cubature orders 3, 4, 5, and 6
have relative period errors `0.3602`, `0.05560`, `0.006438`, and `0.0005120`.
Orientation, reality-factor, half-period, and half-level mutations all fail.

## Sphere-Filling Level and Ceiling

For two oriented five-ball extensions of a common `S4`, the glued domain is an
oriented `S5`. With `c=k/(240*pi^2)`, its phase ambiguity is
`exp(-2*pi*i*k*n)`, equal to one for every integer winding exactly when `k` is
integer. This is the accepted mathematical sphere-filling level theorem.

P057 does not derive the period lattice on arbitrary closed five-manifolds,
any needed bordism or spin refinement, an identification `k=N_c`, a baryon
current, representation selection, gauge descent or anomaly inflow, physical
WZW dynamics, absolute scale, or a substrate realization. S3, S4, WZ3, and WZ4
remain pending and supply no premises.

## Terminal Disposition

WZ2 maps only to `C-WZW-002`, through the exact replacement rather than its
failed generator. Its process exit, local projector algebra, radial profile,
and conditional phase examples remain historical evidence. The SU(3) map,
`S5` identification, normalized integer integral, numerical generator witness,
non-tautological additivity, `N_c`, and physical interpretations are rejected.
