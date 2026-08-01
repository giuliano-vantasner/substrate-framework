# FS3 Source Adjudication

FS3 is qualified. Its exact time-derivative, conditional power-functional, and
axisymmetric TT geometry map to `C-GW-004`; its special-frequency cycle mean
and Fourier fraction map separately to numeric-evidence claim `C-SG-010`. It
does not establish a conserved physical 3+1 breather source, gravitational
theory, radiation channel, or detector waveform.

## Reproduction and Compatibility

The hash-pinned source exits cleanly with five checks under NumPy 2.5.1. It
already implements the version-compatible choice `numpy.trapezoid` with an
older-NumPy `numpy.trapz` fallback, so P042 does not alter predecessor evidence
or mistake the API rename for a scientific result. A hash-bound reproduction
record avoids rerunning the unchanged dense source during verifier repairs.

## Exact Derivative and Conditional Power

P042 differentiates the exact `C-SG-009` moment rather than finite differences
of spatial quadrature. If `d=mu'''(t)`, `C-MOM-002` gives normalized
`I_STF'''=diag(2d/3,-d/3,-d/3)` with norm squared `2d^2/3`, while FS3's triple
`Q'''=diag(2d,-d,-d)` has norm squared `6d^2`.

Under the separately declared `C-GW-001` inputs, the normalized convention has
conditional instantaneous power `P=(G/5)|I_STF'''|^2=2Gd^2/15`. The triple
convention requires `G/45`, giving the identical result. FS3 instead applies
`G/5` to triple `Q`, producing `6Gd^2/5`, exactly nine times too large. It
likewise combines `Q=3I_STF` with the normalized waveform coefficient `2G`,
rather than `2G/3`, making its field amplitude three times too large.

The exact power is nonnegative and not identically zero, but it is not strictly
positive for all times. At `omega=1/sqrt(2)`, `mu'''` vanishes at the moment's
minimum and maximum symmetry phases and equals `-64/3` at
`t=pi/(4*omega)`. FS3 removes edge samples before testing `min(P)>0`, so its
sample grid misses the exact zeros and turns a discretization accident into a
headline predicate.

## Cycle Average and Fourier Evidence

For `omega=1/sqrt(2)`, direct adaptive quadrature of the exact third derivative
gives resolution-bounded evidence

`<mu'''^2> = 379.464638068747214229268157492...`.

The corrected unit-coupling conditional average is therefore

`<P>/G = (2/15)<mu'''^2> = 50.595285075832961897235754332...`,

one ninth of FS3's reported spectral `455.35757`. An independent sixty-digit
manual chain-rule derivative agrees. A cosine-series route reconstructs the
same mean by Parseval; the first permitted line at `2*omega` contributes the
resolution-bounded fraction `0.805369871686086...`. This dominance is numeric
evidence at the declared special frequency, while the absence of odd
harmonics follows exactly from `C-SG-009`'s half-period symmetry.

FS3 calls its comparison a closed-form spectral sum, but obtains every
coefficient by applying an FFT to 256 values from the same numerical
`mu_of_t`. That is useful regression evidence, not an independent closed form.
P042 keeps the exact Parseval identity separate from the numerical coefficient
evaluation and refines both direct and spectral routes.

## Viewing Geometry and Waveform Boundary

For a normalized STF derivative with longitudinal scalar `d`, and inclination
`i` measured from the symmetry axis, direct TT projection has normalized plus
coordinate `d*sin(i)^2/sqrt(2)`, conventional matrix readout
`d*sin(i)^2/2`, and cross coordinate zero. Thus the algebraic projection is
linear in the declared transverse basis, vanishes on the symmetry axis, and is
maximal for a perpendicular view. The same result holds for normalized and
triple conventions only when their waveform coefficients are rescaled
inversely.

These statements are properties of a declared tensor passed through the
conditional projector and waveform premise. FS3 imports the standard
linearized-gravity waveform, declares the rigid transverse embedding and
coupling, and constructs no complete locally conserved stress tensor,
three-dimensional field solution, gravitational action, retarded dynamics, or
physical flux law.

## Additional Source Guard Defect

FS3 reuses the static-kink guard from FS1 with
`d[4*atan(exp(x))]/dx=4*sech(x)`. The exact derivative is `2*sech(x)`, so its
kink density normalization is wrong. Its time-independence still makes the
third derivative zero, but that guard checks a generic constant-tensor fact and
cannot validate the breather's source or gravity interpretation.

## Terminal Disposition

FS3 maps exact conditional tensor and viewing algebra to `C-GW-004` and the
special-frequency refined average to `C-SG-010`. It is otherwise qualified for
its factor-nine power, factor-three waveform, strict-positivity, same-data FFT,
kink derivative, physical source, gravity, radiation, and substrate claims.
Durable evidence is the P042 verifier, its independent time/Fourier review,
the source reproduction record, and this adjudication.
