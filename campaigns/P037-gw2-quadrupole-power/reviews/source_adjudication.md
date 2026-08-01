# GW2 Source Adjudication

GW2 is qualified. Its sphere moments, TT projector, trace annihilation, and
conditional angular contraction map to `C-GW-001`. Its retarded waveform and
Isaacson flux are explicitly imported, its source-quadrupole normalization is
inconsistent with its waveform coefficient, and it does not execute the stated
time average or establish a physical radiative multipole hierarchy.

## GW2.1 and GW2.2: Imported Field and Flux

The source correctly labels both load-bearing inputs as standard linearized-GR
imports: `h_TT=(2G/r) Lambda[ddot Q]` and
`dP/dOmega=r^2/(32*pi*G)<dot h_TT:dot h_TT>`. Its checks differentiate and
multiply those declared prefactors; they do not derive a field equation,
retarded Green function, source coupling, wave-zone approximation, or energy
current from an action. Consequently the later coefficient is conditional on
both inputs, not derived from the angular integral alone.

## GW2.3 and GW2.4: Angular Algebra

The exact sphere moments `integral n_i n_j=4*pi*delta_ij/3` and the rank-four
isotropic tensor with coefficient `4*pi/15` are correct. The symmetrized TT
projector is transverse, traceless, symmetric, and idempotent on symmetric
tensors. P037 reproduces the result with representative exact integrals and a
pure reusable API, then independently checks it using refined Gauss-Legendre
and periodic-azimuth quadrature rather than repeating all 81 source integrals.

## GW2.5: Conditional Coefficient and Convention Defect

For any symmetric tensor `S`, the genuine derived result is
`integral |TT_n(S)|^2 dOmega=(8*pi/5)|STF(S)|^2`. Combining this with declared
waveform coefficient `A` and flux coefficient `B` gives the conditional power
`(8*pi/5)*B*A^2*<|STF(Q''')|^2>`.

GW2 defines `Q=integral rho*(3*x_i*x_j-r^2*delta_ij)=3*I_STF` but uses the
waveform coefficient `2G/r` appropriate to normalized `I_STF`. Preserving the
same waveform requires `2G/(3r)` in front of GW2's `Q`. With the imported flux,
the equivalent formulas are `G/5*|I_STF'''|^2` and
`G/45*|Q'''|^2`. GW2 instead writes `G/5*|Q'''|^2`, nine times the same power.
Its wrong-coefficient guard cannot see this error because it freezes the
inconsistent waveform convention as an input.

## GW2.6: Averaging, Positivity, and Analogy

The conditional functional is nonnegative on real STF tensors and vanishes
exactly when their STF part vanishes. GW2 constructs an STF projection from
nine raw components but checks only the all-zero input and one nonzero input;
a nonzero pure trace or antisymmetric raw tensor is a counterexample to its raw
“zero iff tensor zero” wording. Its angle brackets are explicitly kept
symbolic, so no cycle average is executed. P037 supplies the exact general
single-harmonic average and a directly differentiated circular relative-source
example, keeping them separate from a general field theorem. The G1 analogy is
not an accepted dependency.

## Guards and Lowest-Multipole Claim

Trace annihilation is exact and promoted. The fabricated-coefficient guard only
distinguishes coefficients after the imported field and flux normalizations
are fixed; mutating either premise changes the result. Conservation from
`C-MOM-001` suppresses selected source derivatives but does not prove that the
declared spin-2 model is physical gravity, that its multipole expansion is
complete, or that quadrupole radiation is the universal lowest nonzero channel.

## Terminal Disposition

GW2 maps its exact TT angular reduction and premise-explicit conditional power
to `C-GW-001` and is otherwise qualified. Excluded scope includes a derived
linearized Einstein action or field equation, physical Isaacson energy, a
measured coupling, a universal lowest radiating multipole, the 1+1 lift,
nonlinear gravity, an arbitrary-source radiation verdict, and substrate
identity. Durable evidence is the P037 verifier, independent review, source
reproduction, and this adjudication.
