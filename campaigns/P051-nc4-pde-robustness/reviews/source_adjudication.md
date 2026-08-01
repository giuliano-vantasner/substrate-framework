# NC4 source adjudication

## Scope and reproduction

The primary unit is the hash-pinned 440-line NC4 bridge at
`substrate@6d1f4e0`, SHA-256 `9efa788d...81570`. Its imported `study.py` is
unchanged at the same baseline, SHA-256 `15891957...c9f`. Literal execution on
Python 3.12.2 and NumPy 2.5.1 exits one at the first removed `np.trapz` call,
before any scientific check. An in-memory compatibility alias to
`np.trapezoid` leaves the source otherwise unchanged and reproduces exit zero
with `ALL 30 CHECKS PASS`. The source tally is therefore reproducible but does
not by itself validate its headline.

## NC4.1 amplitude-sweep and topological-discrimination claims

The four rows are not an amplitude-only sweep. Changing `w` also changes
frequency, exact field amplitude, inverse width, binding-gap-derived force
amplitude, interaction width, final time, and—most importantly—a separately
calibrated phase table. The source says those phases maximize discrimination.
Holding the declared phase `5.50` fixed in the corrected solver gives
`dQ=-1.03294` at `w=0.6` but `dQ=+1.94748` at `w=0.8`; the independent direct
solve_ivp route reproduces the reversal. A phase shift by pi exactly maps the
positive-epsilon drive to the negative-epsilon drive, so the ordered sign is
not an invariant chirality label without an independently derived phase map.
The consistent selected sign is post-calibration behavior of four different
drives, not robustness against amplitude.

The reported `q_bulk` is
`[phi(L,t_final)-phi(x_first>10,t_final)]/(2*pi)`. That is a finite-interval
endpoint coordinate. It becomes a topological charge only when its endpoints
meet the accepted boundary hypotheses, and it becomes integer only for vacuum
endpoints. The source's own `-0.572` gap and nonzero elastic-control coordinates
show that those integer-vacuum conditions are absent. Calling the number a
fractional topological charge transfer therefore overstates the diagnostic.
No conserved charge or topological discrimination theorem is established.

## NC4.2 boundary-correlation claim

For the separately calibrated `w=0.6`, phase-5.50 diagnostic experiment, three
corrected fine grids and an adaptive DOP853 route agree that the two prescribed
drive signs give opposite sampled boundary sign correlations. This is honest
finite-time simulation evidence for that declared Neumann IBVP. It is not a
numerical confirmation of NC3's harmonic formula: the nonlinear boundary trace
is not reduced to the formula's two declared sinusoids and the source never
compares its numerical value with `4B*cos(delta)/w`.

The correlation and endpoint gap do not come from the same experiment.
`dQ` uses full drive scale one, while `W_Q` uses scale 0.15 because the source
says the full drive co-flips the boundary velocity and invalidates the desired
witness. Thus the two displayed diagnostics do not jointly demonstrate a
single charge-selection mechanism. C-SG-013 already proves that correlation
and boundary winding do not imply one another.

## NC4.3 convergence claim

The source performs one coupled `dx/2,dt/2` comparison at selected `w=0.6`.
It does not separate spatial and temporal errors, vary the domain or solver
tolerance, check energy flux, refine the other frequencies, or use an
independent method. Its coordinates have true spacing `L/(Nx-1)` while the
stencil uses `L/Nx`, and its right boundary overwrites the last five evolved
cells with the sixth-from-last value.

P051 repairs those implementation defects without editing predecessor
evidence. On corrected grids 600, 1200, and 2400 the calibrated `w=0.6`
endpoint response converges toward about `-1.039`; the diagnostic correlations
converge on the fine-grid branch, timestep halving approaches the fine result,
a same-spacing domain extension preserves it, and the energy-flux residual
decreases. A direct DOP853 method-of-lines route independently preserves those
setup-specific signs. These repairs validate the reusable solver and selected
IBVP response, not the source's four-frequency physical interpretation.

## Rejection guard

At scale zero the drive is identically zero before epsilon is applied. The two
charge runs therefore receive byte-for-byte identical inputs, so their exact
zero difference is duplicate execution rather than a sensitivity oracle.
The correlation is identically zero because its spatial-derivative input is
hard-coded to zero. These checks are useful deterministic regressions but are
validation theater when described as a discriminating competing physical
model: no wrong phase, wrong boundary orientation, common-drive sweep, or
charge/correlation implication mutation is tested.

## Boundary and parity interpretation

NC4 prescribes only `phi_x(0,t)=F(t)`. It does not implement the predecessor
boundary degree of freedom or the claimed relation
`phi_t+epsilon*phi_x=J`. Flipping a Neumann forcing sign is not the accepted
spatial-parity operation unless field, coordinate, domain, boundary normal,
initial data, and forcing are all transformed. The calibrated epsilon-to-phase
and phase-to-chirality dictionaries are declared rather than derived. The
numeric response establishes no parity-invariant or parity-breaking boundary
law, selected state, physical parity violation, V-A interaction, weak force,
particle identity, or substrate realization.

## Positive extraction and terminal decision

P051 extracts a pure `sine_gordon_1d` module with measured grid spacing,
separately named endpoint coordinates, version-independent quadrature, explicit
left-Neumann and right-Sommerfeld conditions, energy-flux diagnostics, a
conservative periodic leapfrog route, and adaptive DOP853 routes. The exact
nonlinear breather converges at second order and an independently written
Fourier evolution reaches about `3.35e-11` RMS error on the enlarged box.

No new scientific claim is warranted. The exact PDE, breather, topological
semantics, and correlation/charge independence are already C-SG-001,
C-SG-005, C-SG-011, and C-SG-013. The surviving driven response is calibrated,
finite-grid, finite-time evidence with no predictive or physical phase map.
NC4 is therefore terminally qualified against those existing claims, and the
provisional C-SG-014 headline is rejected rather than promoted.
