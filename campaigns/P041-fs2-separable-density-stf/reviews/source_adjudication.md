# FS2 Source Adjudication

FS2 is qualified. Its declared separable-density moment and STF algebra maps to
`C-MOM-002`, with convention factors, exact derivatives, and viewing geometry
made explicit. It does not derive the product density as a conserved physical
3+1 breather source or establish gravitational radiation.

## Reproduction and Runtime

The hash-pinned source exits cleanly with five checks under NumPy 2.5.1 and uses
the current `numpy.trapezoid` compatibility pattern. A replay takes over a
minute because it repeatedly evaluates thousands of 60,001-point spatial
integrals. P041 records that hash-matched reproduction once; subsequent exact-
verifier iterations may reuse the durable record while the default command can
still execute the source. This avoids ceremonial recomputation without weakening
the scientific oracle.

## Declared Product-Density Moments

For a centered longitudinal density with total `M` and second moment `mu(t)`,
and a fixed normalized centered axisymmetric transverse profile whose per-axis
variance is `sigma^2`, Fubini gives

`I = diag(mu, M*sigma^2, M*sigma^2)`.

The normalized STF convention is

`I_STF = diag(2*Delta/3, -Delta/3, -Delta/3)`,

and FS2's triple convention is

`Q = 3*I_STF = diag(2*Delta, -Delta, -Delta)`,

where `Delta=mu-M*sigma^2`. The variance input is per transverse axis; the
radial transverse second moment is `2*sigma^2`. Independent direct Gaussian
integration confirms normalization, centering, and this convention.

## Derivatives and Projection Geometry

When `M` and `sigma^2` are constant, every positive time derivative removes
the transverse term. For `d=mu^(n)`, the normalized tensor is
`diag(2d/3,-d/3,-d/3)` with norm squared `2d^2/3`; the triple tensor is
`diag(2d,-d,-d)` with norm squared `6d^2`. Thus the source's convention changes
the contraction by nine.

P041 differentiates the accepted exact `C-SG-009` moment instead of building an
FFT reference from the same sampled `mu_of_t` values. At `omega=1/sqrt(2)` and
`t=pi/(4*omega)`, `mu'''=-64/3` exactly and the triple-tensor norm squared is
`8192/3`. Independent repeated central differences converge to that derivative
at second order.

Algebraic TT projection along the symmetry axis is zero. A perpendicular view
of the normalized derivative is `diag(d/2,-d/2,0)`, with normalized plus
coordinate `d/sqrt(2)` and zero cross. Adding arbitrary pure trace changes
neither projection. These are `C-GW-002` tensor facts, not wave observables.

## Source Oracle and Narrative Defects

FS2 describes its spectral reference as analytic and essentially exact, but it
constructs it by applying an FFT to 256 samples from the same numerical
`mu_of_t` routine under test. Its convergence study is useful regression
evidence, not an independent analytic derivation. Its trace-injection guard is
a valid restatement of already accepted TT algebra.

The working source uses `S_PERP=0.8`, hence per-axis variance `0.64`. A later
annotation says pending P3D3 derives `3.84` and supersedes the Gaussian, while
also saying the original checks are unaffected. Those incompatible values
belong to different declared profiles; the later working-tree narrative cannot
replace the hash-pinned calculation or become accepted authority backward.

## Physical Scope

The source declares `rho=T00*g_perp` but constructs no complete momentum density,
spatial stress, local 3+1 conservation proof, transverse field equation,
solution, stability analysis, gravitational action, retarded field, or flux.
A constant total integral is insufficient for local conservation; P041 supplies
a concrete time-varying constant-monopole density for which zero current fails
continuity. A conservation completion may exist, but FS2 does not provide one.

## Terminal Disposition

FS2 maps its exact conditional product-density moments and projections to
`C-MOM-002` and is otherwise qualified. Excluded scope includes a genuine 3+1
sine-Gordon or oscillon solution, dynamically derived transverse width,
conserved physical stress tensor, gravitational quadrupole, waveform, power,
and substrate realization. Durable evidence is the P041 exact verifier,
independent product-density review, source reproduction, and this adjudication.
