# P067 ME1 Source Adjudication

ME1 exits cleanly with `ALL 4 CHECKS PASS`. The tally reproduces two exact
representative values and unit-density endpoint energy arithmetic, but its
load-bearing global-orbit check does not establish the advertised theorem.

ME1.1 correctly evaluates the standard spin-1 matrices on `(0,1,0)` and
`(1,0,0)`. Those values establish that the representatives attain zero and
one. They do not prove that every zero-spin pure state is on the polar orbit or
that every upper-saturating state is on the ferromagnetic orbit. The claim that
the spin term is the sole discriminant is conditional on the displayed
fixed-density functional and its omitted terms.

ME1.2 describes `n^2-|f|^2` as a sum of squares, but the executable never
exhibits that decomposition. It substitutes 4,000 pseudorandom real component
tuples and accepts the smallest floating value above `-1e-9`. Finite samples
cannot prove global polynomial nonnegativity. The check then evaluates one
representative at each endpoint. No equality condition is solved. Its printed
claim that the path `(cos(t),sin(t),0)` has `|f|^2=cos(t)^2` is false: at
`t=pi/4` its exact value is `3/4`, not `1/2`; the check inspects only the two
endpoints.

P067 replaces that gate with two exact routes. For a pure spinor `Psi`,
`n=Psi^dagger Psi`, `f=Psi^dagger F Psi`, and
`A=Psi_0^2-2 Psi_+ Psi_-`, direct matrix expansion gives
`|f|^2+|A|^2=n^2`. Under the unitary complex-Cartesian map `d=u+i v`, the same
identities are `f=2 u cross v` and `A=d dot d`. Thus zero spin is equivalent to
parallel `u` and `v`; a global phase makes `d` real and an `SO(3)` rotation
maps it to the `m=0` representative. Modulo global phase, `d` and `-d` are the
same ray, giving the polar `RP^2` orbit. Upper saturation is equivalent to
`A=0`, hence `|u|=|v|` and `u dot v=0`; a proper rotation maps that orthogonal
equal-norm frame to a coherent `m=+1` representative, giving the projective
ferromagnetic `S^2` orbit. These are equality-set classifications, not samples.

ME1.3 and ME1.4 contain correct endpoint sign arithmetic at unit norm after
the global theorem is supplied. At fixed density `n`, however, the endpoint
spin value is `n^2` and the polar-minus-ferromagnetic energy difference is
`-c2*n^2/2`. Positive `c2` selects the polar orbit, negative `c2` selects the
ferromagnetic orbit, and the omitted `c2=0` boundary leaves every pure spin-1
ray degenerate. The source's statement that `SO(3)` acts freely on the
ferromagnetic ray orbit is false; its stabilizer is `SO(2)`. The resulting
projective `S^2` statement is not a derivation of the full condensate
order-parameter manifold.

P067 selects Candidates B, C, and D. Candidate A survives only for the narrow
representative and unit-density conditional arithmetic. Candidate E is not
selected because the exact global theorem already determines the minimizer
sets; an additional local Hessian would be weaker and redundant. Candidate F
cannot satisfy the positive objective. Pending O1, ME2, and ME3 supply no
accepted premise. No material coupling sign, atomic realization, spatial
ground state, defect energetics, finite-temperature phase, or substrate
mechanism is promoted.
