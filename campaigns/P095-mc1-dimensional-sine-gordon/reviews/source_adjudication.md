# P095 source adjudication

MC1 is qualified. Its declared cosine density has an exact dimensional
sine-Gordon reduction and an exact physical-coordinate breather, but its
material, energy-invariance, absolute-scale, width, and universal gapless
readings do not survive claim-level review.

For a dimensionless real field and physical coordinates, declare positive
coefficients in the density
`L=lambda*u_t^2/2-T*u_x^2/2-mu*(1-cos(u))`. Direct first variation gives
`lambda*u_tt-T*u_xx+mu*sin(u)=0`. With an energy-per-length density,
`[lambda]=E*time^2/length`, `[T]=E*length`, and `[mu]=E/length`. Thus
`c=sqrt(T/lambda)`, `omega_0=sqrt(mu/lambda)`, and
`ell=sqrt(T/mu)=c/omega_0` have speed, inverse-time, and length dimensions.
The chain rule under `X=x/ell`, `tau=omega_0*t` maps the residual to `mu`
times the accepted normalized sine-Gordon operator.

These ratios are not a full coefficient identification. Their logarithmic
Jacobian has rank two and right nullspace spanned by `(1,1,1)`. Equivalently,
at fixed positive `c` and `omega_0`, every coefficient triple is
`(lambda,lambda*c^2,lambda*omega_0^2)` for arbitrary positive `lambda`.
Multiplying all coefficients by `alpha` preserves the equation and the three
kinematic scales but multiplies physical energy and canonical action by
`alpha`. MC1's absence-of-a-symbol check therefore fails its headline: the
free scale already resides in the common coefficient direction.

Pulling back C-SG-001 at normalized frequency `0<omega<1` gives physical
angular frequency `omega*omega_0`, period `2*pi/(omega*omega_0)`, inverse-tail
scale `eta/ell`, and profile scale `ell/eta`, where
`eta=sqrt(1-omega^2)`. The latter is the scale in the sech argument and the
asymptotic decay length; the exact sech-envelope one-over-e point is
`acosh(e)*ell/eta`, so MC1's width prose is qualified.

Restoring the density and measures is load bearing. The physical energy is
`sqrt(T*mu)*16*eta`, not the bare normalized number `16*eta`. With the accepted
canonical normalization, the action is
`sqrt(lambda*T)*16*acos(omega)`. The factors satisfy
`E_scale=omega_0*J_scale`, and direct differentiation gives
`dE_phys/dJ_phys=omega*omega_0`, the physical angular frequency. Both primary
and independent routes reject mutations that substitute normalized, energy,
or doubled action factors.

At fixed normalized frequency, `mu->0+` sends the physical frequency and
energy to zero while the profile length diverges. Holding a finite positive
physical frequency instead sends `omega_b/omega_0` outside `(0,1)` before the
limit. MC1's chosen finite-width trial indeed fails the linear wave equation,
but one trial does not prove a universal no-localized-periodic-solution
theorem. The general dispersion and tail classification remains for MC2.

Finally, periodicity, bistability, or a medium label does not select the cosine
force: adding a second periodic harmonic changes the field equation. P095
therefore promotes only the exact conditional density reduction,
identifiability class, and physical lift of the already accepted normalized
breather. It does not derive a material, coefficient value, continuum regime,
gap-tail theorem, thermal model, population, or engineering selector.
