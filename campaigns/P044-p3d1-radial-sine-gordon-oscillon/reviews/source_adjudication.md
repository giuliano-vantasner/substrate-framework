# P3D1 Source Adjudication

P3D1 is qualified. Its declared radial equation and Gaussian initial-value
problem produce a reproducible, long-lived localized oscillatory trajectory,
which P044 rebuilds as finite-time simulation evidence in `C-PDE-001`. The
source does not establish an exact periodic breather, an exponential radiation
law, a gravitational monopole theorem, or any particle or substrate identity.

## Reproduction and NumPy Compatibility

The hash-pinned source exits cleanly with six checks in about six seconds under
NumPy 2.5.1. That NumPy release has `numpy.trapezoid` and no longer has
`numpy.trapz`; P3D1's current-name-first compatibility expression therefore
selects the correct implementation. P044 centralizes the same two-version
dispatch in the package numerics layer because the framework still supports
NumPy 1.26, then routes canonical radial and vortex quadratures through it.

The source reports a late FFT frequency `0.9210`, a late center amplitude
`4.454`, a relative core-energy slope magnitude `1.301e-4`, closed-box energy
ranges `2.930e-4` and `7.416e-5`, and a core-trajectory difference ratio
`3.05`. These are useful comparison values, not inputs to P044's selection or
pass thresholds.

## Equation, Initial Data, and Positive Numerical Object

The declared dimensionless radial action is

`S=4*pi*integral dt dr r^2[u_t^2/2-u_r^2/2-(1-cos(u))]`.

Exact variation gives
`u_tt-u_rr-2*u_r/r+sin(u)=0`, and even origin regularity gives the stencil
`6*(u_1-u_0)/dr^2`. P044 also checks the exact local energy-continuity identity
and validates the spatial operator on the regular soluble linear mode
`sin(k*r)/r`, with maximum residual decreasing by factors greater than `3.9`
on spacings `0.2`, `0.1`, and `0.05`.

For `u(r,0)=3*exp(-(r/4)^2)`, `u_t(r,0)=0`, `0<=r<=200`, and `0<=t<=450`, the
canonical leapfrog baseline uses `dr=0.05`, `dt=0.02`, a homogeneous outer
Dirichlet boundary, and a quadratic velocity sponge over `150<r<=200`. The
energy inside `r<=30` in the late window `360<=t<=430` is
`0.931904002` times its settled-window mean over `120<=t<=180`; the late
center half-range is `4.348390815`. At the final state, radii 10, 20, 30, and
40 contain respectively about 94.08%, 94.72%, 94.87%, and 95.09% of the
remaining domain energy. This is direct finite-time localization evidence.

Hann-windowed quadratic FFT peaks and independently interpolated rising
crossings, evaluated on windows beginning at `t=220` and `t=300`, place the
fundamental estimates between `0.9171` and `0.9232`. P044 therefore records
only the conservative resolution-bounded interval `0.90<omega<0.94`, below
the linear threshold one. It does not call a single FFT bin an exact
frequency.

## Refinement, Boundaries, and Independent Route

The center trace is self-convergent on `dr=0.1`, `0.05`, and `0.025`: its
coarse/fine and fine/finer RMS differences through `t=60` are
`5.5327e-3` and `1.3612e-3`. Closed-box total-energy ranges at those meshes are
`1.1781e-3`, `2.9390e-4`, and `7.3437e-5`, decreasing at second order. The
closed boundary remains below `1e-20` at its monitor during the causal
energy-audit window.

At fixed `dr=0.05`, halving `dt` changes settled energy retention by less than
`1.3e-5` and early settled frequency estimates by less than `3e-5`. Moving the
sponge start and outer boundary through domains 160, 200, and 240 changes the
coarse-grid retention by less than `6e-8` and crossing frequency by less than
`2e-8`; the largest field reaching a sponge monitor is below `0.004`.

The primary review also compares a SciPy DOP853 method-of-lines integration
against leapfrog. A more independent review evolves the nonsingular transformed
field `v=r*u`, reconstructs the origin from even regularity, and uses Simpson
rather than trapezoidal energy quadrature. It agrees with the direct-radial
route to `9.9410e-3` relative center RMS and `2.5348e-3` maximum relative core
energy, while its closed-energy range is `2.3863e-3` on the deliberately
coarser `dr=0.2` grid.

## Mutation and Counterexample Results

Removing or changing the `2/r` coefficient fails both the exact transformed
identity and the `Delta(r^2)=6` operator test, including at the origin. An
`A=4`, width-three seed evolved with the same method retains only
`0.078534130` of its settled core energy, has late center half-range
`0.023711686`, and has fundamental estimates at approximately one; it fails
the localized sub-gap verdict. Courant factors at or above one are rejected
before evolution. These failures demonstrate sensitivity to the PDE geometry,
initial-data branch, and explicit-method stability condition.

## Source Overclaims and Numerical Defects

The source's nonzero late core-energy slope contradicts literal exact
periodicity. Comparing two initial seeds and two fitted slopes cannot identify
the functional form `exp(-c/epsilon)`, estimate `c`, or establish monotonicity
over a family. In addition, a sub-gap fundamental does not prevent nonlinear
higher harmonics above threshold from radiating.

P3D1 labels scalar energy conservation a silent gravitational monopole, but it
defines neither a gravitational action nor a conserved gravitational source
map. Scalar energy conservation remains a numerical consistency check for the
declared flat-space PDE. Its claim that non-integrability forbids every exact
3D periodic localized solution is also not proved: non-integrability does not
by itself supply such a no-go theorem, and Derrick scaling concerns static
profiles.

The source records time `n*dt` while evaluating `u_curr` and its centered
velocity at `(n-1)*dt`. This one-step timestamp shift is small for its reported
FFT but is corrected in the canonical solver. The source also lacks timestep
and domain refinement, an independent integrator, a soluble operator limit,
frequency-window sensitivity, and an explicit non-finite solver-failure gate.

## Terminal Disposition

P3D1 maps only its specified finite-time radial trajectory to `C-PDE-001` and
is otherwise qualified. Exact or eternal breathers, exponential lifetime,
family-wide stability, no-go theorems, gravitational silence or radiation,
absolute scale, particle interpretation, and substrate realization remain
outside the accepted claim. Pending P3D2, P3D3, and P3D4 may consume the new
radial solver only after their own claim-level audits; their narrative does not
expand `C-PDE-001`.
