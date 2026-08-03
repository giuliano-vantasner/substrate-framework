# P094 source adjudication

LB4 is qualified. A distinct exact Brownian-phase theorem survives, but the
source does not derive its phase process, diffusion coefficient, effective
temperature, breather projection, lifetime window, or discharge selector.

For a declared process `delta_t=sqrt(2*D)*W_t`, with `D>=0`, `t>=0`, and
integer harmonic `n`, Gaussian integration gives
`E[exp(i*n*delta_t)]=exp(-n^2*D*t)`. Its variance is `2*D*t`; therefore one
mean phasor is `exp(-D*t)` while iid same-time pair coherence is
`exp(-2*D*t)`. This corrects LB4's factor-two naming: the source calls `D*t`
the phase RMS squared and then transfers the mean-phasor exponent to a
pair-visibility consumer.

Endpoint values are not uniform-window averages. Over `[0,T]`, the mean
phasor average is `(1-exp(-D*T))/(D*T)` and the pair-coherence average is
`(1-exp(-2*D*T))/(2*D*T)`, with continuous value one at `D=0`. Independently
multiplying a declared deterministic coordinate-amplitude envelope
`exp(-Gamma*t/2)` by the Brownian mean phasor gives the coherent mean-field
factor `exp(-(Gamma/2+D)*t)`; its quadratic factor is
`exp(-(Gamma+2*D)*t)`. None of these quantities is a survival probability,
population fraction, total energy, or event rate.

LB4's physical coefficient fails dependency closure. Its FDT check is a
self-equality after defining `S_xi=2*Gamma*Theta_eff`. The cited Ohmic source
starts from an assumed spectrum; its low-frequency positive-temperature limit
is white, while its zero-temperature spectrum remains frequency dependent and
vanishes in the low-frequency limit. A cited coth-scale source also warns that
the relevant slow bath mode must be identified; LB4 simply inserts
`omega_b`. Dimensional consistency cannot fix the admitted order-one phase
projection coefficient.

An explicit countermodel makes the normalization failure concrete. For the
classical Langevin oscillator
`dq=p*dt`,
`dp=(-omega^2*q-Gamma*p)*dt+sqrt(2*Gamma*Theta)*dW`,
the Gibbs density is stationary. With `x=omega*q`, `y=p`, and
`E=(x^2+y^2)/2`, Ito's formula gives phase quadratic-variation rate
`2*Gamma*Theta*x^2/(x^2+y^2)^2`. Averaging over a fixed-energy fast phase
gives Brownian `D=Gamma*Theta/(4*E)` under these conventions, not LB4's
factor-one coefficient. Moreover the exact energy generator has drift
`Gamma*(Theta-p^2)` and stochastic noise, so fixed energy is not exact. This
countermodel is evidence against LB4's derivation, not a promoted universal
breather coefficient.

The lifetime composition is likewise conditional. C-SG-016 gives an evolving
action, energy, and frequency under explicit adiabatic assumptions, not a
global finite-amplitude amplitude law with fixed `D`. If `D` were proportional
to inverse energy, energy decay would make it time dependent. The source also
labels `omega_b*t_w` as cycles, omitting the factor `2*pi`.

The declared grid cannot validate the target. It ranges from about `0.0014` to
`0.9465`; for any desired `g` in `(0,1)`, the free surface
`n_w=-log(g)/(delta*(1/2+theta))` reproduces it. Bracketing `0.125`, choosing a
central point near it, and rejecting arbitrary constant alternatives are not
model selection. The overdamped, zero-energy, DBD, and spark conclusions also
extrapolate outside the declared weak-noise phase model or insert unsupported
population and event premises.

P094 therefore promotes only `C-COH-002`: the exact conditional Brownian
characteristic, its observable-specific endpoint and window formulas, and the
abstract coherent-factor composition. All FDT, thermal, breather-survival,
population, and discharge readings remain outside the accepted claim.
