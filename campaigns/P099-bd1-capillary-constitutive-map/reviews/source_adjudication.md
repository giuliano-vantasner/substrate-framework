# P099 source adjudication

BD1 reproduces all eighteen source checks, and its central substitution is
exact under its displayed premises. For positive line tension and area drive,
the capillary energy has critical radius `T/P`; the barrier relative to `R=0`
is `pi*T^2/P`, so a radius-independent core offset cancels from the relative
height but remains in the absolute top energy.

Declaring
`T=pi*K_F*s^2*log(R_o/r_c)+epsilon_core` and
`P=g*A^2*k^2*l_m/2` gives
`R_*=2*T/(g*A^2*k^2*l_m)` and
`E_barrier=2*pi*T^2/(g*A^2*k^2*l_m)`. P099 independently rederives the Frank
annulus integral, tilted-well difference, standing-profile average, completed
square, and full sign domain. The formula and its exact conditional
sensitivities therefore survive as C-RG-002.

The source does not check the dimensions it claims. P099 repairs that defect:
if `[A]=L^alpha`, dimensional closure requires
`[g]=E*L^(-1-2*alpha)`, after which the bias, area drive, radius, and barrier
have the required dimensions. No value of `alpha` follows. More generally,
`p~g*A^m*k^n*l_m` closes with coupling length exponent
`n-3-m*alpha`; for dimensionless amplitude, linear and quadratic amplitude
laws can even share the same coupling dimension. Dimensional analysis does
not select BD1's quadratic law.

The exact log-exponent rows for `(R_*,E_barrier)` against
`(T,g,A,k,l_m)` have rank two and three null directions. Radius plus barrier
identifies the effective line tension but not the four drive constituents;
the barrier alone has rank one and identifies none. A three-parameter
rescaling changes `A`, `k`, and `l_m` while compensating `g`, preserving both
observables. The Frank/core component elasticities are state dependent because
the line tension is additive.

BD1's physical language is broader than its oracle. Its standing wave is a
declared profile, not a derived pulson or material stress; `k~omega` lacks a
dispersion and unit convention; barrier divergence does not prove a physical
channel never fires; and symbolic substitution does not predict a rate or
output power. B1, E1, and E2 are queue label collisions, while BD4 is a pending
downstream consumer. All eighteen predicates are individually classified in
`evidence/check-adjudication.yaml`.

BD1 is therefore qualified, not migrated without qualification. C-RG-002
accepts the exact conditional constitutive theorem and its ceiling. It derives
no material, coupling, amplitude convention or magnitude, frequency law,
temperature dependence, nucleation rate, DBD event, isotope effect, nuclear
process, or output power.
