# SA3 Source Adjudication

SA3 is qualified. One exact-parameter finite-time driven trajectory survives as
`C-PDE-011`; the claimed fast-versus-slow physical seeding mechanism does not.

The declared equation is a valid dimensionless 1+1 forced sine-Gordon IBVP,
but its energy language is wrong. For
`phi_tt-phi_xx+sin(phi)=J-gamma*phi_t`, the exact local balance is
`partial_t T00=partial_x(phi_t*phi_x)+J*phi_t-gamma*phi_t^2`. Homogeneous fixed
Dirichlet endpoints remove boundary work, leaving actual source work
`integral J*phi_t dx dt` and damping loss. SA3 instead calls
`integral f(t)^2 dt` deposited energy. Canonical instrumentation gives about
789.25 source-work units for the fast run and 2641.92 for the slow run. The
slow Gaussian is also centered only 0.75 widths after the simulation begins,
so its applied squared norm is about 347.97 rather than the full-line 400.
The drives are equal under neither the source proxy actually applied nor PDE
work.

The source classifier is insufficient. Its reported frequencies 0.2790 and
0.2793 are exactly raw FFT bin four on the two late windows; 0.2093 in the
second-frequency run is bin three. No peak interpolation or independent
estimator exists. It also labels `phi_cur` at `(n-1)*dt` with `n*dt`. More
importantly, sub-gap center frequency and radius-12 energy cannot distinguish a
breather from radiation, a box mode, or solitons outside the chosen ball. The
second-frequency core mean 29.161 exceeds the maximum C-SG-002 single-breather
energy 16 and therefore cannot identify one breather.

The slow run is not vacuum. The canonical source equation on the source domain
ends with total energy about 71.20, maximum field about 25.50, and eight
crossings between adjacent `2*pi` sectors while retaining zero net endpoint
winding. It is a multi-transition solitonic configuration whose energy sits
largely outside the late radius-12 tally. Thus SA3.3's “seeds nothing” guard
only proves that one diagnostic ball is small at one time.

A narrow positive object remains. For the exact fast source, full-line proxy
target 400, zero data, homogeneous Dirichlet walls, declared quadratic damping,
and finite interval through `T=410`, the late center trace fits the exact
C-SG-001 rest-breather waveform at roughly 2% relative RMS error. Three grids
`dx=0.05,0.025,0.0125` give fitted frequencies
0.295653, 0.250839, and 0.239700; successive differences contract by about a
factor four. Late radius-12 energies converge from 15.4464 to 15.7115 and stay
within 1.2% of the fitted C-SG-002 energies. Final full phase-space snapshots
have joint relative errors from 5.7% to 9.7%. The source-work ledger residual
contracts from about `1.08e-3` to `3.03e-5` relative to work.

Domain extension and sponge-width changes preserve that narrow branch. DOP853
at `dx=0.05` gives fitted frequency 0.307273, zero-crossing frequency 0.307216,
1.98% trace error, 6.86% snapshot error, and a `2.38e-5` absolute energy-ledger
residual. Halving leapfrog timestep moves 0.295653 to 0.304241, reducing its
error relative to DOP853 by more than threefold. An expensive DOP853 half-grid
run gives 0.253796 and agrees with the `dx=0.025` leapfrog result to about 1.2%.

The source family is not robust. Changing only the full-line proxy target from
400 to 380 or 420 destroys both exact-family fits; nearby targets form radiation
or kink-like states. This is mutation sensitivity for the exact trajectory and
a direct rejection of the claimed robust seeding window. No accepted voltage,
plasma, absorption, source-action, population, or event-count map exists, and
SA1/SA2 cannot supply one because those readings were already rejected.

`C-PDE-011` therefore records only the exact dimensionless forcing experiment
and its finite-time error bounds. It establishes no general resonant preference,
no below-gap exclusion theorem, no physical dV/dt mechanism, no probability,
no population, no absolute scale, and no asymptotic stability.
