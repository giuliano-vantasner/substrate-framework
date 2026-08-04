# P152 B1 Source Adjudication

B1 reproduces all eight local checks under an explicit immutable compatibility
alias backed by `np.trapezoid`. Its native abort on this NumPy version is not a
scientific failure. The scientific audit instead separates the moving
projective path from the section used in its Berry calculation.

Checks B0 and B0b correctly show that the real lift
`(cos(phi/2),sin(phi/2))` is normalized, has local one-form zero, changes sign
at the endpoint, and defines a closed nonconstant rank-one projector. Those
facts are the correct base for C-BER-001. A zero local representative does not
imply trivial closed-ray holonomy because the endpoint transition remains.

Checks B1 and B1b evaluate `su2_z(phi)|up>=(exp(-i*phi/2),0)`. Their algebraic
half connection is exact, but this state changes only by phase and its
projector is constant. It is not a section of B0b's moving projector path.
Check B2 then exponentiates the local integral without the nonperiodic endpoint
transition. With the stated convention the two minus signs multiply to plus
one, so B1's fixed-ray closed-ray holonomy is not the advertised minus one.

Check B3 compares four scalar values but does not identify their typed source
objects, as C-CHR-001 already requires. Check B4 numerically regresses the bare
constant integral and does not test the endpoint; its eager legacy fallback is
version-only. The even-winding guard gives plus one but cannot detect either
the fixed projector or the omitted transition.

P152 selects the corrected positive object: the real moving lift has `A=0`
and endpoint transition `(-1)^k`, while its periodic complex gauge has
`A=k/2` and transition one. Both have the same projector and holonomy
`(-1)^k`. B1 is qualified through this theorem and the existing topology and
typed-character claims. No unique or physical vector potential, core source,
dynamics, material realization, coupling, or observation is promoted.
