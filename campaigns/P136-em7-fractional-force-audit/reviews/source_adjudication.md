# P136 EM7 source adjudication

EM7 reproduces all seventeen checks. Its exact subcritical Riesz algebra and
the `(s,d)=(1,3)` Coulomb endpoint survive, but its headline constructive
geometric closure does not. The source mixes subcritical, critical, and
supercritical regimes, gives no metric-measure or diffusion construction, and
uses fixed-endpoint guards that cannot select either parameter.

## Surviving exact surface

In the inverse-angular Fourier convention, the declared symbol
`(k^2)^s` has the plane-wave eigenvalue `|k|^(2s)`. For `r>0`, nonzero `A`,
and `0<s<d/2`, C-KRN-001 gives

`G(r)=Gamma(d/2-s)*r^(2s-d)/[A*4^s*pi^(d/2)*Gamma(s)]`.

Its derivative has radial power `2s-d-1`, and at `d=3,s=1` the kernel is
exactly `1/(4*pi*A*r)`. Those statements are conditional mathematics. They do
not derive an operator, endpoint, source, force dictionary, space, or physical
sector.

## Critical and force completion

Write `s=d/2-epsilon` and subtract the subcritical kernel at a positive
reference radius before taking `epsilon->0+`. The exact result is

`Gcrit(r;r0)=2*log(r0/r)/[A*4^(d/2)*pi^(d/2)*Gamma(d/2)]`.

The unsubtracted kernel diverges through `Gamma(epsilon)`. Changing `r0` adds
only a constant. At `d=2`, `Gcrit=log(r0/r)/(2*pi*A)` and the radial flux is
one, independently matching C-MAX-001.

For the subcritical kernel, separately declaring source `Q`, probe `q`,
`phi=Q*G`, `U=q*phi`, and `F_r=-dU/dr` yields force exponent
`2s-d-1`. Inverse-square behavior therefore gives the family `d=2s+1`.
For example, `(s,d)=(9/10,14/5)` is subcritical and exactly inverse-square.
Neither the exponent nor the source's fixed-`d=3` guard selects a unique
dimension and operator power.

## Rejected source readings

EM7's d=2 check is only the Boolean `2*1==2`; it contains no reference,
subtraction, logarithmic normalization, or flux. Its d=1,s=1 branch is outside
the subcritical integral. The ordinary full-line Green function
`-|x|/(2A)` satisfies the point-source equation distributionally only after a
separate boundary or homogeneous prescription.

The numeric force sweep differentiates hard-coded, unnormalized powers. It
includes the invalid subcritical pair d=1,s=1 and treats d=2.5 as a space
without constructing one. The FFT Green residual uses d=1,s=3/4, also outside
the subcritical domain, smooths the source cusp, imposes a periodic box, and
compares an off-source residual to a near-origin peak. It is not a validation
of the standard Riesz Green distribution. The FFT packet test is regression
evidence for the declared symbol, not for a physical medium.

A positive real `d` in gamma functions is an analytic continuation parameter.
It does not by itself define a measure, metric, Dirichlet form, diffusion,
Hausdorff dimension, spectral dimension, walk dimension, or fractal medium.
EM7's later D3S annotation is also not authoritative: accepted D3S explicitly
rejected its gap-to-s selection, while QCD5 remains pending and circular.

## Decision

C-KRN-002 is accepted as a distinct exact conditional theorem for the
reference-subtracted critical limit and source-probe radial force ledger. EM7
is qualified through C-KRN-001, C-MAX-001, and C-KRN-002. Its claimed single
constructive dimensional mechanism, fractal geometry, endpoint selection,
gauge-sector lift, physical inverse-square force, and substrate closure are
rejected or remain unconstructed.
