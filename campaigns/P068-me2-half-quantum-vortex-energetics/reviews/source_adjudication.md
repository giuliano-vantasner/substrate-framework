# P068 ME2 Source Adjudication

ME2 exits cleanly with `ALL 4 CHECKS PASS`. Its executable proves selected
scalar arithmetic, but it defines the purported pair energy as a count times
one isolated self energy and never constructs the fixed-boundary defect
configuration named by its headline.

ME2.1 sets `E_vortex(charge,count)=count*K*charge**2*L`. The ratio one half is
therefore exact for two independent copies assigned the same outer logarithm.
For two defects in one domain with total boundary charge one, a common far
field remains. In the declared matched-shell model, `n` equal near fields from
`xi` to separation scale `d` and one total-charge far field from `d` to `R`
give

`E_split=pi*K*Q^2*((1/n)*log(d/xi)+log(R/d))`.

The unsplit field energy is `pi*K*Q^2*log(R/xi)`. Their difference is
`-pi*K*Q^2*(1-1/n)*log(d/xi)`, before core costs. The ratio becomes `1/n` only
at the endpoint `d=R`, where the common far shell vanishes. At `xi=1,d=4,R=16`
the two-half field ratio is `3/4`, not `1/2`; at `d=xi` it is one. Thus the
source ratio is not cutoff-independent evidence for a shared-domain pair.

ME2.2 repeats the independent-copy arithmetic for arbitrary `1/n`. That
identity is exact under its declared copies, but `RP2` has only two loop
classes and supplies no arbitrary fractional ladder. Convexity cannot create a
topologically forbidden charge. The executable's claimed all-positive-integer
strict inequality is also evaluated only at `n=2`, though the bare rational
inequality is elementary.

ME2.3 correctly states `pi1(RP2)=Z2`: the projective director generator has
order two. A combined half-quantum vortex, however, uses the full polar order
parameter `(S2 x U1)/Z2`. Its universal cover is `S2 x R`, with deck generator
`g(d,t)=(-d,t+pi)`. The powers `g^k` form `Z`; `g^2(d,t)=(d,t+2*pi)` is a
nontrivial integer phase vortex, not the identity. ME2 conflates these two
typed loop groups.

ME2.4 correctly rejects half winding for a standalone scalar `U1` phase. It
does not derive the defect topology of a spinor condensate. Energetics also
require two stiffnesses: under the declared phase/director functional, two
isolated half textures have field energy
`pi*(K_phase+K_dir)*L/2`, while one integer phase vortex has
`pi*K_phase*L`. Their field ratio is
`(K_phase+K_dir)/(2*K_phase)`, equal to one when the stiffnesses are equal.
Including half and integer core energies gives pair-minus-integer residual
`pi*(K_dir-K_phase)*L/2+2*E_half-E_integer`; only its negative regime favors
the pair.

P068 selects Candidates B through E. Candidate A survives only for the narrow
isolated-copy and projective arithmetic. Candidate F is an explicit ceiling,
not the positive fixed-boundary object. O1 remains pending. No material
stiffness, core, exact multi-core PDE solution, equilibrium separation,
physical vortex realization, experiment, or substrate mechanism is promoted.
