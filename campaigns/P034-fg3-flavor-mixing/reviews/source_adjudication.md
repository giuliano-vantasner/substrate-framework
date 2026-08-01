# FG3 Source Adjudication

FG3 is qualified. Its concrete invertible matrices do admit the displayed
biunitary decompositions, and several abstract unitary and real-symmetric
matrix facts map to `C-MIX-001`. Its returned diagonalizer convention is not
compatible with the mixing formula it then uses, its exceptional singular
subspaces are excluded, and none of its physical CKM, charged-current, GIM, or
anomaly premises belongs to accepted release `v0.29.0`.

## FG3.1: Biunitary Diagonalization

The source's two-by-two invertible example passes exactly. Internally it first
constructs column singular-vector matrices `Umat,Vmat` satisfying
`Umat^dagger M Vmat=Sigma`, then returns row transforms
`A=Umat^dagger,B=Vmat^dagger` satisfying `A M B^dagger=Sigma`. This is a valid
example but not the stated general theorem: division by every singular value
explicitly excludes zero singular values and it does not characterize repeated
subspaces. P034 supplies the full rectangular theorem, null spaces, and
degenerate freedoms in one documented column-basis convention.

## FG3.2: Relative Left Bases

For column bases `U_u,U_d`, `U_u^dagger U_d` is unitary. FG3, however, names
the returned row transform `A` as `U_L` and computes `A_u^dagger A_d`.
Substitution into a common bilinear when mass coordinates are `A*gauge` gives
`A_u A_d^dagger`. An exact rational counterexample makes these two matrices
different while both remain unitary. FG3's checks therefore cannot detect the
orientation error. `C-MIX-001` records both conventions explicitly and assigns
no CKM identity.

## FG3.3: Real Symmetric Two-by-Two Rotation

The displayed `theta=pi/8` calculation is correct for its declared real
symmetric matrix and rotation convention. It diagonalizes one texture. A
physical two-sector mixing angle is a difference of two basis angles, so one
texture does not predict a Cabibbo angle; arbitrary declared textures realize
continuously many relative angles. The source also does not prove the general
two-family phase-removal theorem by exhibiting one real example.

## FG3.4: Currents, GIM, and Anomaly

Neutral-bilinear invariance under one unitary basis change is valid abstract
algebra, but FG3 imports M1, SM2, SM3, W3, and W7, all pending source units with
no accepted mappings in `v0.29.0`. Its anomaly check declares a symbol `A_gen`
and compares `A_gen*Tr(V^dagger V)` with `N*A_gen`; it computes no
representation or charge anomaly. No charged-current, GIM, or anomaly claim is
promoted.

## FG3.5 and FG3.6: Guards

Scaling a unitary matrix makes it nonunitary, and identical ordered bases give
the identity. These are useful mutation and limiting checks. They do not
establish probability conservation or a physical mixing mechanism. Moreover,
diagonal matrices with degeneracies do not select unique common bases without
an extra convention, so the aligned result is stated only for identical
ordered bases in `C-MIX-001`.

## Terminal Disposition

FG3 maps its convention-correct mathematical subclaims to `C-MIX-001` and is
otherwise qualified. Excluded scope comprises a substrate fermion mass matrix,
Yukawa textures, CKM identification, Cabibbo prediction, family count, CP
phase result, charged-current vertex, GIM mechanism, anomaly cancellation, and
all corresponding particle interpretations. Durable evidence is the P034
verifier, independent review, source reproduction, and this adjudication.
