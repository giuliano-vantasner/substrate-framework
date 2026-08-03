# SA4 Source Adjudication

SA4 is qualified without a new accepted claim. Its surviving exact content is
conditional energy bookkeeping and monotone-limit algebra for an inserted
spectral family, not a physical breather-population, electrical-breakdown, or
voltage-slew saturation law.

The threshold construction begins with a correct accepted coordinate but gives
it a new meaning. At the fixed working frequency, C-SG-002 gives the energy of
an already-existing breather as `E_b=16*sqrt(1-omega_b^2)`. It does not say this
is minimum formation work or that arbitrary deposited energy decomposes into
identical breathers. In fact, the exact accepted family has energy approaching
zero as its frequency approaches one, so there is no positive global breather-
energy minimum. For supplied positive `E` and `E_b`, floor division exactly
gives completed units and a remainder, but a required-input threshold would use
a ceiling. Neither rounding convention constructs a field state.

SA4 also makes its crossing by hand. The below-threshold example uses `G=1`,
whereas the count sequence uses `G_BIG=900`, explicitly chosen so a strong slew
clears several energy units. For any positive spectral score `F`, choosing
`G=E_b/F` places the threshold there; choosing
`G=(n+1/2)*E_b/F` realizes any nonnegative integer floor count. Rescaling a
Fourier amplitude by `c` and the gain by `1/c^2` leaves the energy unchanged.
The source supplies neither gain units nor an independent value, so neither its
threshold nor count is predicted.

The inserted integral family is exactly increasing and fixed-band bounded under
its own normalization. Its integrand derivative is positive, and dominated
convergence supplies the ceiling. But dividing the same family by `s^2`, as a
fixed-time-domain-peak normalization requires, makes the large-s branch decrease
to zero. Equal maximum-slew sinusoids can also have arbitrarily different band
scores. Scalar slew therefore does not determine the chosen spectrum.

The claimed scale does not survive exact analysis. In the sharp positive-lobe
limit the normalized fill is `exp[-(omega_b/s)^2]`, whose half-fill coordinate
is `omega_b/sqrt(log(2))`; it is independent of the Gaussian bandwidth
`1/tau`. Its small-s behavior is flatter than every power and its large-s
correction is order `1/s^2`, whereas a Michaelis curve is linear at small s and
has a `1/s` tail. Independent adaptive quadrature reproduces the source fit
residual 0.196 at scale about 0.90, an RMS discrepancy above 0.15 over eight
normalized samples. The broad check `0.05<scale<5` proves no physical map.

The rejection guard is also narrower than its labels. At finite tau,
`chi_b(0)=2*exp(-tau^2*omega_b^2)>0`; tau=10 only makes it smaller than a
chosen tolerance, and tau=5 breaks the verdict. C-SG-015's exact zero temporal
mean belongs to an undriven field trace, not this Gaussian susceptibility. The
adiabatic checks evaluate a separately normalized overlap rather than
`E_seed` or the floor count. A constant kernel makes every normalized overlap
one by definition, so its fabricated ratio is a planted tautology rather than
a falsification of a competing physical response.

Consumers do not close the gaps. The engineering mirror inserts the breakdown
branch and uses voltage nowhere above it; its six direct `np.trapz` calls retain
the already-recorded current-NumPy compatibility failure. The nucleation model
maps units through the old `DVDT_SAT`, inserts a 2.5 base, and restores a 0.05
floor. The later DBD pipeline keeps free base and overlap factors and returns a
continuous count. Named C035 rungs retain their original Michaelis constants.
P090's exact work uses no quadrature, and its only independent sampled
regression uses adaptive SciPy integration rather than a version-specific
NumPy alias.

SA4 therefore establishes no physical zero-below-breakdown law, derived
population, derived saturation scale, formation probability, plasma response,
or engine replacement. Its elementary surviving algebra has no distinct
accepted consumer and warrants no canonical package or release change.
