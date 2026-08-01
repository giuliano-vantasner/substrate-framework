# Source adjudication: EL5 linear-system consistency

## Decision

EL5 is qualified. Its exact coefficient/augmented-rank distinction and
duplicate-row consistency condition support `C-LIN-001`. It does not establish
that an electron is an output, predict a mass ratio from closed inputs, show
that restoring the electron reopens a null direction in its actual matrix, or
replay accepted-framework consumers.

## Check-family audit

EL5.1 correctly shows that the source electron coefficient row equals the
hadronic row. The named five-by-two object is a coefficient matrix, not an
augmented matrix. Row equality adds a coefficient dependency; by itself it says
nothing about right-hand-side compatibility or physical identity.

EL5.1b correctly finds rank two and nullity zero for both coefficient matrices.
Calling the five-row system “more over-determined” records only an increased
equation count. Consistency still requires the augmented-rank test, and
uniqueness follows from full column rank only after consistency is established.

EL5.2 is the specialized content accepted under `C-LIN-001`: two copies of a
nonzero coefficient row with equal right-hand sides form a consistent redundant
pair, while unequal right-hand sides raise augmented rank and make the pair
inconsistent.

EL5.3 solves the declared logarithmic equality correctly, giving the
conditional ratio `m_had/m_e=48*pi^3*b/kappa_h`. The source nevertheless calls
this free-parameter-free while both `b` and `kappa_h` remain symbolic. P021 did
not accept the numerical `b(1)` evidence, and the source explicitly describes
`kappa_h` as unpinned. Selecting `kappa_h=48*pi^3*b/R` reproduces any positive
target ratio `R`, so the equation is not a prediction from closed premises.

EL5.4 combines two different matrices. Its actual restored-electron matrix is
five-by-three with rank three and nullity zero; it is not underdetermined. A
separate four-by-five OD-v1-shaped matrix has rank four and nullity one. The
second is a valid underdetermined example but does not prove the claimed status
change for the first.

EL5.5 is a valid inconsistency mutation for a duplicate-row pair and is covered
by `C-LIN-001`'s general diagnostic.

EL5.6 reproducibly runs seven pinned predecessor scripts in fresh interpreters,
checks clean exits, and locates their terminal tallies. Those standalone files
do not import the accepted `substrate_framework` package or the P021/P022 APIs;
their green status therefore proves only that the historical files still pass
their own checks. It is useful migration compatibility evidence, not downstream
replay of the promoted claims and not verification of the electron conclusion.

EL5.7 correctly rejects a deliberately broken subprocess and shows the narrow
exit/tail harness is sensitive.

EL5.8 correctly scans executable EL5 syntax for a short forbidden set. As with
earlier lexical guards, it cannot establish semantic dependency closure or
remove symbolic free inputs.

## Exact qualification

Accepted content is limited to the general linear-system classification,
duplicate-row coefficient behavior, and augmented-rank consistency mutation.
The exact conditional source ratio and predecessor subprocess tallies remain
evidence, but EL5 does not predict a mass, eliminate `b` or `kappa_h`, establish
an electron object, or demonstrate accepted-framework consumer closure.
