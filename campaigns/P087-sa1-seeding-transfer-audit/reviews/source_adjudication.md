# SA1 Source Adjudication

SA1 is qualified. Its exact rest-breather temporal structure survives, but its
physical seeding-transfer headline does not.

At every fixed finite position, write the accepted C-SG-001 rest breather in
phase form as `m_x(y)=4*atan(a_x*sin(y))`, with
`a_x=eta/(omega*cosh(eta*x))>0`. The trace is odd and half-wave
antisymmetric. In the declared real Fourier convention this sets the mean and
all cosine coefficients to zero and removes every even sine coefficient.
Integration by parts followed by a tangent substitution gives the exact
fundamental coefficient

`b_1(x)=8*a_x/(sqrt(1+a_x^2)+1)>0`.

At the core this is `8*eta/(1+omega)`. SA1 instead computes the leading
arctangent term `4*eta/omega` and labels it as the full coefficient. At
`omega=1/sqrt(2)` the two are respectively about 3.3137 and 4.

The surviving Fourier theorem is not a susceptibility. SA1 supplies no driven
equation, perturbing interaction, input/output observable pair, retarded
condition, causality, or response normalization. Its inserted symmetric
Gaussian pair is positive at finite-width DC:
`chi(0)=2*A*exp(-omega_b^2*tau^2)`. It reaches zero only as `tau` tends to
infinity, a different statement from exact vanishing as frequency tends to
zero, and the pair contains no third-harmonic line in that limit.

The numerical overlap is also not a population derivation. SA1 divides each
deposition spectrum by its own total, so the reported coordinate is invariant
under the spectrum-magnitude input that its prose says controls the result.
It remains freely scalable with kernel amplitude `A`, lacks a unit and
absorption-efficiency ledger, need not be integer, and has no downstream
formation or counting law. Other non-derivative high-pass kernels vanish at
DC, so zero mean does not identify a voltage-derivative interaction.

The external engineering mirror repeats these interpretations and, under the
current NumPy, fails before its tally because it calls the removed `np.trapz`
alias six times. The framework's sampled integrations already use the shared
version-compatible `trapezoid_integral`; P087's accepted result is exact and
requires none. Named C035 rungs still use inserted Michaelis triggers and do
not consume SA1.

C-SG-015 therefore promotes only the exact fixed-position temporal-Fourier
theorem, with phase-origin and physical-interpretation ceilings explicit. SA1
does not establish a causal susceptibility, deposition-to-breather transfer,
seeded population, dV/dt law, breakdown gate, or engine mechanism.
