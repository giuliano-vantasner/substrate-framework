# PG3 Source Adjudication

PG3's eight-check process exits cleanly and its static profile contains useful
conditional evidence, but its bound-mode, quantum-number, gap-ratio, and Roper
headline do not survive action-level audit.

## Reproduction Boundary

The audited unit is the SHA-256-pinned PG3 file at
`substrate@6d1f4e0`. Its native Python 3.12.2 process under NumPy 1.26.4,
SciPy 1.14.1, and SymPy 1.14.0 exits zero after 166.65 seconds with `ALL 8
CHECKS PASS`. The source's local NumPy dispatch correctly uses the new
`trapezoid` name when present and retains `trapz` only for its legacy NumPy
environment. Canonical P062 code calls the shared compatibility helper, which
uses `numpy.trapezoid` in the framework's NumPy 2.5.1 environment.

## Action and Stationarity

The declared reduced static density is

`e=(r^2+2 sin^2 f) f'^2+2 sin^2 f+sin^4 f/r^2`.

Exact variation reproduces PG3's ODE. Independent DOP853 Robin-tail shooting
and `solve_bvp` collocation both find a nontrivial branch with fitted origin
slope approaching 2.007528 and energy coefficient approaching 1.2314 as the
outer domain grows. Simpson and trapezoidal energy routes agree, the E2/E4
virial imbalance decreases, and an independently finite-differenced EOM
residual decreases by approximately four under each spacing halving. This
supports a conditional stationary-profile claim.

PG3's advertised machine-epsilon stationarity number is not independent: it
defines `fpp_exact` with the ODE right-hand side and immediately substitutes it
into the same ODE residual. The remaining finite-difference cross-check is the
actual numerical stationarity evidence.

## Exact Second Variation

For `f+epsilon*eta`, the coefficient of `epsilon^2` before integration by
parts is `A eta'^2+B eta eta'+D eta^2`, where

- `A=r^2+2 sin^2 f`,
- `B=4 sin(2f) f'`, and
- `D` is PG3's displayed local `C_pot`.

Endpoint-fixed integration by parts gives the self-adjoint coefficient
`C=D-B'/2`. PG3 uses `D` alone and says stationarity removes the mixed term;
it does not. P062 derives the complete epsilon expansion and Green boundary
form symbolically twice. Omitting the correction changes the load-bearing box
level and, when combined with PG3's removed-origin window, reproduces the
source's reported scale.

## Continuum and Wall Test

The separately declared kinetic weight is `W=A`. In the massless tail,
`A/W` tends to one and `C/W` tends to `2/r^2`, then zero. The half-line
continuum therefore begins at `Omega^2=0`. A positive level in a finite
Dirichlet box is not below that threshold and cannot be called bound.

With the complete Hessian and physical-origin endpoint, consistent-mass FEM
gives lowest levels 0.131132, 0.061072, and 0.034754 at outer walls 12, 18,
and 24. A separate mass-lumped finite-volume route gives 0.131130, 0.061072,
and 0.034754. The products with wall radius squared approach a constant, and
the node counts remain 0, 1, 2, 3. This is the expected continuum box ladder,
not convergence to a positive localized mode. PG3's N-to-2N test refines only
the mesh while holding the decisive walls fixed.

## Derrick, Quantum Labels, and Scale

For `f_s(r)=f(exp(s)r)`, the exact tangent is `r f'` and the energy is
`exp(-s)E2+exp(s)E4`. At `E2=E4`, its curvature is `E2+E4>0`; dilation is
stiff, not an exact zero direction. PG3's interpolated one-dimensional radial
shift is not a rigid translation of the full three-dimensional hedgehog and
does not verify the asserted l=1 translational mode.

The quantum check assigns `roper_J=J_N` and then checks that one half differs
from three halves. Spatial `l=0` does not derive the pending collective
quantization, spin/isospin, fermionic, parity, baryon, or Roper map. Likewise,
a Hessian eigenvalue is a squared classical frequency. A conditional
one-quantum harmonic gap is `S*nu*sqrt(lambda)`, retaining an action scale,
inverse-time scale, energy normalization, and quantization premise. PG3's
`lambda/[3/(2L)]` therefore is not the claimed physical scale-free gap ratio.

## Disposition

PG3 is qualified. C-MOD-001 may promote the exact conditional radial Hessian,
Green, Derrick, and continuum theorem. C-MOD-002 may promote the refined
conditional stationary profile and finite-box continuum evidence. C-SCL-001
may promote the explicit classical-mode scale ledger. PG3 establishes no
positive bound radial excitation, Roper identity, J=1/2 state, physical mass,
gap ratio, Skyrmion-nucleon dictionary, or substrate realization. B1, E2, E4,
and S2 remain pending and supply no accepted premise.
