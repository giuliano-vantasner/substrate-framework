# P093 source adjudication

LB3 is qualified. Its unchanged script provides useful finite-grid regression
evidence for the already accepted conditional C-SG-016 damped-family law, but
its pointwise-rate, convergence, high-damping, survival, and physical readings
are broader than the implemented oracles.

The numerical recurrence is sound at its declared level. Before the separate
edge-sponge update it is exactly the centered-damping leapfrog already exposed
by `evolve_bulk_driven_sine_gordon_leapfrog`, and at `Gamma=0` it reduces to the
lossless centered recurrence. The source's planted lossless breather has tiny
core-energy drift, and its `dx=0.05` and `dx=0.025` fitted rates agree. These are
valid regressions, not a new solver or API.

The measured observable is finite-core energy over `|x|<14`, not total energy.
C-SG-012 gives the exact control-volume identity

`dE_R/dt=[phi_t*phi_x]_{-R}^{R}-Gamma*integral_{-R}^{R}phi_t^2 dx`.

LB3 records neither the flux through `x=+/-14` nor a core balance ledger. Its
fit therefore cannot distinguish uniform damping from radiation crossing the
diagnostic boundary. The separate outer sponge adds another dissipative
operation outside the declared uniform-Gamma recurrence and is likewise absent
from an energy ledger.

The source then fits one constant log slope over `40<=t<=120` while calling
`Gamma*D(omega_meas)` a pointwise rate at the current frequency. Under accepted
C-SG-016, frequency and `D` evolve throughout that window. Regressing the
accepted nonlinear reduced energy over the source's exact 1000 sample times
predicts the four reported rates as follows:

| initial omega | Gamma | LB3 measured | reduced-window slope | source FFT-bin point rate |
| --- | ---: | ---: | ---: | ---: |
| 0.7 | 0.010 | 0.00954640 | 0.00954126 | 0.00960991 |
| 0.5 | 0.010 | 0.00919841 | 0.00919865 | 0.00905358 |
| 0.7 | 0.005 | 0.00451065 | 0.00450853 | 0.00452679 |
| 0.7 | 0.015 | 0.0148707 | 0.0146672 | 0.0144149 |

The accepted window regression is closer in every case. This is useful support
for C-SG-016, but it is not an independent pointwise confrontation and adds no
distinct claim.

The frequency oracle is also coarser than the narrative implies. The source's
1000 samples are spaced by 0.08, so the angular FFT bin is exactly `pi/40`.
The printed frequencies `0.9425` and `0.8639` are the twelfth and eleventh bins.
The accepted family frequency changes by more than one bin across every fitted
window. An unwindowed single-bin argmax cannot resolve one instantaneous
frequency from that chirped trace, and source rounding before form-factor
quadrature adds no independence.

The source's high-damping run does show rapid finite-time relaxation under its
declared `t>T_int`, amplitude `1e-4`, sign-change, and mean-energy `0.1*E_b`
thresholds. It does not validate the claimed `Gamma=2*omega_b` field boundary:
for `Gamma=1.75`, the accepted normalized `k=0` field mode has natural frequency
one and remains underdamped because `1.75<2`. C-DYN-001 also proves that exact
nontrivial time-periodic finite-energy fields are excluded for every positive
uniform damping value under zero integrated flux. Operational transient
relaxation, linear-mode damping, exact periodic existence, phase coherence,
survival probability, and population remain distinct.

LB3 couples spatial and temporal halving and varies neither domain, integration
method, core radius, fit window, nor a load-bearing energy ledger. C-SG-016
already has stronger total-energy mesh, domain, DOP853, damping-rate, lossless,
and ledger evidence. A new PDE rerun would therefore duplicate accepted
validation without a distinct positive claim. P093 adds no claim or canonical
API, maps LB3 to C-SG-016 and C-DYN-001, preserves its regression evidence, and
excludes continuum, exact-damped-breather, survival, material, spark, DBD, and
substrate interpretations.
